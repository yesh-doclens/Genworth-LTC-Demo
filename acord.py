import streamlit as st
import pandas as pd
import json
import re
from langchain_aws import ChatBedrockConverse

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
    with open("acord.md", "r") as f:
        md = f.read()

    tab1, tab2, tab3 = st.tabs(["📊 **Overview**", "📄 **PDF & Data View**", "💬 **Chat**"])
    
    with tab1:
        st.write("### Application Overview")
        
        # --- Row 1: High Level Header Tiles (Large) ---
        col_hdr1, col_hdr2, col_hdr3 = st.columns([1.5, 1, 1])
        with col_hdr1:
            st.markdown("""
            <div class="status-card" style="border-left: 5px solid #2563EB;">
                <div style="font-size: 0.85rem; color: #64748B; font-weight: 600;">FIRST NAMED INSURED</div>
                <div style="font-size: 1.4rem; font-weight: 700; margin: 4px 0;">Blue Ridge Office Solution, LLC</div>
                <div style="color: #475569; font-size: 0.9rem;">2450 Market Street, Suite 310, Denver, CO 80205</div>
            </div>
            """, unsafe_allow_html=True)
        with col_hdr2:
            st.markdown("""
            <div class="status-card" style="text-align: center;">
                <div style="font-size: 0.85rem; color: #64748B; font-weight: 600;">PROPOSED PREMIUM</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #15803D; margin: 8px 0;">$1,750</div>
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
                    <div><small style="color:#94A3B8;">Safety Program</small><br><span style="color:#15803D; font-weight:600;">Active</span></div>
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

    with tab2:
        col1, col2 = st.columns(spec=[1, 1], gap="medium")
        with col1:
            st.pdf("Acord-125-Commercial-Insurance.pdf", height=800)
        with col2:
            # st.markdown("### Extracted Content")
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

            if custom_text := st.chat_input("Ask about the ACORD data...", key="acord_chat_input"):
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
