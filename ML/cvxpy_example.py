"""
requirements:
- pip install cvxpy numpy
"""

import cvxpy as cp
import numpy as np

sku_names = ['potato', 'corn', 'tomato', 'beaf']
sku_price = np.array([5.5, 16, 8, 60])  # 单位是千克

target_name = ["protein", "carbohydrate"]
target = np.array([100, 200])
target_dict = dict(zip(target_name, target))

budget = 30

ingredient = np.array([  # 单位是千克含量
    # protein, carbohydrate
    [18.7, 201.3],  # potato
    [32.2, 190.2],  # corn
    [8.8, 39.2],  # tomato
    [263.3, 0]  # beaf
])

w = cp.Variable(len(sku_names))

cost = sku_price @ w

obj = cp.Minimize(cost)

constraints = [ingredient.T @ w >= target, w >= 0, cost <= budget]

prob = cp.Problem(obj, constraints)

result = prob.solve()

if w.value is None:
    print("No solution!!!")
else:
    print(f"{dict(zip(sku_names, w.value))}")
    print(f"Price: {w.value @ sku_price}")
    print(f"Target: {ingredient.T @ w.value}")
