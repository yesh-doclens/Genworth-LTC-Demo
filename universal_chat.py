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
    Classify the following user query into one of these categories:
    1. APPLICATION_FORM: Related to applicant info, demographics, or specific answers in the main Application Form.
    2. MEDICAL_RECORDS: Related to supporting documents, APS, Lab results, Rx history, or Functional interview details.
    3. REVIEW_REPORT: Related to completeness, discrepancies, NIGO items, action items, suitability, or underwriting risk profile.
    4. EMAILS: Related to communication or submission notes.
    5. GENERAL: Anything else.

    User Query: "{query}"

    Return ONLY a JSON object with "category".
    Example: {{"category": "MEDICAL_RECORDS"}}
    """
    
    response = llm.invoke(prompt)
    try:
        json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        return {"category": "GENERAL"}
    except:
        return {"category": "GENERAL"}

def get_tab_context(category, credentials, query, genworth_page=False, filters=None):
    context = ""
    
    if category == "APPLICATION_FORM":
        filename = "form_genworth.md" if genworth_page else "acord.md"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                context = f.read()
            
    elif category == "MEDICAL_RECORDS":
        from supporting_docs import get_all_medical_context
        context = get_all_medical_context()
            
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
        
    elif category == "REVIEW_REPORT":
        if genworth_page:
            review_file = "review/review.md"
            if os.path.exists(review_file):
                with open(review_file, "r") as f:
                    context = f.read()
            else:
                context = "Review report data (review.md) not found."
        else:
            context = "Detailed review report only available for Genworth LTC submissions."
        
    elif category == "COMPLETENESS_CHECK" or category == "DISCREPANCIES":
        # Fallback for old categories if still triggered
        review_file = "review/review.md"
        if genworth_page and os.path.exists(review_file):
            with open(review_file, "r") as f:
                context = f.read()
        else:
            context = "Reference the completeness dashboard for findings."
    
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
