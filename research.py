import streamlit as st

def render_website_summary():
    st.markdown("### Website Summary")
    services = [
        {"icon": "📄", "name": "Secure Document & Product Destruction", "desc": "Confidential waste handling"},
        {"icon": "🗑️", "name": "Waste Removal", "desc": "Commercial and residential waste collection"},
        {"icon": "🌱", "name": "LEED Services & Training", "desc": "Assistance with green building certifications"},
        {"icon": "♻️", "name": "Recycling", "desc": "Single-stream recycling services"},
        {"icon": "📞", "name": "On-Demand Collection", "desc": "Flexible waste pickup services"},
        {"icon": "🚛", "name": "Composting", "desc": "Organic waste collection for businesses"},
        {"icon": "🤝", "name": "Sustainability Solutions", "desc": "Programs to help businesses operate as model green enterprises"},
        {"icon": "🏗️", "name": "Dumpster Rentals", "desc": "For various project sizes"}
    ]
    
    cols = st.columns(2)
    for i, service in enumerate(services):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="service-card" style="margin-bottom: 16px;">
                <div class="service-icon">{service['icon']}</div>
                <div class="service-name">{service['name']}</div>
                <div class="service-desc">{service['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

def render_reviews(reviewer_type="Employee"):
    st.markdown(f"### {reviewer_type} Reviews")
    col_r1, col_r2 = st.columns([1.5, 1])
    with col_r1:
        ratings = [
            {"stars": 5, "percent": 45},
            {"stars": 4, "percent": 30},
            {"stars": 3, "percent": 15},
            {"stars": 2, "percent": 5},
            {"stars": 1, "percent": 5}
        ]
        for r in ratings:
            st.markdown(f"""
            <div class="bar-row">
                <div class="bar-label">{r['stars']}</div>
                <div class="bar-bg"><div class="bar-fill" style="width: {r['percent']}%"></div></div>
            </div>
            """, unsafe_allow_html=True)
    
    with col_r2:
        st.markdown(f"""
        <div style="text-align: center;">
            <div class="rating-score">{"4.4" if reviewer_type == "Employee" else "4.2"}</div>
            <div style="font-size: 0.9rem; color: #64748B; margin-bottom: 8px;">{"90" if reviewer_type == "Employee" else "156"} reviews</div>
            <div class="rating-stars">★★★★☆</div>
        </div>
        """, unsafe_allow_html=True)

def render_osha():
    st.markdown("### OSHA Compliance Data")
    col1, col2, col3 = st.columns(3)
    col1.metric("Inspections (5yr)", "12")
    col2.metric("Violations", "2", delta="-1")
    col3.metric("Penalty Total", "$1,450")
    
    st.markdown("""
    <div class="status-card">
        <div style="font-weight: 700; margin-bottom: 12px;">Recent Inspections</div>
        <table style="width: 100%; font-size: 0.85rem;">
            <tr style="border-bottom: 1px solid #F1F5F9;">
                <th style="padding: 8px; text-align: left;">Date</th>
                <th style="padding: 8px; text-align: left;">Type</th>
                <th style="padding: 8px; text-align: left;">Status</th>
            </tr>
            <tr>
                <td style="padding: 8px;">2024-03-12</td>
                <td style="padding: 8px;">Safety</td>
                <td style="padding: 8px; color: #00c2c2;">Closed</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

def render_safer():
    st.markdown("### FMCSA SAFER Data")
    st.markdown("""
    <div class="status-card">
        <div style="display: flex; gap: 40px; margin-bottom: 20px;">
            <div>
                <div style="font-size: 0.75rem; color: #64748B;">DOT Number</div>
                <div style="font-weight: 700;">882341</div>
            </div>
            <div>
                <div style="font-size: 0.75rem; color: #64748B;">Safety Rating</div>
                <div style="font-weight: 700; color: #00c2c2;">SATISFACTORY</div>
            </div>
            <div>
                <div style="font-size: 0.75rem; color: #64748B;">Total Vehicles</div>
                <div style="font-weight: 700;">24</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_sos():
    st.markdown("### Secretary of State (SOS)")
    st.markdown("""
    <div class="status-card">
        <div style="margin-bottom: 12px;">
            <div style="font-size: 0.75rem; color: #64748B;">Entity Status</div>
            <div style="font-weight: 700; color: #00c2c2;">Active / Good Standing</div>
        </div>
        <div style="margin-bottom: 12px;">
            <div style="font-size: 0.75rem; color: #64748B;">Incorporation Date</div>
            <div style="font-weight: 700;">January 15, 1998</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_research_page():
    st.markdown("""
    <style>
    .research-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 24px;
        padding-bottom: 12px;
        border-bottom: 1px solid #E2E8F0;
    }
    .research-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1E293B;
    }
    .service-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #E2E8F0;
        height: 100%;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .service-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .service-icon {
        font-size: 1.5rem;
        color: #00c2c2;
        margin-bottom: 12px;
    }
    .service-name {
        font-weight: 700;
        font-size: 1rem;
        color: #334155;
        margin-bottom: 4px;
    }
    .service-desc {
        font-size: 0.85rem;
        color: #64748B;
        line-height: 1.4;
    }
    .rating-container {
        background: white;
        border-radius: 12px;
        padding: 24px;
        border: 1px solid #E2E8F0;
    }
    .rating-score {
        font-size: 3rem;
        font-weight: 800;
        color: #1E293B;
        margin-right: 12px;
    }
    .rating-stars {
        color: #FFB800;
        font-size: 1.2rem;
    }
    .bar-row {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 8px;
    }
    .bar-label {
        font-size: 0.85rem;
        color: #64748B;
        min-width: 20px;
    }
    .bar-bg {
        flex: 1;
        height: 8px;
        background: #F1F5F9;
        border-radius: 4px;
        overflow: hidden;
    }
    .bar-fill {
        height: 100%;
        background: #343B4D;
        border-radius: 4px;
    }
    /* Section dividers for Show All */
    .section-divider {
        margin: 40px 0 20px 0;
        border-top: 1px dashed #E2E8F0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Breadcrumbs & Header
    # st.markdown('<div style="font-size: 0.85rem; color: #64748B; margin-bottom: 8px;">Submissions &gt; Acme Properties</div>', unsafe_allow_html=True)
    
    col_h1, col_h2 = st.columns([2, 1])
    with col_h1:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 12px;">
            <span style="font-size: 2rem; font-weight: 800;">{st.session_state["selected_submission"]}</span>
        </div>
        <div style="font-size: 0.85rem; color: #64748B; margin-top: 4px; ">SUB-000001 • 24 Feb 2026</div>
        <br><br>
        """, unsafe_allow_html=True)
    
    # with col_h2:
    #     st.markdown('<div style="display: flex; justify-content: flex-end; gap: 8px; align-items: center;">', unsafe_allow_html=True)
    #     st.button("🚫 Reject", key="btn_reject_res")
    #     st.button("Generate Summary", type="primary", key="btn_gen_sum_res")
    #     st.markdown('</div>', unsafe_allow_html=True)

    # Search / Ask section
    # st.text_input("Ask anything related to this account", placeholder="Ask anything related to this account", label_visibility="collapsed", key="research_ask")

    # Main Content Area with Sub-Tabs
    sub_tab = st.segmented_control(
        "",
        [
            "Website Summary",
            "Employee Reviews",
            "Customer Reviews",
            "OSHA",
            "SAFER",
            "SOS",
            "Show All"
        ],
        default="Show All",
        key="research_sub_tab",
        label_visibility="collapsed"
    )

    if sub_tab == "Website Summary":
        render_website_summary()
    elif sub_tab == "Employee Reviews":
        render_reviews("Employee")
    elif sub_tab == "Customer Reviews":
        render_reviews("Customer")
    elif sub_tab == "OSHA":
        render_osha()
    elif sub_tab == "SAFER":
        render_safer()
    elif sub_tab == "SOS":
        render_sos()
    elif sub_tab == "Show All":
        render_website_summary()
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        render_reviews("Employee")
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        render_reviews("Customer")
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        render_osha()
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        render_safer()
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        render_sos()
