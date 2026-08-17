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


def choose_fence_type():
    print("\nFence Types:")
    for key, name in FENCE_TYPES.items():
        print(f"  {key}. {name}")
    while True:
        choice = input("Select fence type (1-3): ").strip()
        if choice in FENCE_TYPES:
            return FENCE_TYPES[choice]
        print("  Please enter 1, 2, or 3.")


def calculate_materials(fence_type, linear_feet, num_gates):
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

    if fence_type == "Wood Privacy":
        fence_sections = int(num_sections) - num_gates
        rails = fence_sections * RAILS_PER_SECTION["Wood Privacy"]
        pickets = fence_sections * PICKETS_PER_SECTION["Wood Privacy"]
        results["rails_8ft"] = rails
        results["pickets"] = pickets

    elif fence_type == "Chain Link":
        # Chain link: fabric by linear foot, top rail by 10-ft lengths
        fabric_feet = linear_feet - (num_gates * 4)   # approximate 4-ft gate opening
        top_rail_sections = int((linear_feet - (num_gates * 4)) / 10) + 1
        results["chain_link_fabric_feet"] = max(0, int(fabric_feet))
        results["top_rail_10ft"] = top_rail_sections

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
        print(f"    Chain Link Fabric    : {r['chain_link_fabric_feet']} ft")
    if "top_rail_10ft" in r:
        print(f"    Top Rail (10-ft)     : {r['top_rail_10ft']}")

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

    results = calculate_materials(fence_type, linear_feet, num_gates)
    display_results(results)

    again = input("\nRun another estimate? (y/n): ").strip().lower()
    if again == "y":
        run_estimator()


if __name__ == "__main__":
    run_estimator()
