# mypy: ignore-errors
from scipy.integrate import quad
from numpy import cosh, inf

def integrand(x) -> float:
    return 0.162257/((cosh(0.05*(x - 6)))**(1 / (0.3 * 0.05)))

result, _ = quad(integrand, -inf, inf)
print(result)