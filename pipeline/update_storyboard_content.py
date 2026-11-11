import os
import json

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SB_FILE = os.path.join(PROJECT_ROOT, "data", "ppt_storyboards.json")
BACKUP_FILE = os.path.join(PROJECT_ROOT, "data", "ppt_storyboards.json.bak")

# Create a backup
if os.path.exists(SB_FILE) and not os.path.exists(BACKUP_FILE):
    with open(SB_FILE, 'r', encoding='utf-8') as f:
        data = f.read()
    with open(BACKUP_FILE, 'w', encoding='utf-8') as f:
        f.write(data)
    print("Created backup at", BACKUP_FILE)

with open(SB_FILE, 'r', encoding='utf-8') as f:
    storyboards = json.load(f)

# Definitions of high-quality, student-focused slide decks & narrations
UPDATED_DATA = {
    "q1": {
        "slides": [
            {
                "slide_number": 1,
                "slide_title": "Concept Overview: Diversion vs. Application of Income",
                "section_badge": "Section 4 & Charging Provisions",
                "malayalam_narration": "Section 4 പ്രകാരം assessee-ക്ക് ലഭിക്കുന്ന Total Income-ന്മേലാണ് നികുതി ചുമത്തുന്നത്. എന്നാൽ വരുമാനം assessee-യുടെ കൈകളിൽ എത്തുന്നതിന് മുൻപ് തന്നെ, നിയമപരമായ ഒരു overriding title കാരണം മാറ്റിവെക്കപ്പെട്ടാൽ, അത് assessee-യുടെ വരുമാനമായി കണക്കാക്കില്ല.",
                "cards": [
                    {
                        "title": "Section 4 Charging Principle",
                        "badge": "Core Rule",
                        "bullets": [
                            "Income-tax is levied on real income belonging to the assessee.",
                            "Taxability arises only if the income legally reaches the assessee."
                        ],
                        "is_highlight": False
                    },
                    {
                        "title": "Overriding Title Doctrine",
                        "badge": "Statutory Principle",
                        "bullets": [
                            "Income diverted at source by anterior legal obligation is excluded from total income.",
                            "Amounts diverted by overriding title never reach the assessee as income."
                        ],
                        "is_highlight": True
                    }
                ]
            },
            {
                "slide_number": 2,
                "slide_title": "The Distinction Matrix: Diversion vs. Application",
                "section_badge": "Judicial Precedents & Doctrine",
                "malayalam_narration": "Diversion-ൽ വരുമാനം assessee-യുടെ അടുത്തെത്തുന്നതിന് മുൻപേ, ഒരു anterior legal obligation വഴി തിരിച്ചുവിടപ്പെടുന്നു. അതിനാൽ ഇത് tax ബാധകമല്ല. നേരെമറിച്ച്, Application-ൽ വരുമാനം ആദ്യം assessee-ക്ക് ലഭിക്കുന്നു, അതിനു ശേഷമാണ് അത് ചെലവഴിക്കുന്നത്. അതിനാൽ Application of income പൂർണ്ണമായും taxable ആണ്.",
                "cards": [
                    {
                        "title": "Diversion by Overriding Title",
                        "badge": "Non-Taxable",
                        "bullets": [
                            "Income is diverted before reaching the assessee.",
                            "Source of obligation is an anterior legal title or court decree.",
                            "Excluded completely from total income."
                        ],
                        "is_highlight": True
                    },
                    {
                        "title": "Application of Income",
                        "badge": "Fully Taxable",
                        "bullets": [
                            "Income is received first by the assessee and then applied.",
                            "Discharge of personal or voluntary obligations.",
                            "Fully taxable in the hands of the recipient assessee."
                        ],
                        "is_highlight": False
                    }
                ]
            },
            {
                "slide_number": 3,
                "slide_title": "Landmark Judicial Benchmark: Sitaldas Tirathdas Rule",
                "section_badge": "Supreme Court Ruling",
                "malayalam_narration": "സുപ്രീം കോടതി landmark കേസ് ആയ Sitaldas Tirathdas-ൽ വ്യക്തമാക്കിയ ടെസ്റ്റ് ഇതാണ്: വരുമാനം assessee-യിൽ എത്തുന്നതിന് മുൻപേ ഒരു overriding title വഴി അത് വേർതിരിക്കപ്പെടുന്നുണ്ടോ? ഉണ്ടെങ്കിൽ അത് diversion ആണ്. എന്നാൽ ലഭിച്ച ശേഷമുള്ള ഏതൊരു ബാധ്യതയും വെറും application of income മാത്രമാണ്.",
                "cards": [
                    {
                        "title": "Supreme Court Test (Sitaldas Tirathdas)",
                        "badge": "Anterior Obligation",
                        "bullets": [
                            "Does the order allocate income before it reaches the assessee?",
                            "If diverted at the source, it is diversion by overriding title."
                        ],
                        "is_highlight": True
                    },
                    {
                        "title": "Application Test (Thakar Das Bhargava)",
                        "badge": "Subsequent Application",
                        "bullets": [
                            "Professional fees received and then paid to trust voluntarily.",
                            "Income reached the assessee first; held fully taxable as application."
                        ],
                        "is_highlight": False
                    }
                ],
                "formula_box": {
                    "formula_text": "Income Taxable = Gross Receipt - Amounts Diverted by Anterior Overriding Title",
                    "example_calc": "Decree directs 40% share of profits directly to mother at source -> 40% diverted (non-taxable), only 60% taxable."
                }
            },
            {
                "slide_number": 4,
                "slide_title": "Key Exam Takeaways & Crucial Pitfalls",
                "section_badge": "ICAI Exam Focus",
                "malayalam_narration": "പരീക്ഷയിൽ ശ്രദ്ധിക്കേണ്ട പ്രധാന കാര്യം: assessee സ്വന്തം ഇഷ്ടപ്രകാരം voluntary ആയി മാറ്റിവെക്കുന്ന വരുമാനം ഒരിക്കലും diversion ആകില്ല. നിയമപരമായോ കോടതി ഉത്തരവ് വഴിയോ ഉള്ള ഒരു anterior obligation ഉണ്ടെങ്കിൽ മാത്രമേ diversion by overriding title ക്ലെയിം ചെയ്യാൻ സാധിക്കൂ.",
                "cards": [
                    {
                        "title": "Voluntary Agreement Trap",
                        "badge": "Exam Trap",
                        "bullets": [
                            "Voluntary allocation of income after receipt is ALWAYS application.",
                            "Exam scenarios with voluntary family arrangements are fully taxable."
                        ],
                        "is_highlight": True
                    },
                    {
                        "title": "Legal Anterior Charge Essential",
                        "badge": "Golden Rule",
                        "bullets": [
                            "A valid charge on property or decree must exist prior to accrual.",
                            "Always check timing: does obligation precede receipt or follow it?"
                        ],
                        "is_highlight": False
                    }
                ]
            }
        ]
    },
    "q4": {
        "slides": [
            {
                "slide_number": 1,
                "slide_title": "Concept Overview & Statutory Applicability",
                "section_badge": "Section 4 & Section 115BAC(6)",
                "malayalam_narration": "Section 115BAC(6) പ്രകാരം assessee ഓപ്ഷണൽ Old Tax Regime തിരഞ്ഞെടുക്കുകയാണെങ്കിൽ, പരമ്പരാഗത age-based സ്ലാബ് നിരക്കുകളാണ് ബാധകമാകുന്നത്. വ്യക്തികളുടെ പ്രായവും Residential Status-ഉം അനുസരിച്ചാണ് basic exemption limit നിശ്ചയിക്കുന്നത്.",
                "cards": [
                    {
                        "title": "Section 4 Charging Provision",
                        "badge": "Finance Act",
                        "bullets": [
                            "Income-tax is charged at progressive rates fixed by the annual Finance Act.",
                            "Calculated on the total income of the previous year."
                        ],
                        "is_highlight": False
                    },
                    {
                        "title": "Optional Old Tax Regime",
                        "badge": "Section 115BAC(6)",
                        "bullets": [
                            "Preserves age-based progressive exemption slabs.",
                            "Retains Chapter VI-A deductions, HRA, and housing loan interest."
                        ],
                        "is_highlight": True
                    },
                    {
                        "title": "Residential Status Nuance",
                        "badge": "Resident Status",
                        "bullets": [
                            "Enhanced basic exemption thresholds apply strictly to Residents.",
                            "Non-Residents receive only the basic ₹ 2,50,000 threshold regardless of age."
                        ],
                        "is_highlight": False
                    }
                ]
            },
            {
                "slide_number": 2,
                "slide_title": "Tax Rates & Thresholds Matrix",
                "section_badge": "Annual Finance Act Slabs",
                "malayalam_narration": "ഇവിടെ മൂന്ന് വിഭാഗങ്ങളുണ്ട്. 60 വയസ്സിൽ താഴെയുള്ള വ്യക്തികൾക്ക് 2.5 ലക്ഷം രൂപ വരെ basic exemption ലഭിക്കും. 60 മുതൽ 80 വയസ്സ് വരെയുള്ള Resident Senior Citizens-ന് 3 ലക്ഷം രൂപയും, 80 വയസ്സിനു മുകളിലുള്ള Resident Super Senior Citizens-ന് 5 ലക്ഷം രൂപയുമാണ് basic exemption limit. അതിനു മുകളിലുള്ള വരുമാനത്തിന് 5%, 20%, 30% ക്രമത്തിൽ നികുതി ഈടാക്കുന്നു.",
                "cards": [
                    {
                        "title": "Below 60 Years & Non-Residents",
                        "badge": "Basic: ₹ 2.5 Lakhs",
                        "bullets": [
                            "Up to ₹ 2,50,000: NIL.",
                            "₹ 2,50,001 - ₹ 5,00,000: 5%.",
                            "₹ 5,00,001 - ₹ 10,00,000: 20% | Above ₹ 10L: 30%."
                        ],
                        "is_highlight": False
                    },
                    {
                        "title": "Resident Senior Citizen (60 to < 80)",
                        "badge": "Basic: ₹ 3.0 Lakhs",
                        "bullets": [
                            "Up to ₹ 3,00,000: NIL.",
                            "₹ 3,00,001 - ₹ 5,00,000: 5%.",
                            "₹ 5,00,001 - ₹ 10,00,000: 20% | Above ₹ 10L: 30%."
                        ],
                        "is_highlight": True
                    },
                    {
                        "title": "Resident Super Senior Citizen (≥ 80)",
                        "badge": "Basic: ₹ 5.0 Lakhs",
                        "bullets": [
                            "Up to ₹ 5,00,000: NIL.",
                            "₹ 5,00,001 - ₹ 10,00,000: 20%.",
                            "Above ₹ 10,00,000: 30%."
                        ],
                        "is_highlight": False
                    }
                ]
            },
            {
                "slide_number": 3,
                "slide_title": "Additional Statutory Levies & Relief",
                "section_badge": "Section 87A & Surcharges",
                "malayalam_narration": "കണക്കാക്കിയ നികുതിയിൽ നിന്ന് Resident Individual-ന്റെ Total Income 5 ലക്ഷം രൂപയിൽ കവിയുന്നില്ലെങ്കിൽ, Section 87A പ്രകാരം പരമാവധി 12,500 രൂപ വരെ rebate ലഭിക്കും. നികുതി തുകയ്ക്ക് മുകളിൽ 4% Health & Education Cess നിർബന്ധമായും കൂട്ടിച്ചേർക്കണം.",
                "cards": [
                    {
                        "title": "Section 87A Rebate",
                        "badge": "Max ₹ 12,500",
                        "bullets": [
                            "Available only to Resident Individuals with Total Income ≤ ₹ 5,00,000.",
                            "Rebate is 100% of tax or ₹ 12,500, whichever is lower."
                        ],
                        "is_highlight": True
                    },
                    {
                        "title": "Progressive Surcharge Slabs",
                        "badge": "TI > ₹ 50 Lakhs",
                        "bullets": [
                            "₹ 50L - ₹ 1 Cr: 10% | ₹ 1 Cr - ₹ 2 Cr: 15%.",
                            "₹ 2 Cr - ₹ 5 Cr: 25% | > ₹ 5 Cr: 37% (Old Regime)."
                        ],
                        "is_highlight": False
                    },
                    {
                        "title": "Health & Education Cess",
                        "badge": "Mandatory 4%",
                        "bullets": [
                            "4% HEC is calculated on (Income-tax + Surcharge - Rebates).",
                            "Applies across all assessees and slabs uniformly."
                        ],
                        "is_highlight": False
                    }
                ],
                "formula_box": {
                    "formula_text": "Net Tax Liability = [Tax on Total Income - Section 87A Rebate + Surcharge] + 4% HEC",
                    "example_calc": "Resident Senior Citizen (Age 65) with TI ₹ 5,00,000 -> Slab Tax ₹ 10,000 -> Less 87A Rebate (₹ 10,000) -> Net Tax: ₹ 0"
                }
            },
            {
                "slide_number": 4,
                "slide_title": "Key Exam Takeaways & Crucial Pitfalls",
                "section_badge": "ICAI Exam Focus",
                "malayalam_narration": "പരീക്ഷയിലെ ഏറ്റവും പ്രധാനപ്പെട്ട trap ഓർക്കുക: Senior Citizen, Super Senior Citizen എന്നിവർക്കുള്ള ഉയർന്ന basic exemption benefits റസിഡന്റുകളായ വ്യക്തികൾക്ക് മാത്രമേ ലഭിക്കൂ. ഒരു Non-Resident-ന് 65 വയസ്സോ 85 വയസ്സോ ഉണ്ടെങ്കിലും, 2.5 ലക്ഷം രൂപ മാത്രമാണ് basic exemption ലഭിക്കുക.",
                "cards": [
                    {
                        "title": "Non-Resident Senior Citizen Trap",
                        "badge": "Examiner Trap",
                        "bullets": [
                            "Senior citizen higher basic exemption is restricted to RESIDENTS only.",
                            "Non-resident aged 65 gets only ₹ 2,50,000 basic exemption limit."
                        ],
                        "is_highlight": True
                    },
                    {
                        "title": "Attaining 60 Years on 1st April",
                        "badge": "CBDT Circular",
                        "bullets": [
                            "Individual born on 1st April completes age on 31st March.",
                            "Qualifies as Senior Citizen for the immediately preceding previous year."
                        ],
                        "is_highlight": False
                    },
                    {
                        "title": "Section 87A Status Rule",
                        "badge": "Strict Eligibility",
                        "bullets": [
                            "Rebate under 87A is NEVER available to a Non-Resident.",
                            "HUF and Firms are also not eligible for Section 87A."
                        ],
                        "is_highlight": False
                    }
                ]
            }
        ]
    },
    "q5": {
        "slides": [
            {
                "slide_number": 1,
                "slide_title": "Concept Overview: Section 87A under Normal Provisions",
                "section_badge": "Section 87A & Section 115BAC(6)",
                "malayalam_narration": "Old Tax Regime തിരഞ്ഞെടുക്കുന്ന 60 വയസ്സിൽ താഴെയുള്ള Resident Individual-ന്റെ നികുതി കണക്കാക്കലും, Section 87A പ്രകാരമുള്ള rebate ആനുകൂല്യങ്ങളുമാണ് ഇവിടെ പരിശോധിക്കുന്നത്. ഈ റെജീമിൽ Chapter VI-A ഡിഡക്ഷനുകൾ പൂർണ്ണമായും ക്ലെയിം ചെയ്യാം.",
                "cards": [
                    {
                        "title": "Old Regime Normal Provisions",
                        "badge": "Section 115BAC(6)",
                        "bullets": [
                            "Preserves age-based slabs and Chapter VI-A deductions.",
                            "Assessee exercises formal option to opt out of default regime."
                        ],
                        "is_highlight": False
                    },
                    {
                        "title": "Section 87A Rebate Rule",
                        "badge": "Resident Relief",
                        "bullets": [
                            "Total Income threshold: does not exceed ₹ 5,00,000.",
                            "Maximum rebate limit: ₹ 12,500."
                        ],
                        "is_highlight": True
                    },
                    {
                        "title": "Applicable Category",
                        "badge": "Individual Below 60",
                        "bullets": [
                            "Basic exemption threshold is ₹ 2,50,000.",
                            "Tax slab between ₹ 2.5L and ₹ 5L is taxed at 5%."
                        ],
                        "is_highlight": False
                    }
                ]
            },
            {
                "slide_number": 2,
                "slide_title": "Tax Rates & Slabs Matrix (Below 60 Years)",
                "section_badge": "Old Regime Slabs",
                "malayalam_narration": "ആദ്യത്തെ 2.5 ലക്ഷം രൂപ വരെ നികുതി NIL ആണ്. 2.5 ലക്ഷം മുതൽ 5 ലക്ഷം വരെയുള്ള തുകയ്ക്ക് 5% നിരക്കിൽ പരമാവധി 12,500 രൂപ നികുതി വരുന്നു. 5 ലക്ഷം മുതൽ 10 ലക്ഷം വരെ 20 ശതമാനവും, 10 ലക്ഷത്തിന് മുകളിലുള്ള വരുമാനത്തിന് 30 ശതമാനവുമാണ് നികുതി നിരക്ക്.",
                "cards": [
                    {
                        "title": "Up to ₹ 2,50,000",
                        "badge": "NIL (0%)",
                        "bullets": [
                            "Basic exemption limit for individuals below 60 years.",
                            "Tax payable: ₹ 0."
                        ],
                        "is_highlight": False
                    },
                    {
                        "title": "₹ 2,50,001 - ₹ 5,00,000",
                        "badge": "5% Rate",
                        "bullets": [
                            "Tax on this slab is 5% of (TI - ₹ 2,50,000).",
                            "Maximum tax in this slab: ₹ 12,500."
                        ],
                        "is_highlight": True
                    },
                    {
                        "title": "₹ 5,00,001 - ₹ 10,00,000",
                        "badge": "20% Rate",
                        "bullets": [
                            "₹ 12,500 + 20% of (TI - ₹ 5,00,000).",
                            "Section 87A rebate is NOT available once TI crosses ₹ 5L."
                        ],
                        "is_highlight": False
                    },
                    {
                        "title": "Above ₹ 10,00,000",
                        "badge": "30% Rate",
                        "bullets": [
                            "₹ 1,12,500 + 30% of (TI - ₹ 10,00,000).",
                            "Surcharge applies if TI > ₹ 50 Lakhs."
                        ],
                        "is_highlight": False
                    }
                ]
            },
            {
                "slide_number": 3,
                "slide_title": "Practical Calculation & Section 87A Mechanics",
                "section_badge": "Section 87A Formula",
                "malayalam_narration": "Section 87A പ്രകാരം, ഒരു Resident Individual-ന്റെ Total Income 5 ലക്ഷം രൂപയിൽ കവിയുന്നില്ലെങ്കിൽ, നികുതി തുകയോ 12,500 രൂപയോ ഏതാണോ കുറവ്, അത് പൂർണ്ണമായും rebate ആയി കുറയ്ക്കാം. അതിനാൽ 5 ലക്ഷം രൂപ വരെ വരുമാനമുള്ളവർക്ക് നികുതി ബാധ്യത പൂജ്യമായിരിക്കും.",
                "cards": [
                    {
                        "title": "Rebate Computation Step",
                        "badge": "Step 1",
                        "bullets": [
                            "Check Total Income after Chapter VI-A deductions.",
                            "If Total Income ≤ ₹ 5,00,000, calculate slab tax."
                        ],
                        "is_highlight": False
                    },
                    {
                        "title": "Rebate Quantum",
                        "badge": "Step 2",
                        "bullets": [
                            "Rebate = Min(Tax on Total Income, ₹ 12,500).",
                            "Absorbs entire tax for incomes up to ₹ 5,00,000."
                        ],
                        "is_highlight": True
                    },
                    {
                        "title": "Final Tax Liability",
                        "badge": "Step 3",
                        "bullets": [
                            "Tax after rebate = ₹ 0.",
                            "Since tax is ₹ 0, Health & Education Cess is also ₹ 0."
                        ],
                        "is_highlight": False
                    }
                ],
                "formula_box": {
                    "formula_text": "Tax Payable = (Tax on Total Income - Rebate u/s 87A) + 4% HEC",
                    "example_calc": "Total Income ₹ 4,80,000 -> Tax: 5% of ₹ 2,30,000 = ₹ 11,500 -> Less 87A Rebate: (₹ 11,500) -> Final Tax: ₹ 0"
                }
            },
            {
                "slide_number": 4,
                "slide_title": "Key Exam Takeaways & Crucial Pitfalls",
                "section_badge": "ICAI Exam Focus",
                "malayalam_narration": "പരീക്ഷയിൽ ഓർക്കേണ്ട രണ്ട് പ്രധാന നിബന്ധനകൾ: ഒന്നാമതായി, Section 87A rebate Resident Individuals-ന് മാത്രമേ ലഭ്യമാകൂ, Non-Residents-നോ HUF-നോ ലഭിക്കില്ല. രണ്ടാമതായി, Net Tax Liability-ക്ക് മുകളിലാണ് 4% Health & Education Cess കണക്കാക്കേണ്ടത്.",
                "cards": [
                    {
                        "title": "Non-Resident Disqualification",
                        "badge": "Resident Test",
                        "bullets": [
                            "A Non-Resident with Total Income ₹ 4,50,000 must pay tax.",
                            "Section 87A is strictly unavailable to Non-Residents."
                        ],
                        "is_highlight": True
                    },
                    {
                        "title": "Total Income > ₹ 5,00,000",
                        "badge": "No Marginal Relief",
                        "bullets": [
                            "If Total Income is ₹ 5,00,010, entire ₹ 12,500 rebate is lost.",
                            "Under the Old Regime, there is NO marginal relief for Section 87A!"
                        ],
                        "is_highlight": True
                    },
                    {
                        "title": "Non-Individual Assessees",
                        "badge": "Entity Test",
                        "bullets": [
                            "HUF, AOP, BOI, and Firms cannot claim Section 87A rebate.",
                            "Benefit is exclusively for individuals."
                        ],
                        "is_highlight": False
                    }
                ]
            }
        ]
    },
    "q6": {
        "slides": [
            {
                "slide_number": 1,
                "slide_title": "Concept Overview: Section 115BAC(1A) Default Regime",
                "section_badge": "Section 115BAC(1A)",
                "malayalam_narration": "Finance Act പ്രകാരം എല്ലാ വ്യക്തികൾക്കും Default Tax Regime ബാധകമാകുന്നത് Section 115BAC(1A) വഴിയാണ്. നികുതിദായകൻ പ്രത്യേകം ഫോം സബ്മിറ്റ് ചെയ്ത് opt-out ചെയ്യാത്ത പക്ഷം, ഈ concessional സ്ലാബ് നിരക്കുകളാണ് ബാധകമാകുന്നത്.",
                "cards": [
                    {
                        "title": "Default Regime Status",
                        "badge": "Automatic Applicability",
                        "bullets": [
                            "Applies automatically to Individuals, HUF, AOP, and BOI.",
                            "Assessee must formally opt out to use Old Tax Regime."
                        ],
                        "is_highlight": False
                    },
                    {
                        "title": "Concessional Slabs Structure",
                        "badge": "Lower Tax Rates",
                        "bullets": [
                            "Progressive slabs with uniform exemption limit.",
                            "Broadened bands reduce effective tax rates significantly."
                        ],
                        "is_highlight": True
                    },
                    {
                        "title": "No Age-Based Exemptions",
                        "badge": "Key Characteristic",
                        "bullets": [
                            "No separate higher basic exemption for Senior Citizens.",
                            "Identical exemption limit applies across all age categories."
                        ],
                        "is_highlight": False
                    }
                ]
            },
            {
                "slide_number": 2,
                "slide_title": "Tax Rates & Threshold Slabs Matrix",
                "section_badge": "Section 115BAC(1A) Slabs",
                "malayalam_narration": "ഈ റെജീമിൽ ആദ്യത്തെ 4 ലക്ഷം രൂപ വരെ നികുതി NIL ആണ്. 4 ലക്ഷം മുതൽ 8 ലക്ഷം വരെ 5%, 8 ലക്ഷം മുതൽ 12 ലക്ഷം വരെ 10%, 12 ലക്ഷം മുതൽ 16 ലക്ഷം വരെ 15%, 16 ലക്ഷം മുതൽ 20 ലക്ഷം വരെ 20%, 20 ലക്ഷം മുതൽ 24 ലക്ഷം വരെ 25%, 24 ലക്ഷത്തിന് മുകളിൽ 30% എന്നിങ്ങനെയാണ് നിരക്കുകൾ.",
                "cards": [
                    {
                        "title": "Up to ₹ 4,00,000",
                        "badge": "NIL (0%)",
                        "bullets": [
                            "Universal basic exemption limit.",
                            "Applies uniformly to all individuals regardless of age."
                        ],
                        "is_highlight": True
                    },
                    {
                        "title": "₹ 4,00,001 - ₹ 12,00,000",
                        "badge": "5% & 10% Slabs",
                        "bullets": [
                            "₹ 4,00,001 - ₹ 8,00,000: 5%.",
                            "₹ 8,00,001 - ₹ 12,00,000: 10%."
                        ],
                        "is_highlight": False
                    },
                    {
                        "title": "Above ₹ 12,00,000",
                        "badge": "15% to 30%",
                        "bullets": [
                            "₹ 12L - ₹ 16L: 15% | ₹ 16L - ₹ 20L: 20%.",
                            "₹ 20L - ₹ 24L: 25% | Above ₹ 24L: 30%."
                        ],
                        "is_highlight": False
                    }
                ]
            },
            {
                "slide_number": 3,
                "slide_title": "Rebate u/s 87A & Surcharge Mechanics",
                "section_badge": "Rebate & Surcharges",
                "malayalam_narration": "Default Regime-ൽ Resident Individual-ന്റെ Total Income നിർദ്ദിഷ്ട പരിധി കവിയുന്നില്ലെങ്കിൽ സെക്ഷൻ 87A പ്രകാരമുള്ള enhanced rebate ലഭിക്കും. കൂടാതെ ഉയർന്ന വരുമാനക്കാർക്ക് ബാധകമായ surcharge നിരക്കുകളിൽ പരമാവധി 25% എന്ന സീലിംഗ് മാത്രമേ ഈ റെജീമിൽ വരുന്നുള്ളൂ.",
                "cards": [
                    {
                        "title": "Enhanced Section 87A Rebate",
                        "badge": "Full Rebate",
                        "bullets": [
                            "Resident individuals earning up to threshold pay ZERO tax.",
                            "Absorbs full tax liability before cess."
                        ],
                        "is_highlight": True
                    },
                    {
                        "title": "Capped Surcharge Rate",
                        "badge": "Max 25%",
                        "bullets": [
                            "Highest surcharge under Section 115BAC is capped at 25%.",
                            "The 37% rate under the Old Regime does NOT apply here."
                        ],
                        "is_highlight": False
                    }
                ],
                "formula_box": {
                    "formula_text": "Net Tax = (Slab Tax u/s 115BAC(1A) - Rebate u/s 87A + Surcharge) + 4% HEC",
                    "example_calc": "Total Income ₹ 8,00,000 -> Tax: 5% of ₹ 4,00,000 = ₹ 20,000. Add 4% Cess = ₹ 20,800."
                }
            },
            {
                "slide_number": 4,
                "slide_title": "Key Exam Takeaways & Pitfalls to Avoid",
                "section_badge": "ICAI Exam Focus",
                "malayalam_narration": "പരീക്ഷയിൽ ഏറ്റവും കൂടുതൽ ശ്രദ്ധിക്കേണ്ട കാര്യം: Section 115BAC-ൽ Senior Citizens-നോ Super Senior Citizens-നോ പ്രത്യേക basic exemption limit ഇല്ല. പ്രായഭേദമന്യേ എല്ലാവർക്കും ഒരേ basic exemption സ്ലാബാണ് ബാധകമാകുന്നത്.",
                "cards": [
                    {
                        "title": "Uniform Exemption for All Ages",
                        "badge": "Crucial Nuance",
                        "bullets": [
                            "An 85-year-old assessee gets the same basic exemption as a 25-year-old.",
                            "Do not apply ₹ 3L or ₹ 5L exemption under Section 115BAC!"
                        ],
                        "is_highlight": True
                    },
                    {
                        "title": "Foregone Deductions",
                        "badge": "Section 115BAC(2)",
                        "bullets": [
                            "Chapter VI-A (80C, 80D, 80G) and HRA are not allowed.",
                            "80CCD(2) employer NPS contribution and Standard Deduction are allowed."
                        ],
                        "is_highlight": False
                    }
                ]
            }
        ]
    },
    "q7": {
        "slides": [
            {
                "slide_number": 1,
                "slide_title": "Concept Overview: Enhanced Rebate u/s 87A",
                "section_badge": "Section 115BAC & Section 87A",
                "malayalam_narration": "Section 115BAC പ്രകാരമുള്ള Default Tax Regime-ൽ ഇടത്തരം വരുമാനക്കാർക്ക് ആശ്വാസം നൽകുന്ന ഒന്നാണ് Section 87A പ്രകാരമുള്ള enhanced rebate. വാർഷിക വരുമാനം നിർദ്ദിഷ്ട പരിധിയിലാണെങ്കിൽ നികുതി പൂജ്യമാക്കാൻ ഇത് സഹായിക്കുന്നു.",
                "cards": [
                    {
                        "title": "Default Regime Enhanced Relief",
                        "badge": "Section 87A",
                        "bullets": [
                            "Higher threshold designed to provide zero tax liability for middle-income earners.",
                            "Applies exclusively to Resident Individuals."
                        ],
                        "is_highlight": True
                    },
                    {
                        "title": "Full Tax Absorption",
                        "badge": "100% Rebate",
                        "bullets": [
                            "Rebate covers 100% of income tax computed on the total income.",
                            "Net tax payable before cess becomes zero."
                        ],
                        "is_highlight": False
                    }
                ]
            },
            {
                "slide_number": 2,
                "slide_title": "Tax Slabs Matrix for A.Y. 2026-27",
                "section_badge": "Section 115BAC(1A)",
                "malayalam_narration": "Assessment Year 2026-27-ലെ സ്ലാബുകൾ നോക്കുക. ആദ്യത്തെ 4 ലക്ഷം രൂപയ്ക്ക് 0% നികുതി. 4 മുതൽ 8 ലക്ഷം വരെ 5 ശതമാനവും, 8 മുതൽ 12 ലക്ഷം വരെ 10 ശതമാനവുമാണ് സ്ലാബ് നിരക്കുകൾ.",
                "cards": [
                    {
                        "title": "First Two Slabs",
                        "badge": "0% & 5%",
                        "bullets": [
                            "Up to ₹ 4,00,000: NIL.",
                            "₹ 4,00,001 - ₹ 8,00,000: 5% (₹ 20,000)."
                        ],
                        "is_highlight": False
                    },
                    {
                        "title": "Third Slab",
                        "badge": "10% Rate",
                        "bullets": [
                            "₹ 8,00,001 - ₹ 12,00,000: 10% (₹ 40,000).",
                            "Cumulative tax on ₹ 12,00,000 = ₹ 60,000."
                        ],
                        "is_highlight": True
                    }
                ]
            },
            {
                "slide_number": 3,
                "slide_title": "Enhanced Rebate & Cess Mechanics",
                "section_badge": "Section 87A Absorption",
                "malayalam_narration": "Total Income 12 ലക്ഷം രൂപ വരെയുള്ള Resident Individual-ന് സെക്ഷൻ 87A പ്രകാരം 60,000 രൂപ വരെയുള്ള പൂർണ്ണ നികുതിയും rebate ആയി ലഭിക്കുന്നു. അതിനാൽ 12 ലക്ഷം രൂപ വരെ നികുതി ബാധ്യത NIL ആയി മാറുന്നു. ഇതിനു മുകളിൽ വരുന്ന നികുതിക്ക് മാത്രമേ 4% Cess ബാധകമാകൂ.",
                "cards": [
                    {
                        "title": "Rebate Computation",
                        "badge": "Up to ₹ 60,000",
                        "bullets": [
                            "Tax on ₹ 12 Lakhs is ₹ 60,000 (₹ 20k + ₹ 40k).",
                            "Entire ₹ 60,000 is rebated u/s 87A."
                        ],
                        "is_highlight": True
                    },
                    {
                        "title": "Net Tax Liability",
                        "badge": "Zero Tax",
                        "bullets": [
                            "Income Tax after rebate = ₹ 0.",
                            "Health & Education Cess (4%) on ₹ 0 = ₹ 0."
                        ],
                        "is_highlight": False
                    }
                ],
                "formula_box": {
                    "formula_text": "Net Tax = (Slab Tax on Total Income - Rebate u/s 87A) = ₹ 0 (if TI ≤ ₹ 12,00,000)",
                    "example_calc": "Resident Individual with Total Income ₹ 12,00,000 -> Tax: ₹ 60,000 -> Rebate u/s 87A: (₹ 60,000) -> Net Tax: ₹ 0"
                }
            },
            {
                "slide_number": 4,
                "slide_title": "Key Exam Takeaways & Crucial Pitfalls",
                "section_badge": "ICAI Exam Focus",
                "malayalam_narration": "പരീക്ഷയിലെ പ്രധാന പോയിന്റ്: ശമ്പള വരുമാനക്കാർക്ക് Section 16(ia) പ്രകാരമുള്ള 75,000 രൂപയുടെ Standard Deduction കുറച്ച ശേഷമുള്ള Net Total Income-ലാണ് ഈ 12 ലക്ഷം രൂപയുടെ പരിധി പരിശോധിക്കേണ്ടത്.",
                "cards": [
                    {
                        "title": "Standard Deduction Interaction",
                        "badge": "Section 16(ia)",
                        "bullets": [
                            "Salaried employees receive ₹ 75,000 Standard Deduction under Default Regime.",
                            "Gross salary up to ₹ 12,75,000 results in zero tax!"
                        ],
                        "is_highlight": True
                    },
                    {
                        "title": "Non-Residents Ineligible",
                        "badge": "Resident Test",
                        "bullets": [
                            "Enhanced Section 87A rebate is NOT available to Non-Residents.",
                            "Non-resident with ₹ 10 Lakh income must pay full tax."
                        ],
                        "is_highlight": False
                    }
                ]
            }
        ]
    },
    "q8": {
        "slides": [
            {
                "slide_number": 1,
                "slide_title": "Concept Overview: Marginal Relief under Section 87A",
                "section_badge": "Section 87A Proviso",
                "malayalam_narration": "Section 87A പ്രകാരമുള്ള rebate പരിധിയിൽ നിന്നും വരുമാനം നേരിയ തോതിൽ കൂടുമ്പോൾ ഉണ്ടാകുന്ന അമിത നികുതി ഭാരം ഒഴിവാക്കാനാണ് Marginal Relief നൽകുന്നത്. അധികമായി ലഭിച്ച വരുമാനത്തേക്കാൾ കൂടുതൽ നികുതി നൽകേണ്ടി വരുന്ന സാഹചര്യം ഇത് തടയുന്നു.",
                "cards": [
                    {
                        "title": "The Cliff Effect Problem",
                        "badge": "Why Relief is Needed",
                        "bullets": [
                            "Crossing threshold by ₹ 10,000 could trigger ₹ 61,500 tax if rebate is lost abruptly.",
                            "Assessee would pay more extra tax than the incremental income earned!"
                        ],
                        "is_highlight": False
                    },
                    {
                        "title": "Statutory Proviso Remedy",
                        "badge": "Section 87A Proviso",
                        "bullets": [
                            "Tax liability is restricted so it does not exceed excess income over threshold.",
                            "Tax payable before cess cannot exceed (Total Income - Threshold)."
                        ],
                        "is_highlight": True
                    },
                    {
                        "title": "Resident Individual Applicability",
                        "badge": "Eligibility",
                        "bullets": [
                            "Applies exclusively to Resident Individuals under Default Tax Regime.",
                            "Smooths out the tax burden around threshold transitions."
                        ],
                        "is_highlight": False
                    }
                ]
            },
            {
                "slide_number": 2,
                "slide_title": "Tax Slabs & Rates under Default Tax Regime",
                "section_badge": "Section 115BAC(1A)",
                "malayalam_narration": "ഡിഫോൾട്ട് റെജീമിൽ 12 ലക്ഷം രൂപ വരെയുള്ള നികുതി Section 87A പ്രകാരം പൂർണ്ണമായും ഒഴിവാക്കപ്പെടുന്നു. എന്നാൽ വരുമാനം 12 ലക്ഷത്തിൽ കവിയുമ്പോൾ, ഈ പൂർണ്ണ റിബേറ്റ് നഷ്ടപ്പെടുകയും ഉയർന്ന സ്ലാബ് നിരക്കിൽ നികുതി വരികയും ചെയ്യുന്നു.",
                "cards": [
                    {
                        "title": "Tax up to Threshold",
                        "badge": "Up to ₹ 12,00,000",
                        "bullets": [
                            "Up to ₹ 4L: NIL | ₹ 4L - ₹ 8L: 5% (₹ 20,000).",
                            "₹ 8L - ₹ 12L: 10% (₹ 40,000) -> Absorbed by 87A rebate."
                        ],
                        "is_highlight": False
                    },
                    {
                        "title": "Tax Exceeding Threshold",
                        "badge": "Above ₹ 12,00,000",
                        "bullets": [
                            "₹ 12,00,001 - ₹ 16,00,000 is taxed at 15%.",
                            "Incremental income is taxed at the 15% marginal slab."
                        ],
                        "is_highlight": True
                    }
                ]
            },
            {
                "slide_number": 3,
                "slide_title": "Marginal Relief Calculation & Formula",
                "section_badge": "Statutory Computational Formula",
                "malayalam_narration": "സെക്ഷൻ 87A പ്രൊവിസോ പ്രകാരം, നൽകേണ്ട അധിക നികുതി 12 ലക്ഷത്തിന് മുകളിലുള്ള അധിക വരുമാനത്തേക്കാൾ കവിയാൻ പാടില്ല. അതായത്, സ്ലാബ് പ്രകാരമുള്ള നികുതിയും അധിക വരുമാനവും തമ്മിലുള്ള വ്യത്യാസം marginal relief ആയി കുറവു ചെയ്യപ്പെടുന്നു.",
                "cards": [
                    {
                        "title": "Step 1: Compute Slab Tax",
                        "badge": "Regular Tax",
                        "bullets": [
                            "Calculate tax on Total Income at applicable slab rates.",
                            "E.g., Tax on ₹ 12,10,000 = ₹ 61,500."
                        ],
                        "is_highlight": False
                    },
                    {
                        "title": "Step 2: Statutory Ceiling",
                        "badge": "Relief Cap",
                        "bullets": [
                            "Maximum tax payable = Excess Income over ₹ 12,00,000.",
                            "Tax Payable = ₹ 10,000. Relief = ₹ 61,500 - ₹ 10,000 = ₹ 51,500."
                        ],
                        "is_highlight": True
                    }
                ],
                "formula_box": {
                    "formula_text": "Rebate u/s 87A = Tax on Total Income - (Total Income - ₹ 12,00,000)",
                    "example_calc": "TI ₹ 12,10,000 -> Slab Tax: ₹ 61,500. Excess Income: ₹ 10,000 -> Marginal Relief: ₹ 51,500 -> Net Tax: ₹ 10,000 + 4% Cess = ₹ 10,400."
                }
            },
            {
                "slide_number": 4,
                "slide_title": "Key Exam Takeaways & Crucial Pitfalls",
                "section_badge": "ICAI Exam Focus",
                "malayalam_narration": "പരീക്ഷയിൽ ഓർക്കുക: Marginal Relief കുറച്ച ശേഷമുള്ള net tax തുകയിൽ മാത്രമേ 4% Health & Education Cess കൂട്ടിച്ചേർക്കാവൂ. കൂടാതെ ഈ റിലീഫ് Resident Individuals-ന് മാത്രമേ ലഭ്യമാകൂ.",
                "cards": [
                    {
                        "title": "Cess Calculation Timing",
                        "badge": "Sequence Rule",
                        "bullets": [
                            "Always deduct Marginal Relief first.",
                            "Add 4% Health & Education Cess on net tax after relief."
                        ],
                        "is_highlight": True
                    },
                    {
                        "title": "Relief Zone Boundary",
                        "badge": "Upper Threshold",
                        "bullets": [
                            "Relief applies only until regular slab tax becomes less than excess income.",
                            "Beyond the boundary, regular slab taxation takes over."
                        ],
                        "is_highlight": False
                    }
                ]
            }
        ]
    },
    "q9": {
        "slides": [
            {
                "slide_number": 1,
                "slide_title": "Concept Overview: Surcharge on Domestic Companies",
                "section_badge": "Finance Act Provisions",
                "malayalam_narration": "Domestic Companies-ന്റെ Total Income ഒരു കോടി രൂപ കവിയുമ്പോൾ ബാധകമാകുന്ന surcharge-ഉം, അതിന്മേൽ ലഭിക്കുന്ന Marginal Relief-ഉം ആണ് നമ്മൾ ഇവിടെ പഠിക്കുന്നത്. മുൻവർഷത്തെ ടേൺഓവർ അടിസ്ഥാനമാക്കിയാണ് അടിസ്ഥാന നികുതി നിരക്ക് നിശ്ചയിക്കുന്നത്.",
                "cards": [
                    {
                        "title": "Turnover-Based Tax Rates",
                        "badge": "25% vs 30%",
                        "bullets": [
                            "Turnover in base year ≤ ₹ 400 Cr: Base tax rate is 25%.",
                            "Other Domestic Companies: Base tax rate is 30%."
                        ],
                        "is_highlight": False
                    },
                    {
                        "title": "Surcharge Threshold",
                        "badge": "₹ 1 Crore Milestone",
                        "bullets": [
                            "Total Income ≤ ₹ 1 Crore: NIL surcharge.",
                            "Total Income > ₹ 1 Crore up to ₹ 10 Crores: 7% surcharge."
                        ],
                        "is_highlight": True
                    }
                ]
            },
            {
                "slide_number": 2,
                "slide_title": "Tax Rates & Surcharge Slabs",
                "section_badge": "Domestic Companies",
                "malayalam_narration": "കമ്പനിയുടെ മുൻവർഷത്തെ turnover 400 കോടി രൂപ വരെയാണെങ്കിൽ ബേസ് ടാക്സ് നിരക്ക് 25% ആണ്; അല്ലെങ്കിൽ 30% വരും. Total Income ഒരു കോടി രൂപ വരെ surcharge ഇല്ല. ഒരു കോടി മുതൽ 10 കോടി വരെ 7 ശതമാനവും, 10 കോടിക്ക് മുകളിൽ 12 ശതമാനവുമാണ് സർചാർജ്.",
                "cards": [
                    {
                        "title": "Total Income ≤ ₹ 1 Crore",
                        "badge": "0% Surcharge",
                        "bullets": [
                            "Flat tax rate (25% or 30%) with no surcharge.",
                            "Add 4% Health & Education Cess."
                        ],
                        "is_highlight": False
                    },
                    {
                        "title": "₹ 1 Crore < TI ≤ ₹ 10 Crores",
                        "badge": "7% Surcharge",
                        "bullets": [
                            "Surcharge of 7% is levied on income tax.",
                            "Marginal relief applies immediately above ₹ 1 Crore."
                        ],
                        "is_highlight": True
                    }
                ]
            },
            {
                "slide_number": 3,
                "slide_title": "Marginal Relief Formula & Calculation",
                "section_badge": "Statutory Ceiling Formula",
                "malayalam_narration": "Total Income ഒരു കോടിയിൽ നിന്ന് അല്പം കൂടുമ്പോൾ വരുന്ന അധിക നികുതിയും സർചാർജും, ഒരു കോടിക്ക് മുകളിലുള്ള അധിക വരുമാനത്തേക്കാൾ കൂടുവാൻ പാടില്ല. അതിനാൽ, ടാക്സ് സീലിംഗ് എന്നത് ഒരു കോടി രൂപയ്ക്കുള്ള നികുതിയും അധിക വരുമാനവും ചേർത്ത തുകയായി നിജപ്പെടുത്തുന്നു.",
                "cards": [
                    {
                        "title": "Step 1: Compute Tax + Surcharge",
                        "badge": "Regular Liability",
                        "bullets": [
                            "Compute basic tax @ 25% or 30%.",
                            "Add 7% surcharge on basic tax."
                        ],
                        "is_highlight": False
                    },
                    {
                        "title": "Step 2: Compare with Statutory Cap",
                        "badge": "Ceiling Rule",
                        "bullets": [
                            "Cap = (Tax on ₹ 1 Crore) + (Total Income - ₹ 1,00,00,000).",
                            "Marginal Relief = (Tax + 7% Surcharge) - Statutory Cap."
                        ],
                        "is_highlight": True
                    }
                ],
                "formula_box": {
                    "formula_text": "Marginal Relief = (Tax + Surcharge) - [Tax on ₹ 1 Cr + (Total Income - ₹ 1,00,00,000)]",
                    "example_calc": "TI ₹ 1,01,00,000 (@30%) -> Tax+SC: ₹ 32,42,100 -> Cap: ₹ 30,00,000 + ₹ 1,00,000 = ₹ 31,00,000 -> Relief: ₹ 1,42,100 -> Net Tax + 4% Cess."
                }
            },
            {
                "slide_number": 4,
                "slide_title": "Key Exam Takeaways & Pitfalls to Avoid",
                "section_badge": "ICAI Exam Focus",
                "malayalam_narration": "പരീക്ഷയിലെ പ്രധാന കാര്യം: Marginal Relief കണക്കാക്കുന്നത് surcharge-ന്മേൽ മാത്രമാണ്. Marginal Relief കുറച്ച ശേഷം ലഭിക്കുന്ന തുകയ്ക്ക് മുകളിലാണ് 4% Health & Education Cess കണക്കാക്കേണ്ടത്, മുൻപല്ല.",
                "cards": [
                    {
                        "title": "Cess Added AFTER Marginal Relief",
                        "badge": "Computation Order",
                        "bullets": [
                            "Never add 4% Cess before computing Marginal Relief.",
                            "Cess is always the last statutory addition."
                        ],
                        "is_highlight": True
                    },
                    {
                        "title": "Turnover Year Verification",
                        "badge": "Rate Selection",
                        "bullets": [
                            "Verify turnover of the relevant preceding year carefully.",
                            "Choosing 25% vs 30% incorrectly changes the entire answer."
                        ],
                        "is_highlight": False
                    }
                ]
            }
        ]
    },
    "q10": {
        "slides": [
            {
                "slide_number": 1,
                "slide_title": "Concept Overview: Surcharge for Income Exceeding ₹ 10 Crores",
                "section_badge": "Finance Act Surcharge Slabs",
                "malayalam_narration": "Domestic Company-യുടെ Total Income 10 കോടി രൂപ കവിയുമ്പോൾ സർചാർജ് നിരക്ക് 7 ശതമാനത്തിൽ നിന്നും പെട്ടെന്ന് 12 ശതമാനമായി ഉയരുന്നു. ഈ കുതിച്ചുചാട്ടം മൂലമുണ്ടാകുന്ന അമിത ബാധ്യത ഒഴിവാക്കാനാണ് Marginal Relief നൽകുന്നത്.",
                "cards": [
                    {
                        "title": "Surcharge Jump at ₹ 10 Crores",
                        "badge": "7% to 12%",
                        "bullets": [
                            "Total Income up to ₹ 10 Crores: Surcharge is 7%.",
                            "Total Income exceeding ₹ 10 Crores: Surcharge jumps to 12%."
                        ],
                        "is_highlight": True
                    },
                    {
                        "title": "Marginal Relief Protection",
                        "badge": "Statutory Cap",
                        "bullets": [
                            "Protects companies from paying more extra tax than excess income over ₹ 10 Cr.",
                            "Capped at (Tax on ₹ 10 Cr with 7% Surcharge + Excess Income)."
                        ],
                        "is_highlight": False
                    }
                ]
            },
            {
                "slide_number": 2,
                "slide_title": "Tax Rates, Turnovers & Surcharge Slabs",
                "section_badge": "Higher Tier Thresholds",
                "malayalam_narration": "10 കോടി വരെയുള്ള വരുമാനത്തിന് 7% സർചാർജ് ബാധകമായിരുന്ന സ്ഥാനത്ത്, 10 കോടി കവിയുന്നതോടെ മുഴുവൻ വരുമാനത്തിനും 12% നിരക്കിലാണ് സർചാർജ് ഈടാക്കുന്നത്. ഈ ഘട്ടത്തിൽ കമ്പനിക്ക് നികുതി ഭാരം വർദ്ധിക്കുന്നു.",
                "cards": [
                    {
                        "title": "Applicable Base Tax Rate",
                        "badge": "25% or 30%",
                        "bullets": [
                            "Turnover in base year ≤ ₹ 400 Cr: Base rate is 25%.",
                            "Turnover in base year > ₹ 400 Cr: Base rate is 30%."
                        ],
                        "is_highlight": False
                    },
                    {
                        "title": "Higher Surcharge Tier",
                        "badge": "12% Surcharge",
                        "bullets": [
                            "12% surcharge applies on the entire tax amount.",
                            "Creates a sharp transition right above ₹ 10 Crores."
                        ],
                        "is_highlight": True
                    }
                ]
            },
            {
                "slide_number": 3,
                "slide_title": "Step-by-Step Marginal Relief Computation",
                "section_badge": "₹ 10 Crore Ceiling Formula",
                "malayalam_narration": "ഇവിടെ Marginal Relief കണക്കാക്കുന്ന ഫോർമുല: 12% സർചാർജ് ഉൾപ്പെടെയുള്ള ആകെ നികുതി, 10 കോടി രൂപയ്ക്ക് 7% സർചാർജ് പ്രകാരം വരുന്ന നികുതിയും 10 കോടിക്ക് മുകളിലുള്ള അധിക വരുമാനവും ചേർത്ത തുകയേക്കാൾ കവിയരുത്. കവിയുന്ന തുക relief ആയി ലഭിക്കും.",
                "cards": [
                    {
                        "title": "Step 1: Compute Regular Tax + 12% SC",
                        "badge": "Full Liability",
                        "bullets": [
                            "Compute tax on Total Income.",
                            "Add 12% surcharge on the entire tax amount."
                        ],
                        "is_highlight": False
                    },
                    {
                        "title": "Step 2: Compute Statutory Ceiling",
                        "badge": "Cap Formula",
                        "bullets": [
                            "Cap = [Tax on ₹ 10 Cr + 7% Surcharge] + (Total Income - ₹ 10,00,00,000).",
                            "Marginal Relief = (Tax + 12% Surcharge) - Statutory Cap."
                        ],
                        "is_highlight": True
                    }
                ],
                "formula_box": {
                    "formula_text": "Marginal Relief = (Tax + 12% Surcharge) - [Tax on ₹ 10 Cr + 7% Surcharge + (Total Income - ₹ 10,00,00,000)]",
                    "example_calc": "TI ₹ 10,01,00,000 (@30%) -> Tax + 12% SC = ₹ 3,36,33,600. Cap = ₹ 3,21,00,000 + ₹ 1,00,000 = ₹ 3,22,00,000 -> Relief: ₹ 14,33,600."
                }
            },
            {
                "slide_number": 4,
                "slide_title": "Key Exam Takeaways & Pitfalls to Avoid",
                "section_badge": "ICAI Exam Focus",
                "malayalam_narration": "പരീക്ഷയിൽ ഓർക്കുക: ഫോറിൻ കമ്പനികൾക്ക് സർചാർജ് നിരക്ക് 2% ഉം 5% ഉം മാത്രമാണ്. എന്നാൽ Domestic Companies-ന് ഇത് 7% ഉം 12% ഉം ആണ്. അവസാനമായി 4% Cess നൽകാൻ മറക്കരുത്.",
                "cards": [
                    {
                        "title": "Domestic vs. Foreign Company Rates",
                        "badge": "Entity Distinction",
                        "bullets": [
                            "Domestic Companies: Surcharge is 7% (TI > ₹ 1 Cr) and 12% (TI > ₹ 10 Cr).",
                            "Foreign Companies: Surcharge is 2% (TI > ₹ 1 Cr) and 5% (TI > ₹ 10 Cr)."
                        ],
                        "is_highlight": True
                    },
                    {
                        "title": "Final 4% Cess Addition",
                        "badge": "Final Step",
                        "bullets": [
                            "Net Tax Liability = (Tax + Surcharge - Marginal Relief) × 1.04.",
                            "Round off final tax liability to nearest ₹ 10 u/s 288B."
                        ],
                        "is_highlight": False
                    }
                ]
            }
        ]
    }
}

for key, updated_val in UPDATED_DATA.items():
    if key in storyboards:
        storyboards[key]["slides"] = updated_val["slides"]
        print(f"Updated slides & narration for {key}")

with open(SB_FILE, 'w', encoding='utf-8') as f:
    json.dump(storyboards, f, indent=2, ensure_ascii=False)

print("Saved updated storyboards to", SB_FILE)
