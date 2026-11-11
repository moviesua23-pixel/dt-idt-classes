import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

from pipeline.pre_phase_catalog import run_pre_phase
from pipeline.phase1_extractor import run_phase1
from pipeline.phase2_provisions import run_phase2
from pipeline.phase3_audio import run_phase3

def main():
    print("=== STARTING DIRECT TAX (DT) PIPELINE RUN ===")
    
    print("\n--- [PRE-PHASE] Indexing Table of Contents & Chapter Structure ---")
    run_pre_phase()
    
    print("\n--- [PHASE 1] Smart Q&A Extraction for 10 Questions ---")
    run_phase1(max_questions=10)
    
    print("\n--- [PHASE 2] Provision Summarization & Malayalam Script ---")
    run_phase2()
    
    print("\n--- [PHASE 3] Google Voice Malayalam Audio Generation ---")
    run_phase3()
    
    print("\n=== ALL PHASES COMPLETED SUCCESSFULLY! ===")

if __name__ == '__main__':
    main()
