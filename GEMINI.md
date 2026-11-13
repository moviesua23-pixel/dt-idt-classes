# Project Context & Rules: DT and IDT Classes

## Project Overview
Automated educational lecture generation pipeline for Direct Tax (DT) and Indirect Tax (IDT) CA Final / Inter courses. Generates structured statutory summaries, interactive mindmaps, and voice-synchronized audio explainer clips.

## Audio & Voice Pronunciation Rules
All audio generation, voice scripts (`voice_sync_text`), and educational narrations MUST strictly follow:
- **Sections & Sub-sections**: Must be in standard English (`Section 49(1)`, `Section 2(42A)`, `Section 55(2)(aa)`). Never transliterate or spell in Malayalam script.
- **Dates & Years**: Must be spoken and written in English (`1st April 2001`, `Assessment Year 2024-25`, `Financial Year 2023-24`). Never translate dates into Malayalam words.
- **Tax & Statutory Terms (Universal Domain Principle)**: Do NOT limit to a hardcoded word list. **ANY and EVERY word or concept related to tax, law, statutory provisions, finance, accounting, or computation MUST be in English.** Malayalam is used strictly for conversational teacher explanations, scaffolding, and connectives.
- **Sentence Style**: Natural, friendly Malayalam teacher explanation with embedded English legal terminology (Manglish code-switching standard in Kerala CA education).

Full rule specification is documented in [.agents/rules/voice_pronunciation_rules.md](file:///c:/Users/HP/OneDrive/Desktop/VISHNU/DT%20and%20IDT%20Classes/.agents/rules/voice_pronunciation_rules.md).
