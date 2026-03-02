import streamlit as st
import pandas as pd
from acord import show_acord_page
from application import show_supplemental_page
from lossrun import show_lossrun_page

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="Summit Peak Insurance Agency Dashboard")

# --- Custom CSS for Styling ---
st.markdown(
    """
    <style>
    .stApp { background-color: #F8FAFC; }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }
    
    /* Card-like containers */
    .status-card {
        background-color: white;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
        color: #1E293B;
    }
    
    /* Status Tag (The 'Incomplete' label) */
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
        color: #C2410C;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .badge-green {
        background-color: #F0FDF4;
        color: #15803D;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }

    /* Links/View buttons */
    .view-link {
        color: #64748B;
        text-decoration: none;
        font-size: 0.9rem;
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
        border-color: #CBD5E1;
        color: #1E293B;
    }
    
    /* Primary Button Styling */
    .stButton > button[kind="primary"] {
        background-color: #2563EB;
        color: white;
        border: none;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #1D4ED8;
    }

    /* Sidebar Button Specifics (Top-level) */
    section[data-testid="stSidebar"] div.stButton > button {
        border: 1px solid #E2E8F0 !important;
        background-color: #FFFFFF !important;
        margin-bottom: 6px !important;
        padding: 10px 16px !important;
        font-weight: 500 !important;
        width: 100% !important;
        border-radius: 8px !important;
        text-align: left !important;
        display: flex !important;
        justify-content: space-between !important;
    }
    section[data-testid="stSidebar"] div.stButton > button:hover {
        background-color: #F8FAFC !important;
        border-color: #2563EB !important;
        color: #2563EB !important;
    }

    /* Tree Branch Connector (L-shape) */
    .tree-branch {
        display: flex;
        height: 32px;
        align-items: center;
        margin-left: 20px;
    }
    .tree-connector-v {
        border-left: 2px solid #CBD5E1; /* Muted slate branch */
        height: 100%;
        margin-right: 0px;
    }
    .tree-connector-h {
        border-bottom: 2px solid #CBD5E1;
        width: 14px;
        height: 16px;
        margin-right: 8px;
    }

    /* Sub-navigation link style (Borderless and Transparent) */
    section[data-testid="stSidebar"] [data-testid="column"] div.stButton > button {
        border: none !important;
        background: transparent !important;
        padding: 0px !important;
        font-size: 0.88rem !important;
        color: #475569 !important;
        margin: 0px !important;
        height: 32px !important;
        width: 100% !important;
        text-align: left !important;
        font-weight: 400 !important;
        box-shadow: none !important;
    }
    section[data-testid="stSidebar"] [data-testid="column"] div.stButton > button:hover {
        color: #2563EB !important;
        background: transparent !important;
    }

    /* Active Sub-view Styling */
    .active-subview {
        color: #2563EB !important;
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
        color: #2563EB;
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
    </style>
    """,
    unsafe_allow_html=True,
)


def main():
    if "aws_credentials" not in st.session_state:
        st.session_state["aws_credentials"] = None
    
    if "current_view" not in st.session_state:
        st.session_state["current_view"] = "Completeness Check"
        
    if "sub_view" not in st.session_state:
        st.session_state["sub_view"] = "Agency Information"

    if "expanded_sections" not in st.session_state:
        st.session_state["expanded_sections"] = {
            "ACORD Application": True,
            "Loss Run Insights": False,
            "Supplemental Application": False
        }

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
        st.image("Doclens_logo.png", width=100, use_container_width=True)
        st.write("# SubmissionLens")
        
        # Sidebar Search
        # st.text_input("Search", label_visibility="collapsed", placeholder="🔍 Search", key="sidebar_search")
        
        # st.write("### Navigation")
        
        # --- Custom Document Navigation (Tree-like & Collapsible) ---
        
        # ACORD Application
        expanded_acord = st.session_state["expanded_sections"]["ACORD Application"]
        icon_acord = "▼" if expanded_acord else "▶"
        label_acord = f"📄 ACORD Application {icon_acord}"
        if st.button(label_acord, use_container_width=True, key="nav_acord"):
            # If already active and expanded, toggle close. If not active, switch to it.
            if st.session_state["current_view"] == "ACORD Application":
                st.session_state["expanded_sections"]["ACORD Application"] = not expanded_acord
            else:
                st.session_state["current_view"] = "ACORD Application"
                st.session_state["sub_view"] = "Agency Information"
                st.session_state["expanded_sections"]["ACORD Application"] = True
            st.rerun()
            
        if st.session_state["expanded_sections"]["ACORD Application"]:
            for sub in ["Agency Information", "Applicant Information", "Premises Information"]:
                c1, c2 = st.columns([0.15, 0.85])
                with c1:
                    st.markdown('<div class="tree-branch"><div class="tree-connector-v"></div><div class="tree-connector-h"></div></div>', unsafe_allow_html=True)
                with c2:
                    is_active = st.session_state.get("sub_view") == sub
                    label = f"● {sub}" if is_active else sub
                    if st.button(label, use_container_width=True, key=f"sub_{sub.lower().replace(' ', '_')}"):
                        st.session_state["current_view"] = "ACORD Application"
                        st.session_state["sub_view"] = sub
                        st.rerun()

        # Loss Run Insights
        expanded_loss = st.session_state["expanded_sections"]["Loss Run Insights"]
        icon_loss = "▼" if expanded_loss else "▶"
        label_loss = f"📉 Loss Run Insights {icon_loss}"
        if st.button(label_loss, use_container_width=True, key="nav_lossrun"):
            if st.session_state["current_view"] == "Loss Run Insights":
                st.session_state["expanded_sections"]["Loss Run Insights"] = not expanded_loss
            else:
                st.session_state["current_view"] = "Loss Run Insights"
                st.session_state["sub_view"] = "History"
                st.session_state["expanded_sections"]["Loss Run Insights"] = True
            st.rerun()
            
        if st.session_state["expanded_sections"]["Loss Run Insights"]:
            subs = {"History": "Loss History Summary", "Insights": "Agent Insights"}
            for key, disp in subs.items():
                c1, c2 = st.columns([0.15, 0.85])
                with c1:
                    st.markdown('<div class="tree-branch"><div class="tree-connector-v"></div><div class="tree-connector-h"></div></div>', unsafe_allow_html=True)
                with c2:
                    is_active = st.session_state.get("sub_view") == key
                    label = f"● {disp}" if is_active else disp
                    if st.button(label, use_container_width=True, key=f"sub_{key.lower()}"):
                        st.session_state["current_view"] = "Loss Run Insights"
                        st.session_state["sub_view"] = key
                        st.rerun()

        # Supplemental Application
        expanded_supp = st.session_state["expanded_sections"]["Supplemental Application"]
        icon_supp = "▼" if expanded_supp else "▶"
        label_supp = f"📝 Supplemental Application {icon_supp}"
        if st.button(label_supp, use_container_width=True, key="nav_supp"):
            if st.session_state["current_view"] == "Supplemental Application":
                st.session_state["expanded_sections"]["Supplemental Application"] = not expanded_supp
            else:
                st.session_state["current_view"] = "Supplemental Application"
                st.session_state["sub_view"] = "Insured Details"
                st.session_state["expanded_sections"]["Supplemental Application"] = True
            st.rerun()
            
        if st.session_state["expanded_sections"]["Supplemental Application"]:
            subs = {"Insured Details": "Insured Details", "Operational Information": "Operational Info", "Safety Program & Organization": "Safety Program & Org"}
            for full, disp in subs.items():
                c1, c2 = st.columns([0.15, 0.85])
                with c1:
                    st.markdown('<div class="tree-branch"><div class="tree-connector-v"></div><div class="tree-connector-h"></div></div>', unsafe_allow_html=True)
                with c2:
                    is_active = st.session_state.get("sub_view") == full
                    label = f"● {disp}" if is_active else disp
                    if st.button(label, use_container_width=True, key=f"sub_{full.lower().replace(' ', '_')}"):
                        st.session_state["current_view"] = "Supplemental Application"
                        st.session_state["sub_view"] = full
                        st.rerun()

        label_emails = "📧 **Emails**" if st.session_state["current_view"] == "Emails" else "📧 Emails"
        if st.button(label_emails, use_container_width=True, key="nav_emails"):
            st.session_state["current_view"] = "Emails"
            st.session_state["sub_view"] = None
            st.rerun()

        st.divider()
        st.write("### Review")
        st.caption("CHECKLIST")
        if st.button("✅ Completeness Check", use_container_width=True):
            st.session_state["current_view"] = "Completeness Check"
            st.session_state["sub_view"] = None
            st.rerun()
            
        st.divider()
        if st.button("🔄 Change Credentials", use_container_width=True):
            st.session_state["aws_credentials"] = None
            st.rerun()

    # --- Header Section ---
    col_h1, col_h2 = st.columns([3, 1.2])

    with col_h1:
        st.caption(f"Submissions > Summit Peak Insurance Agency > {st.session_state['current_view']}")
        st.markdown(f"<h1>Summit Peak Insurance Agency <span class='status-tag'>Incomplete ▾</span></h1>", unsafe_allow_html=True)
        st.caption("SUB-000001 • Bill Brothers • Agent Name • 24 Sep 2026")

    with col_h2:
        st.write("##") # Spacer
        btn_col1, btn_col2 = st.columns(2)
        btn_col1.button("🚫 Reject", use_container_width=True)
        btn_col2.button("Generate Summary", type="primary", use_container_width=True)

    # --- AI Input Bar ---
    st.text_input("✨ Ask anything", label_visibility="collapsed", placeholder="Ask anything related to this account...", key="global_ai_chat")

    st.divider()

    # --- Content Body ---
    if st.session_state["current_view"] == "Completeness Check":
        show_completeness_dashboard()
    elif st.session_state["current_view"] == "ACORD Application":
        show_acord_page()
    elif st.session_state["current_view"] == "Supplemental Application":
        show_supplemental_page()
    elif st.session_state["current_view"] == "Loss Run Insights":
        show_lossrun_page()

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

if __name__ == "__main__":
    main()
