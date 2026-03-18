from configurations import page
import streamlit as st

def show_disturbancies_page():
    # Use the same company name as other pages
    company_name = st.session_state.get("selected_submission", "Acme Properties")
    genworth_page = page != "genworth"
    
    st.markdown("""
        <style>
        .section-header-grey {
            font-size: 2.2rem;
            font-weight: 700;
            color: #94A3B8;
            margin-bottom: 32px;
        }
        .disturbancy-card {
            background-color: white;
            padding: 24px;
            border-radius: 12px;
            border: 1px solid #E2E8F0;
            margin-bottom: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        .disturbancy-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: #343B4D;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .disturbancy-desc {
            font-size: 0.95rem;
            color: #64748B;
            line-height: 1.5;
        }
        .severity-badge {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
        }
        .severity-critical { background-color: #FEF2F2; color: #DC2626; border: 1px solid #FCA5A5; }
        .severity-major { background-color: #FFFBEB; color: #D97706; border: 1px solid #FCD34D; }
        .severity-minor { background-color: #F0F9FF; color: #0284C7; border: 1px solid #BAE6FD; }
        </style>
    """, unsafe_allow_html=True)

    # Submissions Header (Matching other detailed pages)
    # st.caption(f"Submissions > {company_name} > Disturbancies")
    # st.markdown(f"""
    # <div style="display: flex; align-items: center; gap: 12px;">
    #     <span style="font-size: 2rem; font-weight: 800;">{company_name}</span>
    #     <span style="background-color: #FEF2F2; color: #DC2626; padding: 4px 12px; border-radius: 6px; font-size: 0.85rem; font-weight: 700; border: 1px solid #FCA5A5;">Incomplete ▾</span>
    # </div>
    # <div style="font-size: 0.85rem; color: #64748B; margin-top: 4px;">SUB-000001 • Bill Brothers • Agent Name • 24 Sep 2026</div>
    # """, unsafe_allow_html=True)
    
    # st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header-grey">Highlighted Discrepancies</div>', unsafe_allow_html=True)

    # Anomaly Data
    if genworth_page:
        anomalies = [
            {
                "title": "Unexpected Premium Drop",
                "severity": "CRITICAL",
                "desc": "The projected premium for 2026 shows a 45% decrease compared to previous loss runs, despite no significant change in exposure or vehicle count.",
                "icon": "📉"
            },
            {
                "title": "Missing Loss History (2023)",
                "severity": "MAJOR",
                "desc": "Loss run documents are missing data for the period of Jan 2023 - Dec 2023. Gap in historical claims coverage identified.",
                "icon": "🔍"
            },
            {
                "title": "Vehicle List Inconsistency",
                "severity": "MINOR",
                "desc": "The Supplemental application lists 15 vehicles, but the ACORD 125 only accounts for 14. One VIN appears to be duplicate or missing.",
                "icon": "🚗"
            },
            {
                "title": "Outdated Safety Manual",
                "severity": "MINOR",
                "desc": "The uploaded Safety & Training Manual hasn't been updated since 2018. Recent regulatory compliance standards may not be met.",
                "icon": "📋"
            }
        ]
    else:
        anomalies = [
            {
                "title": "Material Misrepresentation: Tobacco/Nicotine",
                "severity": "CRITICAL",
                "desc": "Application states 'No' for tobacco/nicotine use in past 12 months, but Rx History shows nicotine patch claims as recent as 10/2025. Material to underwriting and rates.",
                "icon": "⚠️"
            },
            {
                "title": "Unsigned Application & HIPAA",
                "severity": "CRITICAL",
                "desc": "Applicant signature is missing from the main application, and the HIPAA Authorization is not executed. Legal and carrier compliance gap.",
                "icon": "✍️"
            },
            {
                "title": "Missing NY State Addendums",
                "severity": "CRITICAL",
                "desc": "Required NY Home Care Disclosure and Replacement Notice are missing or not executed. Regulatory blocker for New York state application.",
                "icon": "🗽"
            },
            {
                "title": "Data Integrity: Invalid SSN & Routing #",
                "severity": "CRITICAL",
                "desc": "SSN has only 8 digits (123-45-678). Bank routing number (02100002) is also 8 digits. Both require 9 digits for valid processing.",
                "icon": "🆔"
            },
            {
                "title": "Disclosure Gap: Recent Fall History",
                "severity": "MAJOR",
                "desc": "APS records a fall in the shower (09/2025) and reported dizziness, which were not disclosed on the application. Elevates functional risk profile.",
                "icon": "♿"
            },
            {
                "title": "Missing Medical & ADL Detail",
                "severity": "MAJOR",
                "desc": "Prescription medication list (Sec. 5A) was not provided despite 'Yes' answer. ADL 'Bathing' assistance noted but required narrative description is missing.",
                "icon": "📋"
            },
            {
                "title": "Suitability & Hardship Concern",
                "severity": "MAJOR",
                "desc": "Premium marked as NOT affordable without hardship, but required explanation is blank. Suitability acknowledgement missing for NY compliance.",
                "icon": "💰"
            },
            {
                "title": "Clinical Flag: Suboptimal Diabetes Control",
                "severity": "MAJOR",
                "desc": "HbA1c of 8.2% (11/2025) indicates suboptimal control. BP (152/92) also above goal. High risk for functional decline when combined with hypertension.",
                "icon": "🩺"
            }
        ]

    # Render Disturbancy Cards
    for item in anomalies:
        severity_class = f"severity-{item['severity'].lower()}"
        st.markdown(f"""
            <div class="disturbancy-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                    <div class="disturbancy-title">{item['icon']} {item['title']}</div>
                    <span class="severity-badge {severity_class}">{item['severity']}</span>
                </div>
                <div class="disturbancy-desc">{item['desc']}</div>
            </div>
        """, unsafe_allow_html=True)

    # Footer Action
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Flag all as Reviewed", type="primary"):
        st.success("All disturbances marked as reviewed.")
