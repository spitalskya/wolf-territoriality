import numpy as np
import matplotlib.pyplot as plt
from two_wolves_one_d_sim.murray_lewis_wolf_density.wolf_density_n_zero import get_step

# Define probability density function (example: Gaussian distribution)
def probability_density(x, mu, sigma):
    return 0.1622579 / (np.cosh(0.05*(x - 20)))**((1)/(0.3*0.05))

# Function for simulating wolf movement
def simulate_wolf_movement(num_steps, initial_position, mu, sigma):
    current_position = initial_position
    positions = [current_position]

    for _ in range(num_steps):
        """# Calculate unnormalized probabilities
        prob_left = probability_density(current_position - 1, mu, sigma)
        prob_right = probability_density(current_position + 1, mu, sigma)

        # Normalize probabilities to ensure they sum to 1
        total_prob = prob_left + prob_right
        prob_left /= total_prob
        prob_right /= total_prob

        # Generate a random step based on the normalized probabilities
        step = np.random.choice([-1, 1], p=[prob_left, prob_right])"""

        step = get_step(current_position, 10)
        pri
        # Update the current position
        current_position += step

        # Append the new position to the list
        positions.append(current_position)

    return positions

# Parameters for simulation
num_steps = 100000
initial_position = 0
mu = 0  # Mean of the Gaussian distribution
sigma = 1  # Standard deviation of the Gaussian distribution

# Simulate wolf movement
wolf_positions = simulate_wolf_movement(num_steps, initial_position, mu, sigma)

# Plot the results
plt.hist(wolf_positions, bins=30, range=(-0.5, 29.5), density=True)
plt.plot(np.arange(0, 31, 0.1), [probability_density(x, mu, sigma) for x in np.arange(0, 31, 0.1)], color='orange')
plt.title('Wolf Movement Simulation with Probability Density')
plt.xlabel('Time Steps')
plt.ylabel('Wolf Position')
plt.show()
