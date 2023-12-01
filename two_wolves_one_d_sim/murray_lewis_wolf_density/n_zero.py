# mypy: ignore-errors
from scipy.integrate import quad
from scipy.optimize import minimize_scalar
from numpy import cosh, inf

def integrand(x, c_u, d_u, beta, x_u) -> float:
    return 1 / (cosh(beta*(x - x_u)))**((c_u)/(d_u*beta))

def difference_function(A, c_u, d_u, beta, x_u) -> float:
    lower = -inf
    upper = inf
    
    result, _ = quad(integrand, lower, upper, args=(c_u, d_u, beta, x_u))
    return abs(A*result - 1)

def determine_A(c_u, d_u, beta, x_u) -> None:
    result = minimize_scalar(difference_function, args=(c_u, d_u, beta, x_u))
    optimal_constant = result.x

    print(f"The optimal constant is: {optimal_constant}")

if __name__ == '__main__':
    determine_A(1, 0.3, 0.05, 6)
