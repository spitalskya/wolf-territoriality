from numpy import cosh, random
from two_wolves_one_d_sim.murray_lewis_wolf_density.n_zero import determine_A


def probability_density(x, x_u):
    global c_u, d_u, beta, A
    return A / (cosh(beta*(x - x_u)))**((c_u)/(beta*d_u))

def get_step(current_location, den_location) -> int:
    prob_left = probability_density(current_location - 1, den_location)
    prob_right = probability_density(current_location + 1, den_location)

    # Normalize probabilities to ensure they sum to 1
    total_prob = prob_left + prob_right
    prob_left /= total_prob
    prob_right /= total_prob

    # Generate a random step based on the normalized probabilities
    step = random.choice([-1, 1], p=[prob_left, prob_right])
    return step

c_u = 1
d_u = 0.3
beta = 0.01
A = 0.1622579 

if __name__ == '__main__':
    A = determine_A(c_u, d_u, beta, x_u=0)
    print(A)
