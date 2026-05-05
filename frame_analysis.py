import math

# ==========================================================
# PYTHON-BASED STRUCTURAL FRAME ANALYSIS
# Vehicle Frame / Go-Kart / BAJA / Utility Vehicle Chassis
# ==========================================================

# -----------------------------
# MATERIAL DATABASE
# -----------------------------

materials = {
    "Mild Steel": {
        "youngs_modulus": 200e9,       # Pa
        "yield_strength": 250e6        # Pa
    },
    "AISI 4130": {
        "youngs_modulus": 205e9,       # Pa
        "yield_strength": 435e6        # Pa
    },
    "Aluminium 6061-T6": {
        "youngs_modulus": 69e9,        # Pa
        "yield_strength": 276e6        # Pa
    }
}

# -----------------------------
# USER DATA SECTION
# Change values here only
# -----------------------------

frame_length = 1.4          # metre
frame_width = 0.8           # metre
frame_height = 0.5          # metre

material_name = "AISI 4130"

tube_outer_diameter_mm = 25.4      # mm
tube_thickness_mm = 2.0            # mm

vehicle_mass_with_driver = 180     # kg
dynamic_load_factor = 3            # 3g bump condition

# For simple calculation, one main frame member is analysed
member_length = frame_length       # metre

# -----------------------------
# UNIT CONVERSION
# -----------------------------

outer_diameter = tube_outer_diameter_mm / 1000
tube_thickness = tube_thickness_mm / 1000
inner_diameter = outer_diameter - (2 * tube_thickness)

# -----------------------------
# VALIDATION
# -----------------------------

if material_name not in materials:
    raise ValueError("Selected material is not available in material database.")

if inner_diameter <= 0:
    raise ValueError("Invalid tube thickness. Inner diameter became zero or negative.")

# -----------------------------
# MATERIAL PROPERTIES
# -----------------------------

E = materials[material_name]["youngs_modulus"]
yield_strength = materials[material_name]["yield_strength"]

# -----------------------------
# TUBE SECTION PROPERTIES
# -----------------------------

area = (math.pi / 4) * (outer_diameter**2 - inner_diameter**2)

moment_of_inertia = (math.pi / 64) * (
    outer_diameter**4 - inner_diameter**4
)

outer_radius = outer_diameter / 2

# -----------------------------
# LOAD CALCULATION
# -----------------------------

gravity = 9.81

static_load = vehicle_mass_with_driver * gravity
dynamic_load = static_load * dynamic_load_factor

# -----------------------------
# STRUCTURAL CALCULATION
# Simply supported beam with centre load
# -----------------------------

maximum_bending_moment = (dynamic_load * member_length) / 4

bending_stress = (
    maximum_bending_moment * outer_radius
) / moment_of_inertia

deflection = (
    dynamic_load * member_length**3
) / (
    48 * E * moment_of_inertia
)

factor_of_safety = yield_strength / bending_stress

# -----------------------------
# RESULT FUNCTION
# -----------------------------

def print_result():
    print("\n==========================================")
    print(" VEHICLE FRAME STRUCTURAL ANALYSIS RESULT ")
    print("==========================================")

    print(f"\nFrame Length              : {frame_length:.3f} m")
    print(f"Frame Width               : {frame_width:.3f} m")
    print(f"Frame Height              : {frame_height:.3f} m")

    print(f"\nSelected Material         : {material_name}")
    print(f"Young's Modulus           : {E / 1e9:.2f} GPa")
    print(f"Yield Strength            : {yield_strength / 1e6:.2f} MPa")

    print(f"\nTube Outer Diameter       : {tube_outer_diameter_mm:.2f} mm")
    print(f"Tube Inner Diameter       : {inner_diameter * 1000:.2f} mm")
    print(f"Tube Thickness            : {tube_thickness_mm:.2f} mm")

    print(f"\nCross Sectional Area      : {area:.8f} m^2")
    print(f"Moment of Inertia         : {moment_of_inertia:.12f} m^4")

    print(f"\nVehicle Mass with Driver  : {vehicle_mass_with_driver:.2f} kg")
    print(f"Static Load               : {static_load:.2f} N")
    print(f"Dynamic Load Factor       : {dynamic_load_factor}g")
    print(f"Dynamic Load              : {dynamic_load:.2f} N")

    print(f"\nMaximum Bending Moment    : {maximum_bending_moment:.2f} Nm")
    print(f"Bending Stress            : {bending_stress / 1e6:.2f} MPa")
    print(f"Deflection                : {deflection * 1000:.3f} mm")
    print(f"Factor of Safety          : {factor_of_safety:.2f}")

    print("\n------------------------------------------")

    if factor_of_safety >= 2:
        print("STATUS: SAFE")
        print("The frame member is safe for the given loading condition.")
    else:
        print("STATUS: NOT SAFE")
        print("The frame member is not safe for the given loading condition.")
        print("Suggestion: Increase tube diameter, thickness, or add bracing.")

    print("------------------------------------------\n")


# -----------------------------
# MAIN PROGRAM
# -----------------------------

print_result()
