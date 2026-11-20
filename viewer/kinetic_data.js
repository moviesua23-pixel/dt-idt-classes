window.KINETIC_DATA = {
  "version": "2.0.0",
  "archetypes": [
    {
      "id": "give_and_receive",
      "title": "Give & Receive (Asset Handover & Settlement)",
      "type": "specific",
      "category": "Transfers & Settlements",
      "duration": 14.0,
      "selection": {
        "when_to_use": "When one entity hands over an item/asset to another entity, either with a monetary return payment or without payment (unilateral transfer).",
        "not_for": [
          "swap",
          "split_into_parts",
          "chain_passing"
        ],
        "examples": [
          {
            "domain": "Real Estate",
            "description": "Father gifts a residential apartment to his son without monetary return.",
            "slots": {
              "giver": "Father",
              "receiver": "Son",
              "item_label": "Residential House",
              "item_icon": "house",
              "item_value": 4500000,
              "payment_amount": 0,
              "tag_text": "Unilateral Settlement Complete",
              "note": "Property transferred without monetary settlement."
            }
          },
          {
            "domain": "Shares & Securities",
            "description": "Investor sells listed equity shares to an institutional buyer for full settlement.",
            "slots": {
              "giver": "Retail Investor",
              "receiver": "Institutional Fund",
              "item_label": "Equity Portfolio",
              "item_icon": "shares",
              "item_value": 2800000,
              "payment_amount": 2800000,
              "tag_text": "Securities Settlement Complete",
              "note": "Full monetary payment received on trade settlement."
            }
          },
          {
            "domain": "General Goods",
            "description": "Manufacturer delivers industrial machinery to a distributor against partial payment.",
            "slots": {
              "giver": "Manufacturer",
              "receiver": "Distributor",
              "item_label": "Machinery Unit",
              "item_icon": "goods",
              "item_value": 1500000,
              "payment_amount": 1200000,
              "tag_text": "Commercial Delivery Complete",
              "note": "Partial payment received upon delivery."
            }
          }
        ]
      },
      "cues_default": {
        "cue_actors": 0.2,
        "cue_item": 3.0,
        "cue_payment": 7.5
      },
      "slots_default": {
        "title": "Asset Handover & Settlement",
        "giver": "Party One",
        "receiver": "Party Two",
        "item_label": "Capital Asset",
        "item_icon": "house",
        "item_value": 3500000,
        "payment_amount": 3500000,
        "tag_text": "Payment Settlement Complete",
        "note": "Payment received satisfies agreement terms."
      }
    },
    {
      "id": "swap",
      "title": "Swap (Bilateral Asset Exchange)",
      "type": "specific",
      "category": "Transfers & Settlements",
      "duration": 14.0,
      "selection": {
        "when_to_use": "When two entities exchange assets with crossing trajectory paths, followed by value comparison (equal match or cash boot balance difference).",
        "not_for": [
          "give_and_receive",
          "split_into_parts"
        ],
        "examples": [
          {
            "domain": "Real Estate",
            "description": "Two land owners swap commercial plot for residential plot with unequal value cash differential.",
            "slots": {
              "party_a": "Owner One",
              "party_b": "Owner Two",
              "item_a_label": "Commercial Plot",
              "item_a_icon": "house",
              "item_a_val": 4500000,
              "item_b_label": "Residential Plot",
              "item_b_icon": "house",
              "item_b_val": 3800000,
              "title": "Real Estate Plot Exchange"
            }
          },
          {
            "domain": "Shares & Securities",
            "description": "Exchanging debenture certificates for equity shares of equal valuation.",
            "slots": {
              "party_a": "Debenture Holder",
              "party_b": "Issuing Firm",
              "item_a_label": "Secured Debentures",
              "item_a_icon": "shares",
              "item_a_val": 2000000,
              "item_b_label": "Equity Allotment",
              "item_b_icon": "shares",
              "item_b_val": 2000000,
              "title": "Securities Conversion Exchange"
            }
          },
          {
            "domain": "General Goods",
            "description": "Two trading partners swap transport truck for packaging machinery.",
            "slots": {
              "party_a": "Logistics Partner",
              "party_b": "Industrial Unit",
              "item_a_label": "Transport Vehicle",
              "item_a_icon": "goods",
              "item_a_val": 1600000,
              "item_b_label": "Packaging Line",
              "item_b_icon": "goods",
              "item_b_val": 1400000,
              "title": "Equipment Barter Exchange"
            }
          }
        ]
      },
      "cues_default": {
        "cue_parties": 0.2,
        "cue_crossing": 3.0,
        "cue_compare": 8.0
      },
      "slots_default": {
        "title": "Bilateral Asset Exchange",
        "party_a": "Party Alpha",
        "party_b": "Party Beta",
        "item_a_label": "Asset Alpha",
        "item_a_icon": "goods",
        "item_a_val": 3200000,
        "item_b_label": "Asset Beta",
        "item_b_icon": "shares",
        "item_b_val": 2700000
      }
    },
    {
      "id": "split_into_parts",
      "title": "Split into Parts (Entity Division & Partition)",
      "type": "specific",
      "category": "Division & Allocation",
      "duration": 14.0,
      "selection": {
        "when_to_use": "When one whole entity or capital pool divides into 2 to 5 parts, cracking apart and sliding into labelled allocation cards.",
        "not_for": [
          "take_away",
          "merge_into_one"
        ],
        "examples": [
          {
            "domain": "Real Estate",
            "description": "Family estate partition dividing commercial property among three coparceners.",
            "slots": {
              "whole_label": "Family Estate Pool",
              "whole_amount": 9000000,
              "parts": [
                {
                  "label": "Unit One Share",
                  "amount": 3000000
                },
                {
                  "label": "Unit Two Share",
                  "amount": 3000000
                },
                {
                  "label": "Unit Three Share",
                  "amount": 3000000
                }
              ]
            }
          },
          {
            "domain": "Shares & Securities",
            "description": "Demerger of corporate undertaking into two distinct listed companies.",
            "slots": {
              "whole_label": "Combined Enterprise Value",
              "whole_amount": 10000000,
              "parts": [
                {
                  "label": "Parent Retained",
                  "amount": 6000000
                },
                {
                  "label": "Demerged Result",
                  "amount": 4000000
                }
              ]
            }
          },
          {
            "domain": "General Goods",
            "description": "Bulk inventory consignment partitioned across four branch warehouses.",
            "slots": {
              "whole_label": "Consignment Lot",
              "whole_amount": 4000000,
              "parts": [
                {
                  "label": "North Depot",
                  "amount": 1500000
                },
                {
                  "label": "South Depot",
                  "amount": 1000000
                },
                {
                  "label": "East Depot",
                  "amount": 800000
                },
                {
                  "label": "West Depot",
                  "amount": 700000
                }
              ]
            }
          }
        ]
      },
      "cues_default": {
        "cue_whole": 0.5,
        "cue_crack": 3.5,
        "cue_parts": 6.5,
        "cue_verify": 10.5
      },
      "slots_default": {
        "title": "Entity Partition & Allocation",
        "whole_label": "Unified Total Base",
        "whole_amount": 6000000,
        "parts": [
          {
            "label": "Allocation Branch One",
            "amount": 2500000
          },
          {
            "label": "Allocation Branch Two",
            "amount": 2000000
          },
          {
            "label": "Residual Allocation",
            "amount": 1500000
          }
        ]
      }
    },
    {
      "id": "merge_into_one",
      "title": "Merge into One (Combination & Fusion)",
      "type": "specific",
      "category": "Combination & Fusion",
      "duration": 14.0,
      "selection": {
        "when_to_use": "When 2 to 5 separate input streams or corporate bodies converge into the centre, fuse into one combined block, and the total counts up.",
        "not_for": [
          "add_up",
          "split_into_parts"
        ],
        "examples": [
          {
            "domain": "Real Estate",
            "description": "Pooling three adjacent land parcels into a single unified commercial development site.",
            "slots": {
              "title": "Land Parcel Consolidation",
              "result_label": "Unified Development Site",
              "inputs": [
                {
                  "label": "Parcel Plot Alpha",
                  "amount": 2500000
                },
                {
                  "label": "Parcel Plot Beta",
                  "amount": 3500000
                },
                {
                  "label": "Parcel Plot Gamma",
                  "amount": 2000000
                }
              ]
            }
          },
          {
            "domain": "Shares & Securities",
            "description": "Two manufacturing companies combining into an amalgamated enterprise.",
            "slots": {
              "title": "Corporate Amalgamation Merger",
              "result_label": "Combined Enterprise",
              "inputs": [
                {
                  "label": "Company A Capital",
                  "amount": 5000000
                },
                {
                  "label": "Company B Capital",
                  "amount": 4000000
                }
              ]
            }
          },
          {
            "domain": "General Goods",
            "description": "Consolidating component parts into an assembled final industrial product.",
            "slots": {
              "title": "Assembly Value Consolidation",
              "result_label": "Assembled System",
              "inputs": [
                {
                  "label": "Chassis Framework",
                  "amount": 800000
                },
                {
                  "label": "Drive Engine",
                  "amount": 1200000
                },
                {
                  "label": "Control Module",
                  "amount": 500000
                }
              ]
            }
          }
        ]
      },
      "cues_default": {
        "cue_inputs": 0.5,
        "cue_slide": 4.0,
        "cue_fuse": 7.5,
        "cue_total": 10.0
      },
      "slots_default": {
        "title": "Stream Convergence & Fusion",
        "result_label": "Combined Unified Whole",
        "inputs": [
          {
            "label": "Input Entity Alpha",
            "amount": 2800000
          },
          {
            "label": "Input Entity Beta",
            "amount": 3200000
          }
        ]
      }
    },
    {
      "id": "add_up",
      "title": "Add Up (Sequential Stacking & Total Odometer)",
      "type": "specific",
      "category": "Calculation & Math",
      "duration": 14.0,
      "selection": {
        "when_to_use": "When items or additions drop sequentially into a vertical stack with an updating running total odometer.",
        "not_for": [
          "take_away",
          "merge_into_one",
          "compare_two"
        ],
        "examples": [
          {
            "domain": "Real Estate",
            "description": "Summing purchase base, stamp registration fee, and improvement works into gross investment.",
            "slots": {
              "title": "Gross Property Outlay",
              "total_label": "Total Investment",
              "items": [
                {
                  "label": "Purchase Base",
                  "amount": 3000000
                },
                {
                  "label": "Registration Fee",
                  "amount": 250000
                },
                {
                  "label": "Renovation Addition",
                  "amount": 450000
                }
              ]
            }
          },
          {
            "domain": "Shares & Securities",
            "description": "Aggregating quarterly dividend disbursements into annual total yield.",
            "slots": {
              "title": "Annual Securities Inflow",
              "total_label": "Total Inflow",
              "items": [
                {
                  "label": "Quarter One Inflow",
                  "amount": 140000
                },
                {
                  "label": "Quarter Two Inflow",
                  "amount": 160000
                },
                {
                  "label": "Quarter Three Inflow",
                  "amount": 220000
                }
              ]
            }
          },
          {
            "domain": "General Goods",
            "description": "Accumulating direct material, assembly labor, and freight into production cost.",
            "slots": {
              "title": "Production Expense Accumulation",
              "total_label": "Total Production Cost",
              "items": [
                {
                  "label": "Raw Stock",
                  "amount": 800000
                },
                {
                  "label": "Assembly Labor",
                  "amount": 250000
                },
                {
                  "label": "Freight Handling",
                  "amount": 90000
                }
              ]
            }
          }
        ]
      },
      "cues_default": {
        "cue_row_1": 1.0,
        "cue_row_2": 4.0,
        "cue_row_3": 7.0,
        "cue_final": 10.5
      },
      "slots_default": {
        "title": "Summation & Aggregation Ladder",
        "total_label": "Aggregated Total Result",
        "items": [
          {
            "label": "Primary Base Tier",
            "amount": 1200000
          },
          {
            "label": "Secondary Component",
            "amount": 450000
          },
          {
            "label": "Supplemental Receipt",
            "amount": 250000
          }
        ]
      }
    },
    {
      "id": "take_away",
      "title": "Take Away (Chunk Slicing & Remainder Balance)",
      "type": "specific",
      "category": "Calculation & Math",
      "duration": 14.0,
      "selection": {
        "when_to_use": "When a starting gross value is reduced step-by-step by subtracting reduction chunks that slice off and fly to labelled reduction slots, with net remainder glowing green (or red if deficit).",
        "not_for": [
          "add_up",
          "split_into_parts"
        ],
        "examples": [
          {
            "domain": "Real Estate",
            "description": "Gross sale settlement reduced by transfer brokerage fee and original acquisition cost.",
            "slots": {
              "title": "Gross Value Reductions",
              "start_label": "Gross Settlement",
              "start_amount": 6000000,
              "result_label": "Net Realized Balance",
              "steps": [
                {
                  "label": "Brokerage & Legal Outlay",
                  "amount": 200000
                },
                {
                  "label": "Acquisition Cost Base",
                  "amount": 2800000
                }
              ]
            }
          },
          {
            "domain": "Shares & Securities",
            "description": "Gross share redemption receipts deducting security transaction charges and cost base.",
            "slots": {
              "title": "Portfolio Redemption Net",
              "start_label": "Redemption Receipt",
              "start_amount": 3500000,
              "result_label": "Net Profit Balance",
              "steps": [
                {
                  "label": "Transaction Charges",
                  "amount": 50000
                },
                {
                  "label": "Initial Purchase Outlay",
                  "amount": 1800000
                }
              ]
            }
          },
          {
            "domain": "General Goods",
            "description": "Gross commercial invoice amount reducing by trade discount and freight allowance.",
            "slots": {
              "title": "Invoice Settlement Net",
              "start_label": "Gross Invoice Sum",
              "start_amount": 1500000,
              "result_label": "Net Payable Balance",
              "steps": [
                {
                  "label": "Trade Volume Discount",
                  "amount": 150000
                },
                {
                  "label": "Freight Allowance",
                  "amount": 80000
                }
              ]
            }
          }
        ]
      },
      "cues_default": {
        "cue_start": 0.5,
        "cue_slice_1": 3.5,
        "cue_slice_2": 7.0,
        "cue_result": 10.5
      },
      "slots_default": {
        "title": "Sequential Subtraction & Remainder",
        "start_label": "Initial Gross Value",
        "start_amount": 5000000,
        "result_label": "Net Remainder Result",
        "steps": [
          {
            "label": "Primary Outflow Step",
            "amount": 1200000
          },
          {
            "label": "Secondary Outflow Step",
            "amount": 1500000
          }
        ]
      }
    },
    {
      "id": "compare_two",
      "title": "Compare Two (Benchmark Comparison & Scale Tilt)",
      "type": "specific",
      "category": "Valuation & Comparison",
      "duration": 14.0,
      "selection": {
        "when_to_use": "When two values/benchmarks compete, a scale tilts to choose the higher or lower, with winner glowing green and optional limit cap line clipping excess.",
        "not_for": [
          "add_up",
          "give_and_receive"
        ],
        "examples": [
          {
            "domain": "Real Estate",
            "description": "Comparing declared sale price against stamp authority benchmark to pick higher.",
            "slots": {
              "title": "Valuation Benchmark Comparison",
              "label_a": "Agreed Sale Price",
              "val_a": 4000000,
              "label_b": "Valuation Benchmark",
              "val_b": 5500000,
              "mode": "higher",
              "cap_amount": 6000000
            }
          },
          {
            "domain": "Shares & Securities",
            "description": "Adopting the lower between cost and net realizable market price for inventory.",
            "slots": {
              "title": "Market Realizable Valuation",
              "label_a": "Cost Base",
              "val_a": 1500000,
              "label_b": "Realizable Price",
              "val_b": 1200000,
              "mode": "lower",
              "cap_amount": 0
            }
          },
          {
            "domain": "General Goods",
            "description": "Comparing vendor tender price against maximum approved procurement budget.",
            "slots": {
              "title": "Tender Price Evaluation",
              "label_a": "Vendor Quote",
              "val_a": 850000,
              "label_b": "Procurement Budget",
              "val_b": 900000,
              "mode": "lower",
              "cap_amount": 950000
            }
          }
        ]
      },
      "cues_default": {
        "cue_bars": 0.5,
        "cue_scale": 4.5,
        "cue_winner": 8.5
      },
      "slots_default": {
        "title": "Benchmark Valuation Decision",
        "label_a": "Declared Value A",
        "val_a": 1800000,
        "label_b": "Standard Value B",
        "val_b": 2500000,
        "mode": "higher",
        "cap_amount": 2800000
      }
    },
    {
      "id": "time_range",
      "title": "Time Range (Timeline Span & Event Flag)",
      "type": "specific",
      "category": "Timelines & Windows",
      "duration": 14.0,
      "selection": {
        "when_to_use": "When an event must occur within an allowable timeline window/span, showing an axis, start pin, range bar, and event flag dropping inside (pass) or outside (late/early fail).",
        "not_for": [
          "chain_passing",
          "step_sequence"
        ],
        "examples": [
          {
            "domain": "Real Estate",
            "description": "Purchasing new residential property within two-year reinvestment window.",
            "slots": {
              "title": "Reinvestment Window Verification",
              "start_label": "Transfer Date",
              "span_length": 24,
              "span_unit": "Months",
              "span_label": "24 Months Window",
              "event_label": "New House Purchase",
              "event_offset": 18,
              "is_inside": true
            }
          },
          {
            "domain": "Shares & Securities",
            "description": "Holding period classification verifying whether securities were held beyond 12 months.",
            "slots": {
              "title": "Holding Period Duration Window",
              "start_label": "Acquisition Date",
              "span_length": 12,
              "span_unit": "Months",
              "span_label": "12 Months Threshold",
              "event_label": "Disposal Date",
              "event_offset": 15,
              "is_inside": true
            }
          },
          {
            "domain": "General Goods",
            "description": "Supplier warranty claim submitted within 30 days of shipment arrival.",
            "slots": {
              "title": "Warranty Claim Period",
              "start_label": "Delivery Date",
              "span_length": 30,
              "span_unit": "Days",
              "span_label": "30 Days Window",
              "event_label": "Claim Filed",
              "event_offset": 45,
              "is_inside": false
            }
          }
        ]
      },
      "cues_default": {
        "cue_axis": 0.5,
        "cue_window": 4.0,
        "cue_event": 7.5,
        "cue_outcome": 10.5
      },
      "slots_default": {
        "title": "Prescribed Window & Event Timing",
        "start_label": "Initial Baseline Date",
        "span_length": 24,
        "span_unit": "Months",
        "span_label": "Allowable Relief Window",
        "event_label": "Action Completion Event",
        "event_offset": 16,
        "is_inside": true
      }
    },
    {
      "id": "conditions_gate",
      "title": "Conditions Gate (Multi-Criteria Gatekeeper)",
      "type": "specific",
      "category": "Conditions & Decisions",
      "duration": 14.0,
      "selection": {
        "when_to_use": "When 2 to 5 formal eligibility criteria evaluate sequentially with green ticks or red crosses; gate at bottom swings open if criteria met, or locks with shaking doors if failed.",
        "not_for": [
          "compare_two",
          "step_sequence"
        ],
        "examples": [
          {
            "domain": "Real Estate",
            "description": "Checking three eligibility conditions: ownership of one house, Indian location, and purchase within timeline.",
            "slots": {
              "title": "Relief Eligibility Gate",
              "rule": "all",
              "open_caption": "Criteria Fulfilled · Relief Granted",
              "closed_caption": "Criteria Failed · Relief Locked",
              "conditions": [
                {
                  "label": "Single House Ownership",
                  "passed": true
                },
                {
                  "label": "Domestic Asset Location",
                  "passed": true
                },
                {
                  "label": "Timely Acquisition Window",
                  "passed": true
                }
              ]
            }
          },
          {
            "domain": "Shares & Securities",
            "description": "Verifying startup exemption: DPIIT recognized, share premium within limits, and audit completed.",
            "slots": {
              "title": "Startup Exemption Criteria Gate",
              "rule": "all",
              "open_caption": "Exemption Unlocked",
              "closed_caption": "Standard Rate Applied",
              "conditions": [
                {
                  "label": "Official Department Recognition",
                  "passed": true
                },
                {
                  "label": "Standard Valuation Pricing",
                  "passed": true
                },
                {
                  "label": "Audited Compliance Filing",
                  "passed": false
                }
              ]
            }
          },
          {
            "domain": "General Goods",
            "description": "Customs duty drawback clearance: export confirmed, inward foreign exchange, invoice matched.",
            "slots": {
              "title": "Duty Drawback Clearance Gate",
              "rule": "all",
              "open_caption": "Clearance Gate Open",
              "closed_caption": "Duty Hold Enforced",
              "conditions": [
                {
                  "label": "Port Physical Export Verified",
                  "passed": true
                },
                {
                  "label": "Inward Funds Realized",
                  "passed": true
                }
              ]
            }
          }
        ]
      },
      "cues_default": {
        "cue_cards": 0.5,
        "cue_eval": 4.0,
        "cue_gate": 9.0
      },
      "slots_default": {
        "title": "Prescribed Gatekeeper Checklist",
        "rule": "all",
        "open_caption": "All Conditions Met · Gate Unlocked",
        "closed_caption": "Condition Failed · Access Locked",
        "conditions": [
          {
            "label": "Initial Eligibility Condition",
            "passed": true
          },
          {
            "label": "Secondary Compliance Standard",
            "passed": true
          },
          {
            "label": "Eligibility Window Fulfillment",
            "passed": true
          }
        ]
      }
    },
    {
      "id": "chain_passing",
      "title": "Chain Passing (Multi-Owner Succession Hop)",
      "type": "specific",
      "category": "Transfers & Settlements",
      "duration": 14.0,
      "selection": {
        "when_to_use": "When an item hops along a sequential chain of 3 to 5 successive owners, carrying its original cost tag forward across each hop with a 'carried over' confirmation.",
        "not_for": [
          "give_and_receive",
          "step_sequence"
        ],
        "examples": [
          {
            "domain": "Real Estate",
            "description": "Succession chain where grandfather acquires house, bequeaths to father, who gifts to grandson with original cost tag preserved.",
            "slots": {
              "title": "Succession Cost Lineage",
              "item_label": "Ancestral Estate",
              "tag_label": "Original Acquisition Cost",
              "tag_value": 1500000,
              "owners": [
                {
                  "name": "Grandfather",
                  "year": "1995"
                },
                {
                  "name": "Father",
                  "year": "2010"
                },
                {
                  "name": "Grandson",
                  "year": "2024"
                }
              ]
            }
          },
          {
            "domain": "Shares & Securities",
            "description": "Holding period aggregation across holding company, subsidiary transfer, and ultimate shareholder distribution.",
            "slots": {
              "title": "Corporate Shareholding Lineage",
              "item_label": "Equity Holding",
              "tag_label": "Original Base Investment",
              "tag_value": 3500000,
              "owners": [
                {
                  "name": "Parent Co",
                  "year": "2015"
                },
                {
                  "name": "Subsidiary",
                  "year": "2020"
                },
                {
                  "name": "Shareholder",
                  "year": "2024"
                }
              ]
            }
          },
          {
            "domain": "General Goods",
            "description": "Serial chain of custody for vintage industrial vehicle across collectors.",
            "slots": {
              "title": "Asset Custody Succession",
              "item_label": "Vintage Machinery",
              "tag_label": "Base Book Value",
              "tag_value": 750000,
              "owners": [
                {
                  "name": "Origin Factory",
                  "year": "2000"
                },
                {
                  "name": "Regional Plant",
                  "year": "2012"
                },
                {
                  "name": "Current Facility",
                  "year": "2024"
                }
              ]
            }
          }
        ]
      },
      "cues_default": {
        "cue_owners": 0.5,
        "cue_hop_1": 4.0,
        "cue_hop_2": 8.0,
        "cue_carried": 11.0
      },
      "slots_default": {
        "title": "Succession Cost Base Carryover",
        "item_label": "Capital Asset",
        "tag_label": "Original Base Cost",
        "tag_value": 1800000,
        "owners": [
          {
            "name": "Predecessor One",
            "year": "Year One"
          },
          {
            "name": "Intermediary Owner",
            "year": "Year Five"
          },
          {
            "name": "Current Beneficiary",
            "year": "Year Ten"
          }
        ]
      }
    },
    {
      "id": "key_statement",
      "title": "Key Statement (Universal Headline & Marker Sweep)",
      "type": "general",
      "category": "General Catch-All",
      "duration": 14.0,
      "selection": {
        "when_to_use": "Universal fallback when none of the physical action archetypes fit. Highlights a key principle, condition, or conclusion with word-by-word reveal and marker sweep.",
        "not_for": [],
        "examples": [
          {
            "domain": "Real Estate",
            "description": "Mandatory registered conveyance requirement for transfer of immovable property.",
            "slots": {
              "icon_type": "house",
              "statement": "Transfers of immovable property require mandatory registered conveyance to confer legal title.",
              "support_line": "Registration requirement applies across all commercial and residential land transfers."
            }
          },
          {
            "domain": "Shares & Securities",
            "description": "Conclusive classification of institutional investor securities as capital assets.",
            "slots": {
              "icon_type": "shares",
              "statement": "Securities held by institutional foreign funds are conclusively classified as capital assets.",
              "support_line": "Characterization rule overrides trading frequency or business holding intent."
            }
          },
          {
            "domain": "General Goods",
            "description": "Fundamental legal requirement of lawful settlement in commercial contracts.",
            "slots": {
              "icon_type": "goods",
              "statement": "Valid commercial agreements require lawful settlement moving between parties.",
              "support_line": "Essential legal foundation for all business contracts and bilateral transfers."
            }
          }
        ]
      },
      "cues_default": {
        "cue_statement": 0.5,
        "cue_highlight": 4.5,
        "cue_support": 8.5
      },
      "slots_default": {
        "icon_type": "scale",
        "statement": "Legal standards require standard benchmark value adoption when agreed price falls below prescribed limits.",
        "support_line": "Core principle applies across asset exchanges and value reviews."
      }
    },
    {
      "id": "step_sequence",
      "title": "Step Sequence (Linear Roadmap & Milestone Progress)",
      "type": "general",
      "category": "General Catch-All",
      "duration": 14.0,
      "selection": {
        "when_to_use": "When a process, workflow, or procedural timeline progresses linearly across 2 to 6 numbered milestone steps on a track, with active step glowing.",
        "not_for": [
          "time_range",
          "chain_passing"
        ],
        "examples": [
          {
            "domain": "Real Estate",
            "description": "Three steps of net asset gain calculation: determine sale settlement, deduct cost, apply exemption.",
            "slots": {
              "title": "Calculation Workflow Sequence",
              "steps": [
                {
                  "num": "1",
                  "title": "Determine Settlement",
                  "desc": "Adopt agreed price or benchmark value"
                },
                {
                  "num": "2",
                  "title": "Deduct Cost Base",
                  "desc": "Subtract acquisition and improvement costs"
                },
                {
                  "num": "3",
                  "title": "Apply Prescribed Relief",
                  "desc": "Deduct eligible reinvestment relief"
                }
              ]
            }
          },
          {
            "domain": "Shares & Securities",
            "description": "Four steps of share buyback: board approval, special resolution, escrow deposit, share extinguishment.",
            "slots": {
              "title": "Corporate Buyback Procedure",
              "steps": [
                {
                  "num": "1",
                  "title": "Board Approval",
                  "desc": "Director authorization resolution"
                },
                {
                  "num": "2",
                  "title": "Shareholder Vote",
                  "desc": "Special resolution approval"
                },
                {
                  "num": "3",
                  "title": "Escrow Funding",
                  "desc": "Deposit settlement fund in escrow"
                },
                {
                  "num": "4",
                  "title": "Extinguishment",
                  "desc": "Cancel and destroy bought back shares"
                }
              ]
            }
          },
          {
            "domain": "General Goods",
            "description": "Manufacturing order fulfillment: order entry, material assembly, quality audit, dispatch.",
            "slots": {
              "title": "Production Order Roadmap",
              "steps": [
                {
                  "num": "1",
                  "title": "Order Placed",
                  "desc": "Client commercial specifications logged"
                },
                {
                  "num": "2",
                  "title": "Component Assembly",
                  "desc": "Physical manufacture on assembly line"
                },
                {
                  "num": "3",
                  "title": "Quality Audit",
                  "desc": "Technical verification check complete"
                },
                {
                  "num": "4",
                  "title": "Logistics Dispatch",
                  "desc": "Shipment dispatched to buyer"
                }
              ]
            }
          }
        ]
      },
      "cues_default": {
        "cue_step_1": 0.5,
        "cue_step_2": 4.5,
        "cue_step_3": 8.5
      },
      "slots_default": {
        "title": "Linear Procedural Progression",
        "steps": [
          {
            "num": "1",
            "title": "Initial Evaluation Step",
            "desc": "Establish baseline data and eligibility"
          },
          {
            "num": "2",
            "title": "Analytical Evaluation",
            "desc": "Apply relevant benchmarks and adjustments"
          },
          {
            "num": "3",
            "title": "Final Settlement Determination",
            "desc": "Verify compliance and conclude result"
          }
        ]
      }
    },
    {
      "id": "formula_builder",
      "title": "Formula Builder (Chip Equations & Arithmetic Parser)",
      "type": "general",
      "category": "General Catch-All",
      "duration": 14.0,
      "selection": {
        "when_to_use": "When an algebraic or arithmetic equation is assembled chip-by-chip, operators appear, and the computed result counts up.",
        "not_for": [
          "add_up",
          "take_away"
        ],
        "examples": [
          {
            "domain": "Real Estate",
            "description": "Net Net Asset Gain equation: Full Value - (Indexed Cost + Transfer Expenses).",
            "slots": {
              "title": "Net Asset Gain Formula Assembled",
              "chips": [
                {
                  "label": "Full Value",
                  "val": 6000000
                },
                {
                  "op": "−"
                },
                {
                  "label": "Indexed Cost",
                  "val": 3500000
                },
                {
                  "op": "−"
                },
                {
                  "label": "Transfer Outlay",
                  "val": 200000
                },
                {
                  "op": "="
                },
                {
                  "label": "Net Net Asset Gain",
                  "val": 2300000,
                  "is_total": true
                }
              ]
            }
          },
          {
            "domain": "Shares & Securities",
            "description": "Tax on Long Term Net Asset Gains: Gain × 20% + 4% Cess.",
            "slots": {
              "title": "Tax Liability Formula Equation",
              "chips": [
                {
                  "label": "Gain Amount",
                  "val": 1000000
                },
                {
                  "op": "×"
                },
                {
                  "label": "Base Rate",
                  "text": "20%"
                },
                {
                  "op": "+"
                },
                {
                  "label": "Health Cess",
                  "val": 8000
                },
                {
                  "op": "="
                },
                {
                  "label": "Total Tax Due",
                  "val": 208000,
                  "is_total": true
                }
              ]
            }
          },
          {
            "domain": "General Goods",
            "description": "Operating Margin: Gross Revenue - Cost of Goods Sold.",
            "slots": {
              "title": "Commercial Operating Margin",
              "chips": [
                {
                  "label": "Sales Revenue",
                  "val": 4500000
                },
                {
                  "op": "−"
                },
                {
                  "label": "Direct Costs",
                  "val": 2800000
                },
                {
                  "op": "="
                },
                {
                  "label": "Operating Profit",
                  "val": 1700000,
                  "is_total": true
                }
              ]
            }
          }
        ]
      },
      "cues_default": {
        "cue_operand_1": 0.5,
        "cue_operand_2": 4.0,
        "cue_operand_3": 7.5,
        "cue_result": 10.5
      },
      "slots_default": {
        "title": "Arithmetic Formula Construction",
        "chips": [
          {
            "label": "Primary Base Component",
            "val": 5000000
          },
          {
            "op": "−"
          },
          {
            "label": "Prescribed Outflow Base",
            "val": 1800000
          },
          {
            "op": "−"
          },
          {
            "label": "Permissible Outflow",
            "val": 200000
          },
          {
            "op": "="
          },
          {
            "label": "Net Final Balance",
            "val": 3000000,
            "is_total": true
          }
        ]
      }
    },
    {
      "id": "table_reveal",
      "title": "Table Reveal (Structured Matrix & Row Spotlight)",
      "type": "general",
      "category": "General Catch-All",
      "duration": 14.0,
      "selection": {
        "when_to_use": "When tabular data, multi-attribute comparisons, or multi-year schedules reveal row-by-row with a moving spotlight highlight on the key row.",
        "not_for": [
          "add_up",
          "step_sequence"
        ],
        "examples": [
          {
            "domain": "Real Estate",
            "description": "Comparing properties across Location, Guide Rate, Declared Price, and Difference.",
            "slots": {
              "title": "Property Valuation Comparison Matrix",
              "headers": [
                "Property Asset",
                "Declared Value",
                "Standard Rate",
                "Status"
              ],
              "rows": [
                [
                  "Plot Alpha",
                  "₹ 40,00,000",
                  "₹ 42,00,000",
                  "Within Range"
                ],
                [
                  "Plot Beta",
                  "₹ 25,00,000",
                  "₹ 35,00,000",
                  "Review Required"
                ],
                [
                  "Plot Gamma",
                  "₹ 60,00,000",
                  "₹ 60,00,000",
                  "Benchmark Matched"
                ]
              ],
              "spotlight_row": 1
            }
          },
          {
            "domain": "Shares & Securities",
            "description": "Tax rate matrix across equity, debt, listed, and unlisted security categories.",
            "slots": {
              "title": "Security Class Tax Rate Schedule",
              "headers": [
                "Security Asset",
                "Holding Period",
                "Applicable Rate",
                "Indexation"
              ],
              "rows": [
                [
                  "Listed Shares",
                  "12 Months",
                  "10%",
                  "No Indexation"
                ],
                [
                  "Unlisted Shares",
                  "24 Months",
                  "20%",
                  "Indexation Applied"
                ],
                [
                  "Debt Securities",
                  "36 Months",
                  "Slab Rate",
                  "Standard Base"
                ]
              ],
              "spotlight_row": 0
            }
          },
          {
            "domain": "General Goods",
            "description": "Quarterly vendor performance matrix across delivery, quality score, and spend.",
            "slots": {
              "title": "Quarterly Procurement Summary",
              "headers": [
                "Vendor Unit",
                "Deliveries",
                "Quality Index",
                "Total Outflow"
              ],
              "rows": [
                [
                  "Supplier Alpha",
                  "14 Shipments",
                  "98.5%",
                  "₹ 18,50,000"
                ],
                [
                  "Supplier Beta",
                  "22 Shipments",
                  "96.2%",
                  "₹ 29,00,000"
                ],
                [
                  "Supplier Gamma",
                  "8 Shipments",
                  "92.0%",
                  "₹ 11,20,000"
                ]
              ],
              "spotlight_row": 0
            }
          }
        ]
      },
      "cues_default": {
        "cue_header": 0.5,
        "cue_rows": 3.5,
        "cue_spotlight": 8.0
      },
      "slots_default": {
        "title": "Comparative Structured Matrix",
        "headers": [
          "Entity Classification",
          "Baseline Criterion",
          "Evaluation Metric",
          "Result Status"
        ],
        "rows": [
          [
            "Category Alpha",
            "Criteria Standard One",
            "₹ 25,00,000",
            "Approved"
          ],
          [
            "Category Beta",
            "Criteria Standard Two",
            "₹ 38,00,000",
            "Selected"
          ],
          [
            "Category Gamma",
            "Criteria Standard Three",
            "₹ 12,00,000",
            "Exempt"
          ]
        ],
        "spotlight_row": 1
      }
    },
    {
      "id": "concept_map",
      "title": "Concept Map (Hub & Spoke Branch Network)",
      "type": "general",
      "category": "General Catch-All",
      "duration": 14.0,
      "selection": {
        "when_to_use": "When a central concept branches out into 2 to 5 sub-rules, exceptions, or classification branches via animated curves, with one emphasized branch glowing.",
        "not_for": [
          "split_into_parts",
          "conditions_gate"
        ],
        "examples": [
          {
            "domain": "Real Estate",
            "description": "Capital Asset definition branching into: Residential house, Commercial land, Rural land (exempt), Personal effects (exempt).",
            "slots": {
              "title": "Capital Asset Classification Network",
              "hub_label": "Property Scope",
              "branches": [
                {
                  "label": "Residential Asset",
                  "desc": "Covered Capital Asset",
                  "highlight": false
                },
                {
                  "label": "Commercial Land",
                  "desc": "Covered Capital Asset",
                  "highlight": true
                },
                {
                  "label": "Rural Farm Land",
                  "desc": "Excluded from Scope",
                  "highlight": false
                },
                {
                  "label": "Personal Effects",
                  "desc": "Excluded from Scope",
                  "highlight": false
                }
              ]
            }
          },
          {
            "domain": "Shares & Securities",
            "description": "Five heads of income network branching from total gross receipts.",
            "slots": {
              "title": "Classification Network Structure",
              "hub_label": "Income Portfolio",
              "branches": [
                {
                  "label": "Salary Inflow",
                  "desc": "Standard Compensation",
                  "highlight": false
                },
                {
                  "label": "House Property",
                  "desc": "Rental Return",
                  "highlight": false
                },
                {
                  "label": "Business Profits",
                  "desc": "Commercial Operations",
                  "highlight": false
                },
                {
                  "label": "Net Asset Gains",
                  "desc": "Asset Disposal Realization",
                  "highlight": true
                }
              ]
            }
          },
          {
            "domain": "General Goods",
            "description": "Supply chain distribution network branching from central manufacturer to regional distributors.",
            "slots": {
              "title": "Distribution Network Architecture",
              "hub_label": "Central Factory",
              "branches": [
                {
                  "label": "Northern Division",
                  "desc": "Wholesale Distributor",
                  "highlight": false
                },
                {
                  "label": "Southern Hub",
                  "desc": "Direct Retail Outlet",
                  "highlight": true
                },
                {
                  "label": "Export Gateway",
                  "desc": "International Logistics",
                  "highlight": false
                }
              ]
            }
          }
        ]
      },
      "cues_default": {
        "cue_hub": 0.5,
        "cue_branches": 4.5,
        "cue_emphasize": 8.5
      },
      "slots_default": {
        "title": "Hub & Branch Concept Architecture",
        "hub_label": "Central Foundation",
        "branches": [
          {
            "label": "Primary Branch Node",
            "desc": "Standard Operation Protocol",
            "highlight": false
          },
          {
            "label": "Key Selected Branch",
            "desc": "Core Emphasis Criterion",
            "highlight": true
          },
          {
            "label": "Conditional Branch",
            "desc": "Alternative Secondary Route",
            "highlight": false
          }
        ]
      }
    }
  ]
};