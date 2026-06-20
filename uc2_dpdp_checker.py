"""
OrangeTree Global — DPDP Readiness & Data Risk Checker (UC2)
Digital Personal Data Protection Act 2023 (India)
Powered by Claude API (Anthropic)
Run: streamlit run uc2_dpdp_checker.py
"""

import streamlit as st
import anthropic
import json
from datetime import datetime

st.set_page_config(
    page_title="DPDP Readiness Checker | OrangeTree Global",
    page_icon="🛡️",
    layout="wide",
)

st.markdown("""
<style>
    .header-bar {
        background: linear-gradient(90deg, #FF6B35, #F7931E);
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .section-divider {
        border-left: 4px solid #FF6B35;
        padding: 0.4rem 0.8rem;
        background: #fff3ee;
        border-radius: 4px;
        margin: 1.2rem 0 0.6rem 0;
        font-weight: bold;
    }
    .result-card {
        background: #f8f9fa;
        border-left: 4px solid #FF6B35;
        padding: 0.75rem 1rem;
        border-radius: 4px;
        margin: 0.4rem 0;
    }
    .score-box {
        text-align: center;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-bar">
    <h2 style="margin:0">🛡️ DPDP Readiness & Data Risk Checker</h2>
    <p style="margin:0.2rem 0 0 0; opacity:0.9">
        Answer 16 questions about your data practices → get a compliance score, gap analysis & action plan under India's DPDP Act 2023
    </p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Setup")
    api_key = st.text_input(
        "🔑 Anthropic API Key",
        type="password",
        help="Get a free key at console.anthropic.com. Used only for this session — never stored."
    )
    model = st.selectbox(
        "Model",
        ["claude-opus-4-8", "claude-sonnet-4-6", "claude-haiku-4-5-20251001"],
        index=1,
        help="claude-sonnet is the best balance of speed and depth"
    )
    st.markdown("---")
    st.markdown("### 🏢 Your Organisation")
    org_name = st.text_input("Organisation name", placeholder="e.g. Bhawanipur House")
    org_type = st.selectbox("Sector", [
        "F&B / Restaurant", "Retail", "Healthcare / Clinic", "Education / EdTech",
        "Financial Services / NBFC", "Manufacturing", "IT / SaaS", "HR / Staffing", "Other"
    ])
    org_size = st.selectbox("Employees", ["1–10", "11–50", "51–200", "200+"])
    st.markdown("---")
    st.caption("⚖️ Preliminary self-assessment only — not legal advice.")

# ── Questionnaire ─────────────────────────────────────────────────────────────
st.markdown("Answer based on your **current** practices — not planned ones. 'Partially' is a valid answer.")

OPTIONS = ["✅ Yes — in place", "⚠️ Partially", "❌ No", "➖ Not applicable"]
responses = {}

# Pillar 1
st.markdown('<div class="section-divider">Pillar 1 — Consent</div>', unsafe_allow_html=True)
responses["p1_q1"] = st.radio("Do you get explicit consent before collecting personal data?", OPTIONS, key="p1q1", horizontal=True,
    help="Name, phone, email, purchase history — anything that identifies a person. A signup form alone isn't enough; users must actively agree.")
responses["p1_q2"] = st.radio("Can customers withdraw consent and opt out easily?", OPTIONS, key="p1q2", horizontal=True,
    help="Withdrawing consent must be as easy as giving it. A buried unsubscribe link may not be sufficient under DPDP.")
responses["p1_q3"] = st.radio("Do you have a written Privacy Notice visible at point of data collection?", OPTIONS, key="p1q3", horizontal=True,
    help="Tells customers what data you collect, why, and how. Must be visible before they share data — not just in your website footer.")

# Pillar 2
st.markdown('<div class="section-divider">Pillar 2 — Data Minimisation</div>', unsafe_allow_html=True)
responses["p2_q1"] = st.radio("Do you collect only the data you actually use — nothing 'just in case'?", OPTIONS, key="p2q1", horizontal=True,
    help="Example: a restaurant needs a phone number for reservations — but does it need date of birth? Collecting unused data is a DPDP risk.")
responses["p2_q2"] = st.radio("Is data used only for the purpose it was originally collected for?", OPTIONS, key="p2q2", horizontal=True,
    help="Using a delivery phone number for WhatsApp marketing requires separate consent. Repurposing data without fresh consent is a violation.")
responses["p2_q3"] = st.radio("Do you have a register listing what personal data you hold, where, and why?", OPTIONS, key="p2q3", horizontal=True,
    help="Even a simple spreadsheet counts. This is one of the first things a regulator or DPDP audit will ask for.")

# Pillar 3
st.markdown('<div class="section-divider">Pillar 3 — Customer Rights</div>', unsafe_allow_html=True)
responses["p3_q1"] = st.radio("Can a customer ask 'what data do you have on me?' and get an answer?", OPTIONS, key="p3q1", horizontal=True,
    help="If data is scattered across WhatsApp, Excel, and a CRM, this is very hard to fulfil. DPDP requires you to be able to respond.")
responses["p3_q2"] = st.radio("Can customers request correction or deletion of their data?", OPTIONS, key="p3q2", horizontal=True,
    help="Right to Correction and Right to Erasure. A contact email or form is the minimum required process.")
responses["p3_q3"] = st.radio("Do you have a process to respond to these requests within a reasonable time?", OPTIONS, key="p3q3", horizontal=True,
    help="Having the right is only useful if someone processes the request. Is there a named owner and response timeline in your business?")

# Pillar 4
st.markdown('<div class="section-divider">Pillar 4 — Internal Accountability</div>', unsafe_allow_html=True)
responses["p4_q1"] = st.radio("Is someone in your organisation responsible for data protection compliance?", OPTIONS, key="p4q1", horizontal=True,
    help="Doesn't need to be a formal DPO. But someone must own it — otherwise penalties fall on the business owner personally.")
responses["p4_q2"] = st.radio("Do you have a process to detect, contain, and report a data breach?", OPTIONS, key="p4q2", horizontal=True,
    help="If your CRM is hacked or a laptop with customer data is stolen, DPDP requires you to notify the Data Protection Board and affected customers.")
responses["p4_q3"] = st.radio("Do vendor contracts (apps, delivery platforms, payment gateways) include data protection clauses?", OPTIONS, key="p4q3", horizontal=True,
    help="When you share customer data with Zomato, Razorpay, or your cloud tools, you remain legally responsible for how they handle it.")

# Pillar 5
st.markdown('<div class="section-divider">Pillar 5 — Sensitive & Children\'s Data</div>', unsafe_allow_html=True)
responses["p5_q1"] = st.radio("If under-18s use your service, do you have age verification and parental consent?", OPTIONS, key="p5q1", horizontal=True,
    help="DPDP's strictest rules apply to minors. If your service could be used by someone under 18, this applies — even if you don't target children.")
responses["p5_q2"] = st.radio("Is sensitive data (health, financial, biometric) held with extra security?", OPTIONS, key="p5q2", horizontal=True,
    help="Examples: clinic patient records, salary data, dietary restrictions, CCTV / biometric attendance. Requires stronger encryption and tighter access controls.")

# Pillar 6
st.markdown('<div class="section-divider">Pillar 6 — Security & Cross-Border Data</div>', unsafe_allow_html=True)
responses["p6_q1"] = st.radio("Is customer data stored securely with restricted access and password protection?", OPTIONS, key="p6q1", horizontal=True,
    help="Includes Google Sheets (who has the link?), CRM (shared passwords?), WhatsApp groups, email inboxes. Only the right people should have access.")
responses["p6_q2"] = st.radio("Does your customer data leave India — e.g. stored on US/EU cloud servers or foreign SaaS tools?", OPTIONS, key="p6q2", horizontal=True,
    help="Google Workspace, AWS, Mailchimp, HubSpot may store data outside India. DPDP has specific cross-border transfer rules — one of the most overlooked SME risks.")
responses["p6_q3"] = st.radio("Are employee access logs to customer data tracked?", OPTIONS, key="p6q3", horizontal=True,
    help="If an employee leaks customer data, can you detect it? Knowing which team members can access your CRM or customer spreadsheet is a starting point.")

# Optional context
st.markdown("---")
additional_context = st.text_area(
    "Anything else Claude should know about your data practices? *(optional)*",
    placeholder="e.g. We use WhatsApp, Tally, Zoho CRM, Google Sheets. We collect CCTV footage. We have 3 staff with database access...",
    help="More context = more targeted advice"
)

# Progress + Submit
answered = sum(1 for v in responses.values() if v)
st.markdown(f"**{answered} / 16 questions answered**")

col1, col2, col3 = st.columns([2, 2, 2])
with col2:
    analyse_btn = st.button("🔍 Generate My DPDP Report", type="primary",
                             use_container_width=True, disabled=(answered < 16))

if answered < 16:
    st.info(f"{16 - answered} question(s) remaining above.", icon="👆")

# ── Analysis ──────────────────────────────────────────────────────────────────
if analyse_btn:
    if not api_key:
        st.error("Please enter your Anthropic API key in the sidebar.")
        st.stop()

    score_map = {
        "✅ Yes — in place": 3,
        "⚠️ Partially": 1.5,
        "❌ No": 0,
        "➖ Not applicable": 3
    }
    applicable = {k: v for k, v in responses.items() if v != "➖ Not applicable"}
    total_possible = len(applicable) * 3
    total_score = sum(score_map.get(v, 0) for v in applicable.values())
    raw_pct = int((total_score / total_possible) * 100) if total_possible > 0 else 0

    with st.spinner("Analysing your compliance posture across all 6 DPDP pillars..."):
        try:
            client = anthropic.Anthropic(api_key=api_key)
            responses_text = "\n".join([f"- {k}: {v}" for k, v in responses.items()])

            SYSTEM = """You are an expert in India's Digital Personal Data Protection Act 2023.
Return a JSON object with this exact structure:
{
  "overall_risk": "High/Medium/Low",
  "compliance_summary": "2-3 sentences in plain English for an SME owner — no jargon. What does this score mean for their business?",
  "pillar_scores": {
    "Consent": {"score": 0-100, "status": "Compliant/Partial/Non-compliant", "finding": "one practical sentence"},
    "Data Minimisation": {"score": 0-100, "status": "...", "finding": "..."},
    "Customer Rights": {"score": 0-100, "status": "...", "finding": "..."},
    "Accountability": {"score": 0-100, "status": "...", "finding": "..."},
    "Sensitive Data": {"score": 0-100, "status": "...", "finding": "..."},
    "Security": {"score": 0-100, "status": "...", "finding": "..."}
  },
  "critical_gaps": [
    {
      "gap": "Plain-English description",
      "why_it_matters": "Real consequence if not fixed",
      "action": "Specific step to take",
      "effort": "This week / 1–2 weeks / 1–3 months"
    }
  ],
  "quick_wins": ["Action phrased as an instruction, completable this week at no cost"],
  "penalty_risk": "Plain-English summary of fine exposure with rupee figures where applicable",
  "next_steps": ["Step 1 with owner", "Step 2", "Step 3"]
}
Specific to DPDP Act 2023 (India), not GDPR. Return ONLY valid JSON."""

            USER = f"""Organisation: {org_name or 'Unknown'} | Sector: {org_type} | Size: {org_size}
Additional context: {additional_context or 'None'}
Raw score: {raw_pct}%

Responses:
{responses_text}"""

            response = client.messages.create(
                model=model, max_tokens=2500, system=SYSTEM,
                messages=[{"role": "user", "content": USER}]
            )

            raw = response.content[0].text.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            result = json.loads(raw)
            result["raw_pct"] = raw_pct
            st.session_state["dpdp_result"] = result

        except json.JSONDecodeError as e:
            st.error(f"Parsing error: {e}. Please try again.")
            st.code(raw)
        except Exception as e:
            st.error(f"API error: {e}")

# ── Results ───────────────────────────────────────────────────────────────────
if "dpdp_result" in st.session_state:
    r = st.session_state["dpdp_result"]
    st.markdown("---")
    st.markdown(f"## 📊 DPDP Compliance Report — {org_name or 'Your Organisation'}")
    st.caption(f"Generated {datetime.now().strftime('%d %B %Y, %H:%M')} | Preliminary self-assessment only")

    # Score row
    score = r.get("raw_pct", 0)
    risk = r.get("overall_risk", "Medium")
    risk_color = {"High": "#dc3545", "Medium": "#FF6B35", "Low": "#28a745"}.get(risk, "#FF6B35")
    risk_bg    = {"High": "#fff3f3", "Medium": "#fff3ee", "Low": "#f0fff4"}.get(risk, "#fff3ee")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="score-box" style="background:{risk_bg}">
            <div style="font-size:3rem; font-weight:bold; color:{risk_color}">{score}%</div>
            <div style="color:#555; font-size:0.9rem">Compliance Score</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        risk_icon = {"High": "🚨", "Medium": "⚠️", "Low": "✅"}.get(risk, "⚠️")
        st.markdown(f"""<div class="score-box" style="background:{risk_bg}">
            <div style="font-size:2.5rem">{risk_icon}</div>
            <div style="font-weight:bold; color:{risk_color}; font-size:1rem">{risk} Risk</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        gaps = len(r.get("critical_gaps", []))
        st.markdown(f"""<div class="score-box" style="background:#fff3ee">
            <div style="font-size:3rem; font-weight:bold; color:#FF6B35">{gaps}</div>
            <div style="color:#555; font-size:0.9rem">Critical Gaps</div>
        </div>""", unsafe_allow_html=True)

    st.info(r.get("compliance_summary", ""), icon="📋")

    # Pillar scores
    st.markdown('<div class="section-divider">Pillar Breakdown</div>', unsafe_allow_html=True)
    for name, data in r.get("pillar_scores", {}).items():
        ps = data.get("score", 50)
        status = data.get("status", "Partial")
        bar_color = "#28a745" if ps >= 70 else "#FF6B35" if ps >= 40 else "#dc3545"
        icon = "✅" if ps >= 70 else "⚠️" if ps >= 40 else "❌"
        st.markdown(f"""
        <div class="result-card">
            <div style="display:flex; justify-content:space-between">
                <b>{name}</b>
                <span style="color:{bar_color}">{icon} {status} ({ps}%)</span>
            </div>
            <div style="background:#e9ecef; border-radius:4px; height:6px; margin:6px 0">
                <div style="background:{bar_color}; width:{ps}%; height:6px; border-radius:4px"></div>
            </div>
            <small style="color:#555">{data.get('finding', '')}</small>
        </div>""", unsafe_allow_html=True)

    # Critical gaps
    st.markdown('<div class="section-divider">Critical Gaps</div>', unsafe_allow_html=True)
    for i, gap in enumerate(r.get("critical_gaps", []), 1):
        effort = gap.get("effort", "")
        effort_color = "#dc3545" if "month" in effort.lower() else "#FF6B35" if "week" in effort.lower() else "#28a745"
        with st.expander(f"Gap {i}: {gap.get('gap', '')}"):
            st.markdown(f"**Why it matters:** {gap.get('why_it_matters', '')}")
            st.markdown(f"**What to do:** {gap.get('action', '')}")
            st.markdown(f"**Effort:** <span style='color:{effort_color}; font-weight:bold'>{effort}</span>", unsafe_allow_html=True)

    # Quick wins
    st.markdown('<div class="section-divider">Quick Wins — Do These This Week</div>', unsafe_allow_html=True)
    for qw in r.get("quick_wins", []):
        st.markdown(f"✅ {qw}")

    # Penalty risk
    st.markdown('<div class="section-divider">Penalty Exposure</div>', unsafe_allow_html=True)
    st.warning(r.get("penalty_risk", ""), icon="💰")

    # Next steps
    st.markdown('<div class="section-divider">Your Action Plan</div>', unsafe_allow_html=True)
    for i, ns in enumerate(r.get("next_steps", []), 1):
        st.markdown(f"**{i}.** {ns}")

    # Export
    st.markdown("---")
    export_text = f"""DPDP COMPLIANCE REPORT
Organisation: {org_name or 'Unknown'} | Sector: {org_type} | Size: {org_size}
Date: {datetime.now().strftime('%d %B %Y')} | Score: {score}% | Risk: {risk}

SUMMARY
{r.get('compliance_summary', '')}

CRITICAL GAPS
""" + "\n".join([
        f"\nGap {i}: {g.get('gap','')}\n  Why: {g.get('why_it_matters','')}\n  Action: {g.get('action','')}\n  Effort: {g.get('effort','')}"
        for i, g in enumerate(r.get("critical_gaps", []), 1)
    ]) + """

QUICK WINS
""" + "\n".join([f"• {q}" for q in r.get("quick_wins", [])]) + f"""

PENALTY EXPOSURE
{r.get('penalty_risk', '')}

ACTION PLAN
""" + "\n".join([f"{i}. {ns}" for i, ns in enumerate(r.get("next_steps", []), 1)]) + """

Generated by OrangeTree Global AI Suite — UC2: DPDP Readiness Checker
DISCLAIMER: Preliminary self-assessment only. Not legal advice.
"""
    st.download_button(
        "⬇️ Download Report",
        data=export_text,
        file_name=f"DPDP_Report_{(org_name or 'Org').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain"
    )
    st.caption("OrangeTree Global | AI SME Suite — UC2: DPDP Readiness Checker | Not legal advice.")
