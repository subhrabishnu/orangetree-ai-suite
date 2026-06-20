"""
OrangeTree Global — DPDP Readiness & Data Risk Checker (UC2)
Based on Digital Personal Data Protection Act 2023 (India)
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
        background: linear-gradient(90deg, #1a3c5e, #2e6da4);
        padding: 1.2rem 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        color: white;
    }
    .intro-box {
        background: #f0f6ff;
        border: 1px solid #c0d9f5;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1.5rem;
    }
    .why-box {
        background: #fffbe6;
        border-left: 4px solid #f0a500;
        padding: 0.6rem 1rem;
        border-radius: 4px;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
    }
    .section-header {
        background: #e8f0fe;
        border-left: 5px solid #2e6da4;
        padding: 0.6rem 1rem;
        border-radius: 4px;
        margin: 1.5rem 0 0.3rem 0;
        font-weight: bold;
        font-size: 1rem;
    }
    .section-desc {
        font-size: 0.88rem;
        color: #555;
        margin-bottom: 0.8rem;
        padding-left: 0.3rem;
    }
    .pillar-card {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid #dee2e6;
    }
    .score-box {
        text-align: center;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 0.5rem 0;
    }
    .step-badge {
        background: #2e6da4;
        color: white;
        border-radius: 50%;
        width: 24px;
        height: 24px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 0.8rem;
        font-weight: bold;
        margin-right: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-bar">
    <h2 style="margin:0">🛡️ DPDP Readiness & Data Risk Checker</h2>
    <p style="margin:0.3rem 0 0 0; opacity:0.9; font-size:0.95rem">
        Digital Personal Data Protection Act 2023 (India) &nbsp;|&nbsp; Powered by OrangeTree Global × Claude AI
    </p>
</div>
""", unsafe_allow_html=True)

# ── What this tool does ───────────────────────────────────────────────────────
st.markdown("""
<div class="intro-box">
    <h4 style="margin:0 0 0.5rem 0">📌 What does this tool do — and why does it matter?</h4>
    <p style="margin:0 0 0.5rem 0">
        India's <b>Digital Personal Data Protection Act 2023 (DPDP Act)</b> is now law. It applies to <b>any business that
        collects, stores, or processes personal data</b> — including your customers' names, phone numbers, emails,
        purchase history, health information, or any data that can identify a person.
    </p>
    <p style="margin:0 0 0.5rem 0">
        <b>Non-compliance can attract penalties of up to ₹250 crore</b> — even for small businesses.
        Most SMEs don't realise they're already covered by this law.
    </p>
    <p style="margin:0">
        This tool asks you <b>16 plain-language questions</b> about how your business currently handles data.
        Claude AI then analyses your answers, scores your compliance across 6 legal pillars,
        identifies your highest-risk gaps, and tells you exactly what to fix first.
        <b>No legal jargon. No consultant needed to interpret the results.</b>
    </p>
</div>
""", unsafe_allow_html=True)

# How to use this — 3 steps
st.markdown("#### 🗺️ How to use this tool — 3 steps")
col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
    st.markdown("""
    <div style="background:#f8f9fa; border-radius:8px; padding:1rem; text-align:center">
        <div style="font-size:2rem">📋</div>
        <b>Step 1 — Fill in the sidebar</b><br>
        <small>Enter your API key and basic details about your business. This helps Claude give you sector-specific advice, not generic answers.</small>
    </div>""", unsafe_allow_html=True)
with col_s2:
    st.markdown("""
    <div style="background:#f8f9fa; border-radius:8px; padding:1rem; text-align:center">
        <div style="font-size:2rem">✅</div>
        <b>Step 2 — Answer 16 questions</b><br>
        <small>Be honest about your <em>current</em> practices — not what you plan to do. There are no wrong answers; this is a diagnostic, not a test.</small>
    </div>""", unsafe_allow_html=True)
with col_s3:
    st.markdown("""
    <div style="background:#f8f9fa; border-radius:8px; padding:1rem; text-align:center">
        <div style="font-size:2rem">📊</div>
        <b>Step 3 — Get your report</b><br>
        <small>Receive a compliance score, gap analysis, and a prioritised action plan — downloadable and shareable with your team or legal advisor.</small>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Setup")

    st.markdown("**🔑 Your Anthropic API Key**")
    st.markdown("<small>This connects the tool to Claude AI, which analyses your answers. Your key is never stored — it's used only for this session. Get yours free at console.anthropic.com</small>", unsafe_allow_html=True)
    api_key = st.text_input("API Key", type="password", label_visibility="collapsed", placeholder="sk-ant-...")

    st.markdown("---")
    st.markdown("**🤖 AI Model**")
    st.markdown("<small>claude-sonnet is the best balance of speed and accuracy. Use claude-opus for the most detailed analysis.</small>", unsafe_allow_html=True)
    model = st.selectbox("Model", ["claude-opus-4-8", "claude-sonnet-4-6", "claude-haiku-4-5-20251001"],
                         index=1, label_visibility="collapsed")

    st.markdown("---")
    st.markdown("### 🏢 Your Organisation")
    st.markdown("<small>These details help Claude tailor its analysis to your specific sector. A restaurant faces different DPDP risks than a clinic or an HR firm.</small>", unsafe_allow_html=True)

    org_name = st.text_input("Organisation name", placeholder="e.g. Bhawanipur House",
                              help="Used to personalise your report header")
    org_type = st.selectbox("Your sector / industry",
        ["F&B / Restaurant", "Retail", "Healthcare / Clinic", "Education / EdTech",
         "Financial Services / NBFC", "Manufacturing", "IT / SaaS", "HR / Staffing", "Other"],
        help="Different sectors have different data risk profiles under DPDP")
    org_size = st.selectbox("Number of employees",
        ["1–10", "11–50", "51–200", "200+"],
        help="Larger organisations face stricter scrutiny under DPDP")

    st.markdown("---")
    st.info("""⚖️ **Disclaimer**

This tool provides a **preliminary self-assessment only**. It is not legal advice. For binding compliance guidance, consult a DPDP-qualified legal advisor.

*Provided by OrangeTree Global as part of their AI SME Suite.*""")

# ── Questionnaire ─────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("## 📋 The 16-Question Assessment")
st.markdown("""
Answer each question based on **what your business actually does today** — not what you intend to do.
"Partially" is a valid and honest answer. The goal is an accurate picture so the AI can help you prioritise correctly.
""")

OPTIONS = ["✅ Yes — fully in place", "⚠️ Partially — work in progress", "❌ No — not done yet", "➖ Not applicable to us"]

responses = {}

# PILLAR 1
st.markdown('<div class="section-header">📌 Pillar 1 — How You Get Permission to Use Data (Consent)</div>', unsafe_allow_html=True)
st.markdown('<div class="section-desc">The DPDP Act requires that people knowingly agree before you collect their data. This section checks whether your current consent process is legally valid — or whether you\'re collecting data that customers haven\'t actually agreed to share.</div>', unsafe_allow_html=True)

responses["p1_q1"] = st.radio(
    "Do you explicitly ask customers/users for permission before collecting their personal data?",
    OPTIONS, key="p1q1", horizontal=True,
    help="'Personal data' includes name, phone, email, address, purchase history, photos — anything that identifies a person. Simply having a signup form doesn't count as consent unless users actively agree."
)
responses["p1_q2"] = st.radio(
    "Can customers easily withdraw their consent and opt out — and do you actually stop using their data when they do?",
    OPTIONS, key="p1q2", horizontal=True,
    help="Under DPDP, withdrawing consent must be as easy as giving it. A buried 'unsubscribe' link in an email footer may not be sufficient."
)
responses["p1_q3"] = st.radio(
    "Do you have a written Privacy Notice or Policy that customers can read before sharing their data?",
    OPTIONS, key="p1q3", horizontal=True,
    help="This is the page or document that tells people what data you collect, why, and how you use it. It needs to be visible at the point of data collection — not just buried in your website footer."
)

# PILLAR 2
st.markdown('<div class="section-header">📌 Pillar 2 — Collecting Only What You Need (Data Minimisation)</div>', unsafe_allow_html=True)
st.markdown('<div class="section-desc">Many businesses collect far more data than they actually use — "just in case". The DPDP Act prohibits this. You should only collect data that is directly necessary for a specific, stated purpose.</div>', unsafe_allow_html=True)

responses["p2_q1"] = st.radio(
    "Do your forms and systems collect ONLY the data fields you actually use — no 'just in case' extras?",
    OPTIONS, key="p2q1", horizontal=True,
    help="Example: if you run a restaurant, you need a customer's phone for reservations — but do you really need their date of birth? If you collect it and don't use it, that's a DPDP risk."
)
responses["p2_q2"] = st.radio(
    "Is customer data used only for the reason it was originally collected — and not repurposed later?",
    OPTIONS, key="p2q2", horizontal=True,
    help="Example: collecting a phone number for order delivery and then using it for WhatsApp marketing requires separate consent. Repurposing data without fresh consent is a violation."
)
responses["p2_q3"] = st.radio(
    "Do you have a written list or register of what personal data you hold, where it's stored, and why?",
    OPTIONS, key="p2q3", horizontal=True,
    help="Called a 'data inventory' or 'data register'. Most SMEs don't have this — but it's one of the first things a DPDP audit or regulator will ask for. Even a simple spreadsheet counts."
)

# PILLAR 3
st.markdown('<div class="section-header">📌 Pillar 3 — Customer Rights Over Their Own Data</div>', unsafe_allow_html=True)
st.markdown('<div class="section-desc">Under the DPDP Act, individuals have the right to know what data you hold about them, correct it if it\'s wrong, and ask you to delete it entirely. This section checks whether your business can actually honour these rights.</div>', unsafe_allow_html=True)

responses["p3_q1"] = st.radio(
    "If a customer asks 'what data do you have about me?', can you actually retrieve and share it with them?",
    OPTIONS, key="p3q1", horizontal=True,
    help="This is called the 'Right of Access'. If customer data is scattered across WhatsApp chats, Excel sheets, a CRM, and a billing system, this is very hard to fulfil. DPDP requires you to be able to respond."
)
responses["p3_q2"] = st.radio(
    "Can customers request that you correct incorrect data about them — or delete all their data entirely?",
    OPTIONS, key="p3q2", horizontal=True,
    help="This is the 'Right to Correction' and 'Right to Erasure' (similar to GDPR's right to be forgotten). The law requires you to have a process for this — a contact email or form at minimum."
)
responses["p3_q3"] = st.radio(
    "Do you have a process to respond to these data requests within a reasonable timeframe (e.g. 30 days)?",
    OPTIONS, key="p3q3", horizontal=True,
    help="Having the right to request is only useful if someone actually processes the request. Do you have a named person responsible for handling these? A response timeline? This is what regulators will check."
)

# PILLAR 4
st.markdown('<div class="section-header">📌 Pillar 4 — Internal Accountability & Breach Handling</div>', unsafe_allow_html=True)
st.markdown('<div class="section-desc">The DPDP Act places legal responsibility on whoever collects data (called the "Data Fiduciary" — that\'s you). This section checks whether your organisation has ownership of compliance internally and a plan for if something goes wrong.</div>', unsafe_allow_html=True)

responses["p4_q1"] = st.radio(
    "Is there a specific person in your organisation responsible for data protection and DPDP compliance?",
    OPTIONS, key="p4q1", horizontal=True,
    help="This doesn't need to be a dedicated 'Data Protection Officer' (that's required only for large organisations). But someone needs to own it — otherwise nobody does, and penalties fall on the business owner."
)
responses["p4_q2"] = st.radio(
    "If your customer data was breached or leaked, do you have a process to detect it, contain it, and notify affected people?",
    OPTIONS, key="p4q2", horizontal=True,
    help="The DPDP Act requires breach notification. If your CRM is hacked, or a laptop with customer data is stolen, you are legally required to notify the Data Protection Board and affected individuals. Do you know what to do?"
)
responses["p4_q3"] = st.radio(
    "Do your contracts with vendors and third parties (e.g. delivery apps, payment gateways, cloud tools) include data protection clauses?",
    OPTIONS, key="p4q3", horizontal=True,
    help="When you share customer data with a third party (e.g. Zomato, Razorpay, your WhatsApp Business provider), you remain legally responsible for how they handle it. Contracts should specify their data obligations."
)

# PILLAR 5
st.markdown('<div class="section-header">📌 Pillar 5 — Sensitive & Children\'s Data</div>', unsafe_allow_html=True)
st.markdown('<div class="section-desc">Certain types of data carry much higher risk and stricter obligations under DPDP. This section checks if your business handles any of these categories — and if so, whether the extra safeguards are in place.</div>', unsafe_allow_html=True)

responses["p5_q1"] = st.radio(
    "If your service is used by anyone under 18, do you have a process to verify age and get parental consent?",
    OPTIONS, key="p5q1", horizontal=True,
    help="DPDP imposes the strictest rules on data about minors. If your restaurant, app, or service could be used by someone under 18, this applies to you — even if you don't specifically target children."
)
responses["p5_q2"] = st.radio(
    "If you hold sensitive data (health records, financial details, biometrics, location history), do you apply extra security measures?",
    OPTIONS, key="p5q2", horizontal=True,
    help="Sensitive data examples for SMEs: patient records at a clinic, salary data at an HR firm, dietary restrictions at a restaurant, biometric attendance data. These require stronger encryption, tighter access controls, and more explicit consent."
)

# PILLAR 6
st.markdown('<div class="section-header">📌 Pillar 6 — Security & Where Your Data Lives</div>', unsafe_allow_html=True)
st.markdown('<div class="section-desc">Even if your intentions are good, a data breach caused by poor security is a DPDP violation. This section checks whether your basic technical and organisational safeguards are in place — and whether sending data to foreign servers creates cross-border compliance risk.</div>', unsafe_allow_html=True)

responses["p6_q1"] = st.radio(
    "Is your customer data stored securely — with password protection, encryption, and restricted access?",
    OPTIONS, key="p6q1", horizontal=True,
    help="This includes: customer lists in Google Sheets (who has access?), CRM databases (are passwords shared?), WhatsApp Business (who can see customer chats?), email inboxes (2FA enabled?). 'Secure' means only the right people can access it."
)
responses["p6_q2"] = st.radio(
    "Does your customer data leave India — e.g. stored on US/EU cloud servers, processed by foreign SaaS tools?",
    OPTIONS, key="p6q2", horizontal=True,
    help="If you use Google Workspace, AWS, Mailchimp, HubSpot, Zoho (even Zoho stores data abroad in some configurations) — your data may be going outside India. DPDP has specific rules about cross-border transfers. This is one of the most commonly overlooked risks for SMEs."
)
responses["p6_q3"] = st.radio(
    "Are employee access logs to customer data tracked — so you know who accessed what, and when?",
    OPTIONS, key="p6q3", horizontal=True,
    help="If an employee leaks customer data, can you detect it? Logging doesn't need to be sophisticated — even knowing which team members have access to your CRM or customer spreadsheet is a starting point."
)

# Additional context
st.markdown("---")
st.markdown("#### 💬 Anything else Claude should know about your data practices? *(optional)*")
st.markdown("<small style='color:#555'>For example: tools you use (WhatsApp, Tally, Zoho, Google Sheets), how you store customer data today, any past data incidents, or specific concerns you have. The more context you give, the more targeted the advice.</small>", unsafe_allow_html=True)
additional_context = st.text_area("Additional context", label_visibility="collapsed",
    placeholder="e.g. We store customer data in Google Sheets and WhatsApp groups. We use Razorpay for payments. We collect CCTV footage in our restaurant premises. We have 3 staff members with access to the customer database...")

# ── Progress check before submitting ─────────────────────────────────────────
answered = sum(1 for v in responses.values() if v != "")
st.markdown("---")
st.markdown(f"**Progress:** {answered}/16 questions answered")

if answered < 16:
    st.info("Answer all 16 questions above to generate your compliance report.", icon="👆")

# ── Analyse button ────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    analyse_btn = st.button("🔍 Generate My DPDP Report", type="primary", use_container_width=True,
                             disabled=(answered < 16))

if analyse_btn:
    if not api_key:
        st.error("⚠️ Please enter your Anthropic API key in the left sidebar to continue.")
        st.stop()

    # Calculate raw score
    score_map = {
        "✅ Yes — fully in place": 3,
        "⚠️ Partially — work in progress": 1.5,
        "❌ No — not done yet": 0,
        "➖ Not applicable to us": 3
    }
    applicable = {k: v for k, v in responses.items() if v != "➖ Not applicable to us"}
    total_possible = len(applicable) * 3
    total_score = sum(score_map.get(v, 0) for v in applicable.values())
    raw_pct = int((total_score / total_possible) * 100) if total_possible > 0 else 0

    with st.spinner("Claude is analysing your compliance posture across all 6 DPDP pillars..."):
        try:
            client = anthropic.Anthropic(api_key=api_key)

            responses_text = "\n".join([f"- {k}: {v}" for k, v in responses.items()])

            SYSTEM = """You are an expert in India's Digital Personal Data Protection Act 2023 (DPDP Act).
Analyse the compliance questionnaire responses and return a JSON object with this exact structure:
{
  "overall_risk": "High/Medium/Low",
  "compliance_summary": "2-3 sentence plain-language assessment written directly to the business owner — avoid jargon, explain what it means for their business",
  "pillar_scores": {
    "Lawful Basis & Consent": {"score": 0-100, "status": "Compliant/Partial/Non-compliant", "finding": "one practical sentence"},
    "Data Minimisation": {"score": 0-100, "status": "...", "finding": "..."},
    "Data Principal Rights": {"score": 0-100, "status": "...", "finding": "..."},
    "Data Fiduciary Obligations": {"score": 0-100, "status": "...", "finding": "..."},
    "Childrens Data": {"score": 0-100, "status": "...", "finding": "..."},
    "Security & Cross-Border": {"score": 0-100, "status": "...", "finding": "..."}
  },
  "critical_gaps": [
    {"gap": "Plain-English description of the compliance gap", "dpdp_section": "Relevant DPDP Act section", "why_it_matters": "What could actually happen if this isn't fixed", "recommended_action": "Specific, practical step to take", "effort": "Quick fix (1–2 days)/Short-term (1–2 weeks)/Medium-term (1–3 months)"}
  ],
  "quick_wins": ["Specific action completable this week with minimal cost — phrase as an instruction, e.g. 'Draft a one-page privacy notice...'"],
  "estimated_penalty_risk": "Plain-English explanation of potential fine exposure under DPDP Act 2023, with specific rupee figures where relevant",
  "next_steps": ["Prioritised action 1 with who should own it", "Prioritised action 2", "Prioritised action 3"]
}
Be specific to India's DPDP Act 2023, not GDPR. Write in plain English for a non-legal SME owner. Return ONLY valid JSON."""

            USER = f"""Organisation: {org_name or 'Unknown'}
Sector: {org_type}
Size: {org_size} employees
Additional context: {additional_context or 'None provided'}

Questionnaire responses:
{responses_text}

Calculated raw score: {raw_pct}%"""

            response = client.messages.create(
                model=model,
                max_tokens=3000,
                system=SYSTEM,
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
            st.error(f"Response parsing error: {e}. Please try again.")
            st.code(raw)
        except Exception as e:
            st.error(f"API error: {e}")

# ── Results ───────────────────────────────────────────────────────────────────
if "dpdp_result" in st.session_state:
    r = st.session_state["dpdp_result"]
    st.markdown("---")
    st.markdown(f"## 📊 Your DPDP Compliance Report")
    if org_name:
        st.markdown(f"**Organisation:** {org_name} &nbsp;|&nbsp; **Sector:** {org_type} &nbsp;|&nbsp; **Date:** {datetime.now().strftime('%d %B %Y')}")

    # What these numbers mean
    st.markdown("""
    <div style="background:#f0f6ff; border:1px solid #c0d9f5; border-radius:8px; padding:0.8rem 1.2rem; margin-bottom:1rem; font-size:0.88rem">
    📖 <b>How to read this report:</b> Your compliance score reflects how well your current practices align with the DPDP Act 2023.
    A score below 60% means there are likely gaps that carry real legal risk. Focus on <b>Critical Gaps</b> first, then the <b>Quick Wins</b> —
    those are things you can fix this week at little or no cost.
    </div>
    """, unsafe_allow_html=True)

    # Score row
    score = r.get("raw_pct", 0)
    risk = r.get("overall_risk", "Medium")
    risk_color = {"High": "#dc3545", "Medium": "#ff8c00", "Low": "#28a745"}.get(risk, "#ff8c00")
    risk_bg = {"High": "#fff3f3", "Medium": "#fff9ec", "Low": "#f0fff4"}.get(risk, "#fff9ec")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="score-box" style="background:{risk_bg}">
            <div style="font-size:3rem; font-weight:bold; color:{risk_color}">{score}%</div>
            <div style="font-size:0.9rem; color:#555">Compliance Score<br><small>0% = no compliance, 100% = fully compliant</small></div>
        </div>""", unsafe_allow_html=True)
    with c2:
        risk_label = {"High": "You are at significant legal risk. Act on the critical gaps below before anything else.", "Medium": "Moderate risk. You have some practices in place but gaps that need addressing.", "Low": "Good baseline. Some refinements needed to be fully compliant."}.get(risk, "")
        st.markdown(f"""<div class="score-box" style="background:{risk_bg}">
            <div style="font-size:2.5rem">{{"High": "🚨", "Medium": "⚠️", "Low": "✅"}}.get("{risk}", "⚠️")</div>
            <div style="font-size:1rem; font-weight:bold; color:{risk_color}">{risk} Risk</div>
            <div style="font-size:0.8rem; color:#555; margin-top:0.3rem">{risk_label}</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        gaps = len(r.get("critical_gaps", []))
        st.markdown(f"""<div class="score-box" style="background:#f8f9fa">
            <div style="font-size:3rem; font-weight:bold; color:#333">{gaps}</div>
            <div style="font-size:0.9rem; color:#555">Critical Gaps Found<br><small>Each gap is a specific area of legal exposure</small></div>
        </div>""", unsafe_allow_html=True)

    # Summary
    st.markdown("### 🗒️ Plain-English Summary")
    st.markdown("<small style='color:#555'>What this means for your business — no legal jargon:</small>", unsafe_allow_html=True)
    st.info(r.get("compliance_summary", ""), icon="📋")

    # Pillar scores
    st.markdown("### 🔍 Breakdown by DPDP Pillar")
    st.markdown("<small style='color:#555'>The DPDP Act has 6 areas of obligation. Here's how your business scores on each one:</small>", unsafe_allow_html=True)
    pillars = r.get("pillar_scores", {})
    for pillar_name, pillar_data in pillars.items():
        ps = pillar_data.get("score", 50)
        status = pillar_data.get("status", "Partial")
        finding = pillar_data.get("finding", "")
        bar_color = "#28a745" if ps >= 70 else "#ffc107" if ps >= 40 else "#dc3545"
        icon = "✅" if ps >= 70 else "⚠️" if ps >= 40 else "❌"
        st.markdown(f"""
        <div class="pillar-card">
            <div style="display:flex; justify-content:space-between; align-items:center">
                <b>{pillar_name}</b>
                <span style="color:{bar_color}">{icon} {status} &nbsp; ({ps}%)</span>
            </div>
            <div style="background:#e9ecef; border-radius:4px; height:8px; margin:6px 0">
                <div style="background:{bar_color}; width:{ps}%; height:8px; border-radius:4px"></div>
            </div>
            <small style="color:#555">{finding}</small>
        </div>""", unsafe_allow_html=True)

    # Critical gaps
    st.markdown("### ❗ Critical Gaps — What You Need to Fix")
    st.markdown("<small style='color:#555'>These are the specific areas where your current practices don't meet DPDP requirements. Each one is a potential source of legal liability. They are ordered by severity.</small>", unsafe_allow_html=True)
    gaps_list = r.get("critical_gaps", [])
    if gaps_list:
        for i, gap in enumerate(gaps_list, 1):
            effort = gap.get("effort", "Unknown")
            effort_color = "#dc3545" if "month" in effort.lower() else "#ffc107" if "week" in effort.lower() else "#28a745"
            with st.expander(f"Gap {i}: {gap.get('gap', '')}"):
                st.markdown(f"**Why this matters:** {gap.get('why_it_matters', '')}")
                st.markdown(f"**DPDP Act reference:** {gap.get('dpdp_section', 'N/A')}")
                st.markdown(f"**What to do:** {gap.get('recommended_action', '')}")
                st.markdown(f"**Effort to fix:** <span style='color:{effort_color}; font-weight:bold'>{effort}</span>", unsafe_allow_html=True)
    else:
        st.success("No critical gaps identified.", icon="✅")

    # Quick wins
    st.markdown("### ⚡ Quick Wins — Do These This Week")
    st.markdown("<small style='color:#555'>These are low-cost, low-effort actions that meaningfully reduce your risk right away — no legal consultant required.</small>", unsafe_allow_html=True)
    for qw in r.get("quick_wins", []):
        st.markdown(f"✅ {qw}")

    # Penalty risk
    st.markdown("### 💰 What's at Stake — Potential Penalties")
    st.markdown("<small style='color:#555'>Based on your responses, here's what the DPDP Act's penalty framework means for your business:</small>", unsafe_allow_html=True)
    st.warning(r.get("estimated_penalty_risk", ""), icon="💰")

    # Next steps
    st.markdown("### 🗺️ Your Prioritised Action Plan")
    st.markdown("<small style='color:#555'>If you only do three things after reading this report, do these — in order:</small>", unsafe_allow_html=True)
    for i, ns in enumerate(r.get("next_steps", []), 1):
        st.markdown(f"**{i}.** {ns}")

    # CTA
    st.markdown("---")
    st.markdown("""
    <div style="background:#f0f6ff; border:1px solid #c0d9f5; border-radius:8px; padding:1rem 1.5rem; margin-bottom:1rem">
    <h4 style="margin:0 0 0.5rem 0">🌳 Need help implementing these changes?</h4>
    <p style="margin:0">OrangeTree Global offers a <b>DPDP Compliance Sprint</b> — a 2-week engagement where we help you close the critical gaps identified in this report,
    draft your Privacy Notice, set up your data inventory, and train your team. <br><b>Contact: ssbishnu@gmail.com</b></p>
    </div>
    """, unsafe_allow_html=True)

    # Export
    export_text = f"""DPDP COMPLIANCE REPORT
{'=' * 50}
Organisation: {org_name or 'Unknown'}
Sector: {org_type} | Size: {org_size}
Date: {datetime.now().strftime('%d %B %Y, %H:%M')}
Compliance Score: {score}% | Risk Level: {risk}

PLAIN-ENGLISH SUMMARY
{r.get('compliance_summary', '')}

CRITICAL GAPS
""" + "\n".join([
    f"\nGap {i}: {g.get('gap', '')}\n  Why it matters: {g.get('why_it_matters', '')}\n  Action: {g.get('recommended_action', '')}\n  Effort: {g.get('effort', '')}"
    for i, g in enumerate(gaps_list, 1)
]) + f"""

QUICK WINS (DO THIS WEEK)
""" + "\n".join([f"• {qw}" for qw in r.get("quick_wins", [])]) + f"""

PENALTY EXPOSURE
{r.get('estimated_penalty_risk', '')}

YOUR ACTION PLAN
""" + "\n".join([f"{i}. {ns}" for i, ns in enumerate(r.get("next_steps", []), 1)]) + f"""

{'=' * 50}
Generated by OrangeTree Global AI SME Suite — DPDP Readiness Checker (UC2)
DISCLAIMER: Preliminary self-assessment only. Not legal advice. Consult a qualified DPDP legal advisor for binding guidance.
"""
    st.download_button(
        "⬇️ Download Full Report as Text File",
        data=export_text,
        file_name=f"DPDP_Report_{(org_name or 'Organisation').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain",
        use_container_width=False
    )
    st.caption("OrangeTree Global | AI SME Suite — UC2: DPDP Readiness Checker | Preliminary assessment only, not legal advice.")
