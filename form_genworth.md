# WHITE LABEL LONG-TERM CARE INSURANCE APPLICATION
> **Status: NIGO (Not In Good Order)** — Intentionally incomplete for Intelligent Intake demo

| Field                  | Value                        |
|------------------------|------------------------------|
| Carrier                | Demo Carrier – LTC Division  |
| Product                | Traditional LTC              |
| Application ID         | LTC-NY-2026-000174           |
| Submission Channel     | Advisor                      |
| State of Application   | NY                           |
| Effective Date         | 04/01/2026                   |

---

## 1. Applicant / Proposed Insured Information

| Field                  | Value                              | Flag |
|------------------------|------------------------------------|------|
| Full Name              | Jordan A. Taylor                   |      |
| Date of Birth          | 07/14/1961                         |      |
| SSN/Tax ID             | 123-45-678                         | ⚠️ Invalid format (should be 9 digits: XXX-XX-XXXX) |
| Gender                 | M                                  |      |
| Marital Status         | Married                            |      |
| Primary Phone          | (212) 555-0199                     |      |
| Email                  | jordan.taylor(at)mail.com          | ⚠️ Non-standard format (@ symbol missing) |
| Residence Address      | 115 W 57th St, New York, NY 10019  |      |
| Mailing Address        | Same as residence                  |      |
| Citizenship            | US                                 |      |
| Driver's License       | NY D123-456-789-012                |      |

---

## 2. Coverage & Benefit Design

| Field               | Value          |
|---------------------|----------------|
| Plan Type           | Home Care Only |
| Benefit Amount      | $200 per day   |
| Benefit Period      | 5 years        |
| Elimination Period  | 90 days        |
| Inflation Option    | 3% Compound    |
| Shared Care         | No             |
| Nonforfeiture       | None           |
| Return of Premium   | No             |

### 2A. Home Care Selection (Triggers State Disclosures)

- [x] Home Care benefits requested
- [x] Care coordination / case management
- [ ] Alternate Plan of Care

> ⚠️ **MISSING:** NY Home Care Disclosure Addendum — NOT attached / NOT signed

---

## 3. Premium & Payment

| Field                  | Value               | Flag |
|------------------------|---------------------|------|
| Mode                   | Monthly             |      |
| Payment Method         | EFT/ACH             |      |
| Initial Premium Amount | $312.45             |      |
| Bank Name              | Metro National Bank |      |
| Routing #              | 02100002            | ⚠️ Invalid (routing numbers must be 9 digits) |
| Account #              | 00987654321         |      |
| Account Type           | Checking            |      |
| Draft Day (Monthly)    | 15th                |      |

---

## 4. Existing Coverage & Replacement

- [ ] No existing LTC coverage
- [x] Yes — Existing LTC coverage

| Field                              | Value    | Flag |
|------------------------------------|----------|------|
| Existing Carrier / Policy #        | —        | ⚠️ MISSING |
| In Force Since                     | 03/2018  |      |
| Will this replace existing coverage? | Yes    |      |
| Replacement Reason                 | —        | ⚠️ MISSING |

---

## 5. Health & Underwriting

| Question                                  | Answer |
|-------------------------------------------|--------|
| Neuro conditions (dementia, Parkinson's, stroke) | No |
| Cancer in past 5 years                    | No     |
| Needs assistance with ADLs                | Yes    |
| Hospitalized/surgery past 2 years         | No     |
| Takes prescription medications            | Yes    |
| Tobacco/nicotine past 12 months           | No     |

### 5A. Prescription Medications

> ⚠️ **MISSING:** Applicant answered YES to prescription medications but did **not** provide medication list (name, dosage, condition required)

---

## 6. Functional Assessment (ADL/IADL)

- [x] **Bathing** *(details required)*
- [ ] Dressing
- [ ] Eating
- [ ] Toileting
- [ ] Transferring
- [ ] Continence

> ⚠️ **MISSING:** ADL selected (Bathing) but **no narrative** provided describing assistance required and frequency

---

## 7. Financial Suitability

| Field                                | Value     | Flag |
|--------------------------------------|-----------|------|
| Annual Household Income              | $85,000   |      |
| Liquid Assets                        | $25,000   |      |
| Net Worth (approx.)                  | $210,000  |      |
| Primary Source of Premium            | Savings   |      |
| Is premium affordable without hardship? | **No** | ⚠️ Explanation required but NOT provided |

---

## 8. Authorizations & Notices

| Authorization                        | Status |
|--------------------------------------|--------|
| Electronic records & e-sign consent  | ✅ Signed |
| HIPAA Authorization                  | ❌ MISSING — not executed |
| Privacy notice acknowledgment        | ✅ Signed |
| Fraud warning acknowledgment         | ✅ Signed |

---

## 9. Advisor / Producer Information

| Field             | Value                          | Flag |
|-------------------|--------------------------------|------|
| Advisor Name      | Casey Morgan                   |      |
| Agency/Firm       | NorthStar Financial Partners   |      |
| NPN/License #     | —                              | ⚠️ MISSING |
| State(s) Licensed | NY, NJ                         |      |
| Phone             | (646) 555-0134                 |      |
| Email             | casey.morgan@northstarfp.com   |      |

---

## 10. Signatures

| Signer                        | Signature         | Date       | Flag |
|-------------------------------|-------------------|------------|------|
| Applicant / Proposed Insured  | —                 | —          | ❌ MISSING — NOT SIGNED |
| Advisor / Producer            | //s/ Casey Morgan | 03/05/2026 | ✅   |

---

## Appendix — State-Specific Addendum (NY)

| Document                          | Status |
|-----------------------------------|--------|
| Home Care Disclosure (NY)         | ❌ MISSING / NOT ATTACHED |
| Replacement Notice (replacing LTC)| ❌ MISSING / NOT ATTACHED |
| Suitability Acknowledgement       | ❌ MISSING — explanation required where affordability is NO |

---

## ⚠️ NIGO Summary — All Deficiencies

| # | Section              | Issue                                                                 | Severity |
|---|----------------------|-----------------------------------------------------------------------|----------|
| 1 | Applicant Info       | SSN invalid format — only 8 digits (123-45-678)                      | 🔴 Critical |
| 2 | Applicant Info       | Email in non-standard format — `(at)` instead of `@`                 | 🟡 Minor |
| 3 | Home Care Disclosure | NY Home Care Disclosure Addendum missing / not signed                 | 🔴 Critical |
| 4 | Premium & Payment    | Bank routing number invalid — only 8 digits (should be 9)            | 🔴 Critical |
| 5 | Existing Coverage    | Existing carrier / policy number missing                              | 🔴 Critical |
| 6 | Existing Coverage    | Replacement reason not provided                                       | 🔴 Critical |
| 7 | Health & Underwriting| Prescription medication list missing (answered YES)                   | 🔴 Critical |
| 8 | Functional Assessment| ADL narrative missing (Bathing selected, no description provided)     | 🔴 Critical |
| 9 | Financial Suitability| Affordability marked NO — explanation not provided                    | 🔴 Critical |
| 10| Authorizations       | HIPAA authorization not signed / not executed                         | 🔴 Critical |
| 11| Advisor Info         | Advisor NPN/License number missing                                    | 🔴 Critical |
| 12| Signatures           | Applicant e-signature missing                                         | 🔴 Critical |
| 13| NY Addendum          | Home Care Disclosure (NY) not attached                                | 🔴 Critical |
| 14| NY Addendum          | Replacement Notice not attached                                       | 🔴 Critical |
| 15| NY Addendum          | Suitability Acknowledgement missing explanation                       | 🔴 Critical |

---

> **Total Deficiencies: 15**
> **Critical: 14 | Minor: 1**
> 
> *This application cannot be processed until all critical items are resolved.*