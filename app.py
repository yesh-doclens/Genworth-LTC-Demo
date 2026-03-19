import streamlit as st
import pandas as pd
from acord import show_acord_page
from application import show_supplemental_page
from lossrun import show_lossrun_page
from research import show_research_page
from dashboard import show_dashboard
from disturbancies import show_disturbancies_page
from supporting_docs import show_supporting_docs_page
import base64
from universal_chat import classify_query, get_tab_context, get_universal_answer
from configurations import page
import os
# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="DocLens SubmissionLens")

# --- Custom CSS for Styling ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp { background-color: #F8FAFC; }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #343b4d !important;
        color: #A0AEC0 !important;
    }
    
    section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        background-color: #343b4d !important;
    }

    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] small {
        color: #FFFFFF !important;
    }

    /* Sidebar Divider */
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.1) !important;
    }

    /* Sidebar Category Labels (Simulation of DEPARTMENT/FOLDER) */
    .sidebar-category {
        font-size: 0.7rem;
        font-weight: 700;
        color: #A0AEC0 !important;
        margin-bottom: 8px;
        margin-top: 16px;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    
    /* Card-like containers */
    .status-card {
        background-color: white;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
        color: #1E293B;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    /* Status Tag */
    .status-tag {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        vertical-align: middle;
        margin-left: 10px;
    }
    
    /* Progress Badges */
    .badge-orange {
        background-color: #FFF7ED;
        color: #ffb800;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .badge-green {
        background-color: #F0FDF4;
        color: #00c2c2;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }

    .badge-red {
        background-color: #FEF2F2;
        color: #d92d20;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }

    /* Links/View buttons */
    .view-link {
        color: #00c2c2;
        text-decoration: none;
        font-size: 0.9rem;
        font-weight: 600;
    }
    /* General Button Styling */
    .stButton > button {
        text-align: left;
        justify-content: flex-start;
        border: 1px solid #E2E8F0;
        background-color: #FFFFFF;
        padding: 8px 16px;
        color: #475569;
        font-size: 0.95rem;
        border-radius: 8px;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background-color: #F8FAFC;
        border-color: #00c2c2;
        color: #1E293B;
    }
    
    /* Primary Button Styling */
    .stButton > button[kind="primary"] {
        background-color: #00c2c2;
        color: white;
        border: none;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #008a8a;
    }

    /* Sidebar Button Specifics (Top-level) */
    section[data-testid="stSidebar"] div.stButton > button {
        border: none !important;
        background-color: transparent !important;
        margin-bottom: 2px !important;
        padding: 8px 12px !important;
        font-weight: 400 !important;
        width: 100% !important;
        border-radius: 6px !important;
        text-align: left !important;
        color: #A0AEC0 !important;
        display: flex !important;
        justify-content: flex-start !important;
    }
    section[data-testid="stSidebar"] div.stButton > button:hover {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #FFFFFF !important;
    }
    section[data-testid="stSidebar"] div.stButton > button[disabled] {
        background-color: rgba(0, 194, 194, 0.1) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* Tree Branch Connector (L-shape) */
    .tree-branch {
        display: flex;
        height: 32px;
        align-items: center;
        margin-left: 12px;
    }
    .tree-connector-v {
        border-left: 1px solid rgba(160, 174, 192, 0.3);
        height: 100%;
        margin-right: 0px;
    }
    .tree-connector-h {
        border-bottom: 1px solid rgba(160, 174, 192, 0.3);
        width: 10px;
        height: 16px;
        margin-right: 8px;
    }

    /* Sub-navigation link style (Borderless and Transparent) */
    section[data-testid="stSidebar"] [data-testid="column"] div.stButton > button {
        font-size: 0.82rem !important;
        height: 28px !important;
        color: #A0AEC0 !important;
    }
    section[data-testid="stSidebar"] [data-testid="column"] div.stButton > button:hover {
        color: #FFFFFF !important;
    }

    /* Active Sub-view Styling */
    .active-nav {
        background-color: rgba(0, 194, 194, 0.1) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        background-color: transparent;
        border-bottom: 1px solid #E2E8F0;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        white-space: pre-wrap;
        background-color: #F1F5F9;
        border: 1px solid #E2E8F0;
        margin-right: 4px;
        border-radius: 8px 8px 0px 0px;
        color: #64748B;
        font-weight: 400;
        padding: 0px 24px;
        transition: all 0.2s;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #1E293B;
        background-color: #E2E8F0;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #00c2c2;
        background-color: #FFFFFF;
        border-bottom: 1px solid #FFFFFF;
        margin-bottom: -1px;
        font-weight: 600;
    }

    .stTabs [data-baseweb="tab-panel"] {
        border: 1px solid #E2E8F0;
        border-top: none;
        padding: 30px;
        background-color: #FFFFFF;
        border-radius: 0px 0px 12px 12px;
        margin-top: -1px;
    }

    /* Search Input Styling */
    div[data-testid="stTextInput"] input {
        background-color: #F1F5F9;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
    }

    /* Table Header */
    .stDataFrame thead tr th {
        background-color: #545b6d !important;
        color: white !important;
    }

    /* Email Styling */
    .email-container {
        background-color: white;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        overflow: hidden;
        margin-bottom: 24px;
    }
    .email-header {
        background-color: #F8FAFC;
        padding: 24px;
        border-bottom: 1px solid #E2E8F0;
    }
    .email-body {
        padding: 24px;
        line-height: 1.6;
        color: #1E293B;
    }
    .email-attachment {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 12px;
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        margin-top: 8px;
        transition: all 0.2s;
        cursor: pointer;
    }
    .email-attachment:hover {
        border-color: #00c2c2;
        background-color: #F0FDFA;
    }
    .attachment-icon {
        font-size: 1.1rem;
    }
    .attachment-name {
        font-weight: 600; 
        color: #1E293B;
        font-size: 0.85rem;
    }
    .attachment-size {
        font-size: 0.7rem; 
        color: #64748B;
    }
    .attachment-download {
        margin-left: auto;
        color: #00c2c2;
        font-size: 1.1rem;
    }

    /* Resizable PDF Container */
    .resizable-input-container {
        resize: horizontal;
        overflow: auto;
        min-width: 200px;
        max-width: 95%;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 4px;
    }
    .resizable-input-container iframe {
        width: 100% !important;
        height: 800px !important;
    }

    /* Truly Resizable Split View */
    .split-view-container > div {
        display: flex !important;
        flex-direction: row !important;
        align-items: stretch !important;
        width: 100% !important;
        gap: 10px !important;
    }
    .split-view-container [data-testid="column"]:first-child {
        flex: 0 0 auto !important;
        width: auto !important;
        max-width: 90% !important;
        min-width: 200px !important;
    }
    .split-view-container [data-testid="column"]:last-child {
        flex: 1 1 0% !important;
        width: auto !important;
        min-width: 300px !important;
        padding-left: 10px !important;
    }
    </style>
    </style>
    """,
    unsafe_allow_html=True,
)


def main():
    if "aws_credentials" not in st.session_state:
        st.session_state["aws_credentials"] = None
    
    if "current_view" not in st.session_state:
        st.session_state["current_view"] = "Dashboard"
        
    if "selected_submission" not in st.session_state:
        st.session_state["selected_submission"] = None

    if "sub_view" not in st.session_state:
        st.session_state["sub_view"] = "Agency Information"

    if "expanded_sections" not in st.session_state:
        st.session_state["expanded_sections"] = {
            "Application Form": True,
            "Loss Run Insights": False,
            "Supplemental Application": False
        }

    if "universal_chat_response" not in st.session_state:
        st.session_state["universal_chat_response"] = None
    
    if "chat_id" not in st.session_state:
        st.session_state["chat_id"] = 0

    if st.session_state["aws_credentials"] is None:
        st.title("Welcome to Doclens Submissions")
        aws_access_key = st.text_input("Enter AWS Access Key", type="password")
        aws_secret_key = st.text_input("Enter AWS Secret Key", type="password")
        aws_session_token = st.text_input("Enter AWS Session Token (if applicable)", type="password")

        if st.button("✅ Save Credentials"):
            if not aws_access_key or not aws_secret_key:
                st.error("Access key and secret key are required")
            else:
                st.session_state["aws_credentials"] = {
                    "aws_access_key": aws_access_key,
                    "aws_secret_key": aws_secret_key,
                    "aws_session_token": aws_session_token,
                }
                st.success("Credentials saved")
                st.rerun()
        return

    # --- Sidebar ---
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align: center;">
                <img src="data:image/png;base64,{}" width="120">
            </div>
            """.format(
                base64.b64encode(open("public/genworth-logo.jpeg", "rb").read()).decode()
            ),
            unsafe_allow_html=True,
        )
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Dashboard (Always visible)
        is_dash_active = st.session_state["current_view"] == "Dashboard"
        if st.button("🏠 Dashboard", use_container_width=True, key="nav_dash", disabled=is_dash_active):
            st.session_state["current_view"] = "Dashboard"
            st.session_state["selected_submission"] = None
            st.rerun()

        if st.session_state["current_view"] == "Dashboard":
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            
        
        genworth_page = page == "genworth"

        if st.session_state["selected_submission"]:
            st.markdown('<p class="sidebar-category">Uploads</p>', unsafe_allow_html=True)
            
            # Application Form
            is_acord_active = st.session_state["current_view"] == "Application Form"
            page_name = "📄 Application Form" if not genworth_page else "📄 Application Form"
            if st.button(page_name, use_container_width=True, key="nav_acord", disabled=is_acord_active):
                st.session_state["current_view"] = "Application Form"
                st.session_state["sub_view"] = "Agency Information"
                st.rerun()

            # Supporting Documents
            is_supp_docs_active = st.session_state["current_view"] == "Supporting Documents"
            if genworth_page and st.button("📁 Supporting Documents", use_container_width=True, key="nav_supp_docs", disabled=is_supp_docs_active):
                st.session_state["current_view"] = "Supporting Documents"
                st.session_state["sub_view"] = None
                st.rerun()

            # Loss Run Insights
            is_loss_active = st.session_state["current_view"] == "Loss Run Insights"
            if not genworth_page and st.button("📉 Loss Run Insights", use_container_width=True, key="nav_lossrun", disabled=is_loss_active):
                st.session_state["current_view"] = "Loss Run Insights"
                st.session_state["sub_view"] = "History"
                st.rerun()

            # Supplemental Application
            is_supp_active = st.session_state["current_view"] == "Supplemental Application"
            if not genworth_page and st.button("📝 Supplemental Application", use_container_width=True, key="nav_supp", disabled=is_supp_active):
                st.session_state["current_view"] = "Supplemental Application"
                st.session_state["sub_view"] = "Insured Details"
                st.rerun()

            # st.markdown('<p class="sidebar-category">Communication</p>', unsafe_allow_html=True)
            is_emails_active = st.session_state["current_view"] == "Emails"
            if not genworth_page and st.button("📧 Emails", use_container_width=True, key="nav_emails", disabled=is_emails_active):
                st.session_state["current_view"] = "Emails"
                st.session_state["sub_view"] = None
                st.rerun()

            # st.markdown('<p class="sidebar-category">Enrichment</p>', unsafe_allow_html=True)

            # # Account Research
            # is_research_active = st.session_state["current_view"] == "Account Research"
            # if st.button("🔍 Account Research", use_container_width=True, key="nav_research", disabled=is_research_active):
            #     st.session_state["current_view"] = "Account Research"
            #     st.session_state["sub_view"] = None
            #     st.rerun()
            
            st.markdown('<p class="sidebar-category">Review</p>', unsafe_allow_html=True)

            # Review Tabs (Genworth Specific)
            if genworth_page:
                review_items = [
                    ("🔍 Review Overview", "Review Overview"),
                    ("📊 Completeness Check", "Completeness Check"),
                    ("👤 Identity & Legal", "Identity & Legal"),
                    ("🩺 Health & Medical", "Health & Medical"),
                    ("♿ Functional Assessment", "Functional Assessment"),
                    ("📄 Product & Suitability", "Product & Suitability"),
                    ("💳 Payment & Compliance", "Payment & Compliance"),
                    ("🛡️ Risk Profile", "NIGO & Risk")
                ]
                for label, view_name in review_items:
                    is_active = st.session_state["current_view"] == view_name
                    if st.button(label, use_container_width=True, disabled=is_active):
                        st.session_state["current_view"] = view_name
                        st.session_state["sub_view"] = None
                        st.rerun()
            else:
                is_comp_active = st.session_state["current_view"] == "Completeness Check"
                if st.button("📊 Completeness Check", use_container_width=True, disabled=is_comp_active):
                    st.session_state["current_view"] = "Completeness Check"
                    st.session_state["sub_view"] = None
                    st.rerun()

            # Discrepancies
            is_dist_active = st.session_state["current_view"] == "Discrepancies"
            if st.button("🚩 Discrepancies", use_container_width=True, disabled=is_dist_active):
                st.session_state["current_view"] = "Discrepancies"
                st.session_state["sub_view"] = None
                st.rerun()

            
        
        st.divider()
        if st.button("🔄 Change Credentials", use_container_width=True):
            st.session_state["aws_credentials"] = None
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(
            """
            <div style="text-align: center;">
                <img src="data:image/png;base64,{}" width="50">
            </div>
            """.format(
                base64.b64encode(open("public/Doclens_logo.png", "rb").read()).decode()
            ),
            unsafe_allow_html=True,
        )

    if st.session_state["selected_submission"]:
        # --- Header Section ---
        
        logo_html = ""
        if st.session_state["selected_submission"] == "Genworth Insurance":
            logo_path = "public/genworth-logo.jpeg"
            if os.path.exists(logo_path):
                with open(logo_path, "rb") as f:
                    data = base64.b64encode(f.read()).decode()
                    logo_html = f'<img src="data:image/jpeg;base64,{data}" style="width: 150px; height: 150px; border-radius: 6px; margin-right: 12px; vertical-align: middle;">'

        col_h1, col_h2 = st.columns([3, 1.2])

        with col_h1:
            st.caption(f"Submissions > {st.session_state['selected_submission']} > {st.session_state['current_view']}")
            st.markdown(f"<h1>{logo_html}{st.session_state['selected_submission']} <span class='status-tag'>Incomplete ▾</span></h1>", unsafe_allow_html=True)
            st.caption("SUB-000001 • 04 Jan 2026")

        with col_h2:
            st.write("##") # Spacer
            btn_col1, btn_col2 = st.columns(2)
            btn_col1.button("🚫 Reject", use_container_width=True, key="global_reject")
            btn_col2.button("Generate Summary", type="primary", use_container_width=True, key="global_gen_sum")

        # --- AI Input Bar ---
        query = st.text_input("✨ Ask anything", label_visibility="collapsed", placeholder="Ask anything related to this account...", key=f"global_ai_chat_{st.session_state['chat_id']}")
        
        # Current stored response Query
        stored_query = st.session_state["universal_chat_response"].get("query") if st.session_state["universal_chat_response"] else None
        
        if query and query != stored_query:
            with st.spinner("Analyzing..."):
                classification = classify_query(query, st.session_state["aws_credentials"])
                category = classification.get("category", "GENERAL")
                filters = classification.get("filters")
                
                context = get_tab_context(category, st.session_state["aws_credentials"], query, genworth_page, filters)
                answer = get_universal_answer(query, category, context, st.session_state["aws_credentials"], genworth_page)
                st.session_state["universal_chat_response"] = {
                    "query": query,
                    "category": category,
                    "answer": answer
                }
                st.rerun()

        if st.session_state["universal_chat_response"]:
            resp = st.session_state["universal_chat_response"]
            with st.container(border=True):
                st.markdown(f"**Query:** {resp['query']}")
                st.markdown(f"**Category:** `{resp['category']}`")
                st.markdown(resp['answer'])
                if st.button("Clear Answer"):
                    st.session_state["universal_chat_response"] = None
                    st.session_state["chat_id"] += 1
                    st.rerun()

        st.divider()

    # --- Content Body ---
    if st.session_state["current_view"] == "Dashboard":
        show_dashboard()
    elif st.session_state["current_view"] == "Completeness Check":
        show_completeness_dashboard()
    elif st.session_state["current_view"] == "Application Form":
        show_acord_page()
    elif st.session_state["current_view"] == "Supplemental Application":
        show_supplemental_page()
    elif st.session_state["current_view"] == "Loss Run Insights":
        show_lossrun_page()
    elif st.session_state["current_view"] == "Account Research":
        show_research_page()
    elif st.session_state["current_view"] == "Emails":
        show_emails_page()
    elif st.session_state["current_view"] == "Discrepancies":
        show_disturbancies_page()
    elif st.session_state["current_view"] in [
        "Review Overview", "Identity & Legal", "Health & Medical", "Functional Assessment", 
        "Product & Suitability", "Payment & Compliance", "NIGO & Risk"
    ]:
        show_review_section(st.session_state["current_view"])
    elif st.session_state["current_view"] == "Supporting Documents":
        show_supporting_docs_page()

def show_completeness_dashboard():
    st.subheader("Completeness Check")
    is_genworth = st.session_state.get("selected_submission") == "LTC-NY-2026-000174"

    if not is_genworth: # This block is for the non-Genworth completeness check
        # Completeness Card
        with st.container(border=True):
            st.markdown("""
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: bold; font-size: 1.1rem;">Improve this completeness</span>
                    <span class="badge-orange">2 / 3 checks passed</span>
                </div>
                <hr style="border: 0.5px solid #F1F5F9; margin: 20px 0;">
            """, unsafe_allow_html=True)
            
            c1, c2 = st.columns([4, 1])
            with c1:
                st.markdown('<span><span style="color:#22C55E">●</span> <b>Application Form</b><br><small style="color:#64748B; margin-left:18px;">20 / 21 fields present</small></span>', unsafe_allow_html=True)
            with c2:
                if st.button("View >", key="view_acord"):
                    st.session_state["current_view"] = "Application Form"
                    st.rerun()

            st.write("") # Spacer

            c1, c2 = st.columns([4, 1])
            with c1:
                st.markdown('<span><span style="color:#F59E0B">!</span> <b>Supplemental Application</b><br><small style="color:#C2410C; margin-left:18px;">12 / 28 fields present</small></span>', unsafe_allow_html=True)
            with c2:
                if st.button("View >", key="view_supp"):
                    st.session_state["current_view"] = "Supplemental Application"
                    st.rerun()

        # Validation Card
        st.markdown("""
        <div class="status-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: bold; font-size: 1.1rem;">Validation Checks</span>
                <span class="badge-green">4 / 4 checks passed</span>
            </div>
            <hr style="border: 0.5px solid #F1F5F9; margin: 20px 0;">
            <p>✅ <b>Insured name validation</b><br><small style="color:#64748B; margin-left:25px;">Validating if all documents belong to same Insured</small></p>
            <p>✅ <b>FEIN valid in ACORD</b><br><small style="color:#64748B; margin-left:25px;">The FEIN provided matches the required ACORD format (9 digits, no letters)</small></p>
        </div>
        """, unsafe_allow_html=True)
    else: # This block is for the Genworth "Overview" part of completeness
        # CSS for status badges
        st.markdown("""
            <style>
            .badge-red {
                background-color: #F87171;
                color: white;
                padding: 4px 12px;
                border-radius: 9999px;
                font-size: 0.85rem;
                font-weight: 600;
            }
            </style>
        """, unsafe_allow_html=True)
        
        # IGO / NIGO Status Tile
        st.markdown("""
            <div style="background-color: #FEE2E2; border-left: 10px solid #EF4444; padding: 24px; border-radius: 12px; margin-bottom: 24px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 0.9rem; color: #991B1B; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Submission Status</div>
                        <div style="font-size: 2.5rem; font-weight: 800; color: #991B1B; line-height: 1;">NOT IN GOOD ORDER (NIGO)</div>
                        <div style="font-size: 1.1rem; color: #B91C1C; margin-top: 8px;">15 Deficiencies • 13 Critical • 2 Major</div>
                    </div>
                    <div style="background: white; width: 80px; height: 80px; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);">
                        <span style="font-size: 3rem;">⚠️</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Completeness Card for Genworth
        with st.container(border=True):
            st.markdown("""
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: bold; font-size: 1.1rem;">Application Completeness</span>
                </div>
                <hr style="border: 0.5px solid #F1F5F9; margin: 20px 0;">
            """, unsafe_allow_html=True)

            sections = [
                ("Applicant Demographics", "Invalid SSN & Email format", "CRITICAL", "#EF4444"),
                ("Coverage & Benefit", "Plan type requires NY disclosure", "MAJOR", "#F59E0B"),
                ("Premium & Payment", "Bank routing number invalid (8 digits)", "CRITICAL", "#EF4444"),
                ("Replacement Details", "Missing carrier, policy #, and reason", "CRITICAL", "#EF4444"),
                ("Health & Underwriting", "Material discrepancy: Tobacco/Nicotine", "CRITICAL", "#EF4444"),
                ("Prescription Meds", "Sec. 5A medication list not provided", "CRITICAL", "#EF4444"),
                ("Functional Assessment", "ADL narrative for Bathing missing", "CRITICAL", "#EF4444"),
                ("Financial Suitability", "Hardship explanation & Suitability Ack missing", "CRITICAL", "#EF4444"),
                ("Authorizations", "HIPAA Authorization not signed", "CRITICAL", "#EF4444"),
                ("Advisor Information", "NPN/License number missing", "CRITICAL", "#EF4444"),
                ("Signatures", "Applicant application signature missing", "CRITICAL", "#EF4444"),
                ("State Addenda (NY)", "NY Home Care & Replacement notices missing", "CRITICAL", "#EF4444"),
                ("Identity Check", "SSN format mismatch (8 vs 9 digits)", "CRITICAL", "#EF4444"),
                ("Fall History", "Documented fall (09/2025) not disclosed", "MAJOR", "#F59E0B"),
                ("Beneficiary", "Designation section not completed", "CRITICAL", "#EF4444"),
            ]

            # Header
            st.markdown("""
                <div style="display: grid; grid-template-columns: 3fr 5fr 2fr 1.5fr; gap: 10px; padding: 10px 0; border-bottom: 1px solid #F1F5F9; color: #64748B; font-weight: 600; font-size: 0.85rem;">
                    <div>SECTION</div>
                    <div>REASON / DISCREPANCY</div>
                    <div>SEVERITY</div>
                    <div style="text-align: right;"></div>
                </div>
            """, unsafe_allow_html=True)

            for i, (name, detail, severity, color) in enumerate(sections):
                cols = st.columns([3, 5, 2, 1.5])
                with cols[0]:
                    st.markdown(f'<span style="font-weight: 600; color: #1E293B;">{name}</span>', unsafe_allow_html=True)
                with cols[1]:
                    st.markdown(f'<span style="color: #64748B; font-size: 0.9rem;">{detail}</span>', unsafe_allow_html=True)
                with cols[2]:
                    badge_color = "#FEE2E2" if severity == "CRITICAL" else "#FEF3C7"
                    text_color = "#991B1B" if severity == "CRITICAL" else "#92400E"
                    st.markdown(f'<span style="background-color: {badge_color}; color: {text_color}; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 700;">{severity}</span>', unsafe_allow_html=True)
                with cols[3]:
                    if st.button("View >", key=f"view_sec_{i}", use_container_width=True):
                        st.session_state["current_view"] = "Application Form"
                        st.session_state["acord_active_tab"] = "📄 PDF & Data View"
                        st.rerun()

def show_review_section(section_name):
    # st.subheader(section_name)
    
    # Map section names to tab index or logic
    tab_names = [
        "Review Overview",
        "Identity & Legal", 
        "Health & Medical", 
        "Functional Assessment", 
        "Product & Suitability", 
        "Payment & Compliance", 
        "NIGO & Risk"
    ]
    active_tab = section_name

    if active_tab == tab_names[0]: # Overview
        # IGO / NIGO Status Tile (Completeness Summary)
        st.markdown("""
            <div style="background-color: #FEE2E2; border-left: 10px solid #EF4444; padding: 24px; border-radius: 12px; margin-bottom: 24px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 0.9rem; color: #991B1B; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Submission Status</div>
                        <div style="font-size: 2.5rem; font-weight: 800; color: #991B1B; line-height: 1;">NOT IN GOOD ORDER (NIGO)</div>
                        <div style="font-size: 1.1rem; color: #B91C1C; margin-top: 8px;">15 Deficiencies • 13 Critical • 2 Major</div>
                    </div>
                    <div style="background: white; width: 80px; height: 80px; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);">
                        <span style="font-size: 3rem;">⚠️</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.write("### Review Summary Overview")
        
        # Grid of summary tiles
        col1, col2 = st.columns(2)
        
        with col1:
            with st.container(border=True):
                st.markdown("#### 👤 Identity & Legal")
                st.markdown("""
                - ❌ **SSN:** Invalid (8 digits)
                - ⚠️ **Beneficiary:** Designation missing
                - ❌ **Lapse Designee:** Requirement not addressed
                """)
                if st.button("Full Identity Report", key="goto_identity", use_container_width=True):
                    st.session_state["current_view"] = "Identity & Legal"
                    st.rerun()

            with st.container(border=True):
                st.markdown("#### ♿ Functional Assessment")
                st.markdown("""
                - ✅ **Bathing:** Assistance requirement confirmed
                - ⚠️ **Fall History:** 09/2025 event not disclosed
                - ⚠️ **Environmental:** No grab bars in shower
                """)
                if st.button("Full Functional Report", key="goto_functional", use_container_width=True):
                    st.session_state["current_view"] = "Functional Assessment"
                    st.rerun()

            with st.container(border=True):
                st.markdown("#### 💳 Payment & Compliance")
                st.markdown("""
                - ❌ **Routing #:** Invalid (8 digits)
                - ❌ **HIPAA:** Not signed (Critical)
                - ❌ **Signature:** Applicant sign missing
                """)
                if st.button("Full Payment Report", key="goto_payment", use_container_width=True):
                    st.session_state["current_view"] = "Payment & Compliance"
                    st.rerun()

        with col2:
            with st.container(border=True):
                st.markdown("#### 🩺 Health & Medical")
                st.markdown("""
                - ❌ **Tobacco:** Material Nicotine discrepancy
                - 🟠 **HbA1c:** 8.2% (High)
                - 🟠 **BP:** 152/92 (Stage 2 HTN)
                """)
                if st.button("Full Health Report", key="goto_health", use_container_width=True):
                    st.session_state["current_view"] = "Health & Medical"
                    st.rerun()

            with st.container(border=True):
                st.markdown("#### 📄 Product & Suitability")
                st.markdown("""
                - ❌ **NY Forms:** Replacement Notice & Disclosure missing
                - ⚠️ **Policy Info:** Existing LTC carrier # missing
                - ❌ **Fin. Suitability:** Reported NOT affordable
                """)
                if st.button("Full Product Report", key="goto_product", use_container_width=True):
                    st.session_state["current_view"] = "Product & Suitability"
                    st.rerun()

            with st.container(border=True):
                st.markdown("#### 🛡️ Risk Profile")
                st.markdown("""
                - 🔴 **Overall Risk:** HIGH
                - 🔴 **Integrity:** Tobacco Misrepresentation
                - 🔴 **Compliance:** Critical Missing Signatures
                """)
                if st.button("Full Risk Profile", key="goto_risk", use_container_width=True):
                    st.session_state["current_view"] = "NIGO & Risk"
                    st.rerun()

    elif active_tab == tab_names[1]: # Identity
        st.write("### Identity Verification Matrix")
        st.markdown("""
        | Data Point | Application | APS/PCP | Rx History | Functional Interview | Status |
        |---|---|---|---|---|---|
        | Full Name | Jordan A. Taylor | — | Jordan A. Taylor | Pat Taylor (spouse) | ✅ Consistent |
        | DOB | 07/14/1961 | — | 07/14/1961 | — | ✅ Match |
        | SSN | 123-45-678 | — | — | — | ❌ Invalid |
        | Address | 115 W 57th St, NY | — | — | Apartment confirmed | ✅ Consistent |
        """)
        
        st.write("### Ownership & Beneficiary")
        col_legal1, col_legal2 = st.columns(2)
        with col_legal1:
             st.markdown("""
            <div class="status-card">
                <p>✅ <b>Owner = Insured</b><br><small style="color:#64748B;">Assumed based on no separate owner listed</small></p>
                <p>❌ <b>Beneficiary Designation</b><br><small style="color:#64748B;">No beneficiary section completed</small></p>
            </div>
            """, unsafe_allow_html=True)
        with col_legal2:
             st.markdown("""
            <div class="status-card">
                <p>❌ <b>Third-party Lapse Designee</b><br><small style="color:#64748B;">NY requirement not addressed</small></p>
                <p>⚠️ <b>Spouse Insurable Interest</b><br><small style="color:#64748B;">Pat Taylor involved in care — not co-applicant</small></p>
            </div>
            """, unsafe_allow_html=True)

    elif active_tab == tab_names[2]: # Health
        st.write("### Health Question Accuracy Review")
        st.markdown("""
        | Health Question | Application | Evidence | Discrepancy? |
        |---|---|---|---|
        | Neuro conditions | No | Normal Cognition | ✅ Consistent |
        | ADL Assistance | Yes | Bathing confirmed | ✅ Consistent |
        | Tobacco/Nicotine | **No** | **Nicotine Patch** | ❌ **Inconsistent** |
        | Prescription Meds | Yes | Metformin, etc. | ✅ Consistent |
        """)

        st.write("### Medical & Clinical Status")
        col_cl1, col_cl2 = st.columns(2)
        with col_cl1:
            st.markdown("""
            <div class="status-card" style="border-left: 5px solid #EF4444;">
                <div style="font-weight: 600;">Diabetes & Metabolic Control</div>
                <div style="font-size: 1.2rem; font-weight: 700; margin-top: 8px;">HbA1c: 8.2% <small>(High)</small></div>
                <div style="font-size: 1.2rem; font-weight: 700;">Glucose: 168 mg/dL</div>
                <div style="margin-top: 8px; font-size: 0.85rem; color: #64748B;">Med adherence: Moderate (2 late refills)</div>
            </div>
            """, unsafe_allow_html=True)
        with col_cl2:
            st.markdown("""
            <div class="status-card" style="border-left: 5px solid #F59E0B;">
                <div style="font-weight: 600;">Cardiovascular</div>
                <div style="font-size: 1.2rem; font-weight: 700; margin-top: 8px;">BP: 152/92 <small>(Stage 2 HTN)</small></div>
                <div style="font-size: 1.2rem; font-weight: 700;">BMI: 29.8 <small>(Overweight)</small></div>
                <div style="margin-top: 8px; font-size: 0.85rem; color: #64748B;">eGFR: 72 (Mildly reduced)</div>
            </div>
            """, unsafe_allow_html=True)

    elif active_tab == tab_names[3]: # Functional
        st.write("### ADL/IADL Summary — Cross-Source")
        st.markdown("""
        | Function | Application | APS/PCP | Interview | Status |
        |---|---|---|---|---|
        | Bathing | Needs (checked) | Assist needed | 2-3x/week | ✅ Consistent |
        | Dressing | Not checked | Independent | Independent | ✅ Consistent |
        | Toileting | Not checked | Independent | Independent | ✅ Consistent |
        | Medications | — | Self-manages | Occasional miss | ⚠️ Minor Gap |
        """)

        st.write("### Functional Risk Profile")
        st.markdown("""
        <div class="status-card" style="background-color: #FFFBEB; border: 1px solid #FCD34D;">
            <p>⚠️ <b>Documented Fall (09/2025)</b> - Not disclosed on application</p>
            <p>⚠️ <b>Dizziness & Balance concerns</b> noted by PCP</p>
            <p>⚠️ <b>Environmental Risk:</b> No grab bars in shower</p>
        </div>
        """, unsafe_allow_html=True)

    elif active_tab == tab_names[4]: # Product
        st.write("### Product & Coverage Design")
        st.markdown("""
        | Election | Value | Status |
        |---|---|---|
        | Plan Type | Home Care Only | ✅ Valid; Disclosure Required |
        | Daily Benefit | $200/day | ✅ |
        | Benefit Period | 5 years | ✅ |
        | Elimination | 90 days | ✅ |
        | Inflation | 3% Compound | ✅ Appropriate (age 64) |
        """)

        st.write("### Replacement & Suitability")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown("""
            <div class="status-card">
                <div style="font-weight: 600;">Replacement Flags</div>
                <div style="margin-top: 8px; color: #EF4444;">❌ Existing Co/Policy # missing</div>
                <div style="color: #EF4444;">❌ Replacement reason blank</div>
                <div style="color: #EF4444;">❌ NY Replacement Notice missing</div>
            </div>
            """, unsafe_allow_html=True)
        with col_s2:
            st.markdown("""
            <div class="status-card">
                <div style="font-weight: 600;">Financial Suitability</div>
                <div style="margin-top: 8px; color: #EF4444;">❌ Self-reported NOT affordable</div>
                <div style="color: #EF4444;">❌ Hardship explanation blank</div>
                <div style="color: #EF4444;">❌ Suitability Ack. missing</div>
            </div>
            """, unsafe_allow_html=True)

    elif active_tab == tab_names[5]: # Payment
        st.write("### Payment Setup Review")
        st.markdown("""
        | Item | Value | Status |
        |---|---|---|
        | Bank Name | Metro National Bank | ✅ |
        | Routing # | 02100002 | ❌ **Invalid (8 digits)** |
        | Account # | 00987654321 | ✅ |
        | EFT Audit | Missing User Signature | ❌ |
        """)

        st.write("### Authorization Status")
        st.markdown("""
        <div class="status-card">
            <p>❌ <b>HIPAA Authorization:</b> Not signed | 🔴 Critical</p>
            <p>❌ <b>Applicant Signature:</b> Missing | 🔴 Critical</p>
            <p>✅ <b>Fraud Warning:</b> Acknowledged</p>
            <p>✅ <b>Privacy Notice:</b> Acknowledged</p>
        </div>
        """, unsafe_allow_html=True)

    elif active_tab == tab_names[6]: # Risk
        # 1. Risk & Integrity Summary
        with st.container(border=True):
            st.markdown("""
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span style="font-weight: bold; font-size: 1.15rem; color: #1E293B;">🛡️ Risk & Integrity Summary</span>
                    <span class="badge-red">Multiple Discrepancies</span>
                </div>
                <hr style="border: 0.5px solid #F1F5F9; margin: 15px 0;">
                <p style="color: #EF4444; margin-bottom: 8px;">❌ <b>Material Discrepancy: Tobacco/Nicotine</b><br><small style="color:#64748B; margin-left:25px;">Application says 'No', but Rx records show nicotine patch claims (10/2025)</small></p>
                <p style="color: #F59E0B; margin-bottom: 8px;">⚠️ <b>Disclosure Gap: Fall History</b><br><small style="color:#64748B; margin-left:25px;">Fall in shower (09/2025) noted in APS but not disclosed on application</small></p>
                <p style="color: #EF4444; margin-bottom: 8px;">❌ <b>Identity Check: Invalid SSN</b><br><small style="color:#64748B; margin-left:25px;">SSN provided has only 8 digits (123-45-678)</small></p>
                <p style="color: #EF4444; margin-bottom: 8px;">❌ <b>Financial Check: Invalid Routing #</b><br><small style="color:#64748B; margin-left:25px;">Bank routing number has only 8 digits (02100002)</small></p>
            """, unsafe_allow_html=True)

        # 2. Underwriting Risk Profile
        with st.container(border=True):
            st.markdown("<span style='font-weight: bold; font-size: 1.15rem; color: #1E293B;'>📈 Underwriting Risk Profile</span>", unsafe_allow_html=True)
            st.write("")
            st.markdown("""
            | Risk Domain | Level | Key Drivers |
            |---|---|---|
            | Functional | 🟡 Moderate | Bathing impairment; Fall history |
            | Medical | 🟠 Moderate-High | A1c 8.2%; HTN uncontrolled |
            | Misrepresentation | 🔴 High | Tobacco/NRT discrepancy |
            | Compliance | 🔴 High | Missing signatures/NY forms |
            """)

        # 3. Action Items
        with st.container(border=True):
            st.markdown("<span style='font-weight: bold; font-size: 1.15rem; color: #1E293B;'>⚡ Priority 1 Action Items (Critical)</span>", unsafe_allow_html=True)
            st.write("")
            items = [
                "Obtain applicant e-signature on application",
                "Obtain signed HIPAA Authorization",
                "Attach & sign NY Home Care Disclosure",
                "Attach & sign NY Replacement Notice",
                "Provide existing LTC carrier name and policy number",
                "Provide replacement reason",
                "Provide Sec. 5A Prescription list",
                "Provide Bathing ADL narrative",
                "Provide Advisor NPN/License number"
            ]
            for item in items:
                st.markdown(f"🔴 **{item}**")

def show_emails_page():
    st.subheader("Emails")
    st.caption("Review submission emails and documents")
    
    st.markdown("""
    <div class="email-container">
        <div class="email-header">
            <div style="display: flex; justify-content: space-between;">
                <span style="font-weight: 700; font-size: 1.2rem;">New Commercial Auto Submission - Blue Ridge Office Solution, LLC</span>
                <span style="color: #64748B;">Feb 24, 2026, 10:45 AM</span>
            </div>
            <div style="margin-top: 12px;">
                <span style="color: #64748B;">From:</span> <b style="color: #1E293B;">Sarah Ellis &lt;sarah.ellis@summitpeakins.com&gt;</b>
            </div>
            <div style="margin-top: 4px;">
                <span style="color: #64748B;">To:</span> <b style="color: #1E293B;">Submissions &lt;submissions@doclens.ai&gt;</b>
            </div>
        </div>
        <div class="email-body">
            Hi Team,<br><br>
            Please find the submission for <b>Blue Ridge Office Solution, LLC</b>. This is a new account we are targeting for their Commercial Auto and General Liability needs.<br><br>
            The attached package includes the ACORD 125/137, current driver and vehicle lists, and loss runs for the past 5 years. I've also included the completed supplemental application.<br><br>
            Let me know if you need any additional information to get this quoted.<br><br>
            Best regards,<br>
            <b>Sarah Ellis</b><br>
            Summit Peak Insurance
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("#### Attachments (5)")
    
    attachments = [
        ("📄", "ACORD_125_BlueRidge.pdf", "1.2 MB"),
        ("📊", "Vehicle_Fleet_List.xlsx", "450 KB"),
        ("👤", "Driver_MVR_Reports.zip", "3.8 MB"),
        ("📉", "Loss_Runs_Past_5_Years.pdf", "2.1 MB"),
        ("📝", "Supplemental_Application_Auto.pdf", "890 KB")
    ]
    
    for icon, name, size in attachments:
        st.markdown(f"""
        <div class="email-attachment">
            <span class="attachment-icon">{icon}</span>
            <div style="flex-grow: 1;">
                <div class="attachment-name">{name}</div>
                <div class="attachment-size">{size}</div>
            </div>
            <span class="attachment-download">📥</span>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
