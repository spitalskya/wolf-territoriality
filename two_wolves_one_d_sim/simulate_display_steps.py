import numpy as np
import json
from two_wolves_one_d_sim.simulation import Simulation


def run_simulation(simulation: Simulation) -> tuple[int, int]:
    for _ in range(20):
        simulation.tick()
        print(simulation)
    return (simulation.wolf_a.den_location, simulation.wolf_b.den_location)


if __name__ == "__main__":
    with open('two_wolves_one_d_sim/config.json', 'r') as file:
        config = json.load(file)
    size = config["size"]
    mark_decay = config["mark_decay"]
    mark_intensity_increase = config["mark_intensity_increase"]
    den_intensity_increase = config["den_intensity_increase"]
    discomfort_constants = config["discomfort_constants"]
    murray_lewis_density_parameters = config["murray_lewis_density_parameters"]

    run_simulation(
        Simulation(size=size, 
                   mark_decay=mark_decay, 
                   mark_intensity_increase=mark_intensity_increase,
                   den_intensity_increase=den_intensity_increase,
                   discomfort_constants = discomfort_constants,
                   murray_lewis_density_parameters=murray_lewis_density_parameters)
        )
