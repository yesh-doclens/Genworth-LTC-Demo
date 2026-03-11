import streamlit as st
import pandas as pd
from acord import show_acord_page
from application import show_supplemental_page
from lossrun import show_lossrun_page
from research import show_research_page
from dashboard import show_dashboard
from disturbancies import show_disturbancies_page
import base64
from universal_chat import classify_query, get_tab_context, get_universal_answer
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
            "ACORD Application": True,
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
                base64.b64encode(open("Doclens_logo.png", "rb").read()).decode()
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
        
        if st.session_state["selected_submission"]:
            st.markdown('<p class="sidebar-category">Uploads</p>', unsafe_allow_html=True)
            
            # ACORD Application
            is_acord_active = st.session_state["current_view"] == "ACORD Application"
            if st.button("📄 ACORD Application", use_container_width=True, key="nav_acord", disabled=is_acord_active):
                st.session_state["current_view"] = "ACORD Application"
                st.session_state["sub_view"] = "Agency Information"
                st.rerun()

            # Loss Run Insights
            is_loss_active = st.session_state["current_view"] == "Loss Run Insights"
            if st.button("📉 Loss Run Insights", use_container_width=True, key="nav_lossrun", disabled=is_loss_active):
                st.session_state["current_view"] = "Loss Run Insights"
                st.session_state["sub_view"] = "History"
                st.rerun()

            # Supplemental Application
            is_supp_active = st.session_state["current_view"] == "Supplemental Application"
            if st.button("📝 Supplemental Application", use_container_width=True, key="nav_supp", disabled=is_supp_active):
                st.session_state["current_view"] = "Supplemental Application"
                st.session_state["sub_view"] = "Insured Details"
                st.rerun()

            # st.markdown('<p class="sidebar-category">Communication</p>', unsafe_allow_html=True)
            is_emails_active = st.session_state["current_view"] == "Emails"
            if st.button("📧 Emails", use_container_width=True, key="nav_emails", disabled=is_emails_active):
                st.session_state["current_view"] = "Emails"
                st.session_state["sub_view"] = None
                st.rerun()

            st.markdown('<p class="sidebar-category">Enrichment</p>', unsafe_allow_html=True)

            # Account Research
            is_research_active = st.session_state["current_view"] == "Account Research"
            if st.button("🔍 Account Research", use_container_width=True, key="nav_research", disabled=is_research_active):
                st.session_state["current_view"] = "Account Research"
                st.session_state["sub_view"] = None
                st.rerun()
            
            st.markdown('<p class="sidebar-category">Review</p>', unsafe_allow_html=True)

            is_comp_active = st.session_state["current_view"] == "Completeness Check"
            if st.button("✅ Completeness Check", use_container_width=True, disabled=is_comp_active):
                st.session_state["current_view"] = "Completeness Check"
                st.session_state["sub_view"] = None
                st.rerun()

            # Disturbancies
            is_dist_active = st.session_state["current_view"] == "Discrepancies"
            if st.button("⚠️ Discrepancies", use_container_width=True, disabled=is_dist_active):
                st.session_state["current_view"] = "Discrepancies"
                st.session_state["sub_view"] = None
                st.rerun()
            
        st.divider()
        if st.button("🔄 Change Credentials", use_container_width=True):
            st.session_state["aws_credentials"] = None
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state["selected_submission"]:
        # --- Header Section ---
        col_h1, col_h2 = st.columns([3, 1.2])

        with col_h1:
            st.caption(f"Submissions > {st.session_state["selected_submission"]} > {st.session_state['current_view']}")
            st.markdown(f"<h1>{st.session_state['selected_submission']} <span class='status-tag'>Incomplete ▾</span></h1>", unsafe_allow_html=True)
            st.caption("SUB-000001 • 24 Feb 2026")

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
                
                context = get_tab_context(category, st.session_state["aws_credentials"], query, filters)
                answer = get_universal_answer(query, category, context, st.session_state["aws_credentials"])
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
    elif st.session_state["current_view"] == "ACORD Application":
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

def show_completeness_dashboard():
    st.subheader("Completeness Check")

    # Completeness Card
    st.markdown("""
    <div class="status-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: bold; font-size: 1.1rem;">Improve this completeness</span>
            <span class="badge-orange">2 / 3 checks passed</span>
        </div>
        <hr style="border: 0.5px solid #F1F5F9; margin: 20px 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
            <span><span style="color:#22C55E">●</span> <b>ACORD</b><br><small style="color:#64748B; margin-left:18px;">20 / 21 fields present</small></span>
            <a class="view-link" href="#">View ></a>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
            <span><span style="color:#F59E0B">!</span> <b>Supplemental Application</b><br><small style="color:#C2410C; margin-left:18px;">12 / 28 fields present</small></span>
            <a class="view-link" href="#">View ></a>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
