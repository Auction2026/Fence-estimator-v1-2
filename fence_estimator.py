"""
Fence Depot Estimator
Chain-Link Fencing — Residential & Commercial
Includes: full materials, colours, gate types, shop drawings, installation & labour.
"""

# ---------------------------------------------------------------------------
# COLOURS AVAILABLE
# ---------------------------------------------------------------------------
CHAIN_LINK_COLOURS = {
    "1": "Galvanized (Silver)",
    "2": "Black Vinyl-Coated",
    "3": "Green Vinyl-Coated",
    "4": "Brown Vinyl-Coated",
    "5": "Almond Vinyl-Coated",
}

# ---------------------------------------------------------------------------
# GAUGE OPTIONS (fabric wire gauge)
# ---------------------------------------------------------------------------
FABRIC_GAUGES = {
    "1": ("11-gauge", "Residential standard"),
    "2": ("9-gauge",  "Commercial standard"),
    "3": ("6-gauge",  "Heavy commercial / industrial"),
}

# ---------------------------------------------------------------------------
# MESH SIZE
# ---------------------------------------------------------------------------
MESH_SIZES = {
    "1": '2" mesh (residential)',
    "2": '2-1/4" mesh (commercial)',
    "3": '1-3/4" mesh (security)',
}

# ---------------------------------------------------------------------------
# POST SIZES  (OD inches)  line post / terminal post
# ---------------------------------------------------------------------------
POST_SPECS = {
    "residential": {
        "line":     ("1-5/8\"",  "Schedule 20"),
        "terminal": ("2\"",      "Schedule 20"),
        "gate":     ("2-1/2\"",  "Schedule 20"),
    },
    "commercial": {
        "line":     ("2\"",      "Schedule 40"),
        "terminal": ("2-1/2\"",  "Schedule 40"),
        "gate":     ("3\"",      "Schedule 40"),
    },
}

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def ceil_div(a, b):
    """Ceiling integer division."""
    return -(-int(a) // b)


def hr(char="=", width=60):
    return char * width


def get_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
            print("  Please enter a number greater than 0.")
        except ValueError:
            print("  Invalid input. Please enter a number.")


def get_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value >= 0:
                return value
            print("  Please enter 0 or a positive whole number.")
        except ValueError:
            print("  Invalid input. Please enter a whole number.")


def pick(menu_dict, prompt, extra_label=None):
    """Generic menu picker. Returns key."""
    for k, v in menu_dict.items():
        label = v if isinstance(v, str) else f"{v[0]}  — {v[1]}"
        if extra_label:
            print(f"  {k}. {label}")
        else:
            print(f"  {k}. {label}")
    keys = list(menu_dict.keys())
    while True:
        choice = input(f"{prompt} ({keys[0]}-{keys[-1]}): ").strip()
        if choice in menu_dict:
            return choice
        print(f"  Please enter {', '.join(keys)}.")


# ---------------------------------------------------------------------------
# GATE SHOP DRAWINGS (ASCII)
# ---------------------------------------------------------------------------

def shop_drawing_single_swing(width_ft, height_ft):
    w = max(12, width_ft * 4)
    h = max(6,  height_ft * 2)
    top    = "+" + "-" * (w - 2) + "+"
    mid    = "|" + " " * (w - 2) + "|"
    hinge1 = "|H" + " " * (w - 4) + " |"
    hinge2 = "|H" + " " * (w - 4) + " |"
    latch  = "|" + " " * (w - 4) + "L|"
    diag_row = []
    for i in range(h - 4):
        pos = int((w - 2) * i / (h - 4))
        row = list(" " * (w - 2))
        row[min(pos, w - 3)] = "\\"
        diag_row.append("|" + "".join(row) + "|")

    print(hr("-"))
    print(f"  SHOP DRAWING — SINGLE SWING GATE  ({width_ft} ft wide x {height_ft} ft tall)")
    print(hr("-"))
    print(f"  Frame: 1-5/8\" (res) or 2\" (comm) square tubing / pipe")
    print(f"  Hinge: 2 x heavy-duty offset hinges on hinge post")
    print(f"  Latch: 1 x fork latch + keeper on latch post")
    print(f"  Infill: chain-link fabric, same spec as fence")
    print()
    print("  " + top)
    print("  " + hinge1)
    for row in diag_row:
        print("  " + row)
    print("  " + hinge2)
    print("  " + latch)
    print("  " + top)
    print(f"\n  Width = {width_ft} ft   Height = {height_ft} ft")
    print(f"  Frame perimeter = {width_ft*2 + height_ft*2} ft of frame pipe/tube")
    print(f"  Fabric = {width_ft} ft wide x {height_ft} ft tall (1 piece)")
    print(f"  Hinges: 2   Latch: 1   Hinge post OD: 2-1/2\" or 3\"")
    print(hr("-"))


def shop_drawing_double_swing(width_ft, height_ft):
    leaf = width_ft // 2
    print(hr("-"))
    print(f"  SHOP DRAWING — DOUBLE SWING GATE  ({width_ft} ft wide x {height_ft} ft tall)")
    print(hr("-"))
    print(f"  Two leaves, each {leaf} ft wide x {height_ft} ft tall")
    print(f"  Frame: 1-5/8\" (res) or 2\" (comm) pipe, each leaf")
    print(f"  Hinges: 2 per leaf = 4 total (one leaf per hinge post)")
    print(f"  Latch: centre fork latch or drop rod")
    print()
    w = max(8, leaf * 4)
    h = max(5, height_ft * 2)
    top = "+" + "-" * (w - 2) + "+"
    mid = "|" + " " * (w - 2) + "|"
    print(f"  LEFT LEAF              RIGHT LEAF")
    for i in range(h):
        if i == 0 or i == h - 1:
            print(f"  {top}    {top}")
        elif i == 1:
            print(f"  |H{' '*(w-4)} |    | {' '*(w-4)}H|")
        elif i == h - 2:
            print(f"  |H{' '*(w-4)} |    | {' '*(w-4)}H|")
        elif i == h // 2:
            print(f"  |{' '*(w-4)}L|    |L{' '*(w-4)} |")
        else:
            print(f"  {mid}    {mid}")
    print(f"\n  Each leaf: fabric {leaf} ft x {height_ft} ft")
    print(f"  Total frame pipe: {(leaf*2+height_ft*2)*2} ft  (both leaves)")
    print(f"  Drop rod (centre lock): 1   Hinges: 4   Latch: 1")
    print(hr("-"))


def shop_drawing_cantilever_slide(width_ft, height_ft):
    clearance = int(width_ft * 1.5)   # cantilever back-span = 1.5x opening
    print(hr("-"))
    print(f"  SHOP DRAWING — CANTILEVER SLIDE GATE  ({width_ft} ft opening x {height_ft} ft tall)")
    print(hr("-"))
    print(f"  Gate panel length = {clearance} ft  (1.5x opening — no ground track)")
    print(f"  Frame: 2\" or 2-1/2\" square tube (commercial spec)")
    print(f"  Rollers: 4 x cantilever roller carriages on single post")
    print(f"  Guide post: 1 (at far side of opening)")
    print(f"  Stop post: 1 (open side)")
    print()
    bar  = "=" * (clearance * 2)
    top  = "+" + bar + "+"
    rails= "|" + "=" * (clearance * 2) + "|"
    mid  = "|" + " " * (clearance * 2) + "|"
    print(f"  {top}")
    print(f"  {rails}   <— top rail")
    for _ in range(max(2, height_ft - 2)):
        print(f"  {mid}")
    print(f"  {rails}   <— bottom rail")
    print(f"  {top}")
    print()
    print(f"  [ROLLER]  [ROLLER]              [GUIDE]")
    print(f"      |         |                    |")
    print(f"  POST(latch end)            GUIDE POST")
    print()
    print(f"  Panel length : {clearance} ft")
    print(f"  Panel height : {height_ft} ft")
    print(f"  Roller carriages : 4   Guide post: 1   Stop: 1")
    print(f"  Frame pipe   : ~{(clearance*2 + height_ft*2)} ft of 2\" sq tube")
    print(hr("-"))


def shop_drawing_roll_slide(width_ft, height_ft):
    print(hr("-"))
    print(f"  SHOP DRAWING — ROLLING SLIDE GATE  ({width_ft} ft opening x {height_ft} ft tall)")
    print(hr("-"))
    print(f"  Requires ground track ({width_ft + 2} ft) embedded in concrete")
    print(f"  Gate panel: {width_ft} ft wide x {height_ft} ft tall")
    print(f"  Frame: 2\" sq tube (commercial spec)")
    print(f"  Wheels: 4 x V-groove wheel rollers on bottom rail")
    print(f"  Top guide bracket: 1 on support post")
    print()
    bar = "-" * (width_ft * 3)
    print(f"  +{bar}+")
    for i in range(max(3, height_ft)):
        print(f"  |{' ' * (width_ft * 3)}|")
    print(f"  +{bar}+")
    print(f"  W   W                         W   W   <— V-groove wheels")
    print(f"  ===={bar}====   <— ground track")
    print()
    print(f"  Ground track : {width_ft + 2} ft")
    print(f"  Wheels: 4   Top guide: 1   Frame pipe: ~{width_ft*2 + height_ft*2} ft")
    print(hr("-"))


# ---------------------------------------------------------------------------
# GATE DETAILS INPUT
# ---------------------------------------------------------------------------

GATE_TYPES = {
    "1": "Single Swing",
    "2": "Double Swing",
    "3": "Cantilever Slide (commercial)",
    "4": "Rolling Slide (commercial)",
}

GATE_WIDTHS = {
    "Single Swing":           [3, 4, 5, 6],
    "Double Swing":           [8, 10, 12, 14, 16, 20, 24],
    "Cantilever Slide (commercial)": [10, 12, 14, 16, 20, 24, 30],
    "Rolling Slide (commercial)":    [10, 12, 14, 16, 20, 24, 30],
}


def collect_gates(fence_height):
    gates = []
    num = get_positive_int("\nHow many gates total? ")
    for i in range(num):
        print(f"\n  --- Gate {i+1} ---")
        print("  Gate type:")
        for k, v in GATE_TYPES.items():
            print(f"    {k}. {v}")
        gt_key = pick(GATE_TYPES, "  Gate type")
        gate_type = GATE_TYPES[gt_key]

        common_widths = GATE_WIDTHS[gate_type]
        print(f"  Common widths (ft): {', '.join(str(w) for w in common_widths)}")
        gate_width = get_positive_float("  Gate width (ft): ")
        gate_height = fence_height   # gates match fence height

        gates.append({
            "type":   gate_type,
            "width":  gate_width,
            "height": gate_height,
        })
    return gates


# ---------------------------------------------------------------------------
# BARBWIRE INPUT
# ---------------------------------------------------------------------------

def collect_barbwire(linear_feet):
    print("\nBarb wire / razor wire options:")
    print("  1. No barb wire")
    print("  2. 3-strand barb wire (standard commercial)")
    print("  3. 5-strand barb wire (high security)")
    print("  4. Razor (concertina) coil on top")
    choice = pick({"1": "None", "2": "3-strand", "3": "5-strand", "4": "Razor"}, "  Select")
    if choice == "1":
        return None
    strands_map = {"2": 3, "3": 5}
    if choice in strands_map:
        strands = strands_map[choice]
        # arms every 10 ft, each arm holds strands
        arms = ceil_div(linear_feet, 10)
        # wire rolls: 1 roll = 1320 ft
        rolls = ceil_div(linear_feet * strands, 1320)
        return {"type": f"{strands}-strand barb wire", "arms": arms, "wire_rolls_1320ft": rolls, "strands": strands}
    else:
        # razor coil: 1 coil per 3 linear ft
        coils = ceil_div(linear_feet, 3)
        return {"type": "Razor coil", "coils": coils}


# ---------------------------------------------------------------------------
# CORE CHAIN-LINK CALCULATION
# ---------------------------------------------------------------------------

def calculate_chain_link(sector, linear_feet, fence_height, colour_key,
                          gauge_key, mesh_key, gates, barbwire,
                          num_corners=0):
    """
    sector: 'residential' or 'commercial'
    Returns dict of all materials.
    """
    post_spacing = 10   # ft between line posts
    gate_width_total = sum(g["width"] for g in gates)
    fence_run = max(0.0, linear_feet - gate_width_total)

    # --- Posts ---
    # Terminal posts: 2 end posts + 2 per corner + 2 per gate
    terminal_posts = 2 + (num_corners * 2) + (len(gates) * 2)
    # Line posts fill in the remaining run
    line_post_count = max(0, ceil_div(fence_run, post_spacing) - 1)
    total_posts = terminal_posts + line_post_count

    post_spec = POST_SPECS[sector]
    post_bury = 3 if sector == "residential" else 3.5
    line_post_length   = fence_height + post_bury
    terminal_post_length = fence_height + post_bury

    # --- Concrete ---
    # residential: 2 x 60-lb bags per post; commercial: 3 x 80-lb bags per post
    if sector == "residential":
        concrete_bags = total_posts * 2
        concrete_bag_lb = 60
    else:
        concrete_bags = total_posts * 3
        concrete_bag_lb = 80

    # --- Fabric ---
    fabric_feet = int(fence_run)
    fabric_rolls = ceil_div(fabric_feet, 50)

    # --- Top rail ---
    top_rail_lengths = ceil_div(fence_run, 10)

    # --- Tension wire ---
    tension_wire_rolls = ceil_div(fence_run, 100)   # 100-ft rolls, 9-gauge

    # --- Hardware ---
    tension_bars   = terminal_posts
    brace_bands    = terminal_posts * 2
    rail_ends      = line_post_count          # eye top per line post
    loop_caps      = line_post_count          # loop cap per line post
    post_caps      = terminal_posts
    # Tie wires: every 24" on top rail + every 18" on tension wire
    tie_wires_top  = ceil_div(fence_run, 2)
    tie_wires_bot  = ceil_div(fence_run, 1.5)
    tie_wires_total = tie_wires_top + tie_wires_bot

    # --- Gate materials ---
    gate_materials = []
    for g in gates:
        gtype   = g["type"]
        gw      = g["width"]
        gh      = g["height"]
        frame_ft = gw * 2 + gh * 2
        fabric_sf = gw * gh
        spec = post_spec["gate"]

        gm = {
            "type":        gtype,
            "width_ft":    gw,
            "height_ft":   gh,
            "frame_pipe_ft": frame_ft,
            "fabric_sqft":   fabric_sf,
            "gate_post_od":  spec[0],
        }
        if "Swing" in gtype:
            gm["hinges"]  = 2 if "Single" in gtype else 4
            gm["latch"]   = 1
            gm["hinge_post_od"] = spec[0]
        if "Slide" in gtype or "Cantilever" in gtype:
            gm["rollers"] = 4
            gm["guide_post"] = 1
            gm["stop_post"]  = 1
            if "Cantilever" in gtype:
                gm["panel_length_ft"] = int(gw * 1.5)
        if "Rolling" in gtype:
            gm["track_ft"] = gw + 2
            gm["wheels"]   = 4
        gate_materials.append(gm)

    return {
        "sector":          sector,
        "linear_feet":     linear_feet,
        "fence_height":    fence_height,
        "fence_run":       fence_run,
        "colour":          CHAIN_LINK_COLOURS[colour_key],
        "gauge":           FABRIC_GAUGES[gauge_key][0],
        "mesh":            MESH_SIZES[mesh_key],
        "num_corners":     num_corners,
        "gates":           gates,
        "gate_materials":  gate_materials,
        "barbwire":        barbwire,
        # posts
        "terminal_posts":        terminal_posts,
        "line_posts":            line_post_count,
        "total_posts":           total_posts,
        "line_post_length_ft":   line_post_length,
        "terminal_post_length_ft": terminal_post_length,
        "line_post_od":          post_spec["line"][0],
        "terminal_post_od":      post_spec["terminal"][0],
        # concrete
        "concrete_bags":    concrete_bags,
        "concrete_bag_lb":  concrete_bag_lb,
        # fabric
        "fabric_feet":      fabric_feet,
        "fabric_rolls":     fabric_rolls,
        # top rail
        "top_rail_lengths": top_rail_lengths,
        # tension wire
        "tension_wire_rolls": tension_wire_rolls,
        # hardware
        "tension_bars":   tension_bars,
        "brace_bands":    brace_bands,
        "rail_ends":      rail_ends,
        "loop_caps":      loop_caps,
        "post_caps":      post_caps,
        "tie_wires":      tie_wires_total,
    }


# ---------------------------------------------------------------------------
# LABOUR ESTIMATE
# ---------------------------------------------------------------------------

def labour_estimate(r):
    """
    Returns dict of estimated labour hours by trade task.
    Based on typical production rates.
    """
    lf   = r["linear_feet"]
    tp   = r["total_posts"]
    sect = r["sector"]

    # Rates (hours per unit)
    rate_layout    = 0.05   # per linear ft: layout & string line
    rate_dig       = 0.20 if sect == "residential" else 0.30   # per post: dig & set
    rate_fabric    = 0.04   # per linear ft: hang & tie fabric
    rate_rail      = 0.06   # per linear ft: install top rail
    rate_tensioning= 0.03   # per linear ft: tension & tie
    rate_gate_swing= 3.5    # per swing gate: frame, hang, adjust
    rate_gate_slide= 8.0    # per slide/cantilever gate: frame, rollers, adjust
    rate_barbwire  = 0.05   # per linear ft per strand
    rate_cleanup   = 0.02   # per linear ft

    h_layout    = lf * rate_layout
    h_posts     = tp * rate_dig
    h_fabric    = lf * rate_fabric
    h_rail      = lf * rate_rail
    h_tensioning= lf * rate_tensioning
    h_gates     = 0.0
    for g in r["gates"]:
        if "Swing" in g["type"]:
            h_gates += rate_gate_swing
        else:
            h_gates += rate_gate_slide
    h_barbwire  = 0.0
    bw = r.get("barbwire")
    if bw and "strands" in bw:
        h_barbwire = lf * rate_barbwire * bw["strands"]
    elif bw and "coils" in bw:
        h_barbwire = lf * 0.08
    h_cleanup   = lf * rate_cleanup

    total = h_layout + h_posts + h_fabric + h_rail + h_tensioning + h_gates + h_barbwire + h_cleanup

    return {
        "layout":      round(h_layout, 1),
        "post_dig_set": round(h_posts, 1),
        "fabric_hang": round(h_fabric, 1),
        "top_rail":    round(h_rail, 1),
        "tensioning":  round(h_tensioning, 1),
        "gates":       round(h_gates, 1),
        "barbwire":    round(h_barbwire, 1),
        "cleanup":     round(h_cleanup, 1),
        "total":       round(total, 1),
    }


# ---------------------------------------------------------------------------
# INSTALLATION STEPS
# ---------------------------------------------------------------------------

INSTALL_STEPS_RESIDENTIAL = [
    "1.  Mark fence line with stakes and string line.",
    "2.  Locate all underground utilities before digging.",
    "3.  Dig terminal post holes: 8\" dia x depth ({post_bury} ft bury).",
    "4.  Set terminal posts (end, corner, gate posts) plumb in concrete.",
    "5.  Let concrete cure 24–48 hours before continuing.",
    "6.  Stretch string line between terminal posts at top height.",
    "7.  Locate and dig line post holes every 10 ft.",
    "8.  Set line posts plumb and align with string line.",
    "9.  Install top rail through loop caps on line posts and brace bands on terminals.",
    "10. Unroll chain-link fabric; stand on end at one terminal post.",
    "11. Weave tension bar through first row of fabric; bolt to terminal post.",
    "12. Unroll fabric along fence, connect sections with tying spiral.",
    "13. Use come-along/fence stretcher to tension fabric — no sag.",
    "14. Weave tension bar through far end; bolt to far terminal.",
    "15. Attach fabric to top rail and line posts with tie wires every 24\".",
    "16. Run bottom tension wire through fabric at base; tie every 24\".",
    "17. Hang gate(s): set hinges, hang frame, check swing/operation, install latch.",
    "18. Install post caps on all terminal posts.",
    "19. Final inspection: check plumb, tension, gates, tie wire spacing.",
    "20. Clean up site; remove spoils from post holes.",
]

INSTALL_STEPS_COMMERCIAL = [
    "1.  Survey fence line; establish corners and bearing.",
    "2.  Obtain permits and call before you dig (utility locate).",
    "3.  Dig terminal post holes: 10\" dia x {post_bury} ft deep (frost line).",
    "4.  Form and pour concrete footings for terminal posts; embed posts.",
    "5.  Brace terminal posts in two directions; cure 48–72 hours.",
    "6.  Lay out line post spacing at 10 ft o.c.; dig 8\" dia holes.",
    "7.  Set line posts; fill with concrete; align with string.",
    "8.  Install top rail: thread through loop caps, join with rail sleeves.",
    "9.  Install mid rail if fence height ≥ 8 ft.",
    "10. Unroll fabric (heavier gauge); stand vertical at terminal post.",
    "11. Attach tension bar + hardware to first terminal; stretch fabric.",
    "12. Use mechanical stretcher (come-along + tension bar) for commercial gauge.",
    "13. Secure far end with tension bar to terminal post.",
    "14. Attach fabric: tie wires on top rail every 24\", on mid rail every 24\".",
    "15. Run bottom tension wire; attach every 24\" with hog rings.",
    "16. Install barb wire arms on terminal and line posts if specified.",
    "17. String barb/razor wire on arms; tension each strand.",
    "18. Install gate(s) per gate shop drawing; use heavy-duty hinges.",
    "19. For slide/cantilever gates: set roller carriages, hang panel, align.",
    "20. Test gate operation; adjust stops, latches, locks.",
    "21. Install post caps; apply touch-up paint to any cuts.",
    "22. Final inspection; torque all bolts to spec; sign off checklist.",
]


def print_install_steps(r):
    sector = r["sector"]
    post_bury = 3 if sector == "residential" else 3.5
    print("\n" + hr())
    title = "RESIDENTIAL" if sector == "residential" else "COMMERCIAL"
    print(f"  INSTALLATION STEPS — {title} CHAIN-LINK")
    print(hr())
    steps = INSTALL_STEPS_RESIDENTIAL if sector == "residential" else INSTALL_STEPS_COMMERCIAL
    for step in steps:
        print("  " + step.format(post_bury=post_bury))
    print(hr())


# ---------------------------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------------------------

def display_results(r):
    W = 60
    print("\n" + hr())
    print("  FENCE DEPOT ESTIMATOR — CHAIN-LINK MATERIALS LIST")
    print(hr())
    sector_label = "RESIDENTIAL" if r["sector"] == "residential" else "COMMERCIAL"
    print(f"  Type     : {sector_label} Chain-Link")
    print(f"  Colour   : {r['colour']}")
    print(f"  Fabric   : {r['gauge']}  /  {r['mesh']}")
    print(f"  Length   : {r['linear_feet']:.0f} linear ft")
    print(f"  Height   : {r['fence_height']} ft")
    print(f"  Corners  : {r['num_corners']}")
    print(f"  Gates    : {len(r['gates'])}")
    if r["barbwire"]:
        print(f"  Barbwire : {r['barbwire']['type']}")
    print(hr("-"))

    # POSTS
    print("  POSTS:")
    print(f"    Terminal posts  {r['terminal_post_od']} OD  x {r['terminal_post_length_ft']:.0f} ft : {r['terminal_posts']}")
    print(f"    Line posts      {r['line_post_od']} OD  x {r['line_post_length_ft']:.0f} ft : {r['line_posts']}")
    print(f"    Total posts                              : {r['total_posts']}")
    print(hr("-"))

    # CONCRETE
    print("  CONCRETE:")
    print(f"    {r['concrete_bag_lb']}-lb bags                            : {r['concrete_bags']}")
    print(hr("-"))

    # FABRIC & RAIL
    print("  FABRIC & RAIL:")
    print(f"    Chain-link fabric ({r['gauge']}, {r['mesh']})  : {r['fabric_feet']} ft  ({r['fabric_rolls']} x 50-ft rolls)")
    print(f"    Top rail 1-5/8\" (10-ft lengths)        : {r['top_rail_lengths']}")
    print(hr("-"))

    # TENSION & HARDWARE
    print("  TENSION & HARDWARE:")
    print(f"    Tension wire (9-gauge, 100-ft rolls)   : {r['tension_wire_rolls']}")
    print(f"    Tension bars                           : {r['tension_bars']}")
    print(f"    Brace bands                            : {r['brace_bands']}")
    print(f"    Rail ends / eye tops (line posts)      : {r['rail_ends']}")
    print(f"    Loop caps (line posts)                 : {r['loop_caps']}")
    print(f"    Post caps (terminal posts)             : {r['post_caps']}")
    print(f"    Tie wires                              : {r['tie_wires']}")
    print(hr("-"))

    # BARBWIRE
    bw = r["barbwire"]
    if bw:
        print("  BARBWIRE / SECURITY TOPPING:")
        if "arms" in bw:
            print(f"    Type                                 : {bw['type']}")
            print(f"    Barb wire arms (every 10 ft)         : {bw['arms']}")
            print(f"    Wire rolls (1320-ft rolls)           : {bw['wire_rolls_1320ft']}")
        else:
            print(f"    Type                                 : {bw['type']}")
            print(f"    Razor coil sections (3 ft each)      : {bw['coils']}")
        print(hr("-"))

    # GATES
    if r["gate_materials"]:
        print("  GATES:")
        for i, gm in enumerate(r["gate_materials"], 1):
            print(f"\n    Gate {i}: {gm['type']}  ({gm['width_ft']} ft wide x {gm['height_ft']} ft tall)")
            print(f"      Gate post OD       : {gm['gate_post_od']}")
            print(f"      Frame pipe         : {gm['frame_pipe_ft']} ft of {gm['gate_post_od']} pipe")
            print(f"      Gate fabric        : {gm['width_ft']} ft x {gm['height_ft']} ft")
            if "hinges" in gm:
                print(f"      Hinges             : {gm['hinges']}")
                print(f"      Latch              : {gm['latch']}")
            if "rollers" in gm:
                print(f"      Roller carriages   : {gm['rollers']}")
                print(f"      Guide post         : {gm['guide_post']}")
                print(f"      Stop post          : {gm['stop_post']}")
            if "panel_length_ft" in gm:
                print(f"      Panel length       : {gm['panel_length_ft']} ft (cantilever back-span)")
            if "track_ft" in gm:
                print(f"      Ground track       : {gm['track_ft']} ft")
                print(f"      V-groove wheels    : {gm['wheels']}")
        print(hr("-"))

    # WASTE NOTE
    print("  NOTE: Add 10% to all material quantities for waste/cuts.")
    print(hr())


def display_labour(r):
    lab = labour_estimate(r)
    print("\n" + hr())
    print("  LABOUR ESTIMATE (hours)")
    print(hr())
    print(f"  Layout & string line        : {lab['layout']:>6.1f} hrs")
    print(f"  Post dig & set              : {lab['post_dig_set']:>6.1f} hrs")
    print(f"  Top rail installation       : {lab['top_rail']:>6.1f} hrs")
    print(f"  Fabric hang & tie           : {lab['fabric_hang']:>6.1f} hrs")
    print(f"  Tensioning & tie wires      : {lab['tensioning']:>6.1f} hrs")
    print(f"  Gate(s)                     : {lab['gates']:>6.1f} hrs")
    if lab["barbwire"] > 0:
        print(f"  Barb/razor wire             : {lab['barbwire']:>6.1f} hrs")
    print(f"  Site cleanup                : {lab['cleanup']:>6.1f} hrs")
    print(hr("-"))
    print(f"  TOTAL ESTIMATED HOURS       : {lab['total']:>6.1f} hrs")
    print(hr())
    print("  Labour rates vary by region. Adjust to local market.")
    print(hr())


# ---------------------------------------------------------------------------
# MAIN FLOW
# ---------------------------------------------------------------------------

def run_chain_link_estimator():
    print("\n" + hr())
    print("  FENCE DEPOT ESTIMATOR — CHAIN-LINK")
    print(hr())

    # Sector
    print("\nProject type:")
    print("  1. Residential")
    print("  2. Commercial")
    sector_choice = pick({"1": "Residential", "2": "Commercial"}, "Select")
    sector = "residential" if sector_choice == "1" else "commercial"

    # Measurements
    linear_feet  = get_positive_float("\nTotal linear feet of fence: ")
    fence_height = get_positive_float("Fence height (ft): ")
    num_corners  = get_positive_int("Number of corners (not counting ends): ")

    # Colour
    print("\nFabric colour:")
    colour_key = pick(CHAIN_LINK_COLOURS, "Select colour")

    # Gauge
    print("\nFabric wire gauge:")
    gauge_key = pick(FABRIC_GAUGES, "Select gauge", extra_label=True)

    # Mesh size
    print("\nMesh size:")
    mesh_key = pick(MESH_SIZES, "Select mesh")

    # Gates
    gates = collect_gates(fence_height)

    # Barbwire (commercial prompt or optional for residential)
    barbwire = None
    if sector == "commercial":
        barbwire = collect_barbwire(linear_feet)
    else:
        print("\nDo you want barb wire on top? (y/n): ", end="")
        if input().strip().lower() == "y":
            barbwire = collect_barbwire(linear_feet)

    # Calculate
    results = calculate_chain_link(
        sector, linear_feet, fence_height,
        colour_key, gauge_key, mesh_key,
        gates, barbwire, num_corners
    )

    # Display materials
    display_results(results)

    # Shop drawings
    if gates:
        print("\nPrint gate shop drawing(s)? (y/n): ", end="")
        if input().strip().lower() == "y":
            for g in gates:
                if g["type"] == "Single Swing":
                    shop_drawing_single_swing(int(g["width"]), int(g["height"]))
                elif g["type"] == "Double Swing":
                    shop_drawing_double_swing(int(g["width"]), int(g["height"]))
                elif g["type"] == "Cantilever Slide (commercial)":
                    shop_drawing_cantilever_slide(int(g["width"]), int(g["height"]))
                elif g["type"] == "Rolling Slide (commercial)":
                    shop_drawing_roll_slide(int(g["width"]), int(g["height"]))

    # Installation steps
    print("\nPrint installation steps? (y/n): ", end="")
    if input().strip().lower() == "y":
        print_install_steps(results)

    # Labour
    print("\nPrint labour estimate? (y/n): ", end="")
    if input().strip().lower() == "y":
        display_labour(results)

    # Run again
    print("\nRun another estimate? (y/n): ", end="")
    if input().strip().lower() == "y":
        run_chain_link_estimator()


# ---------------------------------------------------------------------------
# WOOD / SPLIT RAIL (kept intact)
# ---------------------------------------------------------------------------

def run_other_estimator():
    FENCE_TYPES_OTHER = {"1": "Wood Privacy", "2": "Split Rail"}
    POST_SPACING_OTHER = {"Wood Privacy": 8, "Split Rail": 8}
    print("\n" + hr())
    print("  FENCE DEPOT ESTIMATOR — WOOD / SPLIT RAIL")
    print(hr())
    print("\nFence type:")
    fence_type = FENCE_TYPES_OTHER[pick(FENCE_TYPES_OTHER, "Select")]
    linear_feet = get_positive_float("\nTotal linear feet: ")
    num_gates   = get_positive_int("Number of gates: ")
    spacing = POST_SPACING_OTHER[fence_type]
    num_sections = linear_feet / spacing
    total_posts = int(num_sections) + 1 + num_gates
    concrete_bags = total_posts * 2
    print("\n" + hr())
    print(f"  {fence_type.upper()} MATERIALS LIST")
    print(hr())
    print(f"  Posts               : {total_posts}")
    print(f"  Concrete (60-lb)    : {concrete_bags} bags")
    if fence_type == "Wood Privacy":
        rails   = (int(num_sections) - num_gates) * 3
        pickets = (int(num_sections) - num_gates) * 27
        print(f"  Rails (8-ft)        : {rails}")
        print(f"  Pickets (6-ft)      : {pickets}")
    else:
        rails = (int(num_sections) - num_gates) * 2
        print(f"  Rails (8-ft)        : {rails}")
    print("  Note: Add 10% for waste.")
    print(hr())


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

def main():
    print("\n" + hr())
    print("  FENCE DEPOT ESTIMATOR")
    print(hr())
    print("\nSelect fence type:")
    print("  1. Chain-Link (Residential or Commercial)")
    print("  2. Wood Privacy / Split Rail")
    choice = pick({"1": "Chain-Link", "2": "Wood/Split Rail"}, "Select")
    if choice == "1":
        run_chain_link_estimator()
    else:
        run_other_estimator()


if __name__ == "__main__":
    main()
