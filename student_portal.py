import streamlit as st
import json
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
AUDIO_DIR = os.path.join(DATA_DIR, "audio")

st.set_page_config(
    page_title="TaxMaster Pro - Direct & Indirect Tax",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ultra-Premium Modern SaaS / EdTech Styling & Animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    :root {
        --primary-gradient: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
        --accent-gradient: linear-gradient(135deg, #6366F1 0%, #4F46E5 50%, #2563EB 100%);
        --emerald-gradient: linear-gradient(135deg, #10B981 0%, #059669 100%);
        --dark-card: #0F172A;
    }
    
    html, body, [class*="css"] {
        font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif;
        color: #0F172A;
        background-color: #F8FAFC;
    }
    
    /* Keyframe Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(18px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulseGlow {
        0%, 100% {
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.2);
        }
        50% {
            box-shadow: 0 0 25px rgba(59, 130, 246, 0.45);
        }
    }

    @keyframes equalizer {
        0%, 100% { height: 6px; }
        50% { height: 18px; }
    }
    
    .animate-fade-in {
        animation: fadeInUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) both;
    }
    
    /* Top Luxury Banner */
    .hero-banner {
        background: linear-gradient(135deg, #090D16 0%, #0F172A 60%, #1E293B 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 2rem 2.5rem;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px -15px rgba(15, 23, 42, 0.35);
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.4s ease both;
    }
    .hero-banner::after {
        content: "";
        position: absolute;
        top: -50%;
        right: -10%;
        width: 350px;
        height: 350px;
        background: radial-gradient(circle, rgba(59, 130, 246, 0.18) 0%, transparent 70%);
        pointer-events: none;
    }
    
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.8px;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }
    .hero-title span.badge-pill {
        font-size: 0.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #2563EB, #3B82F6);
        color: white;
        padding: 0.25rem 0.8rem;
        border-radius: 9999px;
        box-shadow: 0 2px 10px rgba(37, 99, 235, 0.4);
        letter-spacing: 0.5px;
    }
    .hero-subtitle {
        color: #94A3B8;
        font-size: 1.05rem;
        margin-top: 0.4rem;
        font-weight: 400;
        letter-spacing: -0.2px;
    }
    
    /* Breadcrumb Stepper */
    .breadcrumb-pill {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 0.75rem 1.4rem;
        font-size: 0.92rem;
        font-weight: 600;
        color: #475569;
        margin-bottom: 1.8rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
    }
    .breadcrumb-pill strong {
        color: #0F172A;
    }
    
    /* Luxury Subject Card */
    .premium-subject-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 20px;
        padding: 2.5rem 2rem;
        text-align: center;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.06);
        transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
        overflow: hidden;
    }
    .premium-subject-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 20px 40px -10px rgba(37, 99, 235, 0.15);
        border-color: #3B82F6;
    }
    .subject-icon-box {
        width: 76px;
        height: 76px;
        margin: 0 auto 1.4rem auto;
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
    }
    .subject-icon-dt {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        color: #1D4ED8;
    }
    .subject-icon-idt {
        background: linear-gradient(135deg, #FFF7ED 0%, #FFEDD5 100%);
        color: #C2410C;
    }
    
    /* Interactive Chapter & Question Cards */
    .premium-item-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 1.3rem 1.6rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .premium-item-card:hover {
        transform: translateY(-3px);
        border-color: #60A5FA;
        box-shadow: 0 12px 24px rgba(37, 99, 235, 0.08);
    }
    
    /* Tag Pills */
    .tag-pill {
        display: inline-block;
        font-size: 0.78rem;
        font-weight: 700;
        padding: 0.25rem 0.65rem;
        border-radius: 8px;
        letter-spacing: 0.3px;
    }
    .tag-blue { background: #EFF6FF; color: #1D4ED8; border: 1px solid #BFDBFE; }
    .tag-emerald { background: #ECFDF5; color: #047857; border: 1px solid #A7F3D0; }
    .tag-slate { background: #F1F5F9; color: #475569; border: 1px solid #E2E8F0; }
    
    /* Study Viewport Cards */
    .canvas-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 18px;
        padding: 2rem;
        margin-bottom: 1.8rem;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.04);
        position: relative;
    }
    .canvas-card.provision {
        border-top: 6px solid #2563EB;
    }
    .canvas-card.problem {
        border-left: 6px solid #0EA5E9;
        background: #FAFCFF;
    }
    
    /* Malayalam Audio Equalizer Deck */
    .audio-player-deck {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        border: 1px solid #86EFAC;
        border-left: 6px solid #16A34A;
        border-radius: 16px;
        padding: 1.6rem 2rem;
        margin-bottom: 1.8rem;
        box-shadow: 0 6px 18px rgba(22, 163, 74, 0.06);
    }
    .equalizer-icon {
        display: inline-flex;
        align-items: flex-end;
        gap: 3px;
        height: 18px;
        margin-right: 8px;
    }
    .equalizer-bar {
        width: 3px;
        background-color: #16A34A;
        border-radius: 2px;
        animation: equalizer 1.2s ease-in-out infinite;
    }
    .equalizer-bar:nth-child(2) { animation-delay: 0.2s; }
    .equalizer-bar:nth-child(3) { animation-delay: 0.4s; }
    
    /* Luxury Markdown Table Styling */
    table {
        width: 100% !important;
        border-collapse: separate !important;
        border-spacing: 0 !important;
        margin: 1.5rem 0 !important;
        font-size: 0.95rem !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid #CBD5E1 !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03) !important;
    }
    th {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%) !important;
        color: #FFFFFF !important;
        text-align: left !important;
        padding: 14px 18px !important;
        font-weight: 700 !important;
        letter-spacing: 0.3px !important;
        border: none !important;
    }
    td {
        padding: 12px 18px !important;
        border-bottom: 1px solid #E2E8F0 !important;
        color: #1E293B !important;
        font-weight: 500 !important;
    }
    tr:nth-child(even) td {
        background-color: #F8FAFC !important;
    }
    tr:hover td {
        background-color: #EFF6FF !important;
    }
    
    /* Streamlit Button Customization */
    div.stButton > button {
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-family: 'Outfit', sans-serif !important;
        letter-spacing: 0.3px !important;
        padding: 0.6rem 1.4rem !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 15px rgba(37, 99, 235, 0.2) !important;
    }
    div.stButton > button:active {
        transform: scale(0.98) !important;
    }
</style>
""", unsafe_allow_html=True)

def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None

catalog = load_json("catalog.json") or {"chapters": []}
qna_list = load_json("extracted_qna.json") or []
provisions_list = load_json("provisions.json") or []
prov_map = {p.get("question_number"): p for p in provisions_list}

# Navigation State
if "nav_subject" not in st.session_state:
    st.session_state.nav_subject = None

if "nav_chapter" not in st.session_state:
    st.session_state.nav_chapter = None

if "nav_question" not in st.session_state:
    st.session_state.nav_question = None

# Top Luxury Brand Header
st.markdown("""
<div class='hero-banner'>
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <div>
            <div class='hero-title'>
                ⚖️ TaxMaster Pro <span class='badge-pill'>CA FINAL & CMA</span>
            </div>
            <div class='hero-subtitle'>
                Interactive Tax Intelligence Platform • Statutory Rules ❯ Malayalam Audio ❯ ICAI Case Studies
            </div>
        </div>
        <div style='display: flex; gap: 0.8rem; align-items: center;'>
            <span style='background: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.3); padding: 0.4rem 1rem; border-radius: 9999px; font-size: 0.85rem; font-weight: 700; display: flex; align-items: center; gap: 0.4rem;'>
                <span style='width: 8px; height: 8px; background-color: #34D399; border-radius: 50%; display: inline-block;'></span> Engine Active
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# WINDOW 1: SELECT SUBJECT (HERO WINDOW)
# ==============================================================================
if st.session_state.nav_subject is None:
    st.markdown("<div class='animate-fade-in'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2.5rem;'>
        <span class='tag-pill tag-blue' style='font-size: 0.85rem; padding: 0.35rem 0.9rem; margin-bottom: 0.5rem;'>Step 1 of 3</span>
        <h2 style='font-size: 2.2rem; font-weight: 800; color: #0F172A; margin: 0.4rem 0;'>Choose Subject Area</h2>
        <p style='color: #64748B; font-size: 1.05rem;'>Select your tax domain to browse indexed chapters and questions:</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_l, col_dt, col_idt, col_r = st.columns([0.4, 2.2, 2.2, 0.4], gap="large")
    
    with col_dt:
        st.markdown("""
        <div class='premium-subject-card'>
            <div class='subject-icon-box subject-icon-dt'>📘</div>
            <h2 style='font-weight: 800; color: #0F172A; margin-bottom: 0.4rem; font-size: 1.6rem;'>Direct Tax (DT)</h2>
            <p style='color: #64748B; font-size: 0.95rem; line-height: 1.6; margin-bottom: 1.4rem;'>
                Income-tax Act, 1961, Assessment Procedures, Concessional Slabs u/s 115BAC, Capital Gains, Transfer Pricing & International Tax.
            </p>
            <div style='display: flex; justify-content: center; gap: 0.6rem; margin-bottom: 1.8rem;'>
                <span class='tag-pill tag-blue'>25 Chapters Indexed</span>
                <span class='tag-pill tag-emerald'>🟢 10 Questions Live</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Enter Direct Tax Workspace ➔", type="primary", use_container_width=True, key="btn_dt"):
            st.session_state.nav_subject = "Direct Tax (DT)"
            st.rerun()

    with col_idt:
        st.markdown("""
        <div class='premium-subject-card'>
            <div class='subject-icon-box subject-icon-idt'>📙</div>
            <h2 style='font-weight: 800; color: #0F172A; margin-bottom: 0.4rem; font-size: 1.6rem;'>Indirect Tax (IDT)</h2>
            <p style='color: #64748B; font-size: 0.95rem; line-height: 1.6; margin-bottom: 1.4rem;'>
                CGST & IGST Acts, Supply & Valuation, Input Tax Credit (ITC) Rules, Customs Tariff, Valuation & Foreign Trade Policy.
            </p>
            <div style='display: flex; justify-content: center; gap: 0.6rem; margin-bottom: 1.8rem;'>
                <span class='tag-pill tag-slate'>GST & Customs</span>
                <span class='tag-pill tag-blue'>Ingestion Ready</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Enter Indirect Tax Workspace ➔", use_container_width=True, key="btn_idt"):
            st.session_state.nav_subject = "Indirect Tax (IDT)"
            st.rerun()
            
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# WINDOW 2: SELECT CHAPTER (CHAPTER BROWSER)
# ==============================================================================
elif st.session_state.nav_chapter is None:
    st.markdown("<div class='animate-fade-in'>", unsafe_allow_html=True)
    
    # Navigation Breadcrumb & Back action
    col_nav_b, col_nav_crumb = st.columns([1.2, 5])
    with col_nav_b:
        if st.button("⬅️ Change Subject", use_container_width=True):
            st.session_state.nav_subject = None
            st.rerun()
    with col_nav_crumb:
        st.markdown(f"""
        <div class='breadcrumb-pill'>
            <span>🏠 Domain</span> ❯ <strong>{st.session_state.nav_subject}</strong> ❯ <span style='color: #2563EB;'>Select Chapter</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='margin-bottom: 1.6rem;'>
        <h2 style='font-size: 1.8rem; font-weight: 800; color: #0F172A; margin: 0;'>Chapters in {st.session_state.nav_subject}</h2>
        <p style='color: #64748B; margin-top: 0.2rem;'>Select a chapter to access its questions, statutory tables, and audio tuitions:</p>
    </div>
    """, unsafe_allow_html=True)

    chapters = catalog.get("chapters", [])
    if not chapters:
        chapters = [{"chapter_number": 1, "title": "Basic Concepts, Tax Rates and Exempt Income", "page_range": "1.1 - 1.18"}]

    c_col1, c_col2 = st.columns(2, gap="medium")
    for idx, ch in enumerate(chapters):
        col_dest = c_col1 if idx % 2 == 0 else c_col2
        with col_dest:
            ch_num = ch.get("chapter_number")
            ch_title = ch.get("title")
            page_range = ch.get("page_range", "N/A")
            is_active = (ch_num == 1)
            
            st.markdown(f"""
            <div class='premium-item-card' style='border-left: 5px solid {'#2563EB' if is_active else '#CBD5E1'};'>
                <div style='display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;'>
                    <span class='tag-pill tag-blue'>Chapter {ch_num}</span>
                    <span class='tag-pill {'tag-emerald' if is_active else 'tag-slate'}'>
                        {'🟢 10 Questions Active' if is_active else f'Pages {page_range}'}
                    </span>
                </div>
                <div style='font-size: 1.12rem; font-weight: 700; color: #0F172A; margin: 0.4rem 0;'>{ch_title}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Browse Questions in Chapter {ch_num} ➔", key=f"btn_c_{ch_num}", type="primary" if is_active else "secondary", use_container_width=True):
                st.session_state.nav_chapter = ch
                st.rerun()
                
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# WINDOW 3: SELECT QUESTION WINDOW
# ==============================================================================
elif st.session_state.nav_question is None:
    st.markdown("<div class='animate-fade-in'>", unsafe_allow_html=True)
    ch = st.session_state.nav_chapter
    ch_num = ch.get("chapter_number")
    ch_title = ch.get("title")

    # Header Controls
    col_nav_b, col_nav_crumb = st.columns([1.2, 5])
    with col_nav_b:
        if st.button("⬅️ Change Chapter", use_container_width=True):
            st.session_state.nav_chapter = None
            st.rerun()
    with col_nav_crumb:
        st.markdown(f"""
        <div class='breadcrumb-pill'>
            <span>🏠</span> ❯ {st.session_state.nav_subject} ❯ <strong>Chapter {ch_num}</strong> ❯ <span style='color: #2563EB;'>Select Question</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='margin-bottom: 1.8rem;'>
        <h2 style='font-size: 1.8rem; font-weight: 800; color: #0F172A; margin: 0;'>Chapter {ch_num}: {ch_title}</h2>
        <p style='color: #64748B; margin-top: 0.2rem;'>Select an exam question below to study the legal rules, listen to audio, and practice:</p>
    </div>
    """, unsafe_allow_html=True)

    if not qna_list:
        st.info("No questions found for this chapter.")
    else:
        q_col1, q_col2 = st.columns(2, gap="medium")
        for idx, q in enumerate(qna_list):
            q_dest = q_col1 if idx % 2 == 0 else q_col2
            with q_dest:
                q_num = q.get("question_number")
                prov = prov_map.get(q_num, {})
                principle = prov.get("core_principle") or q.get("question_title", "Tax Case Problem")
                secs = prov.get("statutory_sections", [])
                sec_str = " • ".join(secs[:2]) if secs else "General Provision"
                has_audio = os.path.exists(os.path.join(AUDIO_DIR, f"q{q_num}.mp3"))

                st.markdown(f"""
                <div class='premium-item-card' style='border-top: 4px solid #2563EB;'>
                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;'>
                        <span class='tag-pill tag-blue'>Question {q_num}</span>
                        <span class='tag-pill tag-emerald' style='display: flex; align-items: center; gap: 4px;'>
                            🔊 Malayalam Voice
                        </span>
                    </div>
                    <div style='font-weight: 800; font-size: 1.15rem; color: #0F172A; margin-bottom: 0.4rem; line-height: 1.4;'>
                        {principle}
                    </div>
                    <div style='color: #64748B; font-size: 0.88rem; margin-bottom: 0.8rem; font-weight: 600;'>
                        📌 {sec_str}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Study Question {q_num} Now ➔", key=f"btn_card_q_{q_num}", type="primary", use_container_width=True):
                    st.session_state.nav_question = q_num
                    st.rerun()
                    
    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# WINDOW 4: QUESTION STUDY WORKSPACE
# ==============================================================================
else:
    st.markdown("<div class='animate-fade-in'>", unsafe_allow_html=True)
    ch = st.session_state.nav_chapter
    ch_num = ch.get("chapter_number")
    q_num = st.session_state.nav_question
    
    current_q = next((q for q in qna_list if q.get("question_number") == q_num), None)
    current_prov = prov_map.get(q_num, {})

    # Action Bar: Back to Question Grid + Prev/Next Buttons
    col_back, col_trail, col_prev, col_next = st.columns([1.3, 3.7, 0.8, 0.8], gap="small")
    with col_back:
        if st.button("⬅️ All Questions", use_container_width=True):
            st.session_state.nav_question = None
            st.rerun()
            
    with col_trail:
        st.markdown(f"""
        <div class='breadcrumb-pill'>
            <span>{st.session_state.nav_subject}</span> ❯ <span>Ch {ch_num}</span> ❯ <strong style='color: #2563EB;'>Question {q_num} of {len(qna_list)}</strong>
        </div>
        """, unsafe_allow_html=True)
        
    with col_prev:
        if st.button("◀ Prev", disabled=(q_num <= 1), use_container_width=True):
            st.session_state.nav_question = q_num - 1
            st.rerun()
            
    with col_next:
        if st.button("Next ▶", disabled=(q_num >= len(qna_list)), use_container_width=True):
            st.session_state.nav_question = q_num + 1
            st.rerun()

    if current_q:
        # Title of Question
        principle_title = current_prov.get("core_principle", current_q.get("question_title"))
        st.markdown(f"""
        <div style='margin-bottom: 1.5rem;'>
            <span class='tag-pill tag-blue'>ICAI Final Direct Tax</span>
            <h1 style='font-size: 2.1rem; font-weight: 900; color: #0F172A; margin: 0.3rem 0;'>
                Question {q_num}: {principle_title}
            </h1>
        </div>
        """, unsafe_allow_html=True)

        # High-End Tabs with Icon Headers
        tab_rules, tab_problem, tab_solution = st.tabs([
            "⚖️ 1. Statutory Rules & Malayalam Audio",
            "📋 2. Exam Problem & Student Scratchpad",
            "🏆 3. ICAI Recommended Solution"
        ])
        
        # TAB 1: STATUTORY MATRIX & AUDIO
        with tab_rules:
            st.write("")
            st.markdown("<div class='canvas-card provision'>", unsafe_allow_html=True)
            st.markdown("<h3 style='margin-top: 0; color: #1E3A8A; font-weight: 800; font-size: 1.4rem;'>📊 Statutory Provision & Rules Matrix</h3>", unsafe_allow_html=True)
            
            # Statutory Badges
            secs = current_prov.get("statutory_sections", [])
            if secs:
                badges_html = " ".join([f"<span class='tag-pill tag-blue' style='font-size: 0.85rem; padding: 0.3rem 0.8rem;'>📌 {s}</span>" for s in secs])
                st.markdown(f"<div style='margin-bottom: 1rem;'>{badges_html}</div>", unsafe_allow_html=True)
                
            presentation_md = current_prov.get("provision_presentation_markdown")
            if presentation_md:
                st.markdown(presentation_md, unsafe_allow_html=True)
            else:
                for b in current_prov.get("provision_summary", []):
                    st.markdown(f"- {b}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Malayalam Audio Deck
            st.markdown("""
            <div class='audio-player-deck'>
                <div style='display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.6rem;'>
                    <h3 style='margin: 0; color: #166534; font-weight: 800; font-size: 1.3rem; display: flex; align-items: center;'>
                        <div class='equalizer-icon'>
                            <div class='equalizer-bar'></div>
                            <div class='equalizer-bar'></div>
                            <div class='equalizer-bar'></div>
                        </div>
                        മലയാളം ഓഡിയോ വിശദീകരണം (Listen to Provision)
                    </h3>
                    <span class='tag-pill tag-emerald'>Google Voice TTS</span>
                </div>
                <p style='color: #15803D; font-size: 0.95rem; margin-bottom: 1rem;'>
                    ചോദ്യത്തിന്റെ പ്രശ്നങ്ങളിലേക്ക് കടക്കുന്നതിന് മുൻപ്, ഇതിലെ നിയമപരമായ തത്വം മലയാളത്തിൽ ലളിതമായി കേൾക്കാം:
                </p>
            """, unsafe_allow_html=True)
            
            audio_path = os.path.join(AUDIO_DIR, f"q{q_num}.mp3")
            if os.path.exists(audio_path):
                st.audio(audio_path, format="audio/mp3")
            else:
                st.info("Audio pending generation.")
                
            script = current_prov.get("malayalam_audio_script", "")
            if script:
                with st.expander("📄 View Full Malayalam Script"):
                    st.write(script)
            st.markdown("</div>", unsafe_allow_html=True)

        # TAB 2: PROBLEM STATEMENT & SCRATCHPAD
        with tab_problem:
            st.write("")
            st.markdown("<div class='canvas-card problem'>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='margin-top: 0; color: #0284C7; font-weight: 800; font-size: 1.4rem;'>📋 ICAI Exam Case Problem</h3>", unsafe_allow_html=True)
            st.markdown(current_q.get("question_text", ""))
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("#### ✍️ Active Recall Scratchpad")
            st.caption("Draft your tax computation steps, applicable slabs, or legal conclusions before comparing with the official solution:")
            st.text_area(
                "Your working notes:",
                height=180,
                key=f"scratch_{q_num}",
                placeholder="E.g., 1. Determine residential status...\n2. Check if default 115BAC opted out...\n3. Calculate tax under slab..."
            )

        # TAB 3: ICAI RECOMMENDED ANSWER
        with tab_solution:
            st.write("")
            st.markdown("<div class='canvas-card'>", unsafe_allow_html=True)
            st.markdown("<h3 style='margin-top: 0; color: #0F172A; font-weight: 800; font-size: 1.4rem;'>🏆 Official Recommended Solution & Computation</h3>", unsafe_allow_html=True)
            st.markdown(current_q.get("answer_text", ""))
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Mastery Tracker
            c_m1, c_m2 = st.columns(2)
            with c_m1:
                st.checkbox("Mark as Mastered", key=f"master_{q_num}")
            with c_m2:
                st.checkbox("⭐ Star for Final Revision", key=f"star_flag_{q_num}")
                
    st.markdown("</div>", unsafe_allow_html=True)
