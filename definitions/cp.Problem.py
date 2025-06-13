
import cvxpy as cp
from typing import List

def Problem(objective: cp.Minimize | cp.Maximize, constraints: List[cp.Constraint]) -> cp.Problem:
    """
    Defines the portfolio optimization problem with an objective and constraints.

    Args:
        objective: The objective function to minimize or maximize.
        constraints: A list of constraints on the optimization variables.

    Returns:
        A CVXPY Problem object.
    """
    try:
        problem = cp.Problem(objective, constraints)
        return problem
    except Exception as e:
        raise ValueError(f"Error creating CVXPY Problem: {e}")
