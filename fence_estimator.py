"""
Fence Depot Estimator
Calculates materials needed for fence installation projects.
"""


FENCE_TYPES = {
    "1": "Wood Privacy",
    "2": "Chain Link",
    "3": "Split Rail",
}

# Post spacing in feet for each fence type
POST_SPACING = {
    "Wood Privacy": 8,
    "Chain Link": 10,
    "Split Rail": 8,
}

# Rails per section for each fence type
RAILS_PER_SECTION = {
    "Wood Privacy": 3,
    "Chain Link": 0,   # uses tension wire / top rail counted separately
    "Split Rail": 2,
}

# Pickets per section (8-ft section with 3.5" pickets, slight overlap)
PICKETS_PER_SECTION = {
    "Wood Privacy": 27,
    "Chain Link": 0,
    "Split Rail": 0,
}

# Bags of concrete per post (60-lb bags)
CONCRETE_PER_POST = 2


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


def get_fence_height():
    print("\nCommon chain link fence heights (in feet):")
    print("  1. 4 ft")
    print("  2. 5 ft")
    print("  3. 6 ft")
    print("  4. Other")
    while True:
        choice = input("Select height (1-4): ").strip()
        if choice == "1":
            return 4
        elif choice == "2":
            return 5
        elif choice == "3":
            return 6
        elif choice == "4":
            return get_positive_float("Enter fence height in feet: ")
        print("  Please enter 1, 2, 3, or 4.")


def choose_fence_type():
    print("\nFence Types:")
    for key, name in FENCE_TYPES.items():
        print(f"  {key}. {name}")
    while True:
        choice = input("Select fence type (1-3): ").strip()
        if choice in FENCE_TYPES:
            return FENCE_TYPES[choice]
        print("  Please enter 1, 2, or 3.")


def calculate_materials(fence_type, linear_feet, num_gates, fence_height=None):
    spacing = POST_SPACING[fence_type]

    # Number of sections and posts
    num_sections = linear_feet / spacing
    num_posts = int(num_sections) + 1   # one post per section end, plus final post

    # Add gate posts (each gate needs 2 posts; deduct one section per gate)
    gate_posts = num_gates * 2
    total_posts = num_posts + gate_posts - num_gates  # gates replace a section

    # Concrete bags
    concrete_bags = total_posts * CONCRETE_PER_POST

    results = {
        "fence_type": fence_type,
        "linear_feet": linear_feet,
        "num_gates": num_gates,
        "posts": total_posts,
        "concrete_bags": concrete_bags,
    }

    if fence_height is not None:
        results["fence_height"] = fence_height

    if fence_type == "Wood Privacy":
        fence_sections = int(num_sections) - num_gates
        rails = fence_sections * RAILS_PER_SECTION["Wood Privacy"]
        pickets = fence_sections * PICKETS_PER_SECTION["Wood Privacy"]
        results["rails_8ft"] = rails
        results["pickets"] = pickets

    elif fence_type == "Chain Link":
        height = results.get("fence_height", 4)
        gate_width = 4   # standard single gate opening in feet

        # Fabric: linear feet minus gate openings (sold in rolls, round up to 50-ft roll)
        fabric_feet = max(0, linear_feet - (num_gates * gate_width))
        fabric_rolls_50ft = -(-int(fabric_feet) // 50)   # ceiling division

        # Top rail: 1-3/8" pipe in 10-ft lengths, one per line section
        fence_run = max(0, linear_feet - (num_gates * gate_width))
        top_rail_10ft = -(-int(fence_run) // 10)   # ceiling division

        # Posts: terminal posts (end/corner/gate) and line posts
        #   - 2 end posts + 2 posts per gate = terminal posts
        #   - line posts every 10 ft between terminals
        terminal_posts = 2 + (num_gates * 2)
        line_posts = max(0, total_posts - terminal_posts)

        # Post heights: top of post = fence height + 2 ft buried
        line_post_height = height + 2
        terminal_post_height = height + 2

        # Tension wire (bottom): 1 strand, 1 roll per 100 ft (9-gauge)
        tension_wire_rolls = -(-int(fence_run) // 100)

        # Tension bars: 1 per terminal post (woven into fabric at ends/gates)
        tension_bars = terminal_posts

        # Brace bands: 2 per terminal post (secure top rail to terminal post)
        brace_bands = terminal_posts * 2

        # Rail ends (eye tops for line posts): 1 per line post
        rail_ends = line_posts

        # Tie wires: ~1 per foot of fabric on top rail + 1 per foot on tension wire
        tie_wires = int(fence_run) * 2

        # Gate hardware per gate: 2 hinges + 1 latch + gate frame tube (perimeter)
        gate_hinges = num_gates * 2
        gate_latches = num_gates
        gate_frame_perimeter = num_gates * (gate_width * 2 + height * 2)   # ft of 1-3/8" pipe

        # Update total_posts to use line + terminal breakdown
        results["posts"] = total_posts
        results["terminal_posts"] = terminal_posts
        results["line_posts"] = line_posts
        results["line_post_height_ft"] = line_post_height
        results["terminal_post_height_ft"] = terminal_post_height
        results["chain_link_fabric_feet"] = int(fabric_feet)
        results["chain_link_fabric_rolls_50ft"] = fabric_rolls_50ft
        results["top_rail_10ft"] = top_rail_10ft
        results["tension_wire_rolls_100ft"] = tension_wire_rolls
        results["tension_bars"] = tension_bars
        results["brace_bands"] = brace_bands
        results["rail_ends"] = rail_ends
        results["tie_wires"] = tie_wires
        if num_gates > 0:
            results["gate_hinges"] = gate_hinges
            results["gate_latches"] = gate_latches
            results["gate_frame_pipe_ft"] = gate_frame_perimeter

    elif fence_type == "Split Rail":
        fence_sections = int(num_sections) - num_gates
        rails = fence_sections * RAILS_PER_SECTION["Split Rail"]
        results["rails_8ft"] = rails

    return results


def display_results(r):
    print("\n" + "=" * 45)
    print("  FENCE DEPOT ESTIMATOR — MATERIALS LIST")
    print("=" * 45)
    print(f"  Fence Type   : {r['fence_type']}")
    print(f"  Linear Feet  : {r['linear_feet']:.0f} ft")
    print(f"  Gates        : {r['num_gates']}")
    print("-" * 45)
    print("  MATERIALS NEEDED:")
    print(f"    Posts                : {r['posts']}")
    print(f"    Concrete (60-lb bags): {r['concrete_bags']}")

    if "rails_8ft" in r:
        print(f"    Rails (8-ft)         : {r['rails_8ft']}")
    if "pickets" in r:
        print(f"    Pickets              : {r['pickets']}")
    if "chain_link_fabric_feet" in r:
        height_str = f" ({r['fence_height']} ft tall)" if "fence_height" in r else ""
        print(f"\n  CHAIN LINK DETAILS{height_str}:")
        print(f"    Terminal Posts ({r.get('terminal_post_height_ft', '-')} ft) : {r.get('terminal_posts', '-')}")
        print(f"    Line Posts ({r.get('line_post_height_ft', '-')} ft)     : {r.get('line_posts', '-')}")
        print(f"    Chain Link Fabric        : {r['chain_link_fabric_feet']} ft  ({r.get('chain_link_fabric_rolls_50ft', '-')} x 50-ft rolls)")
        print(f"    Top Rail (10-ft lengths) : {r['top_rail_10ft']}")
        print(f"    Tension Wire (100-ft rolls): {r.get('tension_wire_rolls_100ft', '-')}")
        print(f"    Tension Bars             : {r.get('tension_bars', '-')}")
        print(f"    Brace Bands              : {r.get('brace_bands', '-')}")
        print(f"    Rail Ends (eye tops)     : {r.get('rail_ends', '-')}")
        print(f"    Tie Wires                : {r.get('tie_wires', '-')}")
        if r.get("num_gates", 0) > 0:
            print(f"\n  GATE HARDWARE ({r['num_gates']} gate(s)):")
            print(f"    Gate Hinges              : {r.get('gate_hinges', '-')}")
            print(f"    Gate Latches             : {r.get('gate_latches', '-')}")
            print(f"    Gate Frame Pipe          : {r.get('gate_frame_pipe_ft', '-')} ft of 1-3/8\" pipe")

    print("=" * 45)
    print("  Note: Add 10% to material quantities for waste.")
    print("=" * 45)


def run_estimator():
    print("\n" + "=" * 45)
    print("     FENCE DEPOT ESTIMATOR")
    print("=" * 45)

    fence_type = choose_fence_type()
    linear_feet = get_positive_float("\nTotal linear feet of fence: ")
    num_gates = get_positive_int("Number of gates: ")

    fence_height = None
    if fence_type == "Chain Link":
        fence_height = get_fence_height()

    results = calculate_materials(fence_type, linear_feet, num_gates, fence_height)
    display_results(results)

    again = input("\nRun another estimate? (y/n): ").strip().lower()
    if again == "y":
        run_estimator()


if __name__ == "__main__":
    run_estimator()
