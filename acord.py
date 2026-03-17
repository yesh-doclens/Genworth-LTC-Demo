import streamlit as st
from main import get_pdf_base64
import pandas as pd
import json
import re
from langchain_aws import ChatBedrockConverse
from streamlit_pdf_viewer import pdf_viewer
from configurations import page


genworth_page = page != "genworth"
def show_acord_page():
    modelId = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
    
    llm = ChatBedrockConverse(
        model_id=modelId,
        region_name="us-east-2",
        max_tokens=1500,
        aws_access_key_id=st.session_state["aws_credentials"]["aws_access_key"],
        aws_secret_access_key=st.session_state["aws_credentials"]["aws_secret_key"],
        aws_session_token=st.session_state["aws_credentials"]["aws_session_token"],
    )

    with open("policy.json", "r") as f:
        policy_data = json.load(f)

    acord_path = "acord.md" if genworth_page else "form_genworth.md"
    with open(acord_path, "r") as f:
        md = f.read()

    tab1, tab2, tab3 = st.tabs(["📊 **Overview**", "📄 **PDF & Data View**", "💬 **Chat**"])
    
    with tab1:
        st.write("### Application Overview")
        
        if genworth_page:
            # --- Row 1: High Level Header Tiles (Large) ---
            col_hdr1, col_hdr2, col_hdr3 = st.columns([1.5, 1, 1])
            with col_hdr1:
                st.markdown("""
                <div class="status-card" style="border-left: 5px solid #00c2c2;">
                    <div style="font-size: 0.85rem; color: #64748B; font-weight: 600;">FIRST NAMED INSURED</div>
                    <div style="font-size: 1.4rem; font-weight: 700; margin: 4px 0;">Blue Ridge Office Solution, LLC</div>
                    <div style="color: #475569; font-size: 0.9rem;">2450 Market Street, Suite 310, Denver, CO 80205</div>
                </div>
                """, unsafe_allow_html=True)
            with col_hdr2:
                st.markdown("""
                <div class="status-card" style="text-align: center;">
                    <div style="font-size: 0.85rem; color: #64748B; font-weight: 600;">PROPOSED PREMIUM</div>
                    <div style="font-size: 1.8rem; font-weight: 800; color: #00c2c2; margin: 8px 0;">$1,750</div>
                    <div style="font-size: 0.75rem; color: #64748B;">Minimum Policy Premium</div>
                </div>
                """, unsafe_allow_html=True)
            with col_hdr3:
                 st.markdown("""
                <div class="status-card" style="text-align: center;">
                    <div style="font-size: 0.85rem; color: #64748B; font-weight: 600;">SUBMISSION STATUS</div>
                    <div style="margin-top: 12px;"><span class="status-tag" style="font-size: 1rem; padding: 6px 16px;">QUOTE REQUESTED</span></div>
                    <div style="font-size: 0.75rem; color: #64748B; margin-top: 8px;">Effective: 04/01/2023</div>
                </div>
                """, unsafe_allow_html=True)

            # --- Row 2: Detailed Info Tiles (Medium Grid) ---
            st.write("#### Core Information")
            col_info1, col_info2 = st.columns(2)
            with col_info1:
                st.markdown("""
                <div class="status-card">
                    <div style="font-weight: 600; color: #1E293B; margin-bottom: 16px; border-bottom: 1px solid #F1F5F9; padding-bottom: 8px;">🏢 Agency & Producer</div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                        <div><small style="color:#94A3B8;">Agency Name</small><br><b>Summit Peak Insurance</b></div>
                        <div><small style="color:#94A3B8;">Producer Name</small><br><b>Sarah Ellis</b></div>
                        <div><small style="color:#94A3B8;">Agency ID</small><br><b>GPA-001417</b></div>
                        <div><small style="color:#94A3B8;">Producer License</small><br><b>Sarah Ellis (Signed)</b></div>
                        <div><small style="color:#94A3B8;">Phone</small><br><b>703-550-4210</b></div>
                        <div><small style="color:#94A3B8;">Email</small><br><b>ellis@summitpeakins.com</b></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="status-card">
                    <div style="font-weight: 600; color: #1E293B; margin-bottom: 16px; border-bottom: 1px solid #F1F5F9; padding-bottom: 8px;">📄 Policy Details</div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                        <div><small style="color:#94A3B8;">Carrier</small><br><b>Pioneer Mutual</b></div>
                        <div><small style="color:#94A3B8;">Policy Number</small><br><b>GL-4592329</b></div>
                        <div><small style="color:#94A3B8;">Billing Plan</small><br><b>Direct</b></div>
                        <div><small style="color:#94A3B8;">Payment Plan</small><br><b>Annual-AH</b></div>
                        <div><small style="color:#94A3B8;">Deposit</small><br><b>$1,250</b></div>
                        <div><small style="color:#94A3B8;">Audit Type</small><br><b>None Specified</b></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col_info2:
                st.markdown("""
                <div class="status-card">
                    <div style="font-weight: 600; color: #1E293B; margin-bottom: 16px; border-bottom: 1px solid #F1F5F9; padding-bottom: 8px;">👤 Applicant Details</div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                        <div><small style="color:#94A3B8;">FEIN / Tax ID</small><br><b>84-2354321</b></div>
                        <div><small style="color:#94A3B8;">Business Type</small><br><b>LLC</b></div>
                        <div><small style="color:#94A3B8;">SIC Code</small><br><b>7379</b></div>
                        <div><small style="color:#94A3B8;">NAICS Code</small><br><b>56210</b></div>
                        <div><small style="color:#94A3B8;">Official Website</small><br><b>blueridgeoffice.com</b></div>
                        <div><small style="color:#94A3B8;">Business Phone</small><br><b>(303) 555-0123</b></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("""
                <div class="status-card">
                    <div style="font-weight: 600; color: #1E293B; margin-bottom: 16px; border-bottom: 1px solid #F1F5F9; padding-bottom: 8px;">📍 Premises & Operations</div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                        <div><small style="color:#94A3B8;">Location</small><br><b>Denver, CO</b></div>
                        <div><small style="color:#94A3B8;">Annual Revenues</small><br><b>$1,850,000</b></div>
                        <div><small style="color:#94A3B8;">Full-Time Staff</small><br><b>8 Employees</b></div>
                        <div><small style="color:#94A3B8;">Occupied Area</small><br><b>3,200 sq ft</b></div>
                        <div><small style="color:#94A3B8;">Safety Program</small><br><span style="color:#00c2c2; font-weight:600;">Active</span></div>
                        <div><small style="color:#94A3B8;">Interest</small><br><b>Tenant</b></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # --- Row 3: Attached Sections (Small Tiles List) ---
            st.write("#### Attached Coverage Sections")
            cols_sec = st.columns(4)
            sections = [
                ("Crime", "$50,000"),
                ("Equip Floater", "$35,000"),
                ("Property", "$250,000"),
                ("Umbrella", "$1M")
            ]
            for i, (name, val) in enumerate(sections):
                with cols_sec[i]:
                    st.markdown(f"""
                    <div style="background: white; border: 1px solid #E2E8F0; padding: 12px; border-radius: 8px; text-align: center;">
                        <div style="font-size: 0.75rem; color: #64748B; margin-bottom: 4px;">{name.upper()}</div>
                        <div style="font-weight: 700; color: #1E293B;">{val}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            # --- Genworth Layout (similar tiles from form_genworth.md) ---
            # --- Row 1: High Level Header Tiles (Large) ---
            col_hdr1, col_hdr2, col_hdr3 = st.columns([1.5, 1, 1])
            with col_hdr1:
                st.markdown("""
                <div class="status-card" style="border-left: 5px solid #FF4B4B;">
                    <div style="font-size: 0.85rem; color: #64748B; font-weight: 600;">APPLICANT / PROPOSED INSURED</div>
                    <div style="font-size: 1.4rem; font-weight: 700; margin: 4px 0;">Jordan A. Taylor</div>
                    <div style="color: #475569; font-size: 0.9rem;">115 W 57th St, New York, NY 10019</div>
                </div>
                """, unsafe_allow_html=True)
            with col_hdr2:
                st.markdown("""
                <div class="status-card" style="text-align: center;">
                    <div style="font-size: 0.85rem; color: #64748B; font-weight: 600;">INITIAL PREMIUM</div>
                    <div style="font-size: 1.8rem; font-weight: 800; color: #00c2c2; margin: 1px 0;">$312.45</div>
                    <div style="font-size: 0.75rem; color: #64748B;">Mode: Monthly (EFT/ACH)</div>
                </div>
                """, unsafe_allow_html=True)
            with col_hdr3:
                 st.markdown("""
                <div class="status-card" style="text-align: center;">
                    <div style="font-size: 0.85rem; color: #64748B; font-weight: 600;">SUBMISSION STATUS</div>
                    <div style="margin-top: 12px;"><span class="status-tag" style="font-size: 1rem; padding: 6px 16px; background-color: #FEE2E2; color: #EF4444;">NIGO (Not In Good Order)</span></div>
                    <div style="font-size: 0.75rem; color: #64748B; margin-top: 8px;">Effective: 04/01/2026</div>
                </div>
                """, unsafe_allow_html=True)

            # --- Row 2: Detailed Info Tiles (Medium Grid) ---
            st.write("#### Core Information")
            col_info1, col_info2 = st.columns(2)
            with col_info1:
                st.markdown("""
                <div class="status-card">
                    <div style="font-weight: 600; color: #1E293B; margin-bottom: 16px; border-bottom: 1px solid #F1F5F9; padding-bottom: 8px;">🏢 Carrier & Product</div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                        <div><small style="color:#94A3B8;">Carrier</small><br><b>Demo Carrier – LTC Division</b></div>
                        <div><small style="color:#94A3B8;">Product</small><br><b>Traditional LTC</b></div>
                        <div><small style="color:#94A3B8;">Application ID</small><br><b>LTC-NY-2026-000174</b></div>
                        <div><small style="color:#94A3B8;">Submission Channel</small><br><b>Advisor</b></div>
                        <div><small style="color:#94A3B8;">State of App</small><br><b>NY</b></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="status-card">
                    <div style="font-weight: 600; color: #1E293B; margin-bottom: 16px; border-bottom: 1px solid #F1F5F9; padding-bottom: 8px;">👤 Applicant Details</div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                        <div><small style="color:#94A3B8;">DOB</small><br><b>07/14/1961</b></div>
                        <div><small style="color:#94A3B8;">Gender</small><br><b>Male</b></div>
                        <div><small style="color:#94A3B8;">Marital Status</small><br><b>Married</b></div>
                        <div><small style="color:#94A3B8;">SSN/Tax ID</small><br><span style="color:#EF4444;">123-45-678 (⚠️)</span></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col_info2:
                st.markdown("""
                <div class="status-card">
                    <div style="font-weight: 600; color: #1E293B; margin-bottom: 16px; border-bottom: 1px solid #F1F5F9; padding-bottom: 8px;">📈 Coverage & Benefit Design</div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                        <div><small style="color:#94A3B8;">Plan Type</small><br><b>Home Care Only</b></div>
                        <div><small style="color:#94A3B8;">Benefit Amount</small><br><b>$200 per day</b></div>
                        <div><small style="color:#94A3B8;">Benefit Period</small><br><b>5 years</b></div>
                        <div><small style="color:#94A3B8;">Elimination Period</small><br><b>90 days</b></div>
                        <div><small style="color:#94A3B8;">Inflation Option</small><br><b>3% Compound</b></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("""
                <div class="status-card">
                    <div style="font-weight: 600; color: #1E293B; margin-bottom: 16px; border-bottom: 1px solid #F1F5F9; padding-bottom: 8px;">👨‍💼 Advisor Information</div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                        <div><small style="color:#94A3B8;">Advisor Name</small><br><b>Casey Morgan</b></div>
                        <div><small style="color:#94A3B8;">Agency/Firm</small><br><b>NorthStar Financial</b></div>
                        <div><small style="color:#94A3B8;">License(s)</small><br><b>NY, NJ</b></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # --- Row 3: NIGO Summary (Small Tiles List) ---
            st.write("#### Deficiencies Summary")
            cols_def = st.columns(4)
            deficiencies = [
                ("Critical Issues", "14"),
                ("Minor Issues", "1"),
                ("Total Deficiencies", "15"),
                ("Action Required", "Resolve NIGO")
            ]
            for i, (name, val) in enumerate(deficiencies):
                with cols_def[i]:
                    st.markdown(f"""
                    <div style="background: white; border: 1px solid #E2E8F0; padding: 12px; border-radius: 8px; text-align: center;">
                        <div style="font-size: 0.75rem; color: #64748B; margin-bottom: 4px;">{name.upper()}</div>
                        <div style="font-weight: 700; color: {'#EF4444' if i==0 else '#1E293B'};">{val}</div>
                    </div>
                    """, unsafe_allow_html=True)

    with tab2:
        col_header, col_toggle = st.columns([2, 1])
        with col_toggle:
            view_mode = st.segmented_control(
                "View Selection",
                ["Show Input", "Show Extracted Data", "Show Both"],
                # index=2,
                # horizontal=True,
                default="Show Both",
                key="acord_view_mode",
                label_visibility="collapsed"
            )   
        pdf_path = "Acord-125-Commercial-Insurance.pdf" if genworth_page else "NIGO_Filled_LTC_Application_NY.pdf"

        if view_mode == "Show Both":
            st.markdown('<div class="split-view-container">', unsafe_allow_html=True)
            col_left, col_right = st.columns([1, 1], gap="small")
            with col_left:
                pdf_base64 = get_pdf_base64(pdf_path)
                # st.markdown(f'<div class="resizable-input-container"><iframe src="{pdf_base64}#toolbar=1" type="application/pdf"></iframe></div>', unsafe_allow_html=True)
                pdf_viewer(pdf_path, height=800)
            with col_right:
                with st.container(height=800):
                    st.markdown(md)
            st.markdown('</div>', unsafe_allow_html=True)
        elif view_mode == "Show Input":
            st.pdf(pdf_path, height=800)
        elif view_mode == "Show Extracted Data":
            with st.container(height=800):
                st.markdown(md)

    with tab3:
        col1, col2 = st.columns(spec=[1, 1], gap="medium")
        with col1:
            # st.markdown("### Extracted Reference")
            with st.container(height=800):
                st.markdown(md)
        with col2:
            st.markdown("### Chat")
            if "acord_chat" not in st.session_state:
                st.session_state.acord_chat = []
            form_name = "ACORD" if genworth_page else "FORM"
            if custom_text := st.chat_input(f"Ask about the {form_name} data...", key="acord_chat_input"):
                prompt = custom_text
                with st.chat_message("user"):
                    st.markdown(prompt)
                with st.chat_message("assistant"):
                    with st.spinner("Analyzing ACORD application..."):
                        response = llm.invoke(prompt + md)
                    st.markdown(response.content)
                    st.session_state.acord_chat.append({"role": "assistant", "content": response.content})
                    st.session_state.acord_chat.append({"role": "user", "content": prompt})

            # Display chat history
            if len(st.session_state.acord_chat) >= 2:
                for message in st.session_state.acord_chat[:-2][::-1]:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])
            elif len(st.session_state.acord_chat) > 0:
                 for message in st.session_state.acord_chat[::-1]:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])
