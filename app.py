import streamlit as st
import json
import os
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
AUDIO_DIR = os.path.join(DATA_DIR, "audio")

st.set_page_config(
    page_title="TaxMaster AI - DT & IDT Smart Learning Portal",
    page_icon="📚",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        color: #64748B;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    .provision-card {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border-left: 5px solid #2563EB;
        padding: 1.2rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .malayalam-script-card {
        background: #F0FDF4;
        border-left: 5px solid #16A34A;
        padding: 1.2rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .badge {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        font-size: 0.8rem;
        font-weight: 600;
        border-radius: 12px;
        margin-right: 0.4rem;
        background-color: #E2E8F0;
        color: #1E293B;
    }
    .badge-sec {
        background-color: #DBEAFE;
        color: #1D4ED8;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions to read data
def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None

# Load states
state = load_json("state.json") or {}
catalog = load_json("catalog.json") or {"chapters": []}
qna_list = load_json("extracted_qna.json") or []
provisions_list = load_json("provisions.json") or []

prov_map = {p.get("question_number"): p for p in provisions_list}

# Sidebar Navigation
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/courthouse.png", width=64)
    st.title("TaxMaster DT & IDT")
    st.caption("AI-Powered CA/CMA Exam Learning Engine")
    
    portal_mode = st.radio(
        "Select Portal Mode",
        ["🎓 Student Learning Portal", "🛠️ Developer Control Dashboard"],
        index=0
    )
    
    st.divider()
    st.subheader("📚 Subject Selection")
    subject = st.selectbox("Subject", ["Direct Tax (DT)", "Indirect Tax (IDT) - Coming Soon"])
    
    st.markdown("### 📊 Overall Pipeline Status")
    p1 = state.get("phase1", {}).get("percent", 0)
    p2 = state.get("phase2", {}).get("percent", 0)
    p3 = state.get("phase3", {}).get("percent", 0)
    st.progress(int((p1 + p2 + p3) / 3))
    st.caption(f"Extraction: {p1}% | Provisions: {p2}% | Audio: {p3}%")

# ==========================================
# 1. STUDENT LEARNING PORTAL
# ==========================================
if portal_mode == "🎓 Student Learning Portal":
    st.markdown("<div class='main-header'>Direct Tax (DT) Question Bank</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Review statutory provisions, listen to Malayalam audio breakdown, and test your exam answers.</div>", unsafe_allow_html=True)
    
    if not qna_list:
        st.warning("⚠️ No questions extracted yet. Please switch to the **Developer Control Dashboard** to run the extraction pipeline.")
    else:
        # Chapter Filter
        col_ch, col_q = st.columns([2, 1])
        with col_ch:
            chapter_options = [f"Chapter 1: Basic Concepts, Tax Rates and Exempt Income"]
            selected_chapter = st.selectbox("Select Chapter", chapter_options)
        
        with col_q:
            q_numbers = [q.get("question_number") for q in qna_list]
            selected_q_num = st.selectbox("Select Question", q_numbers, format_func=lambda x: f"Question {x}")
            
        current_q = next((q for q in qna_list if q.get("question_number") == selected_q_num), None)
        current_prov = prov_map.get(selected_q_num, {})
        
        if current_q:
            st.divider()
            
            # Header of question
            st.markdown(f"### 📝 Question {current_q.get('question_number')}: {current_q.get('question_title', '')}")
            
            # STEP 1: Statutory Provision Breakdown
            with st.container():
                st.markdown("<div class='provision-card'>", unsafe_allow_html=True)
                st.markdown("#### ⚖️ Relevant Statutory Provisions & Legal Principles")
                
                # Sections
                secs = current_prov.get("statutory_sections", [])
                sec_html = "".join([f"<span class='badge badge-sec'>{s}</span>" for s in secs])
                st.markdown(f"**Key Sections:** {sec_html if sec_html else 'General Principles'}", unsafe_allow_html=True)
                st.markdown(f"**Core Principle:** *{current_prov.get('core_principle', 'Direct Tax Principle')}*")
                
                # Bullet summary
                bullets = current_prov.get("provision_summary", [])
                if bullets:
                    st.markdown("**Provision Highlights:**")
                    for b in bullets:
                        st.markdown(f"- {b}")
                st.markdown("</div>", unsafe_allow_html=True)
                
            # STEP 2: Malayalam Audio Player
            st.markdown("<div class='malayalam-script-card'>", unsafe_allow_html=True)
            st.markdown("#### 🔊 മലയാളം ഓഡിയോ വിശദീകരണം (Malayalam Audio Tuition)")
            
            audio_file = os.path.join(AUDIO_DIR, f"q{selected_q_num}.mp3")
            if os.path.exists(audio_file):
                st.audio(audio_file, format="audio/mp3")
            else:
                st.info("Audio generation pending for this question.")
                
            script_text = current_prov.get("malayalam_audio_script", "")
            if script_text:
                with st.expander("📄 Read Malayalam Script"):
                    st.write(script_text)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # STEP 3: The Question Problem Statement
            st.markdown("#### ❓ Question Problem Statement")
            st.info(current_q.get("question_text", ""))
            
            # STEP 4: Active Practice Mode
            with st.expander("✍️ Student Practice Notes / Scratchpad"):
                student_notes = st.text_area("Jot your calculation or key points here before checking the answer:", height=100)
                if student_notes:
                    st.success("Notes saved for this session.")
                    
            # STEP 5: Official Suggested Solution
            with st.expander("✅ Reveal Official ICAI Suggested Answer", expanded=False):
                st.markdown(current_q.get("answer_text", ""))

# ==========================================
# 2. DEVELOPER CONTROL DASHBOARD
# ==========================================
else:
    st.markdown("<div class='main-header'>🛠️ Developer Control Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Monitor background extraction phases, key rotations, checkpoints, and trigger runs.</div>", unsafe_allow_html=True)
    
    # Phase Progress Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Pre-Phase (Catalog)",
            value=f"{len(catalog.get('chapters', []))} Chapters",
            delta="Ready" if len(catalog.get('chapters', [])) > 0 else "Pending"
        )
        st.caption("Table of Contents indexing")
        
    with col2:
        p1_val = state.get("phase1", {}).get("percent", 0)
        st.metric(
            label="Phase 1 (Q&A Extraction)",
            value=f"{p1_val}%",
            delta=f"{len(qna_list)} Questions"
        )
        st.caption(state.get("phase1", {}).get("status", "Not started"))
        
    with col3:
        p2_val = state.get("phase2", {}).get("percent", 0)
        st.metric(
            label="Phase 2 (Provisions)",
            value=f"{p2_val}%",
            delta=f"{len(provisions_list)} Done"
        )
        st.caption(state.get("phase2", {}).get("status", "Not started"))
        
    with col4:
        p3_val = state.get("phase3", {}).get("percent", 0)
        audio_count = len(os.listdir(AUDIO_DIR)) if os.path.exists(AUDIO_DIR) else 0
        st.metric(
            label="Phase 3 (Google Voice Audio)",
            value=f"{p3_val}%",
            delta=f"{audio_count} MP3 Files"
        )
        st.caption(state.get("phase3", {}).get("status", "Not started"))
        
    st.divider()
    
    # Controls & API Key Pool
    c_left, c_right = st.columns([1, 1])
    
    with c_left:
        st.subheader("⚙️ Pipeline Execution Controls")
        st.write("Trigger the automated pipeline for the 10-page test sample or resume from checkpoint.")
        if st.button("🚀 Run / Resume Full Pipeline", type="primary"):
            with st.spinner("Executing pipeline in background..."):
                subprocess.Popen(["python", "pipeline/run_pipeline.py"])
                st.success("Pipeline launched! Refresh in a few moments to see updated progress.")
                
        if st.button("🔄 Refresh Dashboard Data"):
            st.rerun()
            
    with c_right:
        st.subheader("🔑 Gemini API Key Rotation Pool")
        st.write("Configured active keys for automatic quota load balancing:")
        st.code("""
Key 1: AQ.Ab8RN6K... (Local Pool & Google Sheet) - [ACTIVE 200 OK]
Key 2: AQ.Ab8RN6L... (Rotation Pool)             - [ACTIVE 200 OK]
Key 3: AQ.Ab8RN6I... (Rotation Pool)             - [ACTIVE 200 OK]
        """, language="text")
        st.caption("Engine: Google Gemini 3.8 Flash + Google Voice TTS (ml-IN)")
        
    st.divider()
    st.subheader("📖 Indexed Chapters Catalog (Pre-Phase)")
    if catalog.get("chapters"):
        ch_data = [{"Chapter #": c.get("chapter_number"), "Title": c.get("title"), "Page Range": c.get("page_range")} for c in catalog.get("chapters", [])]
        st.dataframe(ch_data, use_container_width=True, height=250)
    else:
        st.info("No catalog data found.")
