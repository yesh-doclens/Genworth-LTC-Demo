import streamlit as st
import json
import re
from langchain_aws import ChatBedrockConverse
from main import ask_agent, configure_agent

def get_llm(model_id, credentials):
    return ChatBedrockConverse(
        model_id=model_id,
        region_name="us-east-2",
        max_tokens=2000,
        aws_access_key_id=credentials["aws_access_key"],
        aws_secret_access_key=credentials["aws_secret_key"],
        aws_session_token=credentials.get("aws_session_token"),
    )

def classify_query(query, credentials):
    haiku_id = "us.anthropic.claude-3-haiku-20240307-v1:0"
    llm = get_llm(haiku_id, credentials)
    
    prompt = f"""
    Classify the following user query into one of these categories:
    1. ACORD_APPLICATION: Related to general policy, agency, or applicant info in the ACORD form.
    2. LOSS_RUN: Related to claims history, loss trends, or specific past incidents.
    3. SUPPLEMENTAL_APPLICATION: Related to specific operational details, risk/safety questions from the supplemental form.
    4. EMAILS: Related to communication, attachments, or who sent what.
    5. ACCOUNT_RESEARCH: Related to website summary, reviews (employee/customer), OSHA, SAFER (DOT), or SOS (Secretary of State) data.
    6. COMPLETENESS_CHECK: Related to missing fields, check status, or validation results.
    7. DISCREPANCIES: Related to anomalies, inconsistencies, or flagged issues.
    8. GENERAL: Anything else.

    User Query: "{query}"

    If the category is LOSS_RUN, also try to extract:
    - medical_conditions: list of terms (e.g., ["Fractures", "Death"])
    - min_incurred: number
    - max_incurred: number

    Return ONLY a JSON object with "category" and optional "filters" (for LOSS_RUN).
    Example: {{"category": "LOSS_RUN", "filters": {{"medical_conditions": ["Fractures"], "min_incurred": 10000}}}}
    """
    
    response = llm.invoke(prompt)
    try:
        # Extract JSON from response content
        json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        return {"category": "GENERAL"}
    except:
        return {"category": "GENERAL"}

def get_tab_context(category, credentials, query, genworth_page=False, filters=None):
    context = ""
    
    if category == "ACORD_APPLICATION":
        filename = "form_genworth.md" if genworth_page else "acord.md"
        with open(filename, "r") as f:
            context = f.read()
            
    elif category == "SUPPLEMENTAL_APPLICATION":
        # For Genworth, we might just reuse the same form or mark it as N/A
        with open("application.md", "r") as f:
            context = f.read()
            
    elif category == "EMAILS":
        if genworth_page:
            context = """
            Email Summary (Genworth):
            From: James Advisor <james@advisor.com>
            To: Underwriting <underwriting@genworth.com>
            Date: Mar 15, 2026, 09:30 AM
            Subject: LTC Application Submission - Jordan A. Taylor
            Body: Attached is the LTC application for Jordan A. Taylor. Please note the missing HIPAA signature and the SSN format clarification.
            """
        else:
            context = """
            Email Summary:
            From: Sarah Ellis <sarah.ellis@summitpeakins.com>
            To: Submissions <submissions@doclens.ai>
            Date: Feb 24, 2026, 10:45 AM
            Subject: New Commercial Auto Submission - Blue Ridge Office Solution, LLC
            Body: Please find the submission for Blue Ridge Office Solution, LLC. Includes ACORD 125/137, driver and vehicle lists, loss runs (5 years), and supplemental application.
            """
        
    elif category == "ACCOUNT_RESEARCH":
        if genworth_page:
            context = """
            Research Data (Jordan A. Taylor):
            - Identity: Verified Jordan A. Taylor, Resident of NY.
            - SSN Check: Flagged for invalid format (8 digits).
            - Credit Inquiry: Moderate risk profile.
            - Medical MIB: Flagged for 3 recent prescriptions.
            """
        else:
            context = """
            Research Data:
            - Website Summary: Secure Document Destruction, Waste Removal, LEED Services, Recycling, Composting, Dumpster Rentals.
            - Employee Reviews: 4.4/5 (90 reviews).
            - Customer Reviews: 4.2/5 (156 reviews).
            - OSHA: 12 inspections (5yr), 2 violations, $1,450 penalty.
            - SAFER (DOT): 882341, SATISFACTORY rating, 24 vehicles.
            - SOS: Active / Good Standing, Incorporated Jan 15, 1998.
            """
        
    elif category == "COMPLETENESS_CHECK":
        if genworth_page:
            context = """
            Completeness Status (Genworth/LTC):
            - Overall: 15 Deficiencies Found.
            - LTC Application (Jordan Taylor): 16 / 31 core fields present (Red).
            - Signatures & Authorizations: 3 / 5 signed (HIPAA & Applicant missing).
            - NY Addendums: Missing Home Care Disclosure & Replacement Notice.
            - Validation: SSN format check (Failed), Bank routing check (Failed).
            """
        else:
            context = """
            Completeness Status:
            - Overall: 2/3 checks passed.
            - ACORD: 20/21 fields present (Green).
            - Supplemental: 12/28 fields present (Orange).
            - Validation: Insured name validation (Passed), FEIN valid in ACORD (Passed).
            """
        
    elif category == "DISCREPANCIES":
        if genworth_page:
            context = """
            Discrepancies identified (Genworth/LTC):
            - Critical: Incomplete Applicant Details (SSN 8-digit format, missing signatures).
            - Critical: Payment Information Errors (Routing 8-digit, affordability explanation missing).
            - Major: Missing Medical Documentation (Prescription list missing).
            - Major: Functional Assessment Gap (ADL 'Bathing' frequency missing).
            - Critical: Missing NY State Addendums (Home Care Disclosure, Replacement Notice).
            """
        else:
            context = """
            Discrepancies identified:
            - Critical: Unexpected Premium Drop (45% decrease vs loss runs).
            - Major: Missing Loss History (2023 gap identifying Jan-Dec 2023).
            - Minor: Vehicle List Inconsistency (15 in Supplemental vs 14 in ACORD).
            - Minor: Outdated Safety Manual (Not updated since 2018).
            """
    
    elif category == "LOSS_RUN":
        # For Genworth/LTC, Loss Runs might not be as relevant or handled separately
        if genworth_page:
             context = "Loss run data is not available for this individual life/LTC submission."
        else:
            configure_agent(credentials)
            agent_query = query
            if filters:
                conditions = filters.get("medical_conditions", [])
                min_v = filters.get("min_incurred")
                max_v = filters.get("max_incurred")
                if conditions or min_v or max_v:
                    parts = []
                    if conditions: parts.append(f"related to {', '.join(conditions)}")
                    if min_v: parts.append(f"above ${min_v}")
                    if max_v: parts.append(f"below ${max_v}")
                    agent_query = f"Search in loss records: {query}. Filters: {' and '.join(parts)}"
            
            filename = "Loss Run.csv"
            try:
                response_text, df_filtered = ask_agent(agent_query, use_cat=True, filename=filename)
                context = f"Loss Run Agent Answer: {response_text}\n"
                if df_filtered is not None and not df_filtered.empty:
                    context += f"Filtered Data:\n{df_filtered.to_string()}"
            except Exception as e:
                context = f"Error querying loss run agent: {str(e)}"

    return context

def get_universal_answer(query, category, context, credentials, genworth_page=False):
    sonnet_id = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
    llm = get_llm(sonnet_id, credentials)
    
    company_name = "Jordan A. Taylor" if genworth_page else "Blue Ridge Office Solution, LLC"
    product_context = "Genworth LTC Application" if genworth_page else "Commercial Insurance Submission"
    
    prompt = f"""
    You are a universal assistant for a {product_context} platform.
    The user is asking a question about a specific account: "{company_name}".
    
    Category identified: {category}
    Context provided from that category:
    {context}
    
    User Query: "{query}"
    
    Answer the user's query accurately using ONLY the provided context. If the answer is not in the context, say you don't have that information.
    Maintain a professional and helpful tone. Format your answer nicely using markdown.
    """
    
    response = llm.invoke(prompt)
    return response.content
