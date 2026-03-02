import streamlit as st
import pandas as pd
import re
import plotly.express as px
from main import ask_agent, configure_agent

def show_lossrun_page():
    CSV_FILE = "Loss Run.csv"
    IMAGE = "loss-run-cw.pdf"

    st.write("### Loss Run Insights")
    
    # Custom CSS to make bordered containers look like tiles
    st.markdown("""
    <style>
    /* Make Streamlit bordered containers look like our status-card */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: white !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin-bottom: 24px !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] > div {
        padding: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    col_sel1, col_sel2 = st.columns([1, 2])
    with col_sel1:
        add_selectbox = st.selectbox("Select Loss Run document", (CSV_FILE, IMAGE), key="lr_doc_select")
    
    if add_selectbox == CSV_FILE:
        st.session_state.filename = CSV_FILE
        df = pd.read_csv(CSV_FILE)
    elif add_selectbox == IMAGE:
        IMAGE_CSV_FILE = "loss-run-cw.csv"
        st.session_state.filename = IMAGE_CSV_FILE
        df = pd.read_csv(IMAGE_CSV_FILE)

    tab1, tab2, tab3 = st.tabs(["📊 **Overview**", "📄 **Document & Data View**", "💬 **Loss Run Agent**"])

    with tab1:
        # --- Robust Metrics Calculation ---
        total_claims = df['Claim Number'].nunique() if 'Claim Number' in df.columns else 0
        total_incurred = df['Total Incurred'].sum() if 'Total Incurred' in df.columns else 0
        
        # Open Claims: Handle schema differences
        open_claims = 0
        if 'Open Claim' in df.columns:
            open_claims = df[df['Open Claim'] == 'X']['Claim Number'].nunique()
        elif 'Status' in df.columns:
            open_claims = df[df['Status'].str.contains('O', case=False, na=False)]['Claim Number'].nunique()

        # Header Summary Tiles (Dynamic)
        st.write("#### Claims Summary")
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            st.markdown(f"""
            <div class="status-card" style="text-align: center; border-top: 4px solid #2563EB;">
                <div style="font-size: 0.85rem; color: #64748B; font-weight: 600;">TOTAL CLAIMS</div>
                <div style="font-size: 2rem; font-weight: 800; color: #1E293B; margin: 8px 0;">{total_claims}</div>
                <div style="font-size: 0.75rem; color: #64748B;">Distinct Claim Numbers</div>
            </div>
            """, unsafe_allow_html=True)
        with col_s2:
            st.markdown(f"""
            <div class="status-card" style="text-align: center; border-top: 4px solid #15803D;">
                <div style="font-size: 0.85rem; color: #64748B; font-weight: 600;">TOTAL INCURRED</div>
                <div style="font-size: 2rem; font-weight: 800; color: #15803D; margin: 8px 0;">${total_incurred:,.0f}</div>
                <div style="font-size: 0.75rem; color: #64748B;">Cumulative Loss Value</div>
            </div>
            """, unsafe_allow_html=True)
        with col_s3:
            st.markdown(f"""
            <div class="status-card" style="text-align: center; border-top: 4px solid #EAB308;">
                <div style="font-size: 0.85rem; color: #64748B; font-weight: 600;">OPEN CLAIMS</div>
                <div style="font-size: 2rem; font-weight: 800; color: #854D0E; margin: 8px 0;">{open_claims:02d}</div>
                <div style="font-size: 0.75rem; color: #64748B;">Currently Active Claims</div>
            </div>
            """, unsafe_allow_html=True)

        # --- Statistics Section ---
        st.write("#### Statistics")
        
        facility_col = 'Primary Facility' if 'Primary Facility' in df.columns else None
        dept_col = 'Primary Department' if 'Primary Department' in df.columns else ('Department' if 'Department' in df.columns else None)

        # 1. Frequency by Department
        if dept_col:
            with st.container(border=True):
                dept_series = df[dept_col].replace('-', 'Unspecified').fillna('Unspecified').astype(str)
                all_depts = []
                for d in dept_series:
                    all_depts.extend([x.strip() for x in d.split(',') if x.strip() and x.strip() != '-'])
                
                if all_depts:
                    dept_counts = pd.Series(all_depts).value_counts().reset_index()
                    dept_counts.columns = ['Department', 'Count']
                    dept_counts['Legend Label'] = dept_counts['Department'] + " (" + dept_counts['Count'].astype(str) + ")"
                    
                    fig_dept = px.pie(
                        dept_counts, 
                        values='Count', 
                        names='Legend Label',
                        title="Frequency by Department",
                        hole=0.3,
                        color_discrete_sequence=px.colors.qualitative.Pastel,
                        template='plotly_white'
                    )
                    fig_dept.update_layout(
                        margin=dict(l=20, r=20, t=60, b=20), 
                        height=600, 
                        title_x=0.5,
                        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02)
                    )
                    # Add percentages to hover, keep chart clean
                    fig_dept.update_traces(textinfo='none', hovertemplate='%{label}<br>Count: %{value}<br>Percentage: %{percent}')
                    st.plotly_chart(fig_dept, use_container_width=True)
                else:
                    st.info("No department data found.")
        else:
            st.info("Department data not available for this document.")

        # 2. Frequency by Facility
        if facility_col:
            with st.container(border=True):
                frequency_df = df[facility_col].replace('-', 'Unspecified').value_counts().reset_index()
                frequency_df.columns = ['Facility', 'Count']
                fig_fac = px.bar(
                    frequency_df, 
                    x='Count', 
                    y='Facility', 
                    orientation='h',
                    title="Frequency by Primary Facility",
                    color='Facility',
                    text='Count',
                    color_discrete_sequence=px.colors.qualitative.Prism,
                    template='plotly_white'
                )
                fig_fac.update_layout(
                    margin=dict(l=20, r=20, t=60, b=20), 
                    height=500, 
                    showlegend=False, 
                    title_x=0.5,
                    yaxis={'categoryorder':'total ascending'}
                )
                fig_fac.update_traces(textposition='outside')
                st.plotly_chart(fig_fac, use_container_width=True)
        else:
             st.info("Primary Facility data not available for this document.")


        # 3. Top 10 Claims
        if 'Total Incurred' in df.columns and 'Claim Number' in df.columns:
            with st.container(border=True):
                top_10_df = df.nlargest(10, 'Total Incurred').copy()
                top_10_df['Claim Label'] = top_10_df['Claim Number'].astype(str)
                fig_top = px.bar(
                    top_10_df, 
                    x='Claim Label', 
                    y='Total Incurred',
                    text_auto='.2s',
                    title="Top 10 Claims by Incurred Amount",
                    labels={'Claim Label': 'Claim Number', 'Total Incurred': 'Total Incurred ($)'},
                    color_discrete_sequence=['#2563EB'],
                    template='plotly_white'
                )
                fig_top.update_layout(
                    margin=dict(l=20, r=20, t=60, b=20), 
                    height=400,
                    title_x=0.5
                )
                st.plotly_chart(fig_top, use_container_width=True)

    with tab2:
        if add_selectbox == IMAGE:
            col1, col2 = st.columns(spec=[1, 1], gap="medium")
            with col1:
                st.pdf(IMAGE, height=800)
            with col2:
                st.write("#### Data Extraction Preview")
                st.dataframe(df, hide_index=True, use_container_width=True)
        elif add_selectbox == CSV_FILE:
            csv_col1, csv_col2 = st.columns([3, 1])
            with csv_col1:
                st.write("#### Row Level Data")
                st.dataframe(df, hide_index=True, use_container_width=True)
            with csv_col2:
                st.subheader("Schema")
                st.write(df.columns.tolist())

    with tab3:
        st.write("#### Interactive Loss Run Agent")
        options = st.multiselect(
            "Quick filter tags:",
            ["Death", "Fractures", "Abuse", "Batch Actions", "Long Term Care"],
            default=["Fractures"],
            key="lr_search_terms"
        )
        
        col_c1, col_c2 = st.columns([1, 1])
        with col_c1:
            range_check = st.checkbox("Filter by $ Amount", key="lr_range_check")
            value = None
            if range_check:
                value = st.slider("Select Range", 0, 200000, (5000, 50000), step=5000, key="lr_range_slider")
        
        bt = ""
        if st.button("Apply Quick Filter", key="lr_search_button", use_container_width=True):
            if options != [] and value != None:
                bt = f"List records related to {', '.join(options)} with total incurred between {value[0]} and {value[1]}."
            elif options != [] and value == None:
                bt = f"List records related to {', '.join(options)}."
            elif options == [] and value != None:
                bt = f"List all records with total incurred between ${value[0]} and ${value[1]}."

        if "lr_messages" not in st.session_state:
            st.session_state.lr_messages = []
        
        custom_text = st.chat_input("Ask about loss history or specific claims...", key="lr_chat_input")

        if custom_text or bt:
            prompt = bt if bt != "" else custom_text
            use_cat = (bt != "")
            
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Analyzing loss records..."):
                    configure_agent(st.session_state["aws_credentials"])
                    response, df_filtered = ask_agent(prompt, use_cat, filename=st.session_state.filename)
                response_text = re.sub(r"\$(.*)\$", r"\$\1\$", response[0]["text"])
                st.markdown(response_text)
                if df_filtered is not None:
                    st.markdown("***Filtered Data Reference***")
                    st.dataframe(df_filtered, use_container_width=True)
                st.session_state.lr_messages.append({"role": "assistant", "content": response_text, "dataframe": df_filtered})
                st.session_state.lr_messages.append({"role": "user", "content": prompt})

        # Display history
        if len(st.session_state.lr_messages) >= 2:
            for message in st.session_state.lr_messages[:-2][::-1]:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
                    if message["role"] == "assistant" and message.get("dataframe") is not None:
                        st.dataframe(message["dataframe"], use_container_width=True)
