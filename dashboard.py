import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def show_dashboard():
    st.markdown("""
        <style>
        .dashboard-header {
            font-size: 2rem;
            font-weight: 800;
            color: #343B4D;
            margin-bottom: 32px;
        }
        .section-header-grey {
            font-size: 2.2rem;
            font-weight: 700;
            color: #94A3B8;
            margin-bottom: 12px;
        }
        .metric-label-grey {
            font-size: 0.85rem;
            color: #94A3B8;
            font-weight: 600;
            margin-bottom: 8px;
        }
        .metric-value-large {
            font-size: 3rem;
            font-weight: 700;
            color: #343B4D;
        }
        .risk-badge {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 700;
            display: inline-block;
            margin-right: 8px;
        }
        .risk-low { background-color: #00c2c2; color: white; }
        .risk-moderate { background-color: #ffb800; color: white; }
        .risk-high { background-color: #d92d20; color: white; }
        
        .score-badge {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 700;
            display: inline-block;
            text-align: center;
            min-width: 60px;
        }
        .score-high { background-color: #FEF2F2; color: #d92d20; border: 1px solid #FCA5A5; }
        .score-medium { background-color: #FFFBEB; color: #ffb800; border: 1px solid #FCD34D; }
        .score-low { background-color: #F0FDFA; color: #008a8a; border: 1px solid #5EEAD4; }

        /* Table Styling */
        .dash-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 40px;
            background: white;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #E2E8F0;
        }
        .dash-table th {
            background-color: #545b6d;
            color: white;
            text-align: center;
            padding: 16px;
            font-weight: 600;
            font-size: 0.9rem;
        }
        .dash-table td {
            padding: 16px;
            border-bottom: 1px solid #F1F5F9;
            font-size: 0.9rem;
            vertical-align: middle;
            text-align: center;
        }
        .dash-table td:first-child {
            text-align: left;
        }
        .dash-table tr:hover {
            background-color: #F8FAFC;
        }
        .company-name-btn > button {
            text-align: left !important;
            border: none !important;
            background: transparent !important;
            padding: 0 !important;
            color: #343B4D !important;
            font-weight: 600 !important;
            width: auto !important;
        }
        .company-name-btn > button:hover {
            color: #00c2c2 !important;
            text-decoration: underline !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Top Navigation / Title
    st.markdown('<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px; border-bottom: 1px solid #E2E8F0; padding-bottom: 10px;">'
                '<div class="dashboard-header" style="margin-bottom: 0;">Dashboard</div>'
                '</div>', unsafe_allow_html=True)

    # Header Layout
    col_left, col_right = st.columns([2, 1], gap="large")

    with col_left:
        # Risk Distribution Section
        st.markdown('<div class="section-header-grey">Submission Files Risk Distribution</div>', unsafe_allow_html=True)
        st.markdown("""
            <div style="display: flex; gap: 8px; margin-bottom: 40px;">
                <span class="risk-badge risk-low">Low</span>
                <span class="risk-badge risk-moderate">Moderate</span>
                <span class="risk-badge risk-high">High</span>
            </div>
        """, unsafe_allow_html=True)

        # Overview Section
        st.markdown('<div class="section-header-grey">Overview</div>', unsafe_allow_html=True)
        
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.markdown('<div class="metric-label-grey">Submission Files</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-value-large">27</div>', unsafe_allow_html=True)
        with m_col2:
            st.markdown('<div class="metric-label-grey">Submission Documents</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-value-large">1531</div>', unsafe_allow_html=True)
        with m_col3:
            st.markdown('<div class="metric-label-grey">Total Pages</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-value-large">14665</div>', unsafe_allow_html=True)

    with col_right:
        # Donut Chart
        labels = ['Low', 'Moderate', 'High']
        values = [15, 7, 5]
        colors = ['#00c2c2', '#ffb800', '#d92d20']

        fig = go.Figure(data=[go.Pie(
            labels=labels, 
            values=values, 
            hole=.75,
            marker_colors=colors,
            showlegend=False,
            textinfo='none',
        )])
        
        fig.update_layout(
            annotations=[dict(
                text='<span style="font-size: 24px; color: #343B4D;">📄</span><br>'
                     '<span style="font-size: 0.85rem; color: #475569; font-weight: 600; padding-top: 100px;">Total Submission Files</span><br><br>'
                     '<span style="font-size: 1.5rem; color: #1E293B; font-weight: 800;">27</span>',
                x=0.5, y=0.5, showarrow=False, align='center'
            )],
            margin=dict(l=0, r=0, t=0, b=0),
            height=350,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # Submissions Table Section
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 40px; margin-bottom: 0px;">
            <div style="width: 300px;">
                <input type="text" placeholder="Search Company" style="width: 100%; padding: 8px; border-radius: 8px; border: 1px solid #E2E8F0; background: #FFFFFF;">
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Mock Data
    data = [
        {"name": "Acme Properties", "docs": "Acord-125, Loss Runs, Supplemental", "date": "02/19/2026", "score": 2.5},
        {"name": "Blue Ridge Office Solution", "docs": "Acord-125, Driver List", "date": "02/19/2026", "score": 4.8},
        {"name": "Midnight Star Chauffeur", "docs": "Supplemental, Vehicle List", "date": "02/19/2026", "score": 1.2},
        {"name": "Summit West Insurance", "docs": "Acord-125, Loss Runs", "date": "02/18/2026", "score": 8.5},
        {"name": "Green Valley Logistics", "docs": "Acord-125, Supplemental", "date": "02/17/2026", "score": 5.9},
        {"name": "Pioneer Tech Group", "docs": "Acord-126, Driver List", "date": "02/16/2026", "score": 9.1},
        {"name": "Harbor View Estates", "docs": "Loss Runs, ACORD 125", "date": "02/15/2026", "score": 6.2},
    ]

    # Render Table Header (matching the User's modified header from Step 598)
    st.markdown("""
        <table class="dash-table">
            <thead>
                <tr>
                    <th style="text-align: center;">Files Name</th>
                    <th style="text-align: center; padding-left: 100px;">Claim Documents</th>
                    <th style="text-align: center; padding-left: 50px;">Uploaded At</th>
                    <th style="text-align: center;">Submission Score</th>
                </tr>
            </thead>
            <tbody>
    """, unsafe_allow_html=True)

    for i, item in enumerate(data):
        score_val = item['score']
        if score_val < 3:
            badge_text = "High"
            badge_class = "score-high"
        elif score_val < 7:
            badge_text = "Medium"
            badge_class = "score-medium"
        else:
            badge_text = "Low"
            badge_class = "score-low"
            
        cols = st.columns([2, 3, 1.5, 1.5])
        with cols[0]:
            st.markdown('<div class="company-name-btn">', unsafe_allow_html=True)
            if st.button(item['name'], key=f"select_{i}", use_container_width=True):
                st.session_state["selected_submission"] = item['name']
                st.session_state["current_view"] = "Completeness Check"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with cols[1]:
            st.markdown(f'<div style="text-align: center; padding: 12px;">{item["docs"]}</div>', unsafe_allow_html=True)
        with cols[2]:
            st.markdown(f'<div style="text-align: center; padding: 12px;">{item["date"]}</div>', unsafe_allow_html=True)
        with cols[3]:
            st.markdown(f'<div style="text-align: center; padding: 12px;"><span class="score-badge {badge_class}">{badge_text} ({score_val})</span></div>', unsafe_allow_html=True)

    st.markdown("</tbody></table>", unsafe_allow_html=True)
