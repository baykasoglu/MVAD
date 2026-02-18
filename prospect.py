import sympy as sp
def value_function(x, alpha=0.88, beta=0.88, lambd=2.25):
    """
    Computes the Value Function from Prospect Theory.

    Parameters:
        x (float): The outcome value (positive for gains, negative for losses).
        alpha (float): Sensitivity parameter for gains (0 < alpha <= 1, default 0.88).
        beta (float): Sensitivity parameter for losses (0 < beta <= 1, default 0.88).
        lambd (float): Loss aversion coefficient (lambda > 1, default 2.25).

    Returns:
        float: The subjective value of the outcome.
    """
    if x >= 0:
        return x ** alpha  # Gains
    else:
        return -lambd * (-x) ** beta  # Losses



def normalize_distance(distance, max_distance):
    if max_distance <= 0:
        raise ValueError("Maximum distance must be greater than zero.")
    return distance / max_distance
def modified_minkowski_distanceFF(a, e, b, c, m, d, p=2):
    """
    Computes the Modified Minkowski Distance between an interval number [a, b]
    and a triangular fuzzy number (c, m, d) with parameter p.

    Parameters:
        a, b: float  -> Bounds of the interval number [a, b]
        c, m, d: float -> Bounds and mode of the triangular fuzzy number (c, m, d)
        p: float  -> Minkowski parameter (default is 2 for Euclidean distance)

    Returns:
        float -> Computed distance
    """
    CI = (a+b+e)/3
    CF = (c+m+d)/3
    lamda = 1
    # Compute individual distance components
    d1 = abs(a - c) ** p  # Lower bounds
    d2 = abs(CI - CF) ** p  # Midpoints
    d3 = abs(b - d) ** p  # Upper bounds

    # Compute final distance
    distance = ( (d1 + (lamda*d2) + d3) ) ** (1 / p)

    return distance
def modified_minkowski_distance(a, b, c, m, d, p=2):
    """
    Computes the Modified Minkowski Distance between an interval number [a, b]
    and a triangular fuzzy number (c, m, d) with parameter p.

    Parameters:
        a, b: float  -> Bounds of the interval number [a, b]
        c, m, d: float -> Bounds and mode of the triangular fuzzy number (c, m, d)
        p: float  -> Minkowski parameter (default is 2 for Euclidean distance)

    Returns:
        float -> Computed distance
    """
    CI = (a+b)/2
    CF = (c+m+d)/3
    lamda = 1
    # Compute individual distance components
    d1 = abs(a - c) ** p  # Lower bounds
    d2 = abs(CI - CF) ** p  # Midpoints
    d3 = abs(b - d) ** p  # Upper bounds

    # Compute final distance
    distance = ( (d1 + (lamda*d2) + d3) ) ** (1 / p)

    return distance

# Example Usage

referenceValue=[12,3,6,"80+-10","3-5","10000-20000","Yes","Yes",12,8,512,6,"4+-1"]
data_types_ref =["CSINGLETON","CSINGLETON","CSINGLETON","FUZZY","CINTERVAL","CINTERVAL","BOOLEAN","BOOLEAN","CSINGLETON","CSINGLETON","CSINGLETON","CSINGLETON","FUZZY"]

beta=0.88
lambd=2.25

dist1_1 = modified_minkowski_distance(5,5,6,6,6)
pros_val = (-lambd * ((83.13) ** beta))

print(f"dist1_1: {dist1_1:.4f}")
print(f"pros val: {pros_val}")

