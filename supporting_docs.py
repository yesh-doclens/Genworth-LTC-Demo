import streamlit as st
import os
import base64
import json
import re
from universal_chat import get_llm, get_universal_answer

def get_medical_files():
    medical_dir = "medical"
    if not os.path.exists(medical_dir):
        return []
    return [f for f in os.listdir(medical_dir) if f.endswith(".pdf")]

def get_all_medical_context():
    medical_dir = "medical"
    context = ""
    if os.path.exists(medical_dir):
        for f in os.listdir(medical_dir):
            if f.endswith(".md"):
                with open(os.path.join(medical_dir, f), "r") as file:
                    context += f"\n--- File: {f} ---\n"
                    context += file.read()
    return context

def show_supporting_docs_page():
    st.markdown("""
        <style>
        .full-width-tabs [data-baseweb="tab-list"] {
            display: flex;
            width: 100%;
        }
        .full-width-tabs [data-baseweb="tab"] {
            flex: 1;
            text-align: center;
            justify-content: center;
        }
        </style>
    """, unsafe_allow_html=True)

    # st.subheader("Supporting Documents")
    
    # Top-level Tabs for Medical vs Financial
    st.markdown('<div class="full-width-tabs">', unsafe_allow_html=True)
    top_tab1, top_tab2 = st.tabs(["🩺 **Medical Documents**", "💰 **Financial Documents**"])
    st.markdown('</div>', unsafe_allow_html=True)

    with top_tab1:
        files = get_medical_files()
        if not files:
            st.info("No medical documents found.")
            return

        file_mapping = {
            "APS_Snippet_PCP.pdf": "APS.md",
            "Lab_Vitals_Summary.pdf": "lab_vitals.md",
            "Rx_History_Report.pdf": "rx_history.md",
            "Functional_Interview_Call_Notes.pdf": "functional_ADL.md"
        }

        col_sel1, col_sel2 = st.columns([2, 1])
        with col_sel1:
            selected_pdf_filename = st.selectbox("Select Medical Document", files, key="medical_file_select")
        
        selected_pdf = os.path.join("medical", selected_pdf_filename)
        selected_md_filename = file_mapping.get(selected_pdf_filename)
        
        # Load content of selected file
        selected_md = ""
        if selected_md_filename:
            with open(os.path.join("medical", selected_md_filename), "r") as f:
                selected_md = f.read()
        else:
            st.warning("Markdown extraction not found for this PDF.")

        # Internal Tabs for Overview, PDF & Data View, Chat
        tab1, tab2, tab3 = st.tabs(["📊 **Overview**", "📄 **PDF & Data View**", "💬 **Chat**"])

        with tab1:
            st.write("### Medical Overview")
            
            # Extract basic info for tiles (Mocked based on known files context)
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("""
                <div class="status-card" style="border-left: 5px solid #00c2c2;">
                    <div style="font-size: 0.85rem; color: #64748B; font-weight: 600;">KEY VITALS (11/2025)</div>
                    <div style="font-size: 1.1rem; font-weight: 700; margin-top: 8px;">BP: 152/92 <span style="color: #d92d20; font-size: 0.8rem;">(High)</span></div>
                    <div style="font-size: 1.1rem; font-weight: 700;">BMI: 29.8 <span style="color: #ffb800; font-size: 0.8rem;">(Overweight)</span></div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown("""
                <div class="status-card" style="border-left: 5px solid #ffb800;">
                    <div style="font-size: 0.85rem; color: #64748B; font-weight: 600;">LAB RESULTS</div>
                    <div style="font-size: 1.1rem; font-weight: 700; margin-top: 8px;">HbA1c: 8.2% <span style="color: #d92d20; font-size: 0.8rem;">(Poor)</span></div>
                    <div style="font-size: 1.1rem; font-weight: 700;">Glucose: 168 mg/dL</div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown("""
                <div class="status-card" style="border-left: 5px solid #6366F1;">
                    <div style="font-size: 0.85rem; color: #64748B; font-weight: 600;">FUNCTIONAL (ADL)</div>
                    <div style="font-size: 1.1rem; font-weight: 700; margin-top: 8px;">Bathing: <span style="color: #d92d20;">Assisted</span></div>
                    <div style="font-size: 1.1rem; font-weight: 700;">Other: Independent</div>
                </div>
                """, unsafe_allow_html=True)

            with col4:
                st.markdown("""
                <div class="status-card" style="border-left: 5px solid #d92d20;">
                    <div style="font-size: 0.85rem; color: #64748B; font-weight: 600;">FLAGS / CONCERNS</div>
                    <div style="font-size: 0.9rem; font-weight: 700; margin-top: 8px;">⚠️ Recent fall (09/2025)</div>
                    <div style="font-size: 0.9rem; font-weight: 700;">⚠️ Nicotine Patch Claim</div>
                </div>
                """, unsafe_allow_html=True)

            st.write("#### Problem List & Medications")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("""
                <div class="status-card">
                    <div style="font-weight: 600; color: #1E293B; margin-bottom: 12px; border-bottom: 1px solid #F1F5F9; padding-bottom: 8px;">📋 Active Conditions</div>
                    <ul style="margin-bottom: 0;">
                        <li>Type 2 Diabetes Mellitus (dx 2016)</li>
                        <li>Hypertension</li>
                        <li>Hyperlipidemia</li>
                        <li>Osteoarthritis (knees)</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown("""
                <div class="status-card">
                    <div style="font-weight: 600; color: #1E293B; margin-bottom: 12px; border-bottom: 1px solid #F1F5F9; padding-bottom: 8px;">💊 Medications</div>
                    <ul style="margin-bottom: 0;">
                        <li>Metformin 500mg BID</li>
                        <li>Lisinopril 10mg Daily</li>
                        <li>Atorvastatin 20mg Nightly</li>
                        <li>Nicotine Patch 14mg (OTC)</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

        with tab2:
            from streamlit_pdf_viewer import pdf_viewer
            
            col_header, col_toggle = st.columns([2, 1])
            with col_toggle:
                view_mode = st.segmented_control(
                    "View Selection",
                    ["Show Input", "Show Extracted Data", "Show Both"],
                    default="Show Both",
                    key="medical_view_mode",
                    label_visibility="collapsed"
                )

            if view_mode == "Show Both":
                st.markdown('<div class="split-view-container">', unsafe_allow_html=True)
                col_left, col_right = st.columns([1, 1], gap="small")
                with col_left:
                    if selected_pdf:
                        pdf_viewer(selected_pdf, height=800)
                    else:
                        st.warning("PDF version not available.")
                with col_right:
                    with st.container(height=800):
                        st.markdown(selected_md)
                st.markdown('</div>', unsafe_allow_html=True)
            elif view_mode == "Show Input":
                if selected_pdf:
                    pdf_viewer(selected_pdf, height=800)
                else:
                    st.warning("PDF version not available.")
            elif view_mode == "Show Extracted Data":
                with st.container(height=800):
                    st.markdown(selected_md)

        with tab3:
            col1, col2 = st.columns(spec=[1, 1], gap="medium")
            with col1:
                st.write("### Reference Document")
                with st.container(height=800):
                    st.markdown(selected_md)
            with col2:
                st.write("### Chat")
                st.caption("Ask questions about the applicant's medical history across all supporting documents.")
                
                if "medical_chat_history" not in st.session_state:
                    st.session_state["medical_chat_history"] = []
                
                query = st.chat_input("Ask about medical records...", key="medical_chat_input")
                
                if query:
                    with st.spinner("Analyzing medical documents..."):
                        context = get_all_medical_context()
                        answer = get_universal_answer(query, "MEDICAL_RECORDS", context, st.session_state["aws_credentials"], genworth_page=True)
                        st.session_state["medical_chat_history"].append({"role": "user", "content": query})
                        st.session_state["medical_chat_history"].append({"role": "assistant", "content": answer})
                
                # Display chat history in reverse
                for message in reversed(st.session_state["medical_chat_history"]):
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

    with top_tab2:
        st.write("### Financial Documents")
        st.info("No financial documents have been uploaded for this submission yet.")
