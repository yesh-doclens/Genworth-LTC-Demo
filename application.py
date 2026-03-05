import streamlit as st
from main import get_pdf_base64
import json
from langchain_aws import ChatBedrockConverse

def show_supplemental_page():
    modelId = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"

    llm = ChatBedrockConverse(
        model_id=modelId,
        region_name="us-east-2",
        max_tokens=1500,
        aws_access_key_id=st.session_state["aws_credentials"]["aws_access_key"],
        aws_secret_access_key=st.session_state["aws_credentials"]["aws_secret_key"],
        aws_session_token=st.session_state["aws_credentials"]["aws_session_token"],
    )

    with open("quote.json", "r") as f:
        quote_data = json.load(f)
    with open("application.md", "r") as f:
        md = f.read()

    # --- High Level Sections ---
    ni = quote_data.get("quotationRequest", {}).get("namedInsuredInformation", {})
    
    tab1, tab2, tab3 = st.tabs(["📊 **Overview**", "📄 **PDF & Data View**", "💬 **Chat**"])

    with tab1:
        st.write("### Supplemental Application Overview")
        
        # Row 1: Insured Header (Large)
        st.markdown(f"""
        <div class="status-card" style="border-left: 5px solid #00c2c2;">
            <div style="font-size: 0.85rem; color: #64748B; font-weight: 600;">NAMED INSURED</div>
            <div style="font-size: 1.4rem; font-weight: 700; margin: 4px 0;">{ni.get("nameOfInsured") or "Summit Peak Properties"}</div>
            <div style="display: flex; gap: 20px; margin-top: 8px;">
                <div><small style="color:#64748B;">Website</small><br><b>{ni.get("website") or "www.summitpeak.com"}</b></div>
                <div><small style="color:#64748B;">FEIN</small><br><b>{ni.get("federalTaxId") or "843093126"}</b></div>
                <div><small style="color:#64748B;">Years in Biz</small><br><b>{ni.get("yearsInBusiness") or "01"}</b></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Row 2: Operational Details
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="status-card">
                <div style="font-weight: 600; color: #64748B; margin-bottom: 12px; border-bottom: 1px solid #F1F5F9; padding-bottom: 8px;">⚙️ Operations</div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                    <div style="grid-column: span 2;"><small style="color:#94A3B8;">Description</small><br><b>Steel reinforcing/rebar</b></div>
                    <div><small style="color:#94A3B8;">Hours</small><br><b>7 to 7</b></div>
                    <div><small style="color:#94A3B8;">Shifts</small><br><b>01</b></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="status-card">
                <div style="font-weight: 600; color: #64748B; margin-bottom: 12px; border-bottom: 1px solid #F1F5F9; padding-bottom: 8px;">🛡️ Risk & Safety</div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                    <div><small style="color:#94A3B8;">Payroll Liens</small><br><b style="color:#00c2c2;">No</b></div>
                    <div><small style="color:#94A3B8;">Bankruptcy</small><br><b style="color:#00c2c2;">No</b></div>
                    <div><small style="color:#94A3B8;">Safety Program</small><br><span class="status-tag" style="background-color: #DCFCE7; color: #166534;">ACTIVE</span></div>
                    <div><small style="color:#94A3B8;">Compliance</small><br><b style="color:#00c2c2;">Yes</b></div>
                </div>
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
                key="application_view_mode",
                label_visibility="collapsed"
            )

        if view_mode == "Show Both":
            st.markdown('<div class="split-view-container">', unsafe_allow_html=True)
            col_left, col_right = st.columns([1, 1], gap="small")
            with col_left:
                pdf_path = "Limousine_Quotation_Application_Fleet_fillable.pdf"
                # try:
                #     pdf_base64 = get_pdf_base64(pdf_path)
                #     # Using a more robust iframe embed with type and data
                #     pdf_display = f'<div class="resizable-input-container"><iframe src="{pdf_base64}#toolbar=0" type="application/pdf"></iframe></div>'
                #     st.markdown(pdf_display, unsafe_allow_html=True)
                # except Exception as e:
                #     st.error(f"Error loading PDF: {e}")
                #     st.pdf(pdf_path, height=800)
                st.pdf(pdf_path, height=800)
            with col_right:
                with st.container(height=800):
                    st.markdown(md)
            st.markdown('</div>', unsafe_allow_html=True)
        elif view_mode == "Show Input":
            st.pdf("Limousine_Quotation_Application_Fleet_fillable.pdf", height=800)
        elif view_mode == "Show Extracted Data":
            with st.container(height=800):
                st.markdown(md)

    with tab3:
        col1, col2 = st.columns(spec=[1, 1], gap="medium")
        with col1:
            st.markdown("### Data Reference")
            with st.container(height=800):
                st.markdown(md)
        with col2:
            st.markdown("### Chat")
            if "csv_messages" not in st.session_state:
                st.session_state.csv_messages = []

            if custom_text := st.chat_input("Ask about the supplemental application...", key="supp_chat_input"):
                prompt = custom_text
                with st.chat_message("user"):
                    st.markdown(prompt)
                with st.chat_message("assistant"):
                    with st.spinner("Analyzing application..."):
                        response = llm.invoke(prompt + md)
                    st.markdown(response.content)
                    st.session_state.csv_messages.append({"role": "assistant", "content": response.content})
                    st.session_state.csv_messages.append({"role": "user", "content": prompt})

            # Display chat history
            if len(st.session_state.csv_messages) >= 2:
                for message in st.session_state.csv_messages[:-2][::-1]:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])
            elif len(st.session_state.csv_messages) > 0:
                 for message in st.session_state.csv_messages[::-1]:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])
