# mypy: ignore-errors
from scipy.integrate import quad
from scipy.optimize import minimize_scalar
from numpy import cosh, log, inf

def integrand(x, k) -> float:
    global c_u, d_u, beta, n, x_u
    frac = (c_u * n) / (beta)
    return (k - frac*(log(cosh(beta*(x - x_u)))))**(1/n)

def difference_function(k) -> float:
    global upper, lower
    result, _ = quad(integrand,lower, upper, args=(k,))
    return abs(result - 1)


if __name__ == '__main__':
    c_u = 1             # maximum speed of moving towards den
    d_u = 0.12
    beta = 5            # change in the rate of convective movement as the den is approached
    n = 0.5
    x_u = 0.5
    lower = 0
    upper = 30
    
    result = minimize_scalar(difference_function)
    optimal_constant = result.x

    print(f"The optimal constant is: {optimal_constant}")