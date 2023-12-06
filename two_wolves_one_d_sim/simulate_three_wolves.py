import multiprocessing
from two_wolves_one_d_sim.simulation_three_wolves import Simulation


def run_simulation(simulation: Simulation) -> tuple[int, int]:
    for _ in range(100000):
        simulation.tick()
    return (simulation.wolf_a.den.get_location(), simulation.wolf_b.den.get_location(), 
            simulation.wolf_c.den.get_location())

if __name__ == "__main__":
    file_name = 'three_wolves' + '.csv'
    size = 40
    mark_duration = 10
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

    runs = 30000
    processes = 8

    with open(f'two_wolves_one_d_sim/{file_name}', 'w', encoding='utf-8') as file:
        file.write('A,B,C\n')
    
    for i in range(runs // processes):
        with multiprocessing.Pool(processes=processes) as pool:        
            outputs = pool.map(
                run_simulation, [
                    Simulation(size=size, 
                               mark_duration=mark_duration, 
                               discomfort_constants = discomfort_constants,
                               murray_lewis_density_parameters=murray_lewis_density_parameters)
                    for _ in range(processes) 
                    ]
                )
    
        with open(f'two_wolves_one_d_sim/{file_name}', 'a', encoding='utf-8') as file:
            for item in outputs:
                a, b, c = item
                file.write(f'{a},{b},{c}\n')

        if i % 100 == 0:
            print(i)
