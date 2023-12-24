import numpy as np
import multiprocessing
from two_wolves_one_d_sim.simulation import Simulation


def run_simulation(simulation: Simulation) -> tuple[int, int]:
    for _ in range(100000):
        simulation.tick()
    return (simulation.wolf_a.den_location, simulation.wolf_b.den_location)

if __name__ == "__main__":
    file_name = 'test_tweaked' + '.csv'
    size = 30
    mark_decay = 0.1
    mark_intensity_increase = 1
    den_intensity_increase = 5 * mark_intensity_increase
    discomfort_constants = {
        'wolf': 0.1,
        'den': 0.1,
        'mark': 0.01,
        'boundary': 0.01
    }
    murray_lewis_density_parameters = {
        'c_u': 1,
        'd_u': 0.3,
        'beta': 0.05,
        'A': 0.1622579 
    }

    runs = 8
    processes = 8

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
