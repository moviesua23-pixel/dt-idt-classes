/* ==========================================================================
   PURE AUDIO-DRIVEN KINETIC EXPLAINER ENGINE
   Architecture: render(t) is a pure function of audio.currentTime
   ========================================================================== */

(function(){

const FIXTURES = {
  "dt-c2-q14": {
    "question_id": "dt-c2-q14",
    "audio_url": "data/audio/dt-c2-q14.mp3",
    "duration_sec": 46.2,
    "sync_offset_sec": 0.0,
    "context_pill": "§ 45(2) · Conversion into Stock-in-Trade",
    "beats": [
      {
        "id": "b1",
        "layout": "headline",
        "start": 0.0,
        "end": 6.0,
        "voice_sync_text": "Section 45(2) പ്രകാരം ഒരു Capital Asset, Stock-in-trade ആയി convert ചെയ്യുമ്പോൾ transfer നടക്കുന്നു.",
        "title": { "text": "[[Section 45(2)]]", "at": 0.4 },
        "subtitle": { "text": "Capital asset becomes stock-in-trade, and the tax is [[deferred]] until sale.", "at": 1.6 }
      },
      {
        "id": "b2",
        "layout": "timeline",
        "start": 6.0,
        "end": 16.0,
        "voice_sync_text": "പക്ഷെ tax levy ചെയ്യുന്നത് conversion നടക്കുന്ന വർഷമല്ല, മറിച്ച് ആ stock യഥാർത്ഥത്തിൽ വിൽക്കുന്ന മുൻവർഷത്തിലാണ്.",
        "axis_at": 6.3,
        "arrow_at": 9.4,
        "nodes": [
          {
            "side": "left",
            "at": 6.8,
            "title": "Conversion Year",
            "sub": "(2024-25)",
            "tone": "accent",
            "chips": [
              { "text": "Deemed Transfer", "at": 7.8 },
              { "text": "Tax Parked · ₹ 0 Tax", "at": 8.6 }
            ]
          },
          {
            "side": "right",
            "at": 11.0,
            "title": "Actual Sale Year",
            "sub": "(2025-26)",
            "tone": "ok",
            "chips": [
              { "text": "Stock Sold", "at": 12.0 },
              { "text": "Tax Crystallized!", "at": 13.0, "emphasis": true }
            ]
          }
        ]
      },
      {
        "id": "b3",
        "layout": "scene",
        "start": 16.0,
        "end": 24.0,
        "voice_sync_text": "ഒരു practical example നോക്കാം. Rahul 2010-ൽ ₹ 10 Lakhs-ന് വാങ്ങിയ prime land, P.Y. 2024-25-ൽ convert ചെയ്യുന്നു.",
        "image_url": "data/img/dt-c2-q14-b3.svg",
        "zoom": [1.0, 1.06],
        "tags": [
          { "label": "Cost of land", "value": 1000000, "at": 17.6, "tone": "accent", "pos": "top-left" },
          { "label": "Fair market value on conversion", "value": 4500000, "at": 19.6, "tone": "ok", "pos": "mid-right" }
        ]
      },
      {
        "id": "b4",
        "layout": "split",
        "start": 24.0,
        "end": 32.0,
        "voice_sync_text": "Stock ₹ 65 Lakhs-ന് വിൽക്കുമ്പോൾ dual taxation split വരുന്നു: Capital Gain ₹ 26.5L, Business Profit ₹ 20L.",
        "title": { "text": "Two heads of income, [[one year of sale]]", "at": 24.3 },
        "cards": [
          { "kicker": "Capital gains", "title": "u/s 45(2)", "value": 2650000, "note": "FMV on conversion − indexed cost", "at": 25.6, "tone": "accent" },
          { "kicker": "Business income", "title": "u/s 28", "value": 2000000, "note": "Sale price − FMV on conversion", "at": 27.4, "tone": "ok" }
        ]
      },
      {
        "id": "b5",
        "layout": "trap",
        "start": 32.0,
        "end": 40.0,
        "voice_sync_text": "Section 54EC exemption-ൽ 6 months count ചെയ്യേണ്ടത് conversion മുതലല്ല, stock വിൽക്കുന്ന തീയതി മുതലാണെന്ന് Circular 791 വ്യക്തമാക്കുന്നു.",
        "title": { "text": "Exam trap: gain is [[not taxed]] at conversion", "at": 32.3 },
        "cards": [
          { "tone": "bad", "kicker": "Common mistake", "text": "Taxing the gain in the year of conversion", "at": 34.0 },
          { "tone": "good", "kicker": "Correct rule", "text": "Capital gain is charged in the year the stock is sold", "at": 36.4 }
        ]
      },
      {
        "id": "b6",
        "layout": "takeaway",
        "start": 40.0,
        "end": 46.2,
        "voice_sync_text": "അതുകൊണ്ട് ഓർക്കുക: Section 45(2) പ്രകാരം Tax is deferred, not avoided.",
        "title": { "text": "Tax is [[deferred]], not avoided.", "at": 40.4 }
      }
    ]
  }
};
FIXTURES["ch2_q14"] = FIXTURES["dt-c2-q14"];
FIXTURES["dt-c2-q34"] = {
  "question_id": "dt-c2-q34",
  "audio_url": "data/audio/dt-c2-q34.mp3",
  "duration_sec": 261.71,
  "sync_offset_sec": 0.0,
  "context_pill": "Capital Gains | Real Estate Taxation & Section 112",
  "fallback": false,
  "beats": [
    {
      "id": "b1",
      "layout": "story_scene",
      "scene_type": "property_transfer_sdv",
      "kicker": "FACTUAL NARRATIVE & STATUTORY BENCHMARK",
      "badge": "Property Transfer Case",
      "title": {
        "text": "Property Transfer: Stamp Duty Benchmark vs Actual Agreement",
        "at": 0.3
      },
      "voice_sync_text": "Priypetta vidyarthikale, nammude case-ile assessee Mr. Vijay aanu. Vijay 1982-il oru residential house purchase cheythu, total cost ₹ 5,00,000. Ee property 1st April 2001-il Fair Market Value ₹ 15,00,000 aayirunnu, pakshe Stamp Duty Value ₹ 14,00,000 maathram. Ee asset-il randu thavana advance money forfeit cheythittundu: Onnamathathu June 2009-il ₹ 1,50,000, randamathathu July 2016-il ₹ 2,00,000. Pineed September 2015-il first floor construct cheythu for ₹ 5,08,000. Finally, Financial Year 2025-26-il property sale cheyyaan agreement vekkunnu for ₹ 40,00,000, with an advance of ₹ 2,00,000 received via account payee cheque on agreement date. Ennaal agreement date-ile Stamp Duty Value ₹ 52,00,000 aayirunnu! Ee multi-provision puzzle Section 50C, Section 51, matrum Section 112 vechu namukku solve cheyyaam.",
      "elements": {
        "vijay": {
          "label": "Mr. Vijay Assessee Seller",
          "at": 3.58
        },
        "house_1982": {
          "label": "Residential house purchased in 1982",
          "at": 7.78
        },
        "cost_5l": {
          "label": "Purchase cost ₹ 5,00,000",
          "at": 11.36
        },
        "benchmark_2001": {
          "label": "1st April 2001 statutory base comparison",
          "at": 13.86
        },
        "fmv_15l": {
          "label": "Fair Market Value ₹ 15,00,000",
          "at": 17.08
        },
        "sdv_14l": {
          "label": "Stamp Duty Value ₹ 14,00,000",
          "at": 20.9
        },
        "base_coa": {
          "label": "Base COA Lower of FMV/SDV = ₹ 14,00,000",
          "at": 22.5
        },
        "forfeit_2009": {
          "label": "June 2009 advance forfeited ₹ 1,50,000 u/s 51",
          "at": 28.22
        },
        "forfeit_2016": {
          "label": "July 2016 advance forfeited ₹ 2,00,000 u/s 56(2)(ix)",
          "at": 33.14
        },
        "floor_construction": {
          "label": "First floor constructed Sep 2015 ₹ 5,08,000",
          "at": 38.84
        },
        "buyer": {
          "label": "The Buyer FY 2025-26",
          "at": 45.0
        },
        "agreement_sale": {
          "label": "Sale agreement consideration ₹ 40,00,000",
          "at": 48.88
        },
        "cheque_advance": {
          "label": "Advance ₹ 2,00,000 received via Account Payee Cheque",
          "at": 53.36
        },
        "sdv_agreement": {
          "label": "Agreement date Stamp Duty Value ₹ 52,00,000",
          "at": 57.8
        },
        "safe_harbor_breach": {
          "label": "110% safe harbor limit ₹ 44,00,000 breached",
          "at": 59.18
        },
        "deemed_consideration": {
          "label": "Section 50C Deemed Full Value of Consideration = ₹ 52,00,000",
          "at": 61.46
        },
        "statutory_pills": {
          "label": "Section 50C Section 51 Section 112 multi-provision puzzle",
          "at": 63.08
        }
      },
      "start": 0.0,
      "end": 68.84
    },
    {
      "id": "b2",
      "layout": "statute_quote",
      "voice_sync_text": "Nammal aadyam Section 50C-yude agreement date proviso shradhikkannam. Rule ithaanu: Date of agreement-um date of registration-um different aanenkil, agreement date-ile Stamp Duty Value consider cheyyaam, provided advance money account payee cheque vazhiyo electronic clearing system vazhiyo on or before agreement date receive cheythirikkanam. Ivide ₹ 2,00,000 account payee cheque vazhi agreement date-il thanne kittiyathinaal, ₹ 52,00,000 aanu benchmark SDV. Ee SDV actual consideration-te 110 percentinekaal kooduthal aaya kond, Section 50C prakaram full value of consideration aayi ₹ 52,00,000 edukkanam.",
      "title": {
        "text": "Statutory Mandate: Section 50C Agreement Date Proviso",
        "at": 69.49
      },
      "quote": {
        "text": "Where the date of agreement fixing the consideration and the date of registration are not the same, the value adopted by the stamp valuation authority on the date of agreement may be taken, provided consideration or part thereof has been received by way of an account payee cheque or electronic clearing system on or before the date of agreement.",
        "citation": "Proviso to Section 50C(1) of the Income-tax Act, 1961",
        "emphasis": "account payee cheque on or before the date of agreement",
        "at": 69.69
      },
      "context_bubble": {
        "badge": "Section 50C Filter",
        "speaker": "Statutory Benchmark",
        "theme": "Safe Harbor 110% Test",
        "text": "SDV ₹ 52,00,000 exceeds ₹ 44,00,000 (110% of ₹ 40,00,000). Hence ₹ 52,00,000 is Deemed FVC.",
        "at": 75.79
      },
      "start": 69.19,
      "end": 112.39
    },
    {
      "id": "b3",
      "layout": "meter",
      "voice_sync_text": "Aduthathayi, Cost of Acquisition calculate cheyyaam. Section 55(2)(b) prakaram 1st April 2001-nu munpu vaangiya asset-nu Fair Market Value ₹ 15,00,000 and Stamp Duty Value ₹ 14,00,000 compare cheythu lower amount edukkuka, athayath ₹ 14,00,000. Actual cost ₹ 5,00,000 aayathinaal higher value aaya ₹ 14,00,000 COA aayi varum. Ini advance forfeiture: June 2009-il forfeit cheytha ₹ 1,50,000 1st April 2014-nu munpaayathinaal Section 51 prakaram COA-il ninnu deduct cheythu ₹ 12,50,000 aakkum. Ennaal July 2016-ile ₹ 2,00,000 Section 56(2)(ix) prakaram Income from Other Sources-il tax cheythathinaal ivide deduct cheyyilla!",
      "title": {
        "text": "Cost of Acquisition Determination & Section 51 Filter",
        "at": 113.04
      },
      "meter_display": {
        "min_val": 0,
        "max_val": 1500000,
        "current_val": 1250000,
        "unit": "₹",
        "threshold": 1400000,
        "labels": {
          "start": "₹ 0",
          "threshold_label": "Pre-Forfeiture Base: ₹ 14,00,000",
          "current_label": "Net Adjusted COA: ₹ 12,50,000"
        },
        "at": 154.54
      },
      "breakdown": [
        {
          "label": "FMV capped at SDV as on 01-04-2001",
          "val": 1400000,
          "status": "Base COA u/s 55(2)(b)",
          "at": 117.28
        },
        {
          "label": "Less: Advance forfeited in June 2009 (Pre-01-04-2014)",
          "val": -150000,
          "status": "Deducted u/s 51",
          "at": 138.26
        },
        {
          "label": "Advance forfeited in July 2016 (Post-01-04-2014)",
          "val": 0,
          "status": "Taxed u/s 56(2)(ix) as IFOS (No COA reduction)",
          "at": 153.54
        }
      ],
      "outcome": {
        "text": "Effective Cost of Acquisition = ₹ 12,50,000",
        "tone": "ok",
        "at": 155.44
      },
      "start": 112.74,
      "end": 162.7
    },
    {
      "id": "b4",
      "layout": "ledger",
      "voice_sync_text": "Ippo namukku capital gains computation-lekku kadakkaam. Deemed Full Value ₹ 52,00,000-il ninnu brokerage @ 1% on actual price ₹ 40,000 kurachu Net Consideration ₹ 51,60,000 kittunnu. Indexation illathe LTCG ₹ 34,02,000 aanu. Pakshe Finance Act 2024-te amendment prakaram, resident individual-nu 23rd July 2024-nu munpu vaangiya property-il indexation koduthu tax calculate cheyyanulla option undu. Indexed COA ₹ 47,00,000 and Indexed COI ₹ 7,52,000 kurakkumbol ₹ 2,92,000 Long-Term Capital Loss varunnu! Loss vannathinaal indexation scheme-il tax Nil aanu. Assessee-kku beneficial aaya Nil tax liability select cheyyaam!",
      "title": {
        "text": "Computation of Capital Gains & Section 112 Comparison (AY 2026-27)",
        "at": 163.35
      },
      "callout": {
        "badge": "Section 112 Parity Mechanism",
        "text": "Resident Individual owning property acquired before 23-07-2024 gets benefit: If indexed tax is lower or Nil due to capital loss, taxable liability is restricted to Nil!",
        "at": 164.25
      },
      "ledger_rows": [
        {
          "label": "Deemed Full Value of Consideration u/s 50C",
          "amount": 5200000,
          "type": "income",
          "at": 166.45
        },
        {
          "label": "Less: Brokerage Expenses (1% of ₹ 40,00,000)",
          "amount": -40000,
          "type": "deduction",
          "at": 169.99
        },
        {
          "label": "Net Sale Consideration",
          "amount": 5160000,
          "type": "subtotal",
          "at": 174.91
        },
        {
          "label": "Computation A: Without Indexation (LTCG: ₹ 34,02,000 @ 12.5% + Cess)",
          "amount": 442260,
          "type": "taxable",
          "at": 179.69
        },
        {
          "label": "Computation B: With Indexation (₹ 51,60,000 − ₹ 47,00,000 − ₹ 7,52,000 = Loss)",
          "amount": 0,
          "type": "subtotal",
          "at": 181.77
        }
      ],
      "net_total": {
        "label": "Final Tax Liability Payable u/s 112",
        "val": 0,
        "detail": "Nil (Beneficial indexation comparison yields loss; tax is Nil)",
        "at": 208.35
      },
      "start": 163.05,
      "end": 212.29
    },
    {
      "id": "b5",
      "layout": "takeaway",
      "voice_sync_text": "Exam hall-il ormaveykkendiye moonnu non-negotiable statutory rules: Onnamathathu, Section 50C agreement date SDV apply cheyyanenkil advance amount specified banking channel vazhi on or before agreement date receive cheythirikkanam. Randamathathu, Section 51 advance forfeiture cut-off date: 1st April 2014-nu munpulla forfeiture COA-il reduce cheyyumpol, athinu sheshamulla forfeiture Section 56(2)(ix) prakaram IFOS-il tax aakum. Moonnamathathu, Section 112 transitional relief: Real estate acquired before 23rd July 2024 aanenkil, indexation vazhi loss varukayanenkil final tax liability Nil aayi claim cheyyaam!",
      "title": {
        "text": "3 Golden Rules for Exam Mastery",
        "at": 212.94
      },
      "rules": [
        {
          "num": "01",
          "heading": "Section 50C Banking Channel Rule",
          "body": "Agreement date Stamp Duty Value is valid only if advance consideration is received via account payee cheque/ECS on or before the agreement date.",
          "at": 218.64
        },
        {
          "num": "02",
          "heading": "Forfeited Advance Dual Mechanism",
          "body": "Advance forfeited before 01-04-2014 reduces Cost of Acquisition u/s 51. Advance forfeited on or after 01-04-2014 is taxable under IFOS u/s 56(2)(ix).",
          "at": 223.46
        },
        {
          "num": "03",
          "heading": "Section 112 Beneficial Regime",
          "body": "For properties acquired prior to 23-07-2024 by resident individuals, if indexation computation results in capital loss, the tax liability under Section 112 is effectively Nil.",
          "at": 231.14
        }
      ],
      "start": 212.64,
      "end": 261.36
    }
  ]
};
FIXTURES["dt-c2-q30"] = {
  "question_id": "dt-c2-q30",
  "context_pill": "Section 50C · Section 54 · Section 54EC · Section 71 | Multiple Property & Inter-Head Set-off",
  "fallback": false,
  "beats": [
    {
      "id": "b1",
      "layout": "story_scene",
      "scene_type": "rental_and_gift",
      "kicker": "FACTUAL NARRATIVE & STATUTORY CONTEXT",
      "badge": "Double Property Case",
      "title": {
        "text": "Dual Property Scenario: Bangalore Rental & Chennai Gifted House",
        "at": 0.3
      },
      "voice_sync_text": "Students, namukku Question 30-le double property scenario crystal clear aayi analyze cheyyaam. Assessee Mr. Rajesh-inu randu properties aanu ullathu. First property, Bangalore-il ulla let out residential house. Ithu tenant Mr. Kumar-inu vadakakku koduthu, annual rent 3 Lakhs receive cheyyunnu. Assessee ee varsham municipal taxes arrears sahidham 1 Lakh 85 Thousand rupees paid cheythu. Second property, Chennai-il ulla house. Ithu 1st March 2007-il father gift aayi nalkiyathaam. Father-nte cost of acquisition 1 Lakh 25 Thousand rupees maathramaayirunnu. Ee Chennai house August 2025-il 25 Lakhs rupees-inu assessee sell cheythu. Ee randu transactions-um Income Tax Act-il engane deal cheyyunnu ennu nokkaam.",
      "elements": {
        "divider": {
          "label": "Scenario division",
          "at": 3.78
        },
        "bangalore_reg": {
          "label": "Property 1 Bangalore",
          "at": 10.82
        },
        "bangalore_house": {
          "label": "Bangalore residential house",
          "at": 11.84
        },
        "tenant": {
          "label": "tenant Kumar let out",
          "at": 15.5
        },
        "rent_arc": {
          "label": "rent 3 Lakhs receive",
          "at": 18.32
        },
        "rent_pill": {
          "label": "annual rent 3 Lakhs",
          "at": 18.94
        },
        "municipal_tax": {
          "label": "municipal taxes arrears 185000 paid",
          "at": 22.0
        },
        "chennai_reg": {
          "label": "Property 2 Chennai",
          "at": 27.5
        },
        "father": {
          "label": "father gift",
          "at": 32.22
        },
        "son": {
          "label": "Rajesh assessee",
          "at": 33.12
        },
        "chennai_house": {
          "label": "Chennai house sell",
          "at": 39.44
        },
        "gift_deed": {
          "label": "Gift Deed 1st March 2007",
          "at": 40.34
        },
        "previous_cost": {
          "label": "cost acquisition 125000 sell 25 Lakhs",
          "at": 42.34
        }
      },
      "start": 0.0,
      "end": 49.84
    },
    {
      "id": "b2",
      "layout": "story_scene",
      "scene_type": "rental_computation",
      "kicker": "HOUSE PROPERTY DETERMINATION",
      "badge": "Section 23 · 24 · 25A",
      "title": {
        "text": "Computation of Income from Bangalore House Property",
        "at": 50.49
      },
      "voice_sync_text": "Aadyamaayi namukku Bangalore let-out house property-ude net income compute cheyyaam. Gross Annual Value, actual rent aaya 3 Lakh rupees edukkaam. Section 23 prakaaram, assessee actually paid cheytha municipal taxes current plus arrears serthu 1 Lakh 85 Thousand rupees subtract cheyyuka. Appol Net Annual Value 1 Lakh 15 Thousand rupees aayi maari. Section 24(a) standard deduction 30 percent subtract cheythaal 34 Thousand 500 rupees. Next, property major repair-nu edutha loan interest Section 24(b) prakaaram full 1 Lakh 50 Thousand rupees deduct cheyyaam. Pinne, Section 25A prakaaram receive cheytha rent arrears 30 Thousand rupees-il ninnu 30 percent deduction kazhinju taxable 21 Thousand add cheythaal, Net Loss from House Property 48 Thousand 500 rupees aayi maari.",
      "elements": {
        "step_gav": {
          "label": "Gross Annual Value actual rent 3 Lakh",
          "at": 55.61
        },
        "step_mun_tax": {
          "label": "municipal taxes 185000 subtract",
          "at": 62.99
        },
        "step_nav": {
          "label": "Net Annual Value 115000",
          "at": 70.59
        },
        "step_std_ded": {
          "label": "Section 24(a) standard deduction 30 percent 34500",
          "at": 73.97
        },
        "step_interest": {
          "label": "Section 24(b) interest loan repair 150000",
          "at": 85.43
        },
        "step_arrears": {
          "label": "Section 25A rent arrears 21000",
          "at": 91.53
        },
        "net_loss": {
          "label": "Net Loss House Property 48500",
          "at": 102.67
        }
      },
      "start": 50.19,
      "end": 106.51
    },
    {
      "id": "b3",
      "layout": "story_scene",
      "scene_type": "sdv_comparison",
      "kicker": "STATUTORY DEEMED BENCHMARK",
      "badge": "Section 50C Override",
      "title": {
        "text": "Chennai House Transfer & Section 50C Stamp Duty Benchmark",
        "at": 107.16
      },
      "voice_sync_text": "Next, Chennai property transfer-il Capital Gains compute cheyyaam. Evide crucial statutory provision Section 50C aanu. Actual sale consideration 25 Lakh rupees aanu. Ithinte 110 percent safe harbor threshold 27 Lakh 50 Thousand rupees aanu. Ennaal registration authority-ude Stamp Duty Value 30 Lakh rupees aayi nischayichirikkunnu. Stamp Duty Value safe harbor limit-inekaal higher aaya kaaranathaal, Section 50C trigger aavukayum, deemed Full Value of Consideration 30 Lakh rupees aayi enforce cheyyukayum cheyyunnu. Gift aayathinaal Section 49(1) prakaaram father-nte cost of acquisition aaya 1 Lakh 25 Thousand rupees subtract cheythaal, Gross Long Term Capital Gain 28 Lakh 75 Thousand rupees varunnu.",
      "elements": {
        "actual_bar": {
          "label": "actual consideration 25 Lakh",
          "at": 115.8
        },
        "safe_harbor": {
          "label": "110 percent safe harbor 2750000",
          "at": 119.8
        },
        "sdv_bar": {
          "label": "Stamp Duty Value 30 Lakh",
          "at": 127.78
        },
        "stamp_50c": {
          "label": "Section 50C trigger deemed Full Value",
          "at": 135.3
        },
        "gross_ltcg": {
          "label": "Gross Long Term Capital Gain 2875000",
          "at": 136.2
        }
      },
      "start": 106.86,
      "end": 156.98
    },
    {
      "id": "b4",
      "layout": "story_scene",
      "scene_type": "adjacent_flats_merge",
      "kicker": "EXEMPTION REINVESTMENT",
      "badge": "CIT v. Ananda Basappa",
      "title": {
        "text": "Section 54 Relief: Two Adjacent Flats Combined as Single Unit",
        "at": 157.63
      },
      "voice_sync_text": "Rajesh ee sale proceeds upayogichu reinvestment cheyyukayaanu. Section 54 exemption claim cheyyaan Bangalore-il randu adjacent flats, Flat 101 8 Lakhs-inum Flat 102 7 Lakhs-inum purchase cheythu. Randu separate sale deeds aanenkilum, internal wall remove cheythu oru single habitable residential unit aayi modify cheythu. Karnataka High Court-inte landmark CIT versus Ananda Basappa ruling prakaaram, adjacent flats combine cheythu single residential unit aakkiyaal Section 54-le 'a residential house' condition fully satisfy aakum. Athinaal total investment aaya 15 Lakh rupees-um Section 54 exemption aayi allow cheyyappedum.",
      "elements": {
        "flat_101": {
          "label": "Flat 101 8 Lakhs purchase",
          "at": 166.23
        },
        "flat_102": {
          "label": "Flat 102 7 Lakhs purchase",
          "at": 167.03
        },
        "divider_wall": {
          "label": "internal wall remove",
          "at": 174.49
        },
        "merge_pill": {
          "label": "single habitable residential unit modify",
          "at": 176.13
        },
        "court_ruling": {
          "label": "CIT versus Ananda Basappa ruling",
          "at": 183.29
        },
        "sec54_pill": {
          "label": "Section 54 exemption 15 Lakh",
          "at": 189.73
        }
      },
      "start": 157.33,
      "end": 200.73
    },
    {
      "id": "b5",
      "layout": "story_scene",
      "scene_type": "bond_investment",
      "kicker": "STATUTORY TIMELINE & ALLOTMENT",
      "badge": "Hindustan Unilever Rule",
      "title": {
        "text": "Section 54EC Bond Subscription: Date of Payment Benchmark",
        "at": 201.38
      },
      "voice_sync_text": "Bhakki capital gain Rajesh Section 54EC eligible NHAI bonds-il invest cheyyaan theerumaanichu. Sale date 10th August 2025 aanu. Rajesh 10th October 2025-il, athayathu within 2 months cheque payment 10 Lakh rupees complete cheythu. Ennaal NHAI bonds allot cheythathu 1st February 2026-il aanu. Evide Bombay High Court-inte Hindustan Unilever Limited ruling protect cheyyunnu. Assessee 6 months statutory period-naullil payment complete cheythaal, allotment delay aanaalum Section 54EC exemption deny cheyyaan paadilla. So Rajesh-inu 10 Lakh rupees Section 54EC exemption fully eligible aanu.",
      "elements": {
        "timeline_line": {
          "label": "timeline transfer",
          "at": 221.44
        },
        "node_sale": {
          "label": "Sale 10th August 2025",
          "at": 222.34
        },
        "node_payment": {
          "label": "10th October 2025 payment 10 Lakh",
          "at": 230.5
        },
        "paid_bracket": {
          "label": "within 2 months",
          "at": 231.4
        },
        "node_allotment": {
          "label": "allot 1st February 2026",
          "at": 231.98
        },
        "node_deadline": {
          "label": "6 months statutory period",
          "at": 232.88
        },
        "court_ruling": {
          "label": "Hindustan Unilever Limited ruling",
          "at": 233.78
        },
        "sec54ec_pill": {
          "label": "Section 54EC exemption 10 Lakh",
          "at": 238.74
        }
      },
      "start": 201.08,
      "end": 241.8
    },
    {
      "id": "b6",
      "layout": "ledger",
      "kicker": "FINAL TAXABLE INCOME INTEGRATION",
      "badge": "Section 71 Inter-Head Set-off",
      "title": {
        "text": "Computation of Total Taxable Income with Section 71 Set-Off",
        "at": 242.45
      },
      "voice_sync_text": "Ippo final total income synthesis nokkoo. Gross Long Term Capital Gain 28 Lakh 75 Thousand rupees. Section 54 residential flats exemption 15 Lakh rupees, pinne Section 54EC NHAI bonds exemption 10 Lakh rupees, total 25 Lakh rupees exemption subtract cheythaal Net Long Term Capital Gain 3 Lakh 75 Thousand rupees aayi maari. Ividayaanu master stroke: Section 71 inter-head set off prakaaram, Bangalore property-ude Net Loss from House Property aaya 48 Thousand 500 rupees Capital Gains-il ninnu set off cheyyaam. So Rajesh-inte Net Taxable Total Income 3 Lakh 26 Thousand 500 rupees aayi maari!",
      "ledger_rows": [
        {
          "label": "Deemed Full Value of Consideration u/s 50C",
          "val": "₹ 30,00,000",
          "sign": "+",
          "at": 246.64
        },
        {
          "label": "Less: Cost of Acquisition to Previous Owner u/s 49(1)",
          "val": "₹ 1,25,000",
          "sign": "−",
          "at": 251.13
        },
        {
          "label": "Gross Long-Term Capital Gains (LTCG)",
          "val": "₹ 28,75,000",
          "sign": "=",
          "at": 260.83
        },
        {
          "label": "Less: Exemption u/s 54 (Adjacent Flats CIT v. Ananda Basappa)",
          "val": "₹ 15,00,000",
          "sign": "−",
          "at": 261.73
        },
        {
          "label": "Less: Exemption u/s 54EC (NHAI Bonds Hindustan Unilever Ltd.)",
          "val": "₹ 10,00,000",
          "sign": "−",
          "at": 264.59
        },
        {
          "label": "Net Long-Term Capital Gains",
          "val": "₹ 3,75,000",
          "sign": "=",
          "at": 274.39
        },
        {
          "label": "Less: Section 71 Set-off of House Property Loss",
          "val": "₹ 48,500",
          "sign": "−",
          "at": 275.29
        }
      ],
      "net_total": {
        "label": "Net Taxable Total Income",
        "val": "₹ 3,26,500",
        "at": 277.99
      },
      "callout": {
        "badge": "Inter-Head Set-off Master Stroke",
        "text": "Under Section 71(1), loss under 'Income from house property' up to ₹ 2,00,000 can be set off against any other head of income, including Long-Term Capital Gains!",
        "at": 243.35
      },
      "start": 242.15,
      "end": 282.55
    },
    {
      "id": "b7",
      "layout": "takeaway",
      "kicker": "EXAM MASTER PRINCIPLES",
      "badge": "3 Golden Rules",
      "title": {
        "text": "Core Statutory Takeaways for Section 50C, 54 & 54EC",
        "at": 283.2
      },
      "voice_sync_text": "Eethoru complex problem-il ninnu CA exam-il orkkenda moorthu golden rules: First, Section 50C-il Stamp Duty Value actual consideration-te 110 percent-inekaal kooduthalaayal SDV deemed full value aakum. Second, Section 54-il adjacent flats modify cheythu single habitable unit aakkiyaal Ananda Basappa precedent prakaaram exemption valid aanu. Third, Section 54EC-il payment date within 6 months aayal Hindustan Unilever precedent prakaaram bond allotment late aanaalum exemption claim cheyyaam. Brilliant work students!",
      "rules": [
        {
          "title": "Section 50C 110% Safe Harbor Benchmark",
          "text": "If Stamp Duty Value exceeds 110% of Actual Consideration, SDV becomes Deemed Full Value. Always compute 110% before applying Section 50C.",
          "at": 289.74
        },
        {
          "title": "Section 54 Adjacent Flats Unit Doctrine (CIT v. Ananda Basappa)",
          "text": "Two adjacent flats modified into a single residential unit qualify as 'a residential house' even if acquired under separate sale deeds.",
          "at": 300.76
        },
        {
          "title": "Section 54EC Payment Date Landmark (Hindustan Unilever Ltd.)",
          "text": "Payment made within 6 months of transfer satisfies Section 54EC timeline. Subsequent delay in bond allotment does not jeopardize exemption.",
          "at": 310.68
        }
      ],
      "start": 282.9,
      "end": 322.42
    }
  ],
  "duration_sec": 322.77,
  "audio_url": "data/audio/dt-c2-q30.mp3"
};
FIXTURES["dt_c2_q30"] = FIXTURES["dt-c2-q30"];
FIXTURES["ch2_q30"] = FIXTURES["dt-c2-q30"];
if (typeof window !== "undefined") {
  window.EXPLAINER_SCREENPLAYS = window.EXPLAINER_SCREENPLAYS || {};
  window.EXPLAINER_SCREENPLAYS["dt-c2-q30"] = FIXTURES["dt-c2-q30"];
  window.EXPLAINER_SCREENPLAYS["dt_c2_q30"] = FIXTURES["dt-c2-q30"];
  window.EXPLAINER_SCREENPLAYS["ch2_q30"] = FIXTURES["dt-c2-q30"];
}

function bezier(mX1, mY1, mX2, mY2) {
  function A(aA1, aA2) { return 1.0 - 3.0 * aA2 + 3.0 * aA1; }
  function B(aA1, aA2) { return 3.0 * aA2 - 6.0 * aA1; }
  function C(aA1)      { return 3.0 * aA1; }
  function calcBezier(aT, aA1, aA2) { return ((A(aA1, aA2)*aT + B(aA1, aA2))*aT + C(aA1))*aT; }
  function getSlope(aT, aA1, aA2) { return 3.0*A(aA1, aA2)*aT*aT + 2.0*B(aA1, aA2)*aT + C(aA1); }
  return function(x) {
    if (x <= 0) return 0;
    if (x >= 1) return 1;
    let t = x;
    for (let i = 0; i < 8; ++i) {
      const currentSlope = getSlope(t, mX1, mX2);
      if (currentSlope === 0.0) break;
      const currentX = calcBezier(t, mX1, mX2) - x;
      t -= currentX / currentSlope;
    }
    return calcBezier(t, mY1, mY2);
  };
}

const ease = bezier(0.22, 1, 0.36, 1);
const prog = (t, s, d) => ease(Math.min(1, Math.max(0, (t - s) / Math.max(0.001, d))));
const progLinear = (t, s, d) => Math.min(1, Math.max(0, (t - s) / Math.max(0.001, d)));

const EASE = {
  linear: p => p,
  out:    p => 1 - Math.pow(1 - p, 3),
  back:   p => 1 + 2.7 * Math.pow(p - 1, 3) + 1.7 * Math.pow(p - 1, 2),
  spring: p => (p >= 1 ? 1 : 1 - Math.exp(-6 * p) * Math.cos(14 * p)),
};
if (typeof PRESETS !== "undefined" && PRESETS.EASE_EXTRA) {
  Object.assign(EASE, PRESETS.EASE_EXTRA);
}
const inr  = n => "₹ " + Math.round(n).toLocaleString("en-IN");
const EXIT = 0.4;

const NS = "http://www.w3.org/2000/svg";
const TONE = { accent: "#4F46E5", ok: "#059669", warn: "#DC2626", bad: "#DC2626", good: "#059669" };

const isReducedMotion = () => {
  try {
    return window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  } catch(e) {
    return false;
  }
};

const h = (cls, parent, html) => {
  const d = document.createElement("div");
  d.className = cls;
  if (html) d.innerHTML = html;
  parent.appendChild(d);
  return d;
};

const sv = (name, attrs, parent) => {
  const e = document.createElementNS(NS, name);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  parent.appendChild(e);
  return e;
};

const fade = (ctx, el, at, dy = 12, dur = 0.55, outAt = null, outDur = 0.4) => ctx.push({ el, kind: "fade", start: at, dur, dy, out: outAt, outDur });

function words(ctx, parent, text, at, step = 0.05) {
  let n = 0;
  text.split(/(\[\[.*?\]\])/).filter(Boolean).forEach(part => {
    const marked = /^\[\[.*\]\]$/.test(part), raw = marked ? part.slice(2, -2) : part;
    let holder = parent;
    if (marked) {
      holder = document.createElement("span");
      holder.className = "mk";
      parent.appendChild(holder);
    }
    raw.split(/(\s+)/).filter(Boolean).forEach(tok => {
      if (/^\s+$/.test(tok)) {
        holder.appendChild(document.createTextNode(" "));
        return;
      }
      const s = document.createElement("span");
      s.className = "w";
      s.textContent = tok;
      holder.appendChild(s);
      ctx.push({ el: s, kind: "word", start: at + n++ * step, dur: 0.45 });
    });
    if (marked) {
      ctx.push({ el: holder, kind: "mark", start: at + (n - 1) * step + 0.1, dur: 0.3 });
    }
  });
}

const TEMPLATES = {
  headline(el, b, ctx) {
    words(ctx, h("headline", el), b.title.text, b.title.at);
    if (b.subtitle) words(ctx, h("sub", el), b.subtitle.text, b.subtitle.at);
  },
  takeaway(el, b, ctx) {
    if (b.title) words(ctx, h("headline", el), b.title.text || b.title, b.title.at || (b.start + 0.3));
    if (b.subtitle) words(ctx, h("sub", el), b.subtitle.text || b.subtitle, b.subtitle.at || (b.start + 0.8));
    const pointsList = b.points || (b.rules || []).map((r, i) => ({
      num: r.num || (r.step || (i + 1)),
      text: r.text || r.rule || (r.heading ? `<strong>${r.heading}</strong>: ${r.body || ''}` : r),
      at: r.at || (b.start + 0.8 + i * 0.5)
    }));

    if (pointsList.length > 0) {
      const wrap = h("takeaway-list", el);
      pointsList.forEach((pt, idx) => {
        const item = h("takeaway-item", wrap);
        item.innerHTML = `
          <div class="takeaway-num">${pt.num || (idx + 1)}</div>
          <div class="takeaway-text">${pt.text}</div>
        `;
        fade(ctx, item, pt.at || (b.start + 0.8 + idx * 0.5), 10, 0.4);
      });
    }
  },

  timeline(el, b, ctx) {
    const svg = sv("svg", { viewBox: "0 0 960 340", width: "100%", height: "100%" }, el);
    const axis = sv("path", { d: "M 150 170 L 810 170", stroke: "#D1D5DB", "stroke-width": 4, fill: "none", "stroke-linecap": "round", pathLength: 1 }, svg);
    ctx.push({ el: axis, kind: "draw", start: b.axis_at || (b.start + 0.2), dur: 1.0 });

    if (b.arrow_at) {
      const arrow = sv("path", { d: "M 210 170 L 740 170", stroke: TONE.accent, "stroke-width": 5, fill: "none", "stroke-linecap": "round", pathLength: 1 }, svg);
      const head  = sv("path", { d: "M 722 150 L 752 170 L 722 190", stroke: TONE.accent, "stroke-width": 5, fill: "none", "stroke-linecap": "round", "stroke-linejoin": "round", pathLength: 1 }, svg);
      ctx.push({ el: arrow, kind: "draw", start: b.arrow_at, dur: 1.4 });
      ctx.push({ el: head,  kind: "draw", start: b.arrow_at + 1.2, dur: 0.4 });
    }

    if (b.spans && Array.isArray(b.spans)) {
      b.spans.forEach(spn => {
        const x1 = 150 + (spn.from_x !== undefined ? spn.from_x : 0.1) * 660;
        const x2 = 150 + (spn.to_x !== undefined ? spn.to_x : 0.9) * 660;
        const g = sv("g", { class: "fade" }, svg);
        sv("rect", { x: Math.min(x1, x2), y: 130, width: Math.abs(x2 - x1), height: 80, rx: 8, fill: "rgba(79, 70, 229, 0.08)", stroke: TONE[spn.tone] || TONE.accent, "stroke-width": 1.5, "stroke-dasharray": "4 4" }, g);
        const t = sv("text", { x: (x1 + x2) / 2, y: 175, "text-anchor": "middle", "font-size": 18, "font-weight": 600, fill: TONE[spn.tone] || TONE.accent }, g);
        t.textContent = spn.text;
        fade(ctx, g, spn.at);
      });
    }

    if (b.nodes && Array.isArray(b.nodes)) {
      b.nodes.forEach(n => {
        const x = (n.x !== undefined) ? (150 + n.x * 660) : (n.side === "left" ? 180 : 780);
        const c = TONE[n.tone] || TONE.accent;
        const dot = sv("circle", { cx: x, cy: 170, r: 14, fill: "#fff", stroke: c, "stroke-width": 5, class: "fade" }, svg);
        fade(ctx, dot, n.at, 0, 0.5);
        [[n.title, 100, 30, 800, "#111827", 0.2], [n.sub, 130, 22, 500, "#6B7280", 0.4]].forEach(([txt, y, size, w, fill, d]) => {
          if (!txt) return;
          const t = sv("text", { x, y, "text-anchor": "middle", "font-size": size, "font-weight": w, fill, class: "fade" }, svg);
          t.textContent = txt;
          fade(ctx, t, n.at + d);
        });
        if (n.chips && Array.isArray(n.chips)) {
          n.chips.forEach((chip, i) => {
            const w = 40 + chip.text.length * 12, g = sv("g", { class: "fade" }, svg);
            sv("rect", { x: x - w / 2, y: 210 + i * 60, width: w, height: 46, rx: 23, fill: chip.emphasis ? "#FEF08A" : "#fff", stroke: c, "stroke-width": 1.5 }, g);
            const t = sv("text", { x, y: 240 + i * 60, "text-anchor": "middle", "font-size": 22, "font-weight": 700, fill: c }, g);
            t.textContent = chip.text;
            fade(ctx, g, chip.at);
          });
        }
      });
    }
  },

  scene(el, b, ctx) {
    const POS = {
      "top-left": ["6%", "10%"],
      "top-right": ["62%", "10%"],
      "mid-right": ["62%", "34%"],
      "bottom-left": ["6%", "70%"],
      "bottom-right": ["62%", "70%"]
    };
    const scene = h("scene", el);
    fade(ctx, scene, b.start + 0.1, 16, 0.7);
    const img = document.createElement("img");
    img.className = "art";
    const src = (b.image_url && !b.image_url.startsWith("http") && !b.image_url.startsWith("../") && !b.image_url.startsWith("/")) ? ("../" + b.image_url) : (b.image_url || "");
    img.src = src;
    img.alt = "";
    img.style.cssText = "width:100%;height:100%;display:block;object-fit:cover;transform-origin:50% 60%";
    scene.appendChild(img);
    const zFrom = (b.zoom && b.zoom[0]) ? b.zoom[0] : 1.0;
    const zTo = (b.zoom && b.zoom[1]) ? b.zoom[1] : 1.03;
    ctx.push({ el: img, kind: "zoom", start: b.start, dur: b.end - b.start, from: zFrom, to: zTo });
    if (b.tags && Array.isArray(b.tags)) {
      b.tags.forEach(t => {
        const tag = h("tag " + (t.tone === "ok" ? "ok" : ""), scene, "<small></small><b class='num'>₹ 0</b>");
        [tag.style.left, tag.style.top] = POS[t.pos] || POS["top-left"];
        tag.firstChild.textContent = t.label;
        fade(ctx, tag, t.at, 12, 0.5);
        ctx.push({ el: tag.lastChild, kind: "count", start: t.at, dur: 2.0, target: t.value, fmt: t.fmt || "inr" });
      });
    }
  },

  split(el, b, ctx) {
    if (b.title) words(ctx, h("h2", el), b.title.text, b.title.at);
    const row = h("row", el);
    b.cards.forEach(c => {
      const card = h("card " + (c.tone === "ok" ? "b" : "a"), row, "<div class='k'></div><div class='t'></div><div class='v num'>₹ 0</div><div class='e'></div>");
      card.querySelector(".k").textContent = c.kicker || "";
      card.querySelector(".t").textContent = c.title || "";
      card.querySelector(".e").textContent = c.note || "";
      fade(ctx, card, c.at, 16, 0.6);
      ctx.push({ el: card.querySelector(".v"), kind: "count", start: c.at + 0.2, dur: 2.0, target: c.value, fmt: c.fmt || "inr" });
    });
  },

  trap(el, b, ctx) {
    if (b.title) words(ctx, h("h2", el), b.title.text, b.title.at);
    const row = h("row", el);
    b.cards.forEach(c => {
      const card = h("card " + c.tone, row, `<div class='icon'>${c.tone === "bad" ? "✕" : "✓"}</div><div class='k'></div><div class='t small'></div>`);
      card.querySelector(".k").textContent = c.kicker || "";
      card.querySelector(".t").textContent = c.text || "";
      fade(ctx, card, c.at, 16, 0.6);
    });
  },

  fork(el, b, ctx) {
    if (b.title) words(ctx, h("h2", el), b.title.text, b.title.at);
    const forkWrap = h("fork-wrap", el);

    if (b.intro_cards && Array.isArray(b.intro_cards)) {
      const introRow = h("story-steps-row intro-steps-row", forkWrap);
      introRow.style.cssText = "display:flex;gap:1.2cqw;width:90%;margin-bottom:0.8cqw;justify-content:center;transition:all 0.3s ease;";
      b.intro_cards.forEach(ic => {
        const icCard = h("story-step-card intro-scenario-card " + (ic.tone || "info"), introRow);
        icCard.style.cssText = "flex:1;max-width:320px;background:#FFFFFF;border:1.5px solid #E2E8F0;border-radius:12px;padding:0.8cqw 1.2cqw;box-shadow:0 4px 10px rgba(15,23,42,0.04);display:flex;flex-direction:column;gap:0.3cqw;border-top:3.5px solid #4F46E5;";
        icCard.innerHTML = `
          <div class="step-badge" style="background:#EEF2FF;color:#4F46E5;font-size:0.8cqw;font-weight:800;text-transform:uppercase;padding:0.2cqw 0.6cqw;border-radius:6px;width:fit-content;">${ic.badge || "Fact"}</div>
          <div class="step-title" style="font-size:1.15cqw;font-weight:800;color:#0F172A;">${ic.title}</div>
          <div class="step-sub" style="font-size:0.9cqw;color:#64748B;line-height:1.35;">${ic.sub || ""}</div>
          ${ic.val ? `<div class="step-val num">${inr(ic.val)}</div>` : ""}
        `;
        fade(ctx, icCard, ic.at, 10, 0.4, ic.out_at);
      });
      if (b.intro_cards.some(ic => ic.out_at)) {
        const maxOut = Math.max(...b.intro_cards.map(ic => ic.out_at || 0));
        if (maxOut > 0) {
          fade(ctx, introRow, b.intro_cards[0].at, 0, 0.4, maxOut, 0.4);
        }
      }
    }

    if (b.story_steps && Array.isArray(b.story_steps)) {
      const stepsRow = h("story-steps-row", forkWrap);
      b.story_steps.forEach(st => {
        const stCard = h("story-step-card", stepsRow);
        stCard.innerHTML = `
          <div class="step-badge">${st.badge}</div>
          <div class="step-title">${st.title}</div>
          <div class="step-sub">${st.sub}</div>
          ${st.val ? `<div class="step-val num">${inr(st.val)}</div>` : ""}
        `;
        fade(ctx, stCard, st.at, 10, 0.4);
      });
    }

    if (b.divider) {
      const divBox = h("fork-divider", forkWrap);
      divBox.textContent = b.divider.text || b.divider || "";
      fade(ctx, divBox, b.divider.at || (b.start + 1.0), 0, 0.4);
    }

    const branchesRow = h("fork-branches", forkWrap);
    (b.branches || []).forEach(br => {
      const col = h("fork-branch " + br.side, branchesRow);
      const branchAt = br.at !== undefined ? br.at : ((b.divider && b.divider.at) ? b.divider.at + 0.1 : (b.start + 1.2));
      fade(ctx, col, branchAt, 8, 0.4);

      const lbl = h("branch-label", col);
      lbl.textContent = br.label;

      (br.facts || []).forEach(f => {
        const factBox = h("branch-fact", col);
        factBox.textContent = f.text;
        const dx = br.side === "left" ? -20 : 20;
        ctx.push({ el: factBox, kind: "slide", start: f.at, dur: 0.5, dx, dy: 0 });
      });

      if (br.outcome) {
        const outBox = h("branch-outcome", col);
        outBox.textContent = br.outcome.text;
        fade(ctx, outBox, br.outcome.at, 10, 0.5);
      }

      if (b.active && b.active.side === br.side) {
        ctx.push({ el: col, kind: "glow", start: b.active.at, dur: 0.6 });
      }
    });

    if (b.example) {
      const exBox = h("beat-example-card", forkWrap);
      exBox.innerHTML = `
        <div class="ex-character">
          <div class="ex-avatar">
            <svg viewBox="0 0 100 100" width="100%" height="100%">
              <circle cx="50" cy="40" r="28" fill="#F3F4F6" stroke="#111827" stroke-width="3"/>
              <path d="M 20 95 C 20 72 34 68 50 68 C 66 68 80 72 80 95 Z" fill="#4F46E5" opacity="0.9"/>
              <circle cx="41" cy="38" r="3.5" fill="#111827"/>
              <circle cx="59" cy="38" r="3.5" fill="#111827"/>
              <path d="M 36 30 Q 42 26 46 32" stroke="#111827" stroke-width="2.5" fill="none"/>
              <path d="M 54 32 Q 58 34 64 31" stroke="#111827" stroke-width="2.5" fill="none"/>
              <path d="M 43 52 Q 47 48 51 52 T 58 50" stroke="#111827" stroke-width="2.5" fill="none"/>
              <circle cx="76" cy="22" r="11" fill="#F59E0B"/>
              <text x="76" y="26" font-family="system-ui" font-weight="900" font-size="12" fill="#fff" text-anchor="middle">₹</text>
            </svg>
          </div>
          <div>
            <div class="ex-name">${b.example.name || "Mr. Hari"}</div>
            <div class="ex-role">${b.example.role || "Practical Case"}</div>
          </div>
        </div>
        <div class="ex-bubble">${b.example.text}</div>
      `;
      fade(ctx, exBox, b.example.at || (b.title ? b.title.at + 0.5 : b.start), 12, 0.5);
    }
  },

  meter(el, b, ctx) {
    if (b.title) words(ctx, h("h2", el), b.title.text || b.title, b.title.at || (b.start + 0.3));
    const meterWrap = h("meter-wrap", el);

    // Support both b.meter_display and b.limit / b.reading
    const md = b.meter_display || {};
    const limitVal = b.limit ? b.limit.value : (md.threshold || md.max_val || 2500000);
    const limitText = b.limit ? b.limit.text : (md.labels?.threshold_label || "Statutory Ceiling / Threshold");
    const readingValNum = b.reading ? b.reading.value : (md.current_val || 0);
    const readingText = b.reading ? b.reading.text : (md.labels?.current_label || "Eligible Reinvestment");
    const limitAt = b.limit?.at || (md.at || (b.start + 0.8));
    const readingAt = b.reading?.at || (md.at ? md.at + 0.5 : (b.start + 1.4));

    const gaugeBox = h("meter-gauge", meterWrap);
    const track = h("meter-track", gaugeBox);
    const bar = h("meter-bar", track);

    const limitLine = h("meter-limit-line", track);
    const limitLbl = h("meter-limit-label", gaugeBox);
    limitLbl.textContent = limitText + ": " + inr(limitVal);
    fade(ctx, limitLine, limitAt, 0, 0.3);
    fade(ctx, limitLbl, limitAt, 0, 0.3);

    const ratio = Math.min(1.0, Math.max(0.05, readingValNum / Math.max(1, limitVal)));
    ctx.push({ el: bar, kind: "fill", start: readingAt, dur: 1.8, to: ratio });

    const readingBox = h("meter-reading", meterWrap);
    const readingLbl = h("reading-label", readingBox);
    readingLbl.textContent = readingText;
    const readingVal = h("reading-val num", readingBox);
    fade(ctx, readingBox, readingAt, 12, 0.5);
    ctx.push({ el: readingVal, kind: "count", start: readingAt, dur: 1.8, target: readingValNum, fmt: b.reading?.fmt || "inr" });

    if (b.outcome) {
      const outPill = h("meter-outcome " + (b.outcome.tone || "ok"), meterWrap);
      outPill.textContent = b.outcome.text || b.outcome;
      fade(ctx, outPill, b.outcome.at || (readingAt + 1.0), 14, 0.6);
    }

    if (b.padlock) {
      const padBox = h("meter-padlock-box", meterWrap);
      padBox.innerHTML = `
        <div class="padlock-icon unlocked">
          <svg viewBox="0 0 100 100" width="36" height="36">
            <g class="shackle" style="transform-origin: 30px 48px; transform: rotate(-28deg);">
              <path d="M 30 48 V 30 C 30 18 70 18 70 30 V 48" stroke="#059669" stroke-width="7" stroke-linecap="round" fill="none"/>
            </g>
            <rect x="22" y="44" width="56" height="46" rx="10" fill="#10B981" stroke="#065F46" stroke-width="2"/>
            <circle cx="50" cy="62" r="5" fill="#fff"/>
            <path d="M 48 64 L 46 76 L 54 76 L 52 64 Z" fill="#fff"/>
          </svg>
        </div>
        <div class="padlock-label">${b.padlock.text || "Threshold Condition Fulfilled!"}</div>
      `;
      fade(ctx, padBox, b.padlock.at || (b.outcome ? b.outcome.at : readingAt + 1.0), 10, 0.5);
    }

    if (b.breakdown && Array.isArray(b.breakdown)) {
      const bdGrid = h("meter-breakdown-grid", meterWrap);
      bdGrid.style.cssText = "display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;margin-top:14px;width:100%;";
      b.breakdown.forEach((it, idx) => {
        const isOk = !it.status?.toLowerCase().includes("ineligible") && !it.status?.toLowerCase().includes("exclude");
        const card = h("meter-bd-card", bdGrid);
        card.style.cssText = `background:var(--matte);border:1px solid ${isOk ? 'var(--ok)' : 'var(--warn)'};border-radius:10px;padding:8px 12px;display:flex;justify-content:space-between;align-items:center;`;
        card.innerHTML = `
          <div>
            <div style="font-size:0.85rem;font-weight:600;color:var(--ink)">${it.label}</div>
            <div style="font-size:0.75rem;color:${isOk ? 'var(--ok)' : 'var(--warn)'};font-weight:700">${it.status || ''}</div>
          </div>
          <div class="num" style="font-size:0.95rem;font-weight:800;color:var(--ink)">${inr(it.val || 0)}</div>
        `;
        fade(ctx, card, (it.at !== undefined ? it.at : (b.start + 1.0 + idx * 0.4)), 8, 0.4);
      });
    }

    if (b.example) {
      const exBox = h("beat-example-card", meterWrap);
      exBox.innerHTML = `
        <div class="ex-character">
          <div class="ex-avatar">
            <svg viewBox="0 0 100 100" width="100%" height="100%">
              <circle cx="50" cy="40" r="28" fill="#F3F4F6" stroke="#111827" stroke-width="3"/>
              <path d="M 20 95 C 20 72 34 68 50 68 C 66 68 80 72 80 95 Z" fill="#4F46E5" opacity="0.9"/>
              <circle cx="41" cy="38" r="3.5" fill="#111827"/>
              <circle cx="59" cy="38" r="3.5" fill="#111827"/>
              <path d="M 42 49 Q 50 58 58 49" stroke="#059669" stroke-width="3" stroke-linecap="round" fill="none"/>
              <circle cx="76" cy="22" r="11" fill="#059669"/>
              <path d="M 71 22 L 74 25 L 81 18" stroke="#fff" stroke-width="2" fill="none"/>
            </svg>
          </div>
          <div>
            <div class="ex-name">${b.example.name || "Assessee"}</div>
            <div class="ex-role">${b.example.role || "Threshold Qualified"}</div>
          </div>
        </div>
        <div class="ex-bubble">${b.example.text || b.example}</div>
      `;
      fade(ctx, exBox, b.example.at || (b.outcome ? b.outcome.at + 0.3 : readingAt + 1.5), 12, 0.5);
    }
  },

  ledger(el, b, ctx) {
    if (b.title) words(ctx, h("h2", el), b.title.text || b.title, b.title.at || (b.start + 0.3));
    const ledgerTable = h("ledger-table", el);

    const parseVal = v => {
      if (typeof v === "number") return v;
      if (!v) return 0;
      const str = String(v).replace(/,/g, "").replace(/₹/g, "").trim();
      const n = parseFloat(str);
      return isNaN(n) ? 0 : n;
    };

    // Support both b.rows and b.ledger_rows
    const rowsList = b.rows || (b.ledger_rows || []).map((r, i) => {
      const s = r.sign || (r.type === "deduction" ? "minus" : "plus");
      const normSign = (s === "-" || s === "−" || s === "minus") ? "minus" : ((s === "=" || s === "total") ? "total" : "plus");
      return {
        sign: normSign,
        label: r.label || r.particulars || r.text,
        value: parseVal(r.value !== undefined ? r.value : (r.val !== undefined ? r.val : (r.amount || 0))),
        at: r.at || (b.start + 0.6 + i * 0.4),
        fmt: r.fmt || "inr"
      };
    });

    rowsList.forEach((r, idx) => {
      const row = h("ledger-row " + (r.sign || "plus"), ledgerTable);
      const signCol = h("ledger-sign", row);
      signCol.textContent = r.sign === "minus" ? "−" : (r.sign === "total" ? "=" : "+");
      const lblCol = h("ledger-lbl", row);
      lblCol.textContent = r.label;
      const valCol = h("ledger-val num", row);
      valCol.textContent = inr(0);

      const rAt = r.at || (b.start + 0.6 + idx * 0.4);
      ctx.push({ el: row, kind: "slide", start: rAt, dur: 0.5, dx: -15, dy: 0 });
      ctx.push({ el: valCol, kind: "count", start: rAt + 0.1, dur: 1.2, target: r.value, fmt: r.fmt || "inr" });
    });

    const totObj = b.total || b.net_total;
    if (totObj) {
      const totValNum = parseVal(totObj.value !== undefined ? totObj.value : (totObj.val !== undefined ? totObj.val : (totObj.amount !== undefined ? totObj.amount : (totObj.taxable_amount || 0))));
      const totLblText = totObj.label || totObj.particulars || "Taxable Capital Gain";
      const totAt = totObj.at || (b.start + 0.6 + rowsList.length * 0.4 + 0.5);

      const rule = h("ledger-rule", ledgerTable);
      ctx.push({ el: rule, kind: "strike", start: totAt - 0.2, dur: 0.4 });

      const totRow = h("ledger-row total-row", ledgerTable);
      const totSign = h("ledger-sign", totRow);
      totSign.textContent = "=";
      const totLbl = h("ledger-lbl", totRow);
      totLbl.textContent = totLblText;
      const totVal = h("ledger-val num", totRow);

      ctx.push({ el: totRow, kind: "slide", start: totAt, dur: 0.6, dx: 0, dy: 10 });
      ctx.push({ el: totVal, kind: "count", start: totAt + 0.1, dur: 1.5, target: totValNum, fmt: totObj.fmt || "inr" });
    }

    if (b.callout) {
      const calloutBox = h("ledger-callout-box", el);
      calloutBox.innerHTML = `
        <div class="callout-pill">${b.callout.badge || "Tax Alert"}</div>
        <div class="callout-text">${b.callout.text || b.callout}</div>
      `;
      fade(ctx, calloutBox, b.callout.at || (b.start + 2.5), 12, 0.5);
    }
  },

  case_card(el, b, ctx) {
    if (b.title) words(ctx, h("h2", el), b.title.text, b.title.at);
    const card = h("case-card-wrap", el);

    const hdr = h("case-header", card);
    const cName = h("case-name", hdr);
    cName.textContent = b.case.text;
    fade(ctx, cName, b.case.at, 10, 0.4);

    if (b.court) {
      const courtBadge = h("case-court", hdr);
      courtBadge.textContent = b.court.text;
      fade(ctx, courtBadge, b.court.at, 0, 0.4);
    }

    if (b.gap) {
      const gapBox = h("case-gap", card);
      const gapKicker = h("case-kicker", gapBox);
      gapKicker.textContent = "Statutory Ambiguity";
      const gapText = h("case-body", gapBox);
      gapText.textContent = b.gap.text;
      fade(ctx, gapBox, b.gap.at, 12, 0.5);
    }

    if (b.principle) {
      const prinBox = h("case-principle", card);
      const prinKicker = h("case-kicker", prinBox);
      prinKicker.textContent = "Judicial Ruling";
      const prinText = h("case-body principle-text", prinBox);
      words(ctx, prinText, b.principle.text, b.principle.at);
      fade(ctx, prinBox, b.principle.at, 12, 0.5);
    }

    if (b.effect) {
      const effBox = h("case-effect", card);
      const effKicker = h("case-kicker", effBox);
      effKicker.textContent = "Statutory Effect";
      const effText = h("case-body", effBox);
      effText.textContent = b.effect.text;
      fade(ctx, effBox, b.effect.at, 10, 0.5);
    }

    if (b.houses && Array.isArray(b.houses)) {
      const housesGrid = h("case-houses-grid", card);
      b.houses.forEach(hItem => {
        const hCard = h("case-house-card " + (hItem.isTotal ? "total" : ""), housesGrid);
        hCard.innerHTML = `
          <div class="house-loc">${hItem.location}</div>
          <div class="house-status">${hItem.status}</div>
          <div class="house-val num">${inr(hItem.cost)}</div>
        `;
        fade(ctx, hCard, hItem.at, 8, 0.4);
      });
    }
  },

  compare(el, b, ctx) {
    if (b.title) words(ctx, h("h2", el), b.title.text, b.title.at);
    const cmpWrap = h("compare-wrap", el);
    (b.columns || []).forEach((colData, ci) => {
      const col = h("compare-col", cmpWrap);
      const colTitle = h("compare-col-title", col);
      colTitle.textContent = colData.title;
      ctx.push({ el: col, kind: "slide", start: colData.at, dur: 0.5, dx: ci === 0 ? -15 : 15, dy: 0 });

      (colData.rows || []).forEach(r => {
        const row = h("compare-row", col);
        const rLbl = h("compare-row-lbl", row);
        rLbl.textContent = r.label;
        const rVal = h("compare-row-val", row);
        rVal.textContent = r.text;
        fade(ctx, row, r.at, 8, 0.4);
      });
    });

    if (b.highlight && Array.isArray(b.highlight)) {
      b.highlight.forEach(hl => {
        const rows = cmpWrap.querySelectorAll(`.compare-row:nth-child(${hl.row + 1})`);
        rows.forEach(r => {
          ctx.push({ el: r, kind: "glow", start: hl.at, dur: 0.5 });
        });
      });
    }
  },

  checklist(el, b, ctx) {
    if (b.title) words(ctx, h("h2", el), b.title.text, b.title.at);
    const listWrap = h("checklist-wrap", el);

    (b.items || []).forEach(it => {
      const row = h("checklist-row " + (it.result === "pass" ? "pass" : "fail"), listWrap);
      const ico = h("checklist-icon", row);
      ico.textContent = it.result === "pass" ? "✓" : "✕";
      const txt = h("checklist-text", row);
      txt.textContent = it.text;
      ctx.push({ el: row, kind: "slide", start: it.at, dur: 0.5, dx: -12, dy: 0 });
    });
  },

  statute_quote(el, b, ctx) {
    if (b.title) words(ctx, h("h2", el), b.title.text || b.title, b.title.at || (b.start + 0.3));
    const quoteWrap = h("statute-quote-wrap", el);

    if (b.sale_card) {
      const sc = h("quote-sale-card", quoteWrap);
      sc.innerHTML = `
        <div class="sale-card-grid">
          <div class="sale-item">
            <div class="sale-lbl">${b.sale_card.sale_lbl || "Full Consideration (June 2025)"}</div>
            <div class="sale-val num">${inr(b.sale_card.sale_val || 0)}</div>
          </div>
          <div class="sale-sign">−</div>
          <div class="sale-item">
            <div class="sale-lbl">${b.sale_card.cost_lbl || "Adjusted Cost u/s 51"}</div>
            <div class="sale-val num">${inr(b.sale_card.cost_val || 0)}</div>
          </div>
          <div class="sale-sign">=</div>
          <div class="sale-item gain">
            <div class="sale-lbl">${b.sale_card.gain_lbl || "Gross LTCG"}</div>
            <div class="sale-val num">${inr(b.sale_card.gain_val || 0)}</div>
          </div>
        </div>
      `;
      fade(ctx, sc, b.sale_card.at || (b.start + 0.5), 10, 0.4);
    }

    if (b.context_bubble) {
      const cbBox = h("beat-example-card", quoteWrap);
      cbBox.innerHTML = `
        <div class="ex-character">
          <div class="ex-avatar" style="font-size:1.8rem;line-height:1;display:flex;align-items:center;justify-content:center;">§</div>
          <div>
            <div class="ex-name">${b.context_bubble.speaker || "Statutory Intent"}</div>
            <div class="ex-role">${b.context_bubble.theme || "Core Provision"}</div>
          </div>
        </div>
        <div class="ex-bubble">${b.context_bubble.text || b.context_bubble}</div>
      `;
      fade(ctx, cbBox, b.context_bubble.at || (b.start + 0.6), 12, 0.5);
    }

    if (b.example) {
      const exBox = h("beat-example-card", quoteWrap);
      exBox.innerHTML = `
        <div class="ex-character">
          <div class="ex-avatar">
            <svg viewBox="0 0 100 100" width="100%" height="100%">
              <circle cx="50" cy="40" r="28" fill="#F3F4F6" stroke="#111827" stroke-width="3"/>
              <path d="M 20 95 C 20 72 34 68 50 68 C 66 68 80 72 80 95 Z" fill="#4F46E5" opacity="0.9"/>
              <circle cx="41" cy="38" r="3.5" fill="#111827"/>
              <circle cx="59" cy="38" r="3.5" fill="#111827"/>
              <circle cx="76" cy="22" r="11" fill="#F59E0B"/>
              <text x="76" y="26" font-family="system-ui" font-weight="900" font-size="12" fill="#fff" text-anchor="middle">?</text>
            </svg>
          </div>
          <div>
            <div class="ex-name">${b.example.name || "Assessee Question"}</div>
            <div class="ex-role">${b.example.role || "Practical Issue"}</div>
          </div>
        </div>
        <div class="ex-bubble">${b.example.text || b.example}</div>
      `;
      fade(ctx, exBox, b.example.at || (b.start + 0.8), 12, 0.5);
    }

    if (b.quote) {
      const quoteBox = h("statute-quote-box", quoteWrap);
      const qText = typeof b.quote === "string" ? b.quote : (b.quote.text || "");
      const qAt = (b.quote && b.quote.at) ? b.quote.at : (b.start + 1.0);
      fade(ctx, quoteBox, qAt, 10, 0.4);
      words(ctx, quoteBox, qText, qAt, 0.04);
      if (b.quote.citation) {
        const cit = h("quote-citation", quoteBox);
        cit.style.cssText = "font-size:0.85rem;color:var(--ink-soft);margin-top:8px;font-style:italic;display:block;";
        cit.textContent = "— " + b.quote.citation;
      }
    }
  },

  hub_branches(el, b, ctx) {
    if (b.title) words(ctx, h("h2", el), b.title.text, b.title.at);
    const wrap = h("hub-branches-wrap", el);
    const stage = h("hub-branches-stage", wrap);

    const style = b.style || "fade.glow.calm";
    const hero = h("hero", stage);
    const avatarImg = h("hero-avatar", hero);
    avatarImg.innerHTML = `<svg viewBox="0 0 100 100" width="100%" height="100%">
      <circle cx="50" cy="40" r="28" fill="var(--matte, #F3F4F6)" stroke="var(--ink, #111827)" stroke-width="3"/>
      <path d="M 20 95 C 20 72 34 68 50 68 C 66 68 80 72 80 95 Z" fill="var(--accent, #4F46E5)" opacity="0.9"/>
      <circle cx="41" cy="38" r="3.5" fill="var(--ink, #111827)"/>
      <circle cx="59" cy="38" r="3.5" fill="var(--ink, #111827)"/>
      <g class="s-a">
        <path d="M 36 30 Q 42 26 46 32" stroke="var(--ink, #111827)" stroke-width="2.5" stroke-linecap="round" fill="none"/>
        <path d="M 54 32 Q 58 34 64 31" stroke="var(--ink, #111827)" stroke-width="2.5" stroke-linecap="round" fill="none"/>
        <path d="M 43 52 Q 47 48 51 52 T 58 50" stroke="var(--ink, #111827)" stroke-width="2.5" stroke-linecap="round" fill="none"/>
        <circle cx="76" cy="22" r="12" fill="var(--warn, #DC2626)" opacity="0.95"/>
        <text x="76" y="27" font-family="system-ui, sans-serif" font-weight="900" font-size="14" fill="#FFFFFF" text-anchor="middle">?</text>
      </g>
      <g class="s-b">
        <path d="M 36 29 Q 42 28 46 30" stroke="var(--ink, #111827)" stroke-width="2.5" stroke-linecap="round" fill="none"/>
        <path d="M 54 30 Q 58 28 64 29" stroke="var(--ink, #111827)" stroke-width="2.5" stroke-linecap="round" fill="none"/>
        <path d="M 42 49 Q 50 58 58 49" stroke="var(--ok, #059669)" stroke-width="3" stroke-linecap="round" fill="none"/>
        <circle cx="76" cy="22" r="12" fill="var(--ok, #059669)" opacity="0.95"/>
        <path d="M 70 22 L 74 26 L 82 17" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
      </g>
    </svg>`;
    const moodA = h("mood s-a", hero);
    moodA.textContent = b.hero.mood_a;
    const moodB = h("mood s-b", hero);
    moodB.textContent = b.hero.mood_b;

    let lock = null;
    if (b.unlock) {
      lock = h("lock", stage);
      const lockIcon = h("lock-icon", lock);
      lockIcon.innerHTML = `<svg viewBox="0 0 100 100" width="100%" height="100%">
        <g class="shackle" style="transform-origin: 30px 48px;">
          <path d="M 30 48 V 30 C 30 18 70 18 70 30 V 48" stroke="var(--ink, #111827)" stroke-width="7" stroke-linecap="round" fill="none"/>
        </g>
        <rect x="22" y="44" width="56" height="46" rx="10" fill="var(--accent, #4F46E5)" stroke="var(--ink, #111827)" stroke-width="3"/>
        <circle cx="50" cy="62" r="5" fill="#FFFFFF"/>
        <path d="M 48 64 L 46 76 L 54 76 L 52 64 Z" fill="#FFFFFF"/>
      </svg>`;
      const lockText = h("lock-text", lock);
      lockText.textContent = b.unlock.text;
    }

    const branchesGrid = h("branches-grid", wrap);
    const branchEls = (b.branches || []).map(br => {
      const card = h("branch-card" + (br.taxable ? " taxable-remainder" : ""), branchesGrid);
      const icon = h("house-icon", card);
      icon.innerHTML = `<svg viewBox="0 0 100 100" width="100%" height="100%">
        <path d="M 16 46 L 50 18 L 84 46" stroke="var(--ink, #111827)" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" fill="${br.taxable ? 'var(--warn)' : 'var(--accent)'}"/>
        <rect x="68" y="22" width="8" height="16" fill="var(--ink-soft)" stroke="var(--ink)" stroke-width="2"/>
        <rect x="24" y="46" width="52" height="44" rx="4" fill="var(--matte)" stroke="var(--ink)" stroke-width="3"/>
        <rect x="42" y="62" width="16" height="28" rx="2" fill="${br.taxable ? 'var(--warn)' : 'var(--accent)'}" opacity="0.85"/>
      </svg>`;
      const lbl = h("house-label", card);
      lbl.textContent = br.label;
      const tag = h("tag num", card);
      tag.textContent = br.tag;
      return card;
    });

    if (typeof PRESETS !== "undefined" && PRESETS.applyEnter) {
      PRESETS.applyEnter(ctx, hero, b.hero.at, style);
    } else {
      fade(ctx, hero, b.hero.at, 10, 0.5);
    }

    ctx.push({ el: hero, kind: "swap", start: b.hero.mood_at });

    if (lock && b.unlock) {
      const shackle = lock.querySelector(".shackle");
      if (shackle) {
        ctx.push({ el: shackle, kind: "tween", start: b.unlock.at, dur: 0.5, ease: "back", to: { y: -1.2, rot: -35 } });
      }
      fade(ctx, lock, b.unlock.at, 8, 0.4);
    }

    (b.branches || []).forEach((br, i) => {
      if (typeof PRESETS !== "undefined" && PRESETS.applyEnter) {
        PRESETS.applyEnter(ctx, branchEls[i], br.at, style);
      } else {
        fade(ctx, branchEls[i], br.at, 12, 0.5);
      }
    });
  },

  story_scene(el, b, ctx) {
    el.style.cssText = "position:absolute;inset:0;width:100%;height:100%;overflow:hidden;display:flex;flex-direction:column;align-items:center;";

    // Header
    const hdr = h("story-scene-hdr", el);
    hdr.style.cssText = "position:absolute;top:2.2cqw;left:0;right:0;display:flex;flex-direction:column;align-items:center;z-index:5;text-align:center;";
    if (b.kicker) {
      const kick = h("kick", hdr);
      kick.style.cssText = "font-size:0.85cqw;font-weight:800;letter-spacing:0.14em;color:var(--accent,#4F46E5);text-transform:uppercase;";
      kick.textContent = b.kicker;
      fade(ctx, kick, (b.title && b.title.at) ? b.title.at - 0.2 : b.start + 0.1, 8, 0.4);
    }
    if (b.title) {
      const tit = h("h1", hdr);
      tit.style.cssText = "font-size:1.8cqw;font-weight:800;color:var(--ink,#111827);margin-top:0.2cqw;letter-spacing:-0.01em;";
      words(ctx, tit, b.title.text || b.title, (b.title && b.title.at) ? b.title.at : b.start + 0.3);
    }
    if (b.badge) {
      const bd = h("chip", hdr);
      bd.style.cssText = "position:absolute;top:0;right:3cqw;background:var(--tint,#E0E7FF);color:var(--accent,#4F46E5);font-size:0.75cqw;font-weight:800;padding:0.3cqw 0.8cqw;border-radius:999px;border:1px solid #C7D2FE;";
      bd.textContent = b.badge;
      fade(ctx, bd, b.start + 0.4, 0, 0.4);
    }

    const svg = sv("svg", { viewBox: "0 0 1000 562", preserveAspectRatio: "xMidYMid meet" }, el);
    svg.style.cssText = "position:absolute;inset:0;width:100%;height:100%;overflow:visible;";

    const S_EL = (tag, attrs, parent) => {
      const e = document.createElementNS(NS, tag);
      for (const k in attrs) e.setAttribute(k, attrs[k]);
      if (parent) parent.appendChild(e);
      return e;
    };
    const G_EL = (parent, attrs) => S_EL("g", attrs || {}, parent);
    const R_EL = (parent, x, y, w, h, fill, o = {}) => {
      const e = S_EL("rect", { x, y, width: w, height: h, rx: o.rx !== undefined ? o.rx : 8, fill, stroke: o.stroke || "none", "stroke-width": o.sw || 0 }, parent);
      if (o.dash) e.setAttribute("stroke-dasharray", o.dash);
      return e;
    };
    const T_EL = (parent, x, y, str, o = {}) => {
      const e = S_EL("text", { x, y, "text-anchor": o.anchor || "start", "font-size": o.size || 18, "font-weight": o.weight || 600, fill: o.fill || "#111827" }, parent);
      e.textContent = str;
      return e;
    };
    const P_EL = (parent, d, stroke, sw = 3, o = {}) => {
      const e = S_EL("path", { d, stroke, "stroke-width": sw, fill: o.fill || "none", "stroke-linecap": "round", "stroke-linejoin": "round", pathLength: 1 }, parent);
      if (o.dash) e.setAttribute("stroke-dasharray", o.dash);
      return e;
    };

    // Shared SVG draw components
    const makeHouse = (parent, x, y, col, label, sub) => {
      const g = G_EL(parent);
      P_EL(g, `M ${x - 45} ${y + 5} L ${x} ${y - 35} L ${x + 45} ${y + 5} Z`, col, 3.5, { fill: "#EEF2FF" });
      R_EL(g, x + 20, y - 30, 10, 18, "#C7D2FE", { stroke: col, sw: 2, rx: 1 });
      R_EL(g, x - 38, y + 5, 76, 65, "#FFFFFF", { stroke: col, sw: 3.5, rx: 4 });
      R_EL(g, x - 12, y + 32, 24, 38, col, { rx: 3 });
      R_EL(g, x - 30, y + 16, 14, 14, "#FEF08A", { stroke: col, sw: 2, rx: 2 });
      R_EL(g, x + 16, y + 16, 14, 14, "#FEF08A", { stroke: col, sw: 2, rx: 2 });
      if (label) T_EL(g, x, y + 92, label, { size: 16, weight: 800, anchor: "middle", fill: "#0F172A" });
      if (sub) T_EL(g, x, y + 112, sub, { size: 13, weight: 600, anchor: "middle", fill: "#64748B" });
      return g;
    };

    const makePerson = (parent, x, y, col, name, role) => {
      const g = G_EL(parent);
      S_EL("circle", { cx: x, cy: y - 20, r: 16, fill: "#FFFFFF", stroke: col, "stroke-width": 3 }, g);
      S_EL("circle", { cx: x - 5, cy: y - 22, r: 2, fill: col }, g);
      S_EL("circle", { cx: x + 5, cy: y - 22, r: 2, fill: col }, g);
      P_EL(g, `M ${x - 5} ${y - 14} Q ${x} ${y - 10} ${x + 5} ${y - 14}`, col, 2);
      P_EL(g, `M ${x - 22} ${y + 35} C ${x - 22} ${y + 2} ${x - 12} ${y - 2} ${x} ${y - 2} C ${x + 12} ${y - 2} ${x + 22} ${y + 2} ${x + 22} ${y + 35} Z`, col, 3, { fill: "#EEF2FF" });
      if (name) T_EL(g, x, y + 54, name, { size: 14, weight: 800, anchor: "middle", fill: "#0F172A" });
      if (role) T_EL(g, x, y + 70, role, { size: 12, weight: 600, anchor: "middle", fill: col });
      return g;
    };

    const makeFactory = (parent, x, y, col, label, sub) => {
      const g = G_EL(parent);
      R_EL(g, x + 24, y - 36, 12, 32, "#94A3B8", { stroke: col, sw: 2, rx: 1 });
      S_EL("circle", { cx: x + 30, cy: y - 44, r: 5, fill: "#CBD5E1" }, g);
      S_EL("circle", { cx: x + 36, cy: y - 52, r: 7, fill: "#E2E8F0" }, g);
      P_EL(g, `M ${x - 45} ${y} L ${x - 20} ${y - 25} L ${x - 20} ${y} L ${x + 8} ${y - 25} L ${x + 8} ${y} L ${x + 36} ${y - 25} L ${x + 36} ${y} Z`, col, 2.5, { fill: "#EEF2FF" });
      R_EL(g, x - 45, y, 90, 65, "#FFFFFF", { stroke: col, sw: 3.5, rx: 4 });
      R_EL(g, x - 15, y + 25, 30, 40, col, { rx: 2 });
      for (let dy = 32; dy <= 58; dy += 7) {
        P_EL(g, `M ${x - 13} ${y + dy} L ${x + 13} ${y + dy}`, "#FFFFFF", 1.5);
      }
      R_EL(g, x - 38, y + 12, 16, 16, "#FEF08A", { stroke: col, sw: 2, rx: 2 });
      R_EL(g, x + 22, y + 12, 16, 16, "#FEF08A", { stroke: col, sw: 2, rx: 2 });
      if (label) T_EL(g, x, y + 88, label, { size: 15, weight: 800, anchor: "middle", fill: "#0F172A" });
      if (sub) T_EL(g, x, y + 106, sub, { size: 12, weight: 600, anchor: "middle", fill: "#64748B" });
      return g;
    };

    const makeGavel = (parent, x, y, courtText, ruleText, w = 390, h = 76) => {
      const g = G_EL(parent);
      const halfW = w / 2;
      const halfH = h / 2;
      R_EL(g, x - halfW, y - halfH, w, h, "#FFFFFF", { stroke: "#4F46E5", sw: 2.5, rx: 12 });
      
      const leftPad = x - halfW + 24;
      const gav = G_EL(g);
      P_EL(gav, `M ${leftPad} ${y - 5} L ${leftPad + 15} ${y - 20} L ${leftPad + 25} ${y - 10} L ${leftPad + 10} ${y + 5} Z`, "#4F46E5", 2, { fill: "#4F46E5" });
      P_EL(gav, `M ${leftPad + 18} ${y - 8} L ${leftPad + 40} ${y + 14}`, "#4F46E5", 4);
      
      const textX = leftPad + 50;
      T_EL(g, textX, y - 12, courtText || "Landmark Judicial Ruling", { size: 13.5, weight: 800, fill: "#4F46E5" });
      
      if (ruleText && ruleText.length > 38) {
        const words = ruleText.split(" ");
        let l1 = "", l2 = "";
        for (const word of words) {
          if (!l2 && (l1 + " " + word).trim().length <= 42) {
            l1 = (l1 ? l1 + " " + word : word);
          } else {
            l2 = (l2 ? l2 + " " + word : word);
          }
        }
        T_EL(g, textX, y + 8, l1, { size: 11.5, weight: 600, fill: "#374151" });
        T_EL(g, textX, y + 24, l2, { size: 11.5, weight: 600, fill: "#374151" });
      } else {
        T_EL(g, textX, y + 14, ruleText || "Statutory Principle Confirmed", { size: 12, weight: 600, fill: "#374151" });
      }
      return g;
    };

    const at = (key, fallback) => {
      if (b.elements && b.elements[key] && typeof b.elements[key].at === "number") {
        return b.elements[key].at;
      }
      if (b.timings && typeof b.timings[key] === "number") {
        return b.timings[key];
      }
      return b.start + fallback;
    };

    // 1. SCENE: rental_and_gift
    if (b.scene_type === "rental_and_gift") {
      const sep = P_EL(svg, "M 500 120 L 500 480", "#CBD5E1", 2, { dash: "6 6" });
      fade(ctx, sep, at("divider", 0.3), 0, 0.4);

      // LEFT REGION: Bangalore House & Rental Flow
      const regL = G_EL(svg);
      R_EL(regL, 50, 130, 410, 360, "#F8FAFC", { stroke: "#E2E8F0", sw: 1.5, rx: 16 });
      T_EL(regL, 255, 160, "PROPERTY 1 · BANGALORE", { size: 13, weight: 800, fill: "#4F46E5", anchor: "middle", ls: "0.1em" });
      fade(ctx, regL, at("bangalore_reg", 0.4), 10, 0.4);

      const bHouse = makeHouse(svg, 160, 260, "#4F46E5", "Bangalore House", "Let Out to Tenant");
      fade(ctx, bHouse, at("bangalore_house", 0.8), 12, 0.5);

      const tenant = makePerson(svg, 370, 260, "#059669", "Mr. Kumar", "Tenant");
      fade(ctx, tenant, at("tenant", 1.2), 12, 0.5);

      const rentArc = P_EL(svg, "M 340 280 C 290 230 230 230 180 280", "#059669", 3, { dash: "6 4" });
      fade(ctx, rentArc, at("rent_arc", 1.8), 0, 0.4);
      ctx.push({ el: rentArc, kind: "draw", start: at("rent_arc", 1.8), dur: 0.8 });

      const rentPill = G_EL(svg);
      R_EL(rentPill, 205, 205, 110, 32, "#ECFDF5", { stroke: "#059669", sw: 1.5, rx: 16 });
      T_EL(rentPill, 260, 226, "₹ 3,00,000 / yr", { size: 12, weight: 800, fill: "#059669", anchor: "middle" });
      fade(ctx, rentPill, at("rent_pill", 2.2), 8, 0.4);

      const munBox = G_EL(svg);
      R_EL(munBox, 90, 400, 330, 60, "#FFFFFF", { stroke: "#DC2626", sw: 1.5, rx: 10 });
      T_EL(munBox, 105, 425, "Municipal Taxes Paid: ₹ 1,85,000", { size: 13, weight: 800, fill: "#DC2626" });
      T_EL(munBox, 105, 445, "Current ₹ 35k + Arrears ₹ 1.50L (Deductible u/s 23)", { size: 11, weight: 600, fill: "#64748B" });
      fade(ctx, munBox, at("municipal_tax", 2.8), 10, 0.4);

      // RIGHT REGION: Chennai House & Gift Transfer
      const regR = G_EL(svg);
      R_EL(regR, 540, 130, 410, 360, "#F8FAFC", { stroke: "#E2E8F0", sw: 1.5, rx: 16 });
      T_EL(regR, 745, 160, "PROPERTY 2 · CHENNAI (GIFTED)", { size: 13, weight: 800, fill: "#4F46E5", anchor: "middle", ls: "0.1em" });
      fade(ctx, regR, at("chennai_reg", 3.4), 10, 0.4);

      const father = makePerson(svg, 620, 260, "#6B7280", "Father", "Acquired Apr 2006");
      fade(ctx, father, at("father", 3.8), 12, 0.5);

      const son = makePerson(svg, 860, 260, "#4F46E5", "Mr. Rajesh", "Donee / Assessee");
      fade(ctx, son, at("son", 4.2), 12, 0.5);

      const cHouse = makeHouse(svg, 740, 260, "#059669", "Chennai House", "Sold Aug 2025");
      fade(ctx, cHouse, at("chennai_house", 4.6), 12, 0.5);

      const deedBox = G_EL(svg);
      R_EL(deedBox, 675, 205, 130, 32, "#FEF08A", { stroke: "#CA8A04", sw: 1.5, rx: 16 });
      T_EL(deedBox, 740, 226, "Gift Deed · 01.03.2007", { size: 11, weight: 800, fill: "#854D0E", anchor: "middle" });
      fade(ctx, deedBox, at("gift_deed", 5.0), 8, 0.4);

      const costBox = G_EL(svg);
      R_EL(costBox, 580, 400, 330, 60, "#FFFFFF", { stroke: "#4F46E5", sw: 1.5, rx: 10 });
      T_EL(costBox, 595, 425, "Cost to Previous Owner u/s 49(1): ₹ 1,25,000", { size: 13, weight: 800, fill: "#4F46E5" });
      T_EL(costBox, 595, 445, "Sold Aug 2025: Sale Consideration ₹ 25,00,000", { size: 11, weight: 600, fill: "#64748B" });
      fade(ctx, costBox, at("previous_cost", 5.6), 10, 0.4);
    }

    // 2. SCENE: rental_computation
    else if (b.scene_type === "rental_computation") {
      const steps = [
        { key: "step_gav", label: "Gross Annual Value (Actual Rent ₹ 3 Lakhs)", val: "+ ₹ 3,00,000", col: "#059669", tint: "#ECFDF5", sign: "+" },
        { key: "step_mun_tax", label: "Less: Municipal Taxes Paid (Current ₹ 35k + Arrears ₹ 1.5L)", val: "− ₹ 1,85,000", col: "#DC2626", tint: "#FEF2F2", sign: "−" },
        { key: "step_nav", label: "Net Annual Value (NAV)", val: "= ₹ 1,15,000", col: "#4F46E5", tint: "#EEF2FF", sign: "=" },
        { key: "step_std_ded", label: "Less: Section 24(a) Standard Deduction @ 30%", val: "− ₹ 34,500", col: "#DC2626", tint: "#FEF2F2", sign: "−" },
        { key: "step_interest", label: "Less: Section 24(b) Interest on Loan for Major Repairs", val: "− ₹ 1,50,000", col: "#DC2626", tint: "#FEF2F2", sign: "−" },
        { key: "step_arrears", label: "Add: Section 25A Arrears of Rent Received (₹ 30k less 30%)", val: "+ ₹ 21,000", col: "#059669", tint: "#ECFDF5", sign: "+" }
      ];

      const startY = 135, stepH = 46;
      steps.forEach((st, idx) => {
        const row = G_EL(svg);
        const y = startY + idx * (stepH + 8);
        R_EL(row, 150, y, 700, stepH, st.tint, { stroke: st.col, sw: 1.5, rx: 10 });
        T_EL(row, 175, y + 28, st.label, { size: 14, weight: 700, fill: "#0F172A" });
        T_EL(row, 825, y + 28, st.val, { size: 16, weight: 800, fill: st.col, anchor: "end" });
        fade(ctx, row, at(st.key, 0.6 + idx * 0.8), 10, 0.4);
      });

      const resG = G_EL(svg);
      R_EL(resG, 250, startY + 6 * (stepH + 8) + 6, 500, 56, "#FEF2F2", { stroke: "#DC2626", sw: 2.5, rx: 28 });
      T_EL(resG, 500, startY + 6 * (stepH + 8) + 40, "Net Loss from House Property: (₹ 48,500)", { size: 18, weight: 800, fill: "#DC2626", anchor: "middle" });
      fade(ctx, resG, at("net_loss", 5.6), 12, 0.5);
    }

    // 3. SCENE: property_transfer_sdv (Real Estate, Seller, Buyer, House, Extension, Advance Cheque, SDV Gavel)
    else if (b.scene_type === "property_transfer_sdv" || b.elements?.vijay || b.elements?.house_1982) {
      // Ambient Ground line
      P_EL(svg, "M 60 480 L 940 480", "#CBD5E1", 2.5);

      // 1. Assessee / Seller (Mr. Vijay)
      const vijayG = makePerson(svg, 150, 310, "#4F46E5", "Mr. Vijay", "Assessee (Seller)");
      fade(ctx, vijayG, at("vijay", 3.5), 12, 0.5);

      // 2. Residential House (Purchased in 1982)
      const houseG = G_EL(svg);
      // Ground floor structure
      R_EL(houseG, 320, 340, 150, 130, "#FFFFFF", { stroke: "#4F46E5", sw: 3.5, rx: 6 });
      R_EL(houseG, 375, 395, 40, 75, "#4F46E5", { rx: 3 });
      R_EL(houseG, 335, 360, 24, 24, "#FEF08A", { stroke: "#4F46E5", sw: 2, rx: 2 });
      R_EL(houseG, 435, 360, 24, 24, "#FEF08A", { stroke: "#4F46E5", sw: 2, rx: 2 });
      // Ground floor initial roof (fades out when first floor stacks)
      const gfRoof = P_EL(houseG, "M 305 340 L 395 285 L 485 340 Z", "#4F46E5", 3.5, { fill: "#EEF2FF" });
      fade(ctx, gfRoof, at("house_1982", 7.5), 10, 0.4, at("floor_construction", 38.5), 0.4);

      // 1982 Purchase Pill
      const p1982 = G_EL(houseG);
      R_EL(p1982, 305, 490, 180, 32, "#EEF2FF", { stroke: "#4F46E5", sw: 1.5, rx: 16 });
      T_EL(p1982, 395, 511, "Purchased 1982 · ₹ 5,00,000", { size: 11.5, weight: 800, fill: "#4F46E5", anchor: "middle" });
      fade(ctx, p1982, at("cost_5l", 11.3), 8, 0.4);
      fade(ctx, houseG, at("house_1982", 7.5), 12, 0.5);

      // 3. 1st April 2001 Statutory Base Comparison Card
      const bmCard = G_EL(svg);
      R_EL(bmCard, 245, 120, 300, 68, "#FFFFFF", { stroke: "#6366F1", sw: 2, rx: 10 });
      R_EL(bmCard, 245, 120, 300, 22, "#6366F1", { rx: 10 });
      R_EL(bmCard, 245, 132, 300, 10, "#6366F1", { rx: 0 });
      T_EL(bmCard, 395, 136, "01.04.2001 STATUTORY BASE u/s 55(2)(b)", { size: 10.5, weight: 800, fill: "#FFFFFF", anchor: "middle", ls: "0.06em" });
      T_EL(bmCard, 260, 162, "FMV: ₹ 15,00,000", { size: 12.5, weight: 700, fill: "#64748B" });
      T_EL(bmCard, 385, 162, "SDV: ₹ 14,00,000", { size: 12.5, weight: 700, fill: "#DC2626" });
      T_EL(bmCard, 260, 180, "Base COA = Lower of FMV/SDV = ₹ 14,00,000", { size: 11.5, weight: 800, fill: "#059669" });
      fade(ctx, bmCard, at("benchmark_2001", 13.8), 10, 0.5);

      // 4. June 2009 Advance Forfeited (Pre-2014: Deducted from Cost)
      const forf2009 = G_EL(svg);
      R_EL(forf2009, 80, 200, 200, 46, "#FEF2F2", { stroke: "#DC2626", sw: 1.5, rx: 8 });
      T_EL(forf2009, 180, 220, "Forfeited June 2009: ₹ 1.5L", { size: 11.5, weight: 800, fill: "#DC2626", anchor: "middle" });
      T_EL(forf2009, 180, 237, "Deducted from Cost u/s 51", { size: 10, weight: 700, fill: "#059669", anchor: "middle" });
      fade(ctx, forf2009, at("forfeit_2009", 28.2), 10, 0.4);

      // 5. July 2016 Advance Forfeited (Post-2014: Taxed under IFOS)
      const forf2016 = G_EL(svg);
      R_EL(forf2016, 80, 145, 200, 46, "#FEF08A", { stroke: "#CA8A04", sw: 1.5, rx: 8 });
      T_EL(forf2016, 180, 165, "Forfeited July 2016: ₹ 2.0L", { size: 11.5, weight: 800, fill: "#854D0E", anchor: "middle" });
      T_EL(forf2016, 180, 182, "Taxed u/s 56(2)(ix) (Cost unaffected)", { size: 10, weight: 700, fill: "#854D0E", anchor: "middle" });
      fade(ctx, forf2016, at("forfeit_2016", 33.1), 10, 0.4);

      // 6. September 2015 First Floor Construction
      const floorG = G_EL(svg);
      R_EL(floorG, 325, 260, 140, 80, "#EFF6FF", { stroke: "#2563EB", sw: 3, rx: 4 });
      P_EL(floorG, "M 310 260 L 395 205 L 480 260 Z", "#2563EB", 3.5, { fill: "#DBEAFE" });
      R_EL(floorG, 345, 280, 22, 22, "#FEF08A", { stroke: "#2563EB", sw: 2, rx: 2 });
      R_EL(floorG, 420, 280, 22, 22, "#FEF08A", { stroke: "#2563EB", sw: 2, rx: 2 });
      const fPill = G_EL(floorG);
      R_EL(fPill, 275, 215, 240, 26, "#DBEAFE", { stroke: "#2563EB", sw: 1.5, rx: 13 });
      T_EL(fPill, 395, 232, "First Floor Built (Sep 2015): ₹ 5,08,000", { size: 10.5, weight: 800, fill: "#1D4ED8", anchor: "middle" });
      fade(ctx, floorG, at("floor_construction", 38.8), 15, 0.6);

      // 7. Buyer (FY 2025-26)
      const buyerG = makePerson(svg, 850, 310, "#059669", "The Buyer", "FY 2025-26 Agreement");
      fade(ctx, buyerG, at("buyer", 45.0), 12, 0.5);

      // 8. Sale Agreement & Advance Cheque Arc
      const saleCard = G_EL(svg);
      R_EL(saleCard, 520, 310, 250, 60, "#FFFFFF", { stroke: "#059669", sw: 2, rx: 10 });
      T_EL(saleCard, 645, 333, "Agreement Consideration: ₹ 40,00,000", { size: 12.5, weight: 800, fill: "#0F172A", anchor: "middle" });
      T_EL(saleCard, 645, 353, "Advance: ₹ 2,00,000 (Account Payee Cheque)", { size: 11, weight: 700, fill: "#059669", anchor: "middle" });
      fade(ctx, saleCard, at("agreement_sale", 48.8), 10, 0.4);

      // Cheque flow animation arc
      const chqArc = P_EL(svg, "M 810 320 C 720 250 560 250 480 340", "#059669", 3, { dash: "6 4" });
      fade(ctx, chqArc, at("cheque_advance", 52.0), 0, 0.3);
      ctx.push({ el: chqArc, kind: "draw", start: at("cheque_advance", 52.0), dur: 0.8 });

      // 9. Stamp Duty Valuation Gavel & Benchmark
      const sdvCard = G_EL(svg);
      R_EL(sdvCard, 580, 120, 360, 150, "#FFFFFF", { stroke: "#DC2626", sw: 3, rx: 12 });
      R_EL(sdvCard, 580, 120, 360, 30, "#DC2626", { rx: 12 });
      R_EL(sdvCard, 580, 140, 360, 10, "#DC2626", { rx: 0 });
      T_EL(sdvCard, 760, 141, "SECTION 50C BENCHMARK u/s 50C(1) PROVISO", { size: 11, weight: 800, fill: "#FFFFFF", anchor: "middle", ls: "0.06em" });
      T_EL(sdvCard, 605, 175, "Agreement Date SDV: ₹ 52,00,000", { size: 15, weight: 800, fill: "#DC2626" });
      T_EL(sdvCard, 605, 198, "110% Safe Harbor Limit: ₹ 44,00,000", { size: 13, weight: 700, fill: "#854D0E" });
      T_EL(sdvCard, 605, 218, "Breach: SDV (₹ 52L) > 110% of Actual (₹ 44L)", { size: 11.5, weight: 700, fill: "#DC2626" });
      
      const deemPill = G_EL(sdvCard);
      R_EL(deemPill, 595, 232, 330, 28, "#FEF2F2", { stroke: "#DC2626", sw: 1.5, rx: 14 });
      T_EL(deemPill, 760, 251, "DEEMED FULL VALUE OF CONSIDERATION = ₹ 52,00,000", { size: 10.5, weight: 900, fill: "#DC2626", anchor: "middle", ls: "0.04em" });
      fade(ctx, sdvCard, at("sdv_agreement", 57.8), 12, 0.5);

      // 10. Multi-Provision Statutory Pillars (Bottom Center)
      const secRow = G_EL(svg);
      const secs = [
        { label: "Section 50C", sub: "Deemed FVC: ₹ 52L", col: "#DC2626", tint: "#FEF2F2" },
        { label: "Section 51", sub: "Advance Pre-2014 Less", col: "#4F46E5", tint: "#EEF2FF" },
        { label: "Section 112", sub: "Beneficial Parity (Nil Tax)", col: "#059669", tint: "#ECFDF5" }
      ];
      secs.forEach((sc, i) => {
        const pG = G_EL(secRow);
        const px = 250 + i * 180;
        R_EL(pG, px, 490, 160, 48, sc.tint, { stroke: sc.col, sw: 1.5, rx: 10 });
        T_EL(pG, px + 80, 510, sc.label, { size: 12, weight: 800, fill: sc.col, anchor: "middle" });
        T_EL(pG, px + 80, 526, sc.sub, { size: 10, weight: 600, fill: "#374151", anchor: "middle" });
      });
      fade(ctx, secRow, at("statutory_pills", 63.0), 10, 0.4);
    }

    // 4. SCENE: sdv_comparison (Dynamic Fallback for other standard SDV questions)
    else if (b.scene_type === "sdv_comparison") {
      const baseY = 420;
      const actualVal = b.elements?.actual_bar?.val || 2500000;
      const actualLabel = b.elements?.actual_bar?.label || `₹ ${Math.round(actualVal/100000)} Lakhs`;
      const sdvVal = b.elements?.sdv_bar?.val || 3000000;
      const sdvLabel = b.elements?.sdv_bar?.label || `₹ ${Math.round(sdvVal/100000)} Lakhs`;
      const safeVal = Math.round(actualVal * 1.10);

      const bar1 = G_EL(svg);
      R_EL(bar1, 180, baseY - 180, 160, 180, "#EEF2FF", { stroke: "#4F46E5", sw: 3, rx: 12 });
      T_EL(bar1, 260, baseY - 200, "Actual Consideration", { size: 14, weight: 700, fill: "#64748B", anchor: "middle" });
      T_EL(bar1, 260, baseY - 80, inr(actualVal), { size: 24, weight: 800, fill: "#4F46E5", anchor: "middle" });
      fade(ctx, bar1, at("actual_bar", 0.6), 15, 0.5);

      const thLine = G_EL(svg);
      P_EL(thLine, "M 130 220 L 590 220", "#CA8A04", 2.5, { dash: "8 6" });
      R_EL(thLine, 210, 172, 185, 32, "#FEF08A", { stroke: "#CA8A04", sw: 1.5, rx: 16 });
      T_EL(thLine, 302, 193, `110% Safe Harbor: ${inr(safeVal)}`, { size: 12, weight: 800, fill: "#854D0E", anchor: "middle" });
      fade(ctx, thLine, at("safe_harbor", 1.6), 0, 0.4);

      const bar2 = G_EL(svg);
      R_EL(bar2, 420, baseY - 225, 160, 225, "#FEF2F2", { stroke: "#DC2626", sw: 3.5, rx: 12 });
      T_EL(bar2, 500, baseY - 245, "Stamp Duty Value (SDV)", { size: 14, weight: 800, fill: "#DC2626", anchor: "middle" });
      T_EL(bar2, 500, baseY - 100, inr(sdvVal), { size: 26, weight: 800, fill: "#DC2626", anchor: "middle" });
      fade(ctx, bar2, at("sdv_bar", 2.4), 18, 0.5);

      const stamp = G_EL(svg);
      R_EL(stamp, 640, 160, 280, 140, "#FFFFFF", { stroke: "#DC2626", sw: 3, rx: 14 });
      R_EL(stamp, 640, 160, 280, 36, "#DC2626", { rx: 14 });
      R_EL(stamp, 640, 180, 280, 16, "#DC2626", { rx: 0 });
      T_EL(stamp, 780, 184, "SECTION 50C TRIGGERED", { size: 13, weight: 800, fill: "#FFFFFF", anchor: "middle", ls: "0.08em" });
      T_EL(stamp, 780, 220, `SDV (${inr(sdvVal)}) > 110% (${inr(safeVal)})`, { size: 12, weight: 700, fill: "#111827", anchor: "middle" });
      T_EL(stamp, 780, 245, `Deemed Full Value: ${inr(sdvVal)}`, { size: 14, weight: 800, fill: "#DC2626", anchor: "middle" });
      fade(ctx, stamp, at("stamp_50c", 3.6), 12, 0.5);
    }

    // 4. SCENE: adjacent_flats_merge
    else if (b.scene_type === "adjacent_flats_merge") {
      const fWrap = G_EL(svg);
      R_EL(fWrap, 80, 140, 480, 220, "#FFFFFF", { stroke: "#111827", sw: 4, rx: 12 });

      const f1 = G_EL(fWrap);
      R_EL(f1, 95, 155, 215, 190, "#EEF2FF", { stroke: "#4F46E5", sw: 2, rx: 8 });
      T_EL(f1, 202, 230, "Flat 101", { size: 22, weight: 800, fill: "#4F46E5", anchor: "middle" });
      T_EL(f1, 202, 260, "Cost: ₹ 8,00,000", { size: 16, weight: 700, fill: "#0F172A", anchor: "middle" });
      T_EL(f1, 202, 285, "Sale Deed 1 · 02.01.2026", { size: 12, weight: 600, fill: "#64748B", anchor: "middle" });
      fade(ctx, f1, at("flat_101", 0.6), 10, 0.4);

      const f2 = G_EL(fWrap);
      R_EL(f2, 330, 155, 215, 190, "#ECFDF5", { stroke: "#059669", sw: 2, rx: 8 });
      T_EL(f2, 437, 230, "Flat 102", { size: 22, weight: 800, fill: "#059669", anchor: "middle" });
      T_EL(f2, 437, 260, "Cost: ₹ 7,00,000", { size: 16, weight: 700, fill: "#0F172A", anchor: "middle" });
      T_EL(f2, 437, 285, "Sale Deed 2 · 02.01.2026", { size: 12, weight: 600, fill: "#64748B", anchor: "middle" });
      fade(ctx, f2, at("flat_102", 1.2), 10, 0.4);

      const dividerWall = P_EL(fWrap, "M 320 155 L 320 345", "#DC2626", 5, { dash: "6 4" });
      fade(ctx, dividerWall, at("divider_wall", 1.8), 0, 0.4, at("merge_pill", 3.2), 0.4);

      const mergePill = G_EL(svg);
      R_EL(mergePill, 140, 385, 360, 50, "#FEF08A", { stroke: "#CA8A04", sw: 2, rx: 25 });
      T_EL(mergePill, 320, 416, "MODIFIED AS ONE HABITABLE UNIT", { size: 14, weight: 800, fill: "#854D0E", anchor: "middle", ls: "0.06em" });
      fade(ctx, mergePill, at("merge_pill", 3.2), 10, 0.5);

      const courtCard = makeGavel(svg, 780, 210, "CIT v. Ananda Basappa (Kar HC)", "Two adjacent flats modified as one unit qualify u/s 54");
      fade(ctx, courtCard, at("court_ruling", 3.8), 12, 0.5);

      const exCard = G_EL(svg);
      R_EL(exCard, 670, 305, 220, 110, "#ECFDF5", { stroke: "#059669", sw: 2.5, rx: 12 });
      T_EL(exCard, 780, 340, "Section 54 Exemption", { size: 14, weight: 800, fill: "#059669", anchor: "middle" });
      T_EL(exCard, 780, 380, "₹ 15,00,000", { size: 28, weight: 800, fill: "#059669", anchor: "middle" });
      T_EL(exCard, 780, 403, "₹ 8L + ₹ 7L Fully Qualified", { size: 12, weight: 600, fill: "#64748B", anchor: "middle" });
      fade(ctx, exCard, at("sec54_pill", 4.8), 12, 0.5);
    }

    // 5. SCENE: bond_investment
    else if (b.scene_type === "bond_investment") {
      const tl = G_EL(svg);
      P_EL(tl, "M 100 230 L 900 230", "#CBD5E1", 4);
      fade(ctx, tl, at("timeline_line", 0.4), 0, 0.4);

      const nodes = [
        { key: "node_sale", x: 160, date: "10.08.2025", title: "Chennai Sale", sub: "Date of Transfer", col: "#4F46E5" },
        { key: "node_payment", x: 380, date: "10.10.2025", title: "Payment Made", sub: "Invested ₹ 10 Lakhs", col: "#059669" },
        { key: "node_allotment", x: 620, date: "01.02.2026", title: "Bonds Allotted", sub: "NHAI Allotment Date", col: "#CA8A04" },
        { key: "node_deadline", x: 840, date: "10.02.2026", title: "6-Month Deadline", sub: "Statutory Window End", col: "#DC2626" }
      ];

      nodes.forEach((nd, i) => {
        const ng = G_EL(svg);
        S_EL("circle", { cx: nd.x, cy: 230, r: 12, fill: "#FFFFFF", stroke: nd.col, "stroke-width": 4 }, ng);
        T_EL(ng, nd.x, 205, nd.date, { size: 13, weight: 800, fill: nd.col, anchor: "middle" });
        T_EL(ng, nd.x, 265, nd.title, { size: 14, weight: 800, fill: "#0F172A", anchor: "middle" });
        T_EL(ng, nd.x, 285, nd.sub, { size: 11, weight: 600, fill: "#64748B", anchor: "middle" });
        fade(ctx, ng, at(nd.key, 0.6 + i * 0.7), 8, 0.4);
      });

      const brac = P_EL(svg, "M 160 160 L 380 160", "#059669", 3, { dash: "6 4" });
      fade(ctx, brac, at("paid_bracket", 2.2), 0, 0.4);
      const bracLbl = T_EL(svg, 270, 145, "Paid within 2 Months!", { size: 13, weight: 800, fill: "#059669", anchor: "middle" });
      fade(ctx, bracLbl, at("paid_bracket", 2.4), 6, 0.4);

      const courtCard = makeGavel(svg, 360, 405, "Hindustan Unilever Ltd. v. DCIT (Bom HC)", "Payment within 6 months satisfies section 54EC even if allotment is later", 430, 80);
      fade(ctx, courtCard, at("court_ruling", 3.2), 12, 0.5);

      const exPill = G_EL(svg);
      R_EL(exPill, 660, 360, 240, 100, "#ECFDF5", { stroke: "#059669", sw: 2.5, rx: 12 });
      T_EL(exPill, 780, 395, "Section 54EC Exemption", { size: 14, weight: 800, fill: "#059669", anchor: "middle" });
      T_EL(exPill, 780, 435, "₹ 10,00,000", { size: 28, weight: 800, fill: "#059669", anchor: "middle" });
      fade(ctx, exPill, at("sec54ec_pill", 4.2), 12, 0.5);
    }

    // 6. SCENE: factory_shift / factory_relocation
    else if (b.scene_type === "factory_shift" || b.scene_type === "factory_relocation") {
      const sep = P_EL(svg, "M 500 120 L 500 480", "#CBD5E1", 2, { dash: "6 6" });
      fade(ctx, sep, at("divider", 0.3), 0, 0.4);

      // LEFT REGION: Urban Limit & Old Factory
      const regL = G_EL(svg);
      R_EL(regL, 50, 130, 410, 360, "#F8FAFC", { stroke: "#E2E8F0", sw: 1.5, rx: 16 });
      T_EL(regL, 255, 160, "URBAN CORPORATION LIMIT (ORIGINAL SITE)", { size: 12.5, weight: 800, fill: "#DC2626", anchor: "middle", ls: "0.08em" });
      fade(ctx, regL, at("urban_reg", 0.4), 10, 0.4);

      const uFactory = makeFactory(svg, 255, 240, "#DC2626", b.assessee || "Apex Engineering Ltd", "Urban Industrial Unit (Relocating)");
      fade(ctx, uFactory, at("urban_factory", 0.8), 12, 0.5);

      // Transferred Assets Box
      const assetsBox = G_EL(svg);
      R_EL(assetsBox, 75, 365, 360, 105, "#FFFFFF", { stroke: "#DC2626", sw: 1.5, rx: 12 });
      T_EL(assetsBox, 90, 390, "Transferred Assets in Urban Area:", { size: 12, weight: 800, fill: "#DC2626" });
      T_EL(assetsBox, 90, 412, "• Land (LTCG ₹ 5L)  • Building (STCG ₹ 12L)", { size: 11.5, weight: 600, fill: "#374151" });
      T_EL(assetsBox, 90, 432, "• Plant & Machinery (STCG ₹ 11L)", { size: 11.5, weight: 600, fill: "#374151" });
      T_EL(assetsBox, 90, 452, "• Furniture (STCG ₹ 2L · Ineligible u/s 54G)", { size: 11.5, weight: 700, fill: "#B91C1C" });
      fade(ctx, assetsBox, at("assets_box", 1.8), 10, 0.4);

      // CENTER RELOCATION ARROW
      const shiftArrow = P_EL(svg, "M 440 280 C 470 240 530 240 560 280", "#4F46E5", 4, { dash: "8 4" });
      fade(ctx, shiftArrow, at("shift_arrow", 2.4), 0, 0.4);
      ctx.push({ el: shiftArrow, kind: "draw", start: at("shift_arrow", 2.4), dur: 0.8 });

      const shiftPill = G_EL(svg);
      R_EL(shiftPill, 435, 205, 130, 32, "#EEF2FF", { stroke: "#4F46E5", sw: 1.5, rx: 16 });
      T_EL(shiftPill, 500, 226, "SHIFTING RELOCATION", { size: 10.5, weight: 800, fill: "#4F46E5", anchor: "middle" });
      fade(ctx, shiftPill, at("shift_pill", 2.8), 8, 0.4);

      // RIGHT REGION: Rural Non-Urban Zone & New Factory
      const regR = G_EL(svg);
      R_EL(regR, 540, 130, 410, 360, "#F8FAFC", { stroke: "#E2E8F0", sw: 1.5, rx: 16 });
      T_EL(regR, 745, 160, "NON-URBAN RURAL AREA (NEW SITE)", { size: 12.5, weight: 800, fill: "#059669", anchor: "middle", ls: "0.08em" });
      fade(ctx, regR, at("rural_reg", 3.2), 10, 0.4);

      const rFactory = makeFactory(svg, 745, 240, "#059669", "New Rural Undertaking", "Acquired within 1 yr before / 3 yrs after");
      fade(ctx, rFactory, at("rural_factory", 3.6), 12, 0.5);

      // New Reinvestment Pool Box
      const poolBox = G_EL(svg);
      R_EL(poolBox, 565, 365, 360, 105, "#FFFFFF", { stroke: "#059669", sw: 1.5, rx: 12 });
      T_EL(poolBox, 580, 390, "Eligible Reinvestment Pool u/s 54G:", { size: 12, weight: 800, fill: "#059669" });
      T_EL(poolBox, 580, 412, "• Land: ₹ 4L  • Building: ₹ 6L  • P&M: ₹ 15L", { size: 11.5, weight: 600, fill: "#374151" });
      T_EL(poolBox, 580, 432, "Total Qualifying Pool: ₹ 25,00,000", { size: 13, weight: 800, fill: "#059669" });
      T_EL(poolBox, 580, 452, "Furniture (₹ 2L) Excluded from 54G Exemption", { size: 11, weight: 700, fill: "#DC2626" });
      fade(ctx, poolBox, at("pool_box", 4.2), 10, 0.4);
    }

    // 7. UNIVERSAL DYNAMIC FALLBACK FOR ANY OTHER SITUATIONAL STORY SCENE
    else {
      const elems = b.elements || {};
      const keys = Object.keys(elems);
      if (keys.length > 0) {
        const gridCols = Math.min(keys.length, 3);
        const colW = Math.floor(860 / gridCols);
        keys.forEach((k, idx) => {
          const item = elems[k];
          if (!item || typeof item !== "object") return;
          const colIdx = idx % gridCols;
          const rowIdx = Math.floor(idx / gridCols);
          const x = item.x !== undefined ? item.x : (100 + colIdx * colW + colW / 2);
          const y = item.y !== undefined ? item.y : (200 + rowIdx * 140);
          const col = item.col || (item.tone === "ok" ? "#059669" : (item.tone === "bad" ? "#DC2626" : "#4F46E5"));

          let g;
          if (item.type === "person") {
            g = makePerson(svg, x, y, col, item.name || item.label, item.role || item.sub);
          } else if (item.type === "house") {
            g = makeHouse(svg, x, y, col, item.name || item.label, item.role || item.sub);
          } else if (item.type === "factory") {
            g = makeFactory(svg, x, y, col, item.name || item.label, item.role || item.sub);
          } else if (item.type === "gavel") {
            g = makeGavel(svg, x, y, item.title || item.name, item.rule || item.sub, item.w || 380, item.h || 76);
          } else {
            g = G_EL(svg);
            const w = item.w || Math.min(colW - 20, 260);
            const h = item.h || 90;
            R_EL(g, x - w / 2, y - h / 2, w, h, "#FFFFFF", { stroke: col, sw: 2, rx: 12 });
            if (item.badge) {
              R_EL(g, x - w / 2 + 14, y - h / 2 + 12, item.badge.length * 7 + 16, 20, "#EEF2FF", { rx: 10 });
              T_EL(g, x - w / 2 + 22, y - h / 2 + 26, item.badge, { size: 10, weight: 800, fill: "#4F46E5" });
            }
            if (item.title || item.label) {
              T_EL(g, x - w / 2 + 14, y - h / 2 + 50, item.title || item.label, { size: 14, weight: 800, fill: "#0F172A" });
            }
            if (item.sub || item.text) {
              T_EL(g, x - w / 2 + 14, y - h / 2 + 70, item.sub || item.text, { size: 11.5, weight: 600, fill: "#64748B" });
            }
            if (item.val) {
              T_EL(g, x + w / 2 - 14, y - h / 2 + 50, inr(item.val), { size: 14, weight: 800, fill: col, anchor: "end" });
            }
          }
          fade(ctx, g, item.at !== undefined ? item.at : (b.start + 0.5 + idx * 0.4), 10, 0.4);
        });
      }
    }
  }
};

class Explainer {
  constructor({ stage, focal, audio, caption, bar, pill, scrub, speed, playBtn, timeText }) {
    Object.assign(this, { stage, focal, audio, caption, bar, pill, scrub, speed, playBtn, timeText });
    this.anim = [];
    this.beatEls = [];
    this.raf = 0;
    this.sp = null;
    this.offset = 0;
    this.isDebug = window.location.search.includes("debug=1");

    if (this.isDebug && this.stage) {
      this.initDebugHud();
    }

    audio.addEventListener("play",       () => { this.updatePlayIcon(true); this.loop(); });
    audio.addEventListener("pause",      () => { this.updatePlayIcon(false); cancelAnimationFrame(this.raf); });
    audio.addEventListener("seeked",     () => this.render());
    audio.addEventListener("timeupdate", () => { if (audio.paused) this.render(); });

    if (this.scrub) {
      this.scrub.addEventListener("input", () => {
        if (this.audio.duration) {
          this.audio.currentTime = Number(this.scrub.value);
        }
      });
    }

    if (this.speed) {
      this.speed.addEventListener("change", () => {
        this.audio.playbackRate = Number(this.speed.value);
      });
      this.speed.addEventListener("click", (e) => e.stopPropagation());
    }

    if (this.playBtn) {
      this.playBtn.addEventListener("click", () => this.toggle());
    }

    // Space key to toggle play/pause
    this.keyHandler = (e) => {
      if (e.target && (e.target.tagName === "INPUT" || e.target.tagName === "SELECT")) return;
      if (e.code === "Space" || e.key === " ") {
        e.preventDefault();
        this.toggle();
      }
    };
    window.addEventListener("keydown", this.keyHandler);
  }

  initDebugHud() {
    this.debugHud = document.createElement("div");
    this.debugHud.id = "expDebugHud";
    this.debugHud.style.cssText = "position:absolute;top:8px;right:8px;background:rgba(17,24,39,0.85);color:#fff;font-family:monospace;font-size:12px;padding:6px 10px;border-radius:6px;z-index:999;pointer-events:none;display:flex;align-items:center;gap:8px;";
    this.debugDot = document.createElement("span");
    this.debugDot.style.cssText = "width:8px;height:8px;border-radius:50%;background:#4ADE80;opacity:0.3;";
    this.debugText = document.createElement("span");
    this.debugHud.appendChild(this.debugDot);
    this.debugHud.appendChild(this.debugText);
    this.stage.appendChild(this.debugHud);
  }

  updatePlayIcon(isPlaying) {
    if (!this.playBtn) return;
    const playSvg = `<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>`;
    const pauseSvg = `<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>`;
    this.playBtn.innerHTML = isPlaying ? pauseSvg : playSvg;
  }

  toggle() {
    this._userGestureActive = true;
    if (this.isPlaying || (this.audio && !this.audio.paused)) {
      this.pause();
    } else {
      this.play();
    }
  }

  play() {
    if (this.audio && this.audio.src) {
      const p = this.audio.play();
      if (p && typeof p.catch === "function") {
        p.then(() => {
          this.isPlaying = true;
          this.updatePlayIcon(true);
          if (typeof this.onPlay === "function") this.onPlay();
          this.loop();
        }).catch(err => {
          console.warn("Audio autoplay blocked by browser or failed:", err);
          if (this._userGestureActive || (this.audio && this.audio.error)) {
            console.warn("Running visual presentation via animated virtual clock fallback.");
            this.isPlaying = true;
            this.updatePlayIcon(true);
            if (typeof this.onPlay === "function") this.onPlay();
            this.startVirtualClock();
            this.loop();
            return;
          }
          this.isPlaying = false;
          this.updatePlayIcon(false);
          if (typeof this.onPause === "function") this.onPause();
        });
        return;
      }
    }
    this.isPlaying = true;
    this.updatePlayIcon(true);
    if (typeof this.onPlay === "function") this.onPlay();
    this.startVirtualClock();
    this.loop();
  }

  pause() {
    this.isPlaying = false;
    this.updatePlayIcon(false);
    if (typeof this.onPause === "function") this.onPause();
    if (this.audio) this.audio.pause();
    this.stopVirtualClock();
    cancelAnimationFrame(this.raf);
  }

  seek(t) {
    const target = Math.max(0, Math.min(this.sp?.duration_sec || 1000, Number(t) || 0));
    if (this.audio) {
      try { this.audio.currentTime = target; } catch(e) {}
    }
    this._virtualTime = target;
    this._mockTime = target;
    if (this.scrub) this.scrub.value = target;
    this.render();
  }

  startVirtualClock() {
    this._lastClockTick = performance.now();
    this._virtualClockActive = true;
  }

  stopVirtualClock() {
    this._virtualClockActive = false;
  }

  async load(qid, inlineSp = null) {
    let sp = inlineSp;
    const normKey = qid ? qid.replace(/-/g, "_") : "";
    const chKey = qid ? qid.replace(/^dt-/, "").replace(/-/g, "_") : "";

    if (!sp && typeof FIXTURES !== "undefined") {
      sp = FIXTURES[qid] || FIXTURES[normKey] || FIXTURES[chKey];
    }
    if (!sp && window.EXPLAINER_SCREENPLAYS) {
      sp = window.EXPLAINER_SCREENPLAYS[qid] || window.EXPLAINER_SCREENPLAYS[normKey] || window.EXPLAINER_SCREENPLAYS[chKey];
    }

    if (!sp && window.location.protocol !== "file:") {
      try {
        const resp = await fetch(`/api/screenplay/${qid}`);
        if (resp.ok) sp = await resp.json();
      } catch (e) {}
    }

    if (!sp && window.location.protocol !== "file:") {
      try {
        const localResp = await fetch(`data/screenplays/${qid}.json`);
        if (localResp.ok) sp = await localResp.json();
      } catch (e) {}
    }

    // Check window.D for live screenplay
    if (!sp && window.D && window.D.qna) {
      const qObj = window.D.qna.find(item => item.id === qid || ("dt-c" + item.ch + "-q" + item.n) === qid);
      if (qObj) {
        const prov = window.D.prov?.[qObj.topic];
        if (prov && prov.screenplay) {
          sp = prov.screenplay;
        }
      }
    }

    if (!sp && window.EXPLAINER_SCREENPLAYS) {
      sp = window.EXPLAINER_SCREENPLAYS[qid] || window.EXPLAINER_SCREENPLAYS[normKey] || window.EXPLAINER_SCREENPLAYS["dt-c2-q25"] || window.EXPLAINER_SCREENPLAYS["dt-c2-q14"];
    }

    if (!sp) {
      console.warn("Could not find screenplay for", qid, "generating fallback structure...");
      sp = {
        question_id: qid,
        context_pill: "Statutory Pedagogical Explainer",
        duration_sec: 45.0,
        beats: [
          {
            id: "b1",
            layout: "headline",
            start: 0,
            end: 15,
            voice_sync_text: "Statutory overview and core legal doctrine.",
            title: { text: "Statutory Provision Analysis", at: 0.5 },
            subtitle: { text: "Master the statutory principle before solving the exam case.", at: 2.0 }
          },
          {
            id: "b2",
            layout: "takeaway",
            start: 15,
            end: 45,
            voice_sync_text: "Golden takeaways for CA Final / Inter exams.",
            title: { text: "Key Statutory Takeaways", at: 15.5 },
            points: [
              { num: "1", text: "Verify statutory eligibility conditions under relevant section.", at: 18.0 },
              { num: "2", text: "Compute capital gains and appropriate exemptions accurately.", at: 25.0 }
            ]
          }
        ]
      };
    }

    this.sp = sp;
    this.offset = sp.sync_offset_sec || 0;
    this._virtualTime = 0;
    if (this.pill && sp.context_pill) {
      this.pill.textContent = sp.context_pill;
    }

    if (sp.audio_url) {
      const aSrc = (sp.audio_url && !sp.audio_url.startsWith("http") && !sp.audio_url.startsWith("../") && !sp.audio_url.startsWith("/")) ? ("../" + sp.audio_url) : sp.audio_url;
      this.audio.src = aSrc;
    }

    if (this.scrub) {
      this.scrub.min = 0;
      this.scrub.max = sp.duration_sec || 46.2;
      this.scrub.step = 0.05;
      this.scrub.value = 0;
    }

    this.focal.innerHTML = "";
    this.anim = [];
    this.beatEls = sp.beats.map((b, i) => {
      const el = document.createElement("div");
      el.className = "beat " + b.layout;
      el.id = "beat-" + (b.id || (i + 1));
      el.dataset.layout = b.layout;
      this.focal.appendChild(el);
      if (TEMPLATES[b.layout]) {
        TEMPLATES[b.layout](el, b, { push: a => this.anim.push({ ...a, beat: i, p: 0 }) });
      } else {
        console.warn("Unknown layout:", b.layout);
        TEMPLATES.headline(el, { title: { text: "Beat " + (i + 1), at: b.start } }, { push: a => this.anim.push({ ...a, beat: i, p: 0 }) });
      }
      return el;
    });

    this.render();
  }

  time(t) {
    if (t !== undefined && t !== null) {
      this._mockTime = t;
      this.render();
      return t;
    }
    if (this._mockTime !== undefined && this._mockTime !== null) return this._mockTime;
    if (this.audio && this.audio.src && !this.audio.error && !isNaN(this.audio.currentTime) && this.audio.currentTime > 0) {
      return Math.max(0, this.audio.currentTime - this.offset);
    }
    return Math.max(0, (this._virtualTime || 0) - this.offset);
  }

  loop() {
    if (this._virtualClockActive) {
      const now = performance.now();
      const dt = (now - (this._lastClockTick || now)) / 1000 * (this.audio?.playbackRate || 1.0);
      this._lastClockTick = now;
      this._virtualTime = (this._virtualTime || 0) + dt;
      const maxDur = this.sp?.duration_sec || 46.2;
      if (this.scrub) {
        this.scrub.value = this._virtualTime;
      }
      if (this.timeText) {
        const cur = this._virtualTime, dur = maxDur;
        this.timeText.textContent = Math.floor(cur / 60) + ":" + (Math.floor(cur % 60) < 10 ? "0" : "") + Math.floor(cur % 60) + " / " + Math.floor(dur / 60) + ":" + (Math.floor(dur % 60) < 10 ? "0" : "") + Math.floor(dur % 60);
      }
      if (this._virtualTime >= maxDur) {
        this._virtualTime = maxDur;
        this.render();
        this.pause();
        return;
      }
    }
    this.render();
    if (this.isPlaying || (this.audio && !this.audio.paused)) {
      this.raf = requestAnimationFrame(() => this.loop());
    }
  }

  render() {
    if (!this.sp || !this.sp.beats) return;
    const t = this.time(), beats = this.sp.beats;
    let active = 0;
    beats.forEach((b, i) => { if (t >= b.start) active = i; });
    this.beatEls.forEach((e, i) => e.classList.toggle("active", i === active));
    this.stage.dataset.beat = active + 1;

    // Exit drift: previous text fades and rises 8px before the next beat
    const b = beats[active];
    const x = (active < beats.length - 1 && b.end) ? ease((t - (b.end - EXIT)) / EXIT) : 0;
    const el = this.beatEls[active];
    if (el) {
      el.style.opacity = Math.max(0, 1 - x);
      el.style.transform = isReducedMotion() ? "none" : `translateY(${-8 * x}px)`;
    }

    let debugAnchorTriggered = false;

    // Animation updates
    for (const a of this.anim) {
      if (a.beat !== active) continue;
      const p = prog(t, a.start, a.dur);
      a.p = p; // Hook for test assertions

      if (this.isDebug && Math.abs(t - a.start) < 0.05) {
        debugAnchorTriggered = true;
      }

      switch (a.kind) {
        case "word":
          a.el.style.opacity = p;
          a.el.style.transform = isReducedMotion() ? "none" : `translateY(${12 * (1 - p)}px)`;
          break;
        case "mark":
          a.el.style.backgroundSize = `${p * 100}% 88%`;
          break;
        case "draw":
          a.el.style.strokeDasharray = 1;
          a.el.style.strokeDashoffset = 1 - p;
          a.el.style.opacity = p > 0 ? 1 : 0;
          break;
        case "fade":
          if (a.out && t >= a.out) {
            const outProg = ease(Math.min(1, Math.max(0, (t - a.out) / Math.max(0.001, a.outDur || 0.4))));
            a.el.style.opacity = 1 - outProg;
            if (a.dy && !isReducedMotion()) a.el.style.transform = `translateY(${(-a.dy) * outProg}px)`;
            if (outProg >= 1) a.el.style.display = "none";
            else a.el.style.display = "";
          } else {
            a.el.style.display = "";
            a.el.style.opacity = p;
            if (a.dy && !isReducedMotion()) a.el.style.transform = `translateY(${a.dy * (1 - p)}px)`;
          }
          break;
        case "count": {
          const val = a.target * p;
          if (a.fmt === "pct") {
            a.el.textContent = Math.round(val) + "%";
          } else if (a.fmt === "num") {
            a.el.textContent = Math.round(val).toLocaleString("en-IN");
          } else {
            a.el.textContent = inr(val);
          }
          break;
        }
        case "zoom": {
          if (isReducedMotion()) {
            a.el.style.transform = "scale(1)";
          } else {
            const z = Math.min(1, Math.max(0, (t - a.start) / Math.max(0.001, a.dur)));
            a.el.style.transform = `scale(${a.from + (a.to - a.from) * z})`;
          }
          break;
        }
        case "fill": {
          const fillTo = (a.to !== undefined) ? a.to : 1;
          a.el.style.transform = `scaleX(${fillTo * p})`;
          a.el.style.transformOrigin = "left center";
          break;
        }
        case "slide": {
          const dx = (isReducedMotion() ? 0 : (a.dx || 0)) * (1 - p);
          const dy = (isReducedMotion() ? 0 : (a.dy || 0)) * (1 - p);
          a.el.style.opacity = p;
          a.el.style.transform = `translate(${dx}px, ${dy}px)`;
          break;
        }
        case "strike": {
          a.el.style.width = `${p * 100}%`;
          break;
        }
        case "glow": {
          a.el.style.boxShadow = `0 0 ${p * 24}px rgba(79, 70, 229, ${p * 0.35})`;
          a.el.style.borderColor = `rgba(79, 70, 229, ${0.2 + p * 0.8})`;
          a.el.style.backgroundColor = `rgba(224, 231, 255, ${p * 0.25})`;
          break;
        }
        case "tween": {
          const easeFn = (typeof PRESETS !== "undefined" && PRESETS.EASE_EXTRA && PRESETS.EASE_EXTRA[a.ease])
            ? PRESETS.EASE_EXTRA[a.ease]
            : (EASE[a.ease || "out"] || EASE.out);
          const ep = easeFn(progLinear(t, a.start, a.dur));
          const D = { x: 0, y: 0, rot: 0, s: 1, o: 1, clip: 1 };
          const L = (valA, valB, pos) => valA + (valB - valA) * pos;
          const f = Object.assign({}, D, a.from);
          const g = Object.assign({}, D, a.to);
          const reduce = isReducedMotion();
          const y = reduce ? 0 : L(f.y, g.y, ep);
          const sc = reduce ? 1 : L(f.s, g.s, ep);
          a.el.style.transform = `translate(${L(f.x, g.x, ep)}cqw, ${y}cqw) rotate(${L(f.rot, g.rot, ep)}deg) scale(${sc})`;
          a.el.style.opacity = Math.max(0, Math.min(1, L(f.o, g.o, ep)));
          a.el.style.clipPath = `inset(0 ${(1 - L(f.clip, g.clip, ep)) * 100}% 0 0)`;
          break;
        }
        case "swap":
          a.el.dataset.state = t >= a.start ? "b" : "a";
          break;
      }
    }

    if (this.isDebug && this.debugHud) {
      this.debugText.textContent = `t=${t.toFixed(2)}s | B${active + 1}`;
      this.debugDot.style.opacity = debugAnchorTriggered ? "1.0" : "0.25";
      this.debugDot.style.background = debugAnchorTriggered ? "#FACC15" : "#4ADE80";
    }

    if (this.caption) {
      this.caption.textContent = b.voice_sync_text || "";
    }

    const dur = this.sp.duration_sec || this.audio.duration || 1;
    if (this.bar) {
      this.bar.style.width = Math.min(100, Math.max(0, 100 * t / dur)) + "%";
    }

    if (this.scrub && !this.scrub.matches(":active")) {
      this.scrub.value = t;
    }

    if (this.timeText) {
      const fmt = s => {
        const m = Math.floor(s / 60);
        const sec = Math.floor(s % 60);
        return m + ":" + (sec < 10 ? "0" : "") + sec;
      };
      this.timeText.textContent = `${fmt(t)} / ${fmt(dur)}`;
    }
  }

  destroy() {
    cancelAnimationFrame(this.raf);
    this.audio.pause();
    window.removeEventListener("keydown", this.keyHandler);
  }
}

window.Explainer = Explainer;
window.TEMPLATES = TEMPLATES;
window.LAYOUTS = Object.keys(TEMPLATES);

window.EXPLAINER_SCREENPLAYS = window.EXPLAINER_SCREENPLAYS || {};
window.EXPLAINER_SCREENPLAYS["dt-c2-q14"] = {
  "question_id": "dt-c2-q14",
  "audio_url": "data/audio/dt-c2-q14.mp3",
  "duration_sec": 46.2,
  "sync_offset_sec": 0.0,
  "context_pill": "§ 45(2) · Conversion into Stock-in-Trade",
  "beats": [
    {
      "id": "b1",
      "layout": "headline",
      "start": 0.0,
      "end": 6.0,
      "voice_sync_text": "Section 45(2) പ്രകാരം ഒരു Capital Asset, Stock-in-trade ആയി convert ചെയ്യുമ്പോൾ transfer നടക്കുന്നു.",
      "title": { "text": "[[Section 45(2)]]", "at": 0.4 },
      "subtitle": { "text": "Capital asset becomes stock-in-trade, and the tax is [[deferred]] until sale.", "at": 1.6 }
    },
    {
      "id": "b2",
      "layout": "timeline",
      "start": 6.0,
      "end": 16.0,
      "voice_sync_text": "പക്ഷെ tax levy ചെയ്യുന്നത് conversion നടക്കുന്ന വർഷമല്ല, മറിച്ച് ആ stock യഥാർത്ഥത്തിൽ വിൽക്കുന്ന മുൻവർഷത്തിലാണ്.",
      "axis_at": 6.3,
      "arrow_at": 9.4,
      "nodes": [
        {
          "side": "left",
          "at": 6.8,
          "title": "Conversion Year",
          "sub": "(2024-25)",
          "tone": "accent",
          "chips": [
            { "text": "Deemed Transfer", "at": 7.8 },
            { "text": "Tax Parked · ₹ 0 Tax", "at": 8.6 }
          ]
        },
        {
          "side": "right",
          "at": 11.0,
          "title": "Actual Sale Year",
          "sub": "(2025-26)",
          "tone": "ok",
          "chips": [
            { "text": "Stock Sold", "at": 12.0 },
            { "text": "Tax Crystallized!", "at": 13.0, "emphasis": true }
          ]
        }
      ]
    },
    {
      "id": "b3",
      "layout": "scene",
      "start": 16.0,
      "end": 24.0,
      "voice_sync_text": "ഒരു practical example നോക്കാം. Rahul 2010-ൽ ₹ 10 Lakhs-ന് വാങ്ങിയ prime land, P.Y. 2024-25-ൽ convert ചെയ്യുന്നു.",
      "image_url": "data/img/dt-c2-q14-b3.svg",
      "zoom": [1.0, 1.06],
      "tags": [
        { "label": "Cost of land", "value": 1000000, "at": 17.6, "tone": "accent", "pos": "top-left" },
        { "label": "Fair market value on conversion", "value": 4500000, "at": 19.6, "tone": "ok", "pos": "mid-right" }
      ]
    },
    {
      "id": "b4",
      "layout": "split",
      "start": 24.0,
      "end": 32.0,
      "voice_sync_text": "Stock ₹ 65 Lakhs-ന് വിൽക്കുമ്പോൾ dual taxation split വരുന്നു: Capital Gain ₹ 26.5L, Business Profit ₹ 20L.",
      "title": { "text": "Two heads of income, [[one year of sale]]", "at": 24.3 },
      "cards": [
        { "kicker": "Capital gains", "title": "u/s 45(2)", "value": 2650000, "note": "FMV on conversion − indexed cost", "at": 25.6, "tone": "accent" },
        { "kicker": "Business income", "title": "u/s 28", "value": 2000000, "note": "Sale price − FMV on conversion", "at": 27.4, "tone": "ok" }
      ]
    },
    {
      "id": "b5",
      "layout": "trap",
      "start": 32.0,
      "end": 40.0,
      "voice_sync_text": "Section 54EC exemption-ൽ 6 months count ചെയ്യേണ്ടത് conversion മുതലല്ല, stock വിൽക്കുന്ന തീയതി മുതലാണെന്ന് Circular 791 വ്യക്തമാക്കുന്നു.",
      "title": { "text": "Exam trap: gain is [[not taxed]] at conversion", "at": 32.3 },
      "cards": [
        { "tone": "bad", "kicker": "Common mistake", "text": "Taxing the gain in the year of conversion", "at": 34.0 },
        { "tone": "good", "kicker": "Correct rule", "text": "Capital gain is charged in the year the stock is sold", "at": 36.4 }
      ]
    },
    {
      "id": "b6",
      "layout": "takeaway",
      "start": 40.0,
      "end": 46.2,
      "voice_sync_text": "അതുകൊണ്ട് ഓർക്കുക: Section 45(2) പ്രകാരം Tax is deferred, not avoided.",
      "title": { "text": "Tax is [[deferred]], not avoided.", "at": 40.4 }
    }
  ]
};

FIXTURES["test_fixture_all_layouts"] = {
  "question_id": "test_fixture_all_layouts",
  "audio_url": "data/audio/dt-c2-q14.mp3",
  "duration_sec": 65.0,
  "sync_offset_sec": 0.0,
  "context_pill": "Test Suite ? All 13 Layouts Parity Fixture",
  "fallback": false,
  "meta": {
    "concept": "Comprehensive test fixture verifying all 13 layout templates",
    "mechanism": {
      "primary": "threshold",
      "secondary": [
        "date_cutoff",
        "computation"
      ]
    }
  },
  "beats": [
    {
      "id": "b1",
      "layout": "headline",
      "start": 0.0,
      "end": 5.0,
      "purpose": "Verify headline layout",
      "serves": [
        "p1"
      ],
      "voice_sync_text": "Headline test beat with title and subtitle.",
      "title": {
        "text": "[[Section 54]] Test Headline",
        "at": 0.5
      },
      "subtitle": {
        "text": "Testing word reveal and marker sweep",
        "at": 1.5
      }
    },
    {
      "id": "b2",
      "layout": "timeline",
      "start": 5.0,
      "end": 10.0,
      "purpose": "Verify timeline layout with spans and x coordinates",
      "serves": [
        "p2"
      ],
      "voice_sync_text": "Timeline test beat with span windows.",
      "axis_at": 5.2,
      "arrow_at": 6.5,
      "spans": [
        {
          "text": "Exemption Window",
          "from_x": 0.2,
          "to_x": 0.8,
          "tone": "accent",
          "at": 5.5
        }
      ],
      "nodes": [
        {
          "x": 0.2,
          "side": "left",
          "tone": "accent",
          "title": "2024",
          "sub": "Purchase",
          "at": 5.6,
          "chips": [
            {
              "text": "Step 1",
              "at": 6.0
            }
          ]
        },
        {
          "x": 0.8,
          "side": "right",
          "tone": "ok",
          "title": "2026",
          "sub": "Sale",
          "at": 7.0,
          "chips": [
            {
              "text": "Step 2",
              "at": 7.4
            }
          ]
        }
      ]
    },
    {
      "id": "b3",
      "layout": "scene",
      "start": 10.0,
      "end": 15.0,
      "purpose": "Verify scene layout with count tag",
      "serves": [
        "p3"
      ],
      "voice_sync_text": "Scene test beat with image zoom.",
      "image_url": "data/img/dt-c2-q14-b3.svg",
      "zoom": [
        1.0,
        1.03
      ],
      "tags": [
        {
          "pos": "bottom-left",
          "label": "Test Property",
          "value": 1500000,
          "at": 10.5,
          "fmt": "inr"
        }
      ]
    },
    {
      "id": "b4",
      "layout": "split",
      "start": 15.0,
      "end": 20.0,
      "purpose": "Verify split layout",
      "serves": [
        "p4"
      ],
      "voice_sync_text": "Split computation dual cards.",
      "title": {
        "text": "Dual Head [[Split]]",
        "at": 15.2
      },
      "cards": [
        {
          "tone": "accent",
          "kicker": "LTCG",
          "title": "Gain",
          "value": 2500000,
          "note": "Section 45",
          "at": 15.6,
          "fmt": "inr"
        },
        {
          "tone": "ok",
          "kicker": "PGBP",
          "title": "Profit",
          "value": 1000000,
          "note": "Section 28",
          "at": 17.0,
          "fmt": "inr"
        }
      ]
    },
    {
      "id": "b5",
      "layout": "trap",
      "start": 20.0,
      "end": 25.0,
      "purpose": "Verify trap layout",
      "serves": [
        "p5"
      ],
      "voice_sync_text": "Exam trap comparison.",
      "title": {
        "text": "Common [[Mistake]]",
        "at": 20.2
      },
      "cards": [
        {
          "tone": "bad",
          "kicker": "Wrong",
          "text": "Tax on conversion date",
          "at": 20.6
        },
        {
          "tone": "good",
          "kicker": "Correct",
          "text": "Tax on sale date",
          "at": 22.0
        }
      ]
    },
    {
      "id": "b6",
      "layout": "fork",
      "start": 25.0,
      "end": 30.0,
      "purpose": "Verify fork layout (date_cutoff)",
      "serves": [
        "p6"
      ],
      "voice_sync_text": "Cut-off date dividing line test.",
      "title": {
        "text": "Cut-off [[1st April 2014]]",
        "at": 25.2
      },
      "divider": {
        "text": "1st April 2014 dividing line",
        "at": 25.4
      },
      "branches": [
        {
          "side": "left",
          "label": "Before 01-04-2014",
          "facts": [
            {
              "text": "Advance forfeited",
              "at": 26.0
            }
          ],
          "outcome": {
            "text": "Deduct from cost",
            "at": 27.0
          }
        },
        {
          "side": "right",
          "label": "On or after 01-04-2014",
          "facts": [
            {
              "text": "Advance forfeited",
              "at": 26.5
            }
          ],
          "outcome": {
            "text": "Taxable u/s 56(2)(ix)",
            "at": 27.5
          }
        }
      ],
      "active": {
        "side": "left",
        "at": 28.0
      }
    },
    {
      "id": "b7",
      "layout": "meter",
      "start": 30.0,
      "end": 35.0,
      "purpose": "Verify meter layout (threshold)",
      "serves": [
        "p7"
      ],
      "voice_sync_text": "Threshold meter test.",
      "title": {
        "text": "Section 54 [[Threshold Meter]]",
        "at": 30.2
      },
      "limit": {
        "text": "Statutory Limit",
        "value": 20000000,
        "at": 30.4
      },
      "reading": {
        "text": "Current Capital Gain",
        "value": 3425000,
        "at": 31.0,
        "fmt": "inr"
      },
      "outcome": {
        "text": "Two houses unlocked",
        "at": 32.5,
        "tone": "ok"
      }
    },
    {
      "id": "b8",
      "layout": "ledger",
      "start": 35.0,
      "end": 40.0,
      "purpose": "Verify ledger layout (computation)",
      "serves": [
        "p8"
      ],
      "voice_sync_text": "Computation ledger calculation rows.",
      "title": {
        "text": "Taxable LTCG [[Ledger]]",
        "at": 35.2
      },
      "rows": [
        {
          "label": "Full Value of Consideration",
          "value": 4300000,
          "sign": "plus",
          "at": 35.5,
          "fmt": "inr"
        },
        {
          "label": "Less: Cost of Acquisition",
          "value": 875000,
          "sign": "minus",
          "at": 36.5,
          "fmt": "inr"
        },
        {
          "label": "Less: Section 54 Exemption",
          "value": 1200000,
          "sign": "minus",
          "at": 37.5,
          "fmt": "inr"
        }
      ],
      "total": {
        "label": "Taxable Long Term Capital Gain",
        "value": 2225000,
        "at": 38.0,
        "fmt": "inr"
      }
    },
    {
      "id": "b9",
      "layout": "case_card",
      "start": 40.0,
      "end": 45.0,
      "purpose": "Verify case_card layout (precedent)",
      "serves": [
        "p9"
      ],
      "voice_sync_text": "Judicial precedent case law card.",
      "title": {
        "text": "Landmark [[Judicial Precedent]]",
        "at": 40.2
      },
      "case": {
        "text": "Balraj v. CIT (2002)",
        "at": 40.5
      },
      "court": {
        "text": "Delhi High Court",
        "at": 41.0
      },
      "gap": {
        "text": "Unregistered agreement with possession",
        "at": 41.5
      },
      "principle": {
        "text": "Legal registered title is [[not mandatory]] if full consideration is paid",
        "at": 42.0
      },
      "effect": {
        "text": "Section 54 deduction fully allowed",
        "at": 43.0
      }
    },
    {
      "id": "b10",
      "layout": "compare",
      "start": 45.0,
      "end": 50.0,
      "purpose": "Verify compare layout (classification)",
      "serves": [
        "p10"
      ],
      "voice_sync_text": "Comparison table columns.",
      "title": {
        "text": "Classification [[Comparison]]",
        "at": 45.2
      },
      "columns": [
        {
          "title": "Old Regime",
          "at": 45.5,
          "rows": [
            {
              "label": "Exemption",
              "text": "? 2.5 Lakhs",
              "at": 46.0
            }
          ]
        },
        {
          "title": "New Regime",
          "at": 46.5,
          "rows": [
            {
              "label": "Exemption",
              "text": "? 3.0 Lakhs",
              "at": 47.0
            }
          ]
        }
      ],
      "highlight": [
        {
          "row": 0,
          "at": 48.0
        }
      ]
    },
    {
      "id": "b11",
      "layout": "checklist",
      "start": 50.0,
      "end": 55.0,
      "purpose": "Verify checklist layout (condition_chain)",
      "serves": [
        "p11"
      ],
      "voice_sync_text": "Condition chain checklist.",
      "title": {
        "text": "Eligibility [[Checklist]]",
        "at": 50.2
      },
      "items": [
        {
          "text": "Individual or HUF assessee",
          "result": "pass",
          "at": 50.8
        },
        {
          "text": "Long term capital asset transferred",
          "result": "pass",
          "at": 51.8
        },
        {
          "text": "New house within statutory period",
          "result": "pass",
          "at": 52.8
        }
      ]
    },
    {
      "id": "b12",
      "layout": "statute_quote",
      "start": 55.0,
      "end": 60.0,
      "purpose": "Verify statute_quote layout",
      "serves": [
        "p12"
      ],
      "voice_sync_text": "Statutory verbatim extract.",
      "title": {
        "text": "Bare Act [[Extract]]",
        "at": 55.2
      },
      "quote": {
        "text": "Where the amount of the capital gain [[does not exceed two crore rupees]], the assessee may, at his option, purchase two residential houses in India.",
        "at": 55.5
      }
    },
    {
      "id": "b13",
      "layout": "takeaway",
      "start": 60.0,
      "end": 65.0,
      "purpose": "Verify takeaway layout",
      "serves": [
        "p13"
      ],
      "voice_sync_text": "Closing takeaway axiom.",
      "title": {
        "text": "Compliance is [[absolute]], not discretionary.",
        "at": 60.5
      }
    }
  ]
};
window.EXPLAINER_SCREENPLAYS["test_fixture_all_layouts"] = FIXTURES["test_fixture_all_layouts"];

window.EXPLAINER_SCREENPLAYS["ch2_q14"] = window.EXPLAINER_SCREENPLAYS["dt-c2-q14"];

FIXTURES["dt-c2-q25"] = {
  "question_id": "dt-c2-q25",
  "audio_url": "data/audio/dt-c2-q25.mp3",
  "duration_sec": 203.28,
  "sync_offset_sec": 0.0,
  "context_pill": "§ 54 · Two Residential Houses & § 51 Advance Forfeiture",
  "fallback": false,
  "beats": [
    {
      "id": "b1",
      "layout": "fork",
      "start": 0.0,
      "end": 40.73,
      "voice_sync_text": "സെക്ഷൻ 51-ന്റെ പ്രൊവിഷൻ മനസ്സിലാക്കാൻ നമുക്ക് ഹരിയുടെ ഒരു സിമ്പിൾ എക്സാമ്പിൾ നോക്കാം. ഹരി 2002-ൽ 9 ലക്ഷം രൂപയ്ക്ക് ഡൽഹിയിൽ ഒരു റെസിഡൻഷ്യൽ ഹൗസ് വാങ്ങി. 2005 മെയ് മാസത്തിൽ പരി എന്ന ബയറുമായി നെഗോഷ്യേഷൻ നടത്തുമ്പോൾ 25,000 രൂപ അഡ്വാൻസ് മണി വാങ്ങി. പക്ഷെ പിന്നീട് ആ ഡീൽ കാൻസലാവുകയും ഹരി ആ അഡ്വാൻസ് ഫോർഫീറ്റ് ചെയ്യുകയും ചെയ്തു. ഇവിടെ ഒരു കട്ട്-ഓഫ് ഡേറ്റ് ഓർക്കുക: ഒന്നാം തീയതി ഏപ്രിൽ 2014-ന് മുൻപാണ് ഫോർഫീച്ചർ എങ്കിൽ, സെക്ഷൻ 51 പ്രകാരം അത് കോസ്റ്റ് ഓഫ് അക്വിസിഷനിൽ നിന്ന് കുറയ്ക്കണം! അതുകൊണ്ട് ഹരിയുടെ അഡ്ജസ്റ്റഡ് കോസ്റ്റ് 9 ലക്ഷത്തിൽ നിന്ന് 25,000 കുറച്ച് 8 ലക്ഷത്തി 75,000 രൂപയായി മാറുന്നു!",
      "title": {
        "text": "Section 51 · Advance Money Forfeiture Cut-off",
        "at": 0.3
      },
      "story_steps": [
        {
          "badge": "Year 2002",
          "title": "Delhi House Acquisition",
          "sub": "Hari purchased residential house in Delhi",
          "val": 900000,
          "at": 4.8
        },
        {
          "badge": "May 2005",
          "title": "Negotiation with Pari",
          "sub": "Agreement to sell & advance money received",
          "val": 25000,
          "at": 10.5
        },
        {
          "badge": "Deal Cancelled",
          "title": "Advance Forfeited by Hari",
          "sub": "Kept advance upon buyer default u/s 51",
          "val": 25000,
          "at": 18.0
        }
      ],
      "divider": {
        "text": "Forfeiture Cut-off Date: 01-04-2014",
        "at": 22.8
      },
      "branches": [
        {
          "side": "left",
          "label": "Before 01-04-2014 (Hari's Case: May 2005)",
          "facts": [
            {
              "text": "Deduct from Cost of Acquisition u/s 51",
              "at": 29.8
            }
          ],
          "outcome": {
            "text": "Reduces Cost of Acquisition",
            "at": 31.5
          }
        },
        {
          "side": "right",
          "label": "On/After 01-04-2014",
          "facts": [
            {
              "text": "Taxable under IFOS u/s 56(2)(ix)",
              "at": 27.0
            }
          ],
          "outcome": {
            "text": "Income from Other Sources (No Cost Reduction)",
            "at": 28.5
          }
        }
      ],
      "active": {
        "side": "left",
        "at": 29.8
      },
      "example": {
        "name": "Mr. Hari",
        "role": "Adjusted Cost Result",
        "text": "Section 51 Computation: Cost ₹ 9,00,000 − Advance Forfeited ₹ 25,000 = Adjusted Cost ₹ 8,75,000!",
        "at": 33.5
      },
      "style": "zoom_in.color_shift.calm",
      "serves": [
        "p1",
        "p2",
        "c1",
        "c2",
        "f2",
        "d1",
        "n3",
        "t1"
      ]
    },
    {
      "id": "b2",
      "layout": "statute_quote",
      "start": 40.98,
      "end": 78.51,
      "voice_sync_text": "ഇനി 2025 ജൂൺ മാസത്തിൽ ഹരി ഈ വീട് 43 ലക്ഷം രൂപയ്ക്ക് വിൽക്കുന്നു. അപ്പോൾ ഹരിയുടെ ലോങ്-ടേം ക്യാപിറ്റൽ ഗെയിൻ വരുന്നത് 43 ലക്ഷം മൈനസ് 8 ലക്ഷത്തി 75,000, അതായത് 34 ലക്ഷത്തി 25,000 രൂപ! ഇവിടെ ഹരി ചോദിക്കുന്നു: 'എനിക്ക് സെക്ഷൻ 54 പ്രകാരം ഒരു വീടിന് പകരം രണ്ട് റെസിഡൻഷ്യൽ വീടുകൾ വാങ്ങി എക്സംപ്ഷൻ ക്ലെയിം ചെയ്യാൻ പറ്റുമോ?' സെക്ഷൻ 54 സബ് സെക്ഷൻ ഒന്നിന്റെ ഫസ്റ്റ് പ്രൊവൈസോ പറയുന്നത് നോക്കൂ: ക്യാപിറ്റൽ ഗെയിൻ രണ്ട് കോടി രൂപയിൽ കവിയുന്നില്ലെങ്കിൽ, അസ്സസ്സീക്ക് ഇന്ത്യയിൽ രണ്ട് റെസിഡൻഷ്യൽ വീടുകൾ വാങ്ങാനുള്ള സ്റ്റാറ്റ്യൂട്ടറി ഓപ്ഷൻ ലഭിക്കും!",
      "title": {
        "text": "Section 54(1) · First Proviso: Two Residential Houses",
        "at": 41.2
      },
      "sale_card": {
        "sale_lbl": "Full Value of Consideration (June 2025)",
        "sale_val": 4300000,
        "cost_lbl": "Less: Adjusted Cost u/s 51",
        "cost_val": 875000,
        "gain_lbl": "Gross LTCG Generated",
        "gain_val": 3425000,
        "at": 42.5
      },
      "example": {
        "name": "Mr. Hari",
        "role": "Assessee Question",
        "text": "Can I purchase TWO residential houses in India and claim Section 54 exemption?",
        "at": 58.6
      },
      "quote": {
        "text": "Where Capital Gain ≤ [[₹ 2.00 Crore]], Assessee may purchase or construct [[two residential houses in India]] (Once-in-a-lifetime option).",
        "at": 67.5
      },
      "style": "fade.pulse.snappy",
      "serves": [
        "p3",
        "c3",
        "n6",
        "t3"
      ]
    },
    {
      "id": "b3",
      "layout": "meter",
      "start": 78.76,
      "end": 100.41,
      "voice_sync_text": "ഇവിടെ നമ്മുടെ ത്രെഷോൾഡ് മീറ്റർ നോക്കൂ! സ്റ്റാറ്റ്യൂട്ടറി ലിമിറ്റ് രണ്ട് കോടി രൂപയാണ്. ഹരിയുടെ ക്യാപിറ്റൽ ഗെയിൻ എത്രയാണ്? വെറും 34 ലക്ഷത്തി 25,000 രൂപ മാത്രം! ഇത് രണ്ട് കോടി രൂപയേക്കാൾ വളരെ താഴെയാണ്. അതുകൊണ്ട് ദാ, നമ്മുടെ പാഡ്‌ലോക്ക് ഓപ്പൺ ആയി! ഹരിക്ക് ജീവിതത്തിൽ ഒരിക്കൽ മാത്രം ലഭിക്കുന്ന ടു റെസിഡൻഷ്യൽ ഹൗസസ് ഓപ്ഷൻ ഇവിടെ അൺലോക്ക് ആയിരിക്കുന്നു!",
      "title": {
        "text": "Section 54 Statutory Threshold Gauge",
        "at": 79.0
      },
      "limit": {
        "text": "Statutory Ceiling Limit",
        "value": 20000000,
        "at": 81.0
      },
      "reading": {
        "text": "Hari's Long-Term Capital Gain",
        "value": 3425000,
        "at": 84.5,
        "fmt": "inr"
      },
      "outcome": {
        "text": "₹ 34.25 Lakhs ≤ ₹ 2.00 Crore · THRESHOLD SATISFIED",
        "tone": "ok",
        "at": 90.0
      },
      "padlock": {
        "text": "Capital Gain ₹ 34.25L ≤ ₹ 2.00 Crore: TWO HOUSES OPTION UNLOCKED!",
        "at": 92.5
      },
      "example": {
        "name": "Mr. Hari",
        "role": "Threshold Qualified",
        "text": "Once-in-a-lifetime option unlocked! Entitled to claim exemption for 2 residential houses in India.",
        "at": 95.5
      },
      "style": "slide_down.glow.snappy",
      "serves": [
        "c3",
        "n5",
        "n6"
      ]
    },
    {
      "id": "b4",
      "layout": "case_card",
      "start": 100.66,
      "end": 140.83,
      "voice_sync_text": "ഹരി രണ്ട് വീടുകൾ വാങ്ങി. ഒന്ന് ചെന്നൈയിൽ 5 ലക്ഷം രൂപയ്ക്ക്, മറ്റൊന്ന് ഡൽഹിയിൽ 7 ലക്ഷം രൂപയ്ക്ക്. പക്ഷെ ഇവിടെ ഒരു വലിയ പ്രശ്നം വന്നു! ഡൽഹിയിലെ വീടിന്റെ മുഴുവൻ തുകയും നൽകി ഹരി കൈവശം വെച്ചെങ്കിലും, അതിന്റെ സെയിൽ ഡീഡ് രജിസ്റ്റർ ചെയ്തിട്ടില്ല! അസ്സസ്സിങ് ഓഫീസർ ചോദിക്കുന്നു: 'രജിസ്ട്രേഷൻ ഇല്ലാത്ത വീടിന് എങ്ങനെ സെക്ഷൻ 54 കൊടുക്കും?' ഇവിടെയാണ് ഡൽഹി ഹൈക്കോടതിയുടെ ലാൻഡ്മാർക്ക് കേസായ ബൽരാജ് വേഴ്സസ് സി.ഐ.ടി. വരുന്നത്! കോടതി വ്യക്തമാക്കി: സെക്ഷൻ 53A പ്രകാരം പൊസഷനും മുഴുവൻ പെയ്മെന്റും ഉണ്ടെങ്കിൽ സബ്സ്റ്റാൻഷ്യൽ ഓണർഷിപ്പ് ആയി. അതിനാൽ രജിസ്റ്റേർഡ് ഡീഡ് ഇല്ലെങ്കിലും ഡൽഹി വീടിന് സെക്ഷൻ 54 എക്സംപ്ഷൻ പൂർണ്ണമായും ലഭിക്കും!",
      "title": {
        "text": "Judicial Precedent · Section 54 Legal Title",
        "at": 101.0
      },
      "houses": [
        {
          "location": "Chennai House",
          "status": "House 1 · Registered Sale Deed",
          "cost": 500000,
          "at": 102.5
        },
        {
          "location": "Delhi House",
          "status": "House 2 · Possession Taken, Full Payment Paid",
          "cost": 700000,
          "at": 105.0
        },
        {
          "location": "Total Section 54 Exemption",
          "status": "Exemption Allowed for Both Houses",
          "cost": 1200000,
          "isTotal": true,
          "at": 134.0
        }
      ],
      "gap": {
        "text": "AO Objection: Delhi house deed was unregistered on 31-03-2026. Can Section 54 exemption be disallowed?",
        "at": 108.5
      },
      "case": {
        "text": "Balraj v. CIT (2002) 254 ITR 22",
        "at": 118.5
      },
      "court": {
        "text": "Delhi High Court Benchmark",
        "at": 119.5
      },
      "principle": {
        "text": "Section 53A TPA possession and full consideration constitute substantial ownership for Section 54 without registered deed.",
        "at": 122.5
      },
      "effect": {
        "text": "Exemption ALLOWED for Delhi House (₹ 7,00,000) despite lack of registered conveyance.",
        "at": 128.5
      },
      "style": "whip_left.shake.calm",
      "serves": [
        "c4",
        "f4",
        "cl1",
        "cl2",
        "t2"
      ]
    },
    {
      "id": "b5",
      "layout": "ledger",
      "start": 141.08,
      "end": 180.05,
      "voice_sync_text": "ഇനി ഫൈനൽ ക്യാപിറ്റൽ ഗെയിൻസ് ലെഡ്ജർ നോക്കാം. ഫുൾ വാല്യൂ ഓഫ് കൺസിഡറേഷൻ 43 ലക്ഷം രൂപ. ലെസ്സ്: അഡ്ജസ്റ്റഡ് കോസ്റ്റ് ഓഫ് അക്വിസിഷൻ 8 ലക്ഷത്തി 75,000 രൂപ. ഗ്രോസ് ലോങ്-ടേം ക്യാപിറ്റൽ ഗെയിൻ 34 ലക്ഷത്തി 25,000 രൂപ. ഇനി ഇതിൽ നിന്ന് രണ്ട് വീടുകളുടെയും എക്സംപ്ഷൻ കുറയ്ക്കാം: ഡൽഹി വീടിന് 7 ലക്ഷം, ചെന്നൈ വീടിന് 5 ലക്ഷം. ആകെ എക്സംപ്ഷൻ 12 ലക്ഷം രൂപ! ബാക്കി വരുന്ന തുക നോക്കൂ: 34 ലക്ഷത്തി 25,000-ൽ നിന്ന് 12 ലക്ഷം കുറച്ചാൽ കൃത്യം 22 ലക്ഷത്തി 25,000 രൂപ! സ്റ്റുഡന്റ്സ് ഓർക്കുക, ഈ 22 ലക്ഷത്തി 25,000 രൂപ ടാക്സബിൾ ലോങ്-ടേം ക്യാപിറ്റൽ ഗെയിൻ ആണ്!",
      "title": {
        "text": "Statutory Capital Gains Ledger",
        "at": 141.4
      },
      "rows": [
        {
          "sign": "plus",
          "label": "Full Value of Consideration (Sold June 2025)",
          "value": 4300000,
          "at": 144.0,
          "fmt": "inr"
        },
        {
          "sign": "minus",
          "label": "Less: Adjusted Cost u/s 51 (₹ 9,00,000 − ₹ 25,000)",
          "value": 875000,
          "at": 148.2,
          "fmt": "inr"
        },
        {
          "sign": "plus",
          "label": "Gross Long-Term Capital Gain",
          "value": 3425000,
          "at": 152.2,
          "fmt": "inr"
        },
        {
          "sign": "minus",
          "label": "Less: Delhi House Exemption (Balraj v. CIT)",
          "value": 700000,
          "at": 158.8,
          "fmt": "inr"
        },
        {
          "sign": "minus",
          "label": "Less: Chennai House Exemption (Second House)",
          "value": 500000,
          "at": 161.2,
          "fmt": "inr"
        }
      ],
      "total": {
        "label": "Taxable Long-Term Capital Gain",
        "value": 2225000,
        "at": 168.0,
        "fmt": "inr"
      },
      "callout": {
        "badge": "Taxable Remainder",
        "text": "Remaining ₹ 22,25,000 is fully taxable LTCG! Exemption is capped to ₹ 12,00,000 actual investment.",
        "at": 174.8
      },
      "style": "slide_up.shimmer.calm",
      "serves": [
        "c1",
        "c2",
        "c3",
        "c4",
        "f1",
        "f2",
        "f3",
        "f4"
      ]
    },
    {
      "id": "b6",
      "layout": "takeaway",
      "start": 180.3,
      "end": 203.27,
      "voice_sync_text": "അതുകൊണ്ട് എക്സാമിനായി മൂന്ന് ഗോൾഡൻ റൂൾസ് എപ്പോഴും ഓർക്കുക: ഒന്ന്, 2014-ന് മുൻപുള്ള അഡ്വാൻസ് ഫോർഫീച്ചർ കോസ്റ്റ് കുറയ്ക്കുന്നു. രണ്ട്, ക്യാപിറ്റൽ ഗെയിൻ രണ്ട് കോടിയിൽ താഴെയാണെങ്കിൽ രണ്ട് വീടുകൾക്ക് എക്സംപ്ഷൻ ക്ലെയിം ചെയ്യാം. മൂന്ന്, രജിസ്ട്രേഷൻ പൂർത്തിയായില്ലെങ്കിലും സബ്സ്റ്റാൻഷ്യൽ ഓണർഷിപ്പ് ഉണ്ടെങ്കിൽ സെക്ഷൻ 54 ലഭിക്കും. ബാക്കി വരുന്ന ഗെയിൻ കൃത്യമായി ടാക്സ് ചെയ്യപ്പെടും!",
      "title": {
        "text": "Exam Summary · 3 Golden Takeaways",
        "at": 180.6
      },
      "points": [
        {
          "num": "1",
          "text": "Advance forfeited before 01-04-2014 reduces Cost of Acquisition u/s 51.",
          "at": 184.5
        },
        {
          "num": "2",
          "text": "Capital Gains ≤ ₹ 2 Crore unlocks exemption for TWO residential houses u/s 54.",
          "at": 189.2
        },
        {
          "num": "3",
          "text": "Possession + full payment qualifies u/s 53A TPA without deed registration (Balraj v. CIT).",
          "at": 195.0
        },
        {
          "num": "★",
          "text": "Taxable Remainder: Remaining ₹ 22.25L is fully taxable LTCG.",
          "at": 200.8
        }
      ],
      "style": "zoom_in.none.calm",
      "serves": [
        "f1",
        "f2",
        "f3",
        "f4"
      ]
    }
  ]
};
FIXTURES["dt_c2_q25"] = FIXTURES["dt-c2-q25"];
FIXTURES["ch2_q25"] = FIXTURES["dt-c2-q25"];
window.EXPLAINER_SCREENPLAYS["dt-c2-q25"] = FIXTURES["dt-c2-q25"];
window.EXPLAINER_SCREENPLAYS["dt_c2_q25"] = FIXTURES["dt-c2-q25"];
window.EXPLAINER_SCREENPLAYS["ch2_q25"] = FIXTURES["dt-c2-q25"];

FIXTURES["dt-c2-q32"] = {
  "question_id": "dt-c2-q32",
  "audio_url": "data/audio/dt-c2-q32.mp3",
  "duration_sec": 199.31,
  "sync_offset_sec": 0.0,
  "context_pill": "Section 54G | Shifting Industrial Undertaking from Urban to Non-Urban Area",
  "fallback": false,
  "beats": [
    {
      "id": "b1",
      "layout": "fork",
      "voice_sync_text": "Makkale, ശ്രദ്ധichu kekkoo! Namukku Section 54G padikkam. Nammude case studyil, Apex Engineering Ltd enna company oru urban corporation limitil ulla industrial undertaking non-urban area-kku December 2025-il shift cheythu. Financial Year 2025-26 (Assessment Year 2026-27)-il avar pala assets transfer cheythu. Onnamathathu, Land transfer cheythu, sale proceeds ₹ 9 lakhs, cost of acquisition ₹ 4 lakhs, long-term capital asset aanu. Randamathathu, Building transfer cheythu, sale proceeds ₹ 17 lakhs, WDV under Section 50 ₹ 5 lakhs, depreciable asset aayathu kondu short-term capital gain aanu. Moonnamathathu, Plant & Machinery transfer cheythu, sale proceeds ₹ 15 lakhs, WDV under Section 50 ₹ 4 lakhs, short-term capital gain aanu. Naalaamathathu, Furniture transfer cheythu, sale proceeds ₹ 4 lakhs, WDV under Section 50 ₹ 2 lakhs. Athayath, ee four assets transfer cheythu, pakshe naye assets purchase cheythappol oru cheriya twist undu! Avar July 2026-il naye assets vaangiyavarku land-in ₹ 4 lakhs, building-in ₹ 6 lakhs, plant & machinery-in ₹ 15 lakhs, pinne furniture-in ₹ 2 lakhs invest cheythu. Ividuthe most important point enthannu vechaal, Section 54G-il furniture oru eligible capital asset alla! Let's classify them clearly!",
      "title": {
        "text": "Complete Scenario Overview & Eligibility Filter u/s 54G",
        "at": 0.3
      },
      "intro_cards": [
        {
          "badge": "Statutory Focus",
          "title": "Section 54G",
          "sub": "Capital Gains on Shifting Industrial Undertaking from Urban to Non-Urban Area",
          "at": 3.16,
          "out_at": 32.08
        },
        {
          "badge": "Case Study Setup",
          "title": "Apex Engineering Ltd",
          "sub": "Industrial Undertaking Shifted from Urban to Non-Urban Area in Dec 2025",
          "at": 6.18,
          "out_at": 32.08
        },
        {
          "badge": "Transfer / Trigger Event",
          "title": "Sale in March 2026 & New Purchase in July 2026",
          "sub": "Assets Transferred: Land, Building, Plant & Machinery, Furniture",
          "at": 23.02,
          "out_at": 32.08
        }
      ],
      "story_steps": [
        {
          "badge": "Asset 1: Land",
          "title": "Sale: ₹ 9,00,000 | Cost: ₹ 4,00,000",
          "sub": "Long-Term Capital Gain: ₹ 5,00,000",
          "val": 500000,
          "at": 32.48
        },
        {
          "badge": "Asset 2: Building",
          "title": "Sale: ₹ 17,00,000 | WDV u/s 50: ₹ 5,00,000",
          "sub": "Short-Term Capital Gain: ₹ 12,00,000",
          "val": 1200000,
          "at": 41.5
        },
        {
          "badge": "Asset 3: Plant & Machinery",
          "title": "Sale: ₹ 15,00,000 | WDV u/s 50: ₹ 4,00,000",
          "sub": "Short-Term Capital Gain: ₹ 11,00,000",
          "val": 1100000,
          "at": 61.6
        },
        {
          "badge": "Asset 4: Furniture",
          "title": "Sale: ₹ 4,00,000 | WDV u/s 50: ₹ 2,00,000",
          "sub": "Short-Term Capital Gain: ₹ 2,00,000",
          "val": 200000,
          "at": 63.42
        }
      ],
      "divider": {
        "text": "Eligibility Classification u/s 54G",
        "at": 80.1
      },
      "branches": [
        {
          "side": "left",
          "label": "Qualifying Assets u/s 54G",
          "facts": [
            {
              "text": "Land (New investment: ₹ 4,00,000)",
              "at": 82.1
            },
            {
              "text": "Building (New investment: ₹ 6,00,000)",
              "at": 83.0
            },
            {
              "text": "Plant & Machinery (New investment: ₹ 15,00,000)",
              "at": 83.9
            },
            {
              "text": "Total Qualifying New Investment Pool = ₹ 25,00,000",
              "at": 84.8
            }
          ],
          "outcome": {
            "text": "Eligible for Section 54G Exemption Deduction",
            "at": 85.7
          },
          "at": 81.1
        },
        {
          "side": "right",
          "label": "Ineligible Asset u/s 54G",
          "facts": [
            {
              "text": "Furniture (New investment: ₹ 2,00,000)",
              "at": 87.6
            },
            {
              "text": "Statutory Exclusion: Furniture is excluded from Section 54G scope",
              "at": 88.5
            },
            {
              "text": "Result: No exemption available for furniture investment",
              "at": 89.4
            }
          ],
          "outcome": {
            "text": "Ineligible / Fully Taxable Short-Term Capital Gain",
            "at": 90.3
          },
          "at": 86.6
        }
      ],
      "result_card": {
        "badge": "Exam Trap Alert",
        "title": "Furniture Exclusion u/s 54G",
        "sub": "Capital gains on transfer of furniture or new investment in furniture never qualifies for Section 54G exemption!",
        "at": 91.2
      },
      "start": 0.0,
      "end": 85.8
    },
    {
      "id": "b2",
      "layout": "statute_quote",
      "voice_sync_text": "Makkale, ormavekkoo! Section 54G condition enna vechaal, oru industrial undertaking urban area-il ninnu non-urban area-kku shift cheyyumpol, transfer nadakkunnathinu 1 year munpulla or 3 years-nu akathalam new machinery, plant, building, or land acquire cheyyanam. Appol capital gain tax exemption kittum!",
      "title": {
        "text": "Statutory Mandate & Conditions u/s 54G",
        "at": 86.45
      },
      "quote": {
        "text": "Where the capital gain arises from the transfer of a capital asset, being machinery or plant or land or building or any rights in building or land used for the purposes of an industrial undertaking... and the assessee has purchased new machinery or plant or acquired building or land within 1 year before or 3 years after the date of transfer, the capital gain shall be dealt with under section 54G.",
        "citation": "Section 54G of the Income-tax Act, 1961",
        "emphasis": "within 1 year before or 3 years after the date of transfer",
        "at": 86.65
      },
      "context_bubble": {
        "badge": "Statutory Condition",
        "speaker": "Section 54G",
        "theme": "Reinvestment Time Horizon",
        "text": "New assets must be purchased within 1 year before or 3 years after the transfer date. Furniture is strictly excluded from eligible assets.",
        "at": 99.29
      },
      "start": 86.15,
      "end": 109.55
    },
    {
      "id": "b3",
      "layout": "meter",
      "voice_sync_text": "Aaduthathayittu, nalkiya new assets investment-inte total pool evide nokku. Land-il ₹ 4 lakhs, Building-il ₹ 6 lakhs, Plant & Machinery-il ₹ 15 lakhs vaangiya total qualifying investment ₹ 25 lakhs aane! Furniture-il vaangiya ₹ 2 lakhs ivide exclude cheyyanam. So total qualifying exemption pool is ₹ 25 lakhs!",
      "title": {
        "text": "Qualifying Reinvestment Pool u/s 54G",
        "at": 110.2
      },
      "meter_display": {
        "min_val": 0,
        "max_val": 3000000,
        "current_val": 2500000,
        "unit": "₹",
        "threshold": 2300000,
        "labels": {
          "start": "₹ 0",
          "threshold_label": "Max Gain Pool: ₹ 23,00,000",
          "current_label": "Qualifying New Investment: ₹ 25,00,000"
        },
        "at": 130.0
      },
      "breakdown": [
        {
          "label": "New Land Investment",
          "val": 400000,
          "status": "Qualifies u/s 54G",
          "at": 115.54
        },
        {
          "label": "New Building Investment",
          "val": 600000,
          "status": "Qualifies u/s 54G",
          "at": 117.9
        },
        {
          "label": "New Plant & Machinery Investment",
          "val": 1500000,
          "status": "Qualifies u/s 54G",
          "at": 119.92
        },
        {
          "label": "New Furniture Investment",
          "val": 200000,
          "status": "Ineligible / Excluded u/s 54G",
          "at": 126.3
        }
      ],
      "outcome": {
        "text": "Total Qualifying Reinvestment = ₹ 25,00,000 (Exceeds total capital gains, so full gains can be absorbed)",
        "tone": "ok",
        "at": 130.42
      },
      "start": 109.9,
      "end": 133.98
    },
    {
      "id": "b4",
      "layout": "ledger",
      "voice_sync_text": "Ippol nammal step-by-step computation cheyyunnu! Short-term capital gain building-um plant & machinery-um koodi total ₹ 23 lakhs aane. Ee ₹ 25 lakhs exemption aadyam short-term capital gains-l adjust cheyyanam. Because short-term capital gain-inte tax incidence high aanu! Appol short-term capital gain completely nil aayi maarum. Pine baakki ulla exemption long-term capital gain-aaya land-inte ₹ 5 lakhs-il ninnu adjust cheythu baakki taxable long-term capital gain ₹ 2 lakhs aayi varum. Pinne furniture-inte ₹ 2 lakhs short-term capital gain fully taxable aanu!",
      "title": {
        "text": "Computation of Taxable Capital Gains for Assessment Year 2026-27",
        "at": 134.63
      },
      "callout": {
        "badge": "Golden Optimization Trick",
        "text": "Always exhaust Section 54G exemption against Short-Term Capital Gains first, since short-term tax rates are higher than long-term tax rates!",
        "at": 135.53
      },
      "ledger_rows": [
        {
          "label": "1. Short-Term Capital Gain: Building",
          "amount": 1200000,
          "type": "income",
          "at": 137.55
        },
        {
          "label": "2. Short-Term Capital Gain: Plant & Machinery",
          "amount": 1100000,
          "type": "income",
          "at": 164.29
        },
        {
          "label": "Subtotal Short-Term Capital Gain (Building + P&M)",
          "amount": 2300000,
          "type": "subtotal",
          "at": 166.05
        },
        {
          "label": "Less: Section 54G Exemption set off against STCG",
          "amount": -2300000,
          "type": "deduction",
          "at": 166.95
        },
        {
          "label": "Net Short-Term Capital Gain (Building & P&M)",
          "amount": 0,
          "type": "subtotal",
          "at": 167.75
        },
        {
          "label": "3. Short-Term Capital Gain: Furniture (Ineligible)",
          "amount": 200000,
          "type": "taxable",
          "at": 168.21
        },
        {
          "label": "4. Long-Term Capital Gain: Land",
          "amount": 500000,
          "type": "income",
          "at": 169.11
        },
        {
          "label": "Less: Balance Section 54G Exemption set off against LTCG",
          "amount": -200000,
          "type": "deduction",
          "at": 170.01
        },
        {
          "label": "Taxable Long-Term Capital Gain (Land)",
          "amount": 300000,
          "type": "taxable",
          "at": 170.91
        }
      ],
      "net_total": {
        "label": "Total Taxable Capital Gains",
        "val": 500000,
        "detail": "Short-Term ₹ 2,00,000 + Long-Term ₹ 3,00,000 = ₹ 5,00,000",
        "at": 171.81
      },
      "start": 134.33,
      "end": 169.93
    },
    {
      "id": "b5",
      "layout": "takeaway",
      "voice_sync_text": "Avasanam, makkale ee 3 Golden Rules exam-il ormakkuvuka! Onnamathathu, Furniture is never an eligible asset under Section 54G. Randamathathu, always exhaust exemption against Short-Term Capital Gains first for maximum tax saving. Moonnamathathu, depreciable assets-inte WDV is deemed cost under Section 50. Superb, eppol makkalkku Section 54G clear aayille!",
      "title": {
        "text": "3 Golden Rules for CA Final Exam Mastery u/s 54G",
        "at": 170.58
      },
      "rules": [
        {
          "num": "01",
          "heading": "Furniture Exclusion Rule",
          "body": "Capital gains on transfer of furniture or investment in new furniture never qualifies for exemption under Section 54G.",
          "at": 176.38
        },
        {
          "num": "02",
          "heading": "Set-off Priority Optimization",
          "body": "Always exhaust Section 54G exemption first against Short-Term Capital Gains before Long-Term Capital Gains to minimize tax liability.",
          "at": 182.14
        },
        {
          "num": "03",
          "heading": "Depreciable Assets & Section 50",
          "body": "For depreciable assets forming part of a block, capital gains are computed under Section 50 where WDV is treated as the cost of acquisition.",
          "at": 190.06
        }
      ],
      "start": 170.28,
      "end": 198.96
    }
  ]
};
FIXTURES["dt_c2_q32"] = FIXTURES["dt-c2-q32"];
FIXTURES["ch2_q32"] = FIXTURES["dt-c2-q32"];
window.EXPLAINER_SCREENPLAYS["dt-c2-q32"] = FIXTURES["dt-c2-q32"];
window.EXPLAINER_SCREENPLAYS["dt_c2_q32"] = FIXTURES["dt-c2-q32"];
window.EXPLAINER_SCREENPLAYS["ch2_q32"] = FIXTURES["dt-c2-q32"];

FIXTURES["dt_c2_q34"] = FIXTURES["dt-c2-q34"];
FIXTURES["ch2_q34"] = FIXTURES["dt-c2-q34"];
window.EXPLAINER_SCREENPLAYS["dt-c2-q34"] = FIXTURES["dt-c2-q34"];
window.EXPLAINER_SCREENPLAYS["dt_c2_q34"] = FIXTURES["dt-c2-q34"];
window.EXPLAINER_SCREENPLAYS["ch2_q34"] = FIXTURES["dt-c2-q34"];

})();
