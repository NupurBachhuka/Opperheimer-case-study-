from gurobipy import Model, GRB

# Initialize the model
model = Model("Energy Mix Optimization")

# Decision Variables
solar_capacity = model.addVar(vtype=GRB.CONTINUOUS, name="Solar_Capacity")
battery_capacity = model.addVar(vtype=GRB.CONTINUOUS, name="Battery_Capacity")
gas_capacity = model.addVar(vtype=GRB.CONTINUOUS, name="Gas_Capacity")
battery_units = model.addVar(vtype=GRB.INTEGER, name="Battery_Units")
gas_turbines = model.addVar(vtype=GRB.INTEGER, name="Gas_Turbines")

# Parameters (Placeholder Values, Update with Real Data)
demand = 100  # MW/hr constant demand
solar_CUF = 0.3  # Capacity Utilization Factor (30%)
battery_efficiency = 0.88  # Round-trip efficiency
gas_heat_rate = 0.0055  # MMBTU/KWh
solar_cost = 800  # $/kW
battery_cost_per_unit = 141  # $/kWh per unit
gas_cost_per_turbine = 900  # $/MW per turbine
battery_unit_capacity = 1  # MWh per unit
gas_turbine_capacity = 10  # MW per turbine

# Constraints
model.addConstr(solar_capacity * solar_CUF + battery_capacity * battery_efficiency + gas_capacity >= demand, "Demand_Fulfillment")
model.addConstr(solar_capacity * solar_CUF >= 0.7 * demand, "Renewable_Minimum")
model.addConstr(battery_capacity == battery_units * battery_unit_capacity, "Battery_Unit_Definition")
model.addConstr(gas_capacity == gas_turbines * gas_turbine_capacity, "Gas_Turbine_Definition")

# Objective: Minimize Total Cost
model.setObjective(solar_cost * solar_capacity + battery_cost_per_unit * battery_units + gas_cost_per_turbine * gas_turbines, GRB.MINIMIZE)

# Solve the model
model.optimize()

# Print Results
if model.status == GRB.OPTIMAL:
    print(f"Optimal Solar Capacity: {solar_capacity.x:.2f} MW")
    print(f"Optimal Battery Capacity: {battery_capacity.x:.2f} MWh")
    print(f"Optimal Battery Units: {battery_units.x}")
    print(f"Optimal Gas Capacity: {gas_capacity.x:.2f} MW")
    print(f"Optimal Gas Turbines: {gas_turbines.x}")
