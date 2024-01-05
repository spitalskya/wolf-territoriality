import json
import multiprocessing
import numpy as np
from two_wolves_one_d_sim.simulation import Simulation


def run_simulation(simulation: Simulation) -> tuple[int, int]:
    for _ in range(100000):
        simulation.tick()
    return (simulation.wolf_a.den_location, simulation.wolf_b.den_location)


if __name__ == "__main__":
    with open('two_wolves_one_d_sim/config.json', 'r') as file:
        config = json.load(file)
    file_name = config["file_name"]
    size = config["size"]
    mark_decay = config["mark_decay"]
    mark_intensity_increase = config["mark_intensity_increase"]
    den_intensity_increase = config["den_intensity_increase"]
    discomfort_constants = config["discomfort_constants"]
    murray_lewis_density_parameters = config["murray_lewis_density_parameters"]
    
    runs = config["runs"]
    processes = config["processes"]

    with open(f'two_wolves_one_d_sim/simulated_data/{file_name}', 'w', encoding='utf-8') as file:
        file.write('A,B\n')
    
    for i in range(runs // processes):
        with multiprocessing.Pool(processes=processes) as pool:        
            outputs = pool.map(
                run_simulation, [
                    Simulation(size=size, 
                               mark_decay=mark_decay, 
                               mark_intensity_increase=mark_intensity_increase,
                               den_intensity_increase=den_intensity_increase,
                               discomfort_constants = discomfort_constants,
                               murray_lewis_density_parameters=murray_lewis_density_parameters)
                    for _ in range(processes) 
                    ]
                )
    
        with open(f'two_wolves_one_d_sim/simulated_data/{file_name}', 'a', encoding='utf-8') as file:
            for item in outputs:
                a, b = item
                file.write(f'{a},{b}\n')

        if i % 100 == 0:
            print(i)
