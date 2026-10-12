"""
Automated Defect Remediation & IPC-7711/7721 Rework Advisor Engine
Generates comprehensive root-cause analysis, tool & consumable requirements,
and step-by-step standard operating procedures (SOP) for defective PCBs on the conveyor line.
"""

from typing import Dict, List, Any


REWORK_KNOWLEDGE_BASE = {
    "missing": {
        "title": "Missing SMT Component (Open Circuit / Unplaced)",
        "ipc_standard": "IPC-A-610H Class 2/3 Section 8.3 — Non-conforming: Component entirely missing from designated land pattern.",
        "root_cause": [
            "SMT Pick-and-Place nozzle vacuum failure or pressure drop (< -75 kPa).",
            "Component tape feeder pocket indexing jam or peeled cover tape misalignment.",
            "Component adhered to nozzle due to static electricity and blown off-target."
        ],
        "required_tools": [
            "Precision Micro-Soldering Station (e.g. JBC / Weller, set to 330°C - 350°C)",
            "Hot Air Pencil Station (Airflow: 12 L/min @ 340°C)",
            "10x - 40x Stereo Inspection Microscope with ring LED illumination",
            "Anti-static Curved ESD Tweezers (Type 7-SA / 00-SA)",
            "Vacuum Pick-up Pen with ESD silicone tip (diameter matching package)",
            "Benchtop Solder Fume Extraction Absorber"
        ],
        "required_materials": [
            "Lead-Free Solder Wire (SAC305 alloy: 96.5% Sn, 3.0% Ag, 0.5% Cu, diameter 0.4mm)",
            "No-Clean Tacky Rework Flux (IPC J-STD-004 certified ROL0)",
            "Copper Desoldering Braid / Wick (Width 1.5mm - 2.0mm)",
            "99.9% Electronic Grade Isopropyl Alcohol (IPA)",
            "Lint-free ESD Cleanroom Swabs",
            "Replacement OEM SMT Reel / Tray component with verified part number"
        ],
        "step_by_step_sop": [
            "Step 1 - Pad Inspection: Examine bare copper pads under 20x microscope for physical pad lift or trace fracturing.",
            "Step 2 - Pad Planarization: Apply ROL0 tacky flux to pads. Gently glide copper braid with soldering tip at 330°C to flatten residual solder mounds.",
            "Step 3 - Solvent Cleaning: Swab the land pattern with 99.9% IPA to remove oxidized residues; dry with filtered compressed air.",
            "Step 4 - Solder Paste Application: Dispense micro-dots of SAC305 solder paste or pre-tin pads lightly with lead-free solder wire.",
            "Step 5 - Component Placement: Using ESD tweezers or vacuum pen, position replacement component aligning Pin 1 / polarity notch to silkscreen fiducials.",
            "Step 6 - Reflow Soldering: Direct hot air stream at 340°C from 15mm distance in circular motion until solder turns liquidus; allow surface tension self-alignment.",
            "Step 7 - Post-Inspection: Verify solder meniscus fillet wetting angle (15° - 90°) under microscope and re-pass through AOI conveyor inspection."
        ],
        "pnp_machine_action": "Pause SMT Line Feeder #%s. Clean nozzle vacuum tip with ultrasonic bath. Verify tape feeder reel tension and optical centering camera calibration."
    },
    "tombstone": {
        "title": "Tombstoning / Billboarding (Single-End Vertical Lift)",
        "ipc_standard": "IPC-A-610H Class 2/3 Section 8.3.2.9 — Defect: Component lifted vertically with one terminal detached from land pattern.",
        "root_cause": [
            "Unequal solder paste volume printed across the two terminal pads (aperture stencil clogging).",
            "Uneven thermal mass (one pad tied to large ground plane without adequate thermal relief traces).",
            "Reflow profile temperature ramp rate too steep (> 3.0°C/sec), causing differential flux vaporization."
        ],
        "required_tools": [
            "Dual-tip Micro-soldering Tweezers or Hot Air Pencil (320°C)",
            "Ultra-fine curved ESD tweezers (0.15mm tip)",
            "High-magnification digital stereo microscope",
            "Thermal heat shielding polyimide tape (Kapton tape)"
        ],
        "required_materials": [
            "ROL0 Rework Gel Flux (Syringe dispenser)",
            "SAC305 Lead-free Solder Wire (0.38mm diameter)",
            "Desoldering copper braid (1.0mm micro-width)",
            "99.9% IPA and micro-swabs"
        ],
        "step_by_step_sop": [
            "Step 1 - Thermal Shielding: Place Kapton tape over adjacent heat-sensitive components within 5mm radius.",
            "Step 2 - Flux Application: Dispense liquid/gel flux at the base of the lifted terminal and around the standing component.",
            "Step 3 - Reflow Detachment: Touch both terminals simultaneously using micro-tweezer soldering tips (or hot air pencil at 320°C).",
            "Step 4 - Component Re-seating: As solder melts, gently press the component down flush against the PCB substrate using tweezers until both pads wet evenly.",
            "Step 5 - Fillet Verification: Remove heat, hold component stationary for 3 seconds during solidification. Clean flux with IPA.",
            "Step 6 - QA Inspection: Confirm end overlap ≥ 75% of component terminal width and wetting height ≥ 25% of component thickness."
        ],
        "pnp_machine_action": "Inspect solder paste stencil printer aperture cleanliness. Verify reflow oven Zone 2-3 soaking curve to ensure uniform pad heating."
    },
    "tilt": {
        "title": "Rotational Skew & Angular Misalignment",
        "ipc_standard": "IPC-A-610H Class 2 (Skew ≤ 7.5° max) / Class 3 (Skew ≤ 5.0° max) — Defect: Rotational offset exceeds footprint tolerance.",
        "root_cause": [
            "PnP pick-up nozzle rotational theta (θ) motor backlash or vision alignment error.",
            "Conveyor belt vibration or sudden acceleration shock before entering reflow oven.",
            "Unequal surface tension pull from asymmetrical solder paste volume."
        ],
        "required_tools": [
            "Hot Air Rework Station (330°C, low airflow 8 L/min to prevent blowing chip off)",
            "High-precision ESD tweezers",
            "Inspection microscope with angular reticle or measurement overlay"
        ],
        "required_materials": [
            "Tacky No-Clean Flux",
            "99.9% IPA & cleaning wipes"
        ],
        "step_by_step_sop": [
            "Step 1 - Flux Addition: Apply generous tacky flux around all perimeter leads to reduce surface tension friction.",
            "Step 2 - Gentle Re-heating: Apply low-velocity hot air stream at 330°C evenly across package body.",
            "Step 3 - Rotational Realignment: When solder reaches liquidus state, nudge the component corners with fine tweezers to align leads with copper land centers.",
            "Step 4 - Natural Self-Centering: Allow surface tension of liquid solder to pull leads into perfect center alignment; remove heat.",
            "Step 5 - Quality Gate: Verify theta skew < 5.0° under microscope and confirm zero lead shorting."
        ],
        "pnp_machine_action": "Recalibrate Pick-and-Place vision centering camera (Theta angle calibration). Check conveyor rail clamping smoothness."
    },
    "shift": {
        "title": "Translational Placement Shift (X/Y Offset Exceeding Pad Limit)",
        "ipc_standard": "IPC-A-610H Class 2/3 Section 8.3 — Defect: Component end overhang exceeds 25% (Class 2) or 15% (Class 3) of component termination width.",
        "root_cause": [
            "PnP head positioning encoder drift (X/Y axis belt tension loosening).",
            "Conveyor board clamping mechanism slipping during board transfer into reflow.",
            "Excessive solder paste slump during pre-heat stage."
        ],
        "required_tools": [
            "Hot air rework tool @ 330°C",
            "ESD Tweezers",
            "Digital caliper / Optical comparator"
        ],
        "required_materials": [
            "ROL0 Rework Flux",
            "IPA solvent & ESD swabs"
        ],
        "step_by_step_sop": [
            "Step 1: Dispense flux across both sides of shifted terminations.",
            "Step 2: Heat component uniformly with hot air until solder flows.",
            "Step 3: Guide component laterally onto pad centers using tweezer tips.",
            "Step 4: Allow cool down without mechanical disturbance.",
            "Step 5: Clean residues with IPA and check side overhang ≤ 15%."
        ],
        "pnp_machine_action": "Apply automated IPC-CFX offset compensation: adjust feeder X/Y offsets by measured ΔX and ΔY values."
    },
    "severe_thermal_burn": {
        "title": "Severe Substrate Rupture, Delamination & Charring",
        "ipc_standard": "IPC-A-610H Section 10.2.3 — Non-conformance: Substrate blistering, measling, or charred resin exceeding 25% of spacing.",
        "root_cause": [
            "Reflow oven heating element runaway or prolonged conveyor stall inside peak zone (> 260°C for > 90s).",
            "Internal ground plane short circuit during ICT/FCT power-up testing."
        ],
        "required_tools": [
            "PCB Milling & Routing Dremel for damaged laminate removal",
            "Stereo Microscope",
            "UV Curing Lamp (365nm)"
        ],
        "required_materials": [
            "High-temperature 2-part optical epoxy (circuit board repair resin)",
            "Circuit copper trace replacement foil / eyelets",
            "UV-curable solder mask green resin"
        ],
        "step_by_step_sop": [
            "Step 1: Scrape away burnt carbonized FR-4 resin until clean un-charred fiberglass is exposed.",
            "Step 2: Bridge any severed copper tracks using 30 AWG enamel jumper wire or replacement copper foil.",
            "Step 3: Fill cavity with 2-part epoxy resin, cure for 30 minutes at 60°C.",
            "Step 4: Coat with green UV solder mask and cure under 365nm UV lamp.",
            "Step 5: NOTE: For Class 3 mission-critical aerospace/medical boards, quarantine and SCRAP board per MRB disposition."
        ],
        "pnp_machine_action": "Check reflow oven temperature profile immediately. Halt conveyor line until thermal thermocouple verification is complete."
    }
}


def generate_rework_plan_for_board(board_id: str, defect_type: str, components_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Synthesizes actionable engineering rework orders with exact tools, consumables,
    and IPC-compliant SOP steps based on observed defects.
    """
    clean_def = (defect_type or "none").lower()
    
    # Match against defect knowledge base
    matched_key = "missing"
    if "tomb" in clean_def:
        matched_key = "tombstone"
    elif "tilt" in clean_def or "skew" in clean_def:
        matched_key = "tilt"
    elif "shift" in clean_def or "overhang" in clean_def:
        matched_key = "shift"
    elif "burn" in clean_def or "char" in clean_def or "rupture" in clean_def:
        matched_key = "severe_thermal_burn"
    elif "none" in clean_def:
        return {
            "board_id": board_id,
            "status": "PASS",
            "has_defects": False,
            "title": "Conforming Assembly — No Rework Required",
            "ipc_standard": "IPC-A-610H Class 2 & 3 Target Condition: Assembly meets all visual acceptability requirements.",
            "root_cause": ["Nominal SMT line operation."],
            "required_tools": ["Standard AOI verification pass."],
            "required_materials": ["None required."],
            "step_by_step_sop": ["1. Forward board to downstream conformal coating or secondary inspection stage."],
            "pnp_machine_action": "Maintain active feeder calibration offsets. Zero corrections needed."
        }

    kb = REWORK_KNOWLEDGE_BASE.get(matched_key, REWORK_KNOWLEDGE_BASE["missing"])
    
    # Identify defective component IDs
    defective_comps = []
    for c in components_data:
        if c.get("status") in ["DEFECT", "REWORK", "FAIL"] or c.get("is_missing") or c.get("tombstone") or c.get("tilt"):
            cid = c.get("id") or c.get("component_id") or "UNKNOWN"
            defective_comps.append(cid)
            
    if not defective_comps:
        defective_comps = ["Primary Affected Component"]

    return {
        "board_id": board_id,
        "status": "REWORK_REQUIRED",
        "has_defects": True,
        "defect_type": defect_type,
        "affected_components": defective_comps,
        "title": kb["title"],
        "ipc_standard": kb["ipc_standard"],
        "root_cause": kb["root_cause"],
        "required_tools": kb["required_tools"],
        "required_materials": kb["required_materials"],
        "step_by_step_sop": kb["step_by_step_sop"],
        "pnp_machine_action": kb["pnp_machine_action"] % (", ".join(defective_comps)),
        "disposition": "RETURN TO SMT REWORK BENCH 01" if matched_key != "severe_thermal_burn" else "SCRAP / MATERIAL REVIEW BOARD"
    }
