import streamlit as st
import json
import re
from langchain_aws import ChatBedrockConverse
from main import ask_agent, configure_agent
import os 

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
    Classify the following user query into one of these specific insurance review categories:
    1. APPLICATION_FORM: Related to applicant demographics, beneficiary, contact info, or general form data.
    2. COMPLETENESS: Related to status (IGO/NIGO), missing fields, or general deficiency counts.
    3. IDENTITY_LEGAL: Related to SSN, DOB, Address verification, Owner vs Insured, or Lapse Designee.
    4. HEALTH_MEDICAL: Related to health history, tobacco use, HbA1c, lab results, hypertension, or medications.
    5. FUNCTIONAL_ASSESSMENT: Related to ADLs (Bathing, Dressing, etc.), Fall history, Dizziness, or Home safety.
    6. PRODUCT_SUITABILITY: Related to NY State forms, Replacement analysis, affordability, or plan elections ($200/day, 5yr period).
    7. PAYMENT_COMPLIANCE: Related to bank accounts, routing #, HIPAA authorization, or electronic signatures.
    8. RISK_PROFILE: Related to overall risk level (High/Low), misrepresentation flags, or priority action items for the advisor.
    9. SUPPORTING_DOCS: Related to guidelines, product guides, or general LTC rules.
    10. EMAILS: Related to advisor communications or submission notes.
    11. GENERAL: Anything else.

    User Query: "{query}"

    Return ONLY a JSON object with "category".
    Example: {{"category": "HEALTH_MEDICAL"}}
    """
    
    response = llm.invoke(prompt)
    try:
        json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        return {"category": "GENERAL"}
    except:
        return {"category": "GENERAL"}

def extract_section(text, section_keywords):
    """Simple extraction helper to pull relevant sections from review.md"""
    lines = text.split('\n')
    extracted = []
    found = False
    
    for line in lines:
        if "## SECTION" in line:
            if any(key.upper() in line.upper() for key in section_keywords):
                found = True
            else:
                found = False
        
        if found:
            extracted.append(line)
            
    return "\n".join(extracted) if extracted else text

def get_tab_context(category, credentials, query, genworth_page=False, filters=None):
    context = ""
    
    if category == "APPLICATION_FORM":
        filename = "form_genworth.md" if genworth_page else "acord.md"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                context = f.read()
            
    elif category == "SUPPORTING_DOCS":
        from supporting_docs import get_all_medical_context
        # Include medical context AND Guideline hint
        context = get_all_medical_context()
        context += "\n(Guideline Context: Refer to standard LTC Product knowledge for Jordan A. Taylor's case.)"
            
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
            context = "No email records available for this account."
        
    elif category in ["COMPLETENESS", "IDENTITY_LEGAL", "HEALTH_MEDICAL", "FUNCTIONAL_ASSESSMENT", "PRODUCT_SUITABILITY", "PAYMENT_COMPLIANCE", "RISK_PROFILE"]:
        if genworth_page:
            review_file = "review/review.md"
            if os.path.exists(review_file):
                with open(review_file, "r") as f:
                    full_review = f.read()
                
                # Map categories to section keywords
                mapping = {
                    "COMPLETENESS": ["SECTION 1"],
                    "IDENTITY_LEGAL": ["SECTION 2"],
                    "HEALTH_MEDICAL": ["SECTION 3"],
                    "FUNCTIONAL_ASSESSMENT": ["SECTION 4"],
                    "PRODUCT_SUITABILITY": ["SECTION 5", "SECTION 6", "SECTION 7"],
                    "PAYMENT_COMPLIANCE": ["SECTION 8", "SECTION 9"],
                    "RISK_PROFILE": ["SECTION 11", "SECTION 10"]
                }
                
                context = extract_section(full_review, mapping.get(category, []))
            else:
                context = "Review report data (review.md) not found."
        else:
            context = "Detailed review report only available for Genworth LTC submissions."
    
    elif category == "LOSS_RUN":
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
