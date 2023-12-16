import gurobipy as gp
from gurobipy import GRB

# Create a new model
model = gp.Model("quadratic_constraint_solver")

# Define variables
x = model.addVar(lb=-GRB.INFINITY, ub=GRB.INFINITY, name="x")
y = model.addVar(lb=-GRB.INFINITY, ub=GRB.INFINITY, name="y")

# Set objective function (for constraint-solving purposes, set to a constant)
model.setObjective(0, GRB.MAXIMIZE)

# Add constraint based on the quadratic equation
constraint_expr = 0.1 * (300 + 50 * (1 - x * y)) + 300 * x * y - 50 * (1 - x * y) == 0

constraint_2 = x >= 0
constraint_3 = y >= 0
constraint_4 = x <= 1
constraint_5 = y <= 1

model.addConstr(constraint_expr, "quadratic_constraint")
model.addConstr(constraint_2, "quadratic_constraint")
model.addConstr(constraint_3, "quadratic_constraint")
model.addConstr(constraint_4, "quadratic_constraint")
model.addConstr(constraint_5, "quadratic_constraint")

# Optimize the model
model.optimize()

# Print the results
if model.status == GRB.OPTIMAL:
    print("Optimal solution found:")
    print(f"x = {x.x}")
    print(f"y = {y.x}")
else:
    print("No optimal solution found.")