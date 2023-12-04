import multiprocessing
from two_wolves_one_d_sim.simulation import Simulation


def run_simulation(simulation: Simulation) -> tuple[int, int]:
    for _ in range(100000):
        simulation.tick()
    return (simulation.wolf_a.den.get_location(), simulation.wolf_b.den.get_location())

if __name__ == "__main__":
    file_name = 'loc_end_murray_lewis_size_40_smaller_beta.csv'
    with open(f'two_wolves_one_d_sim/{file_name}', 'w', encoding='utf-8') as file:
        file.write('A,B\n')
    
    for i in range(3750):
        with multiprocessing.Pool(processes=8) as pool:        
            outputs = pool.map(run_simulation, [Simulation(40) for _ in range(8)])
    
        with open(f'two_wolves_one_d_sim/{file_name}', 'a', encoding='utf-8') as file:
            for item in outputs:
                a, b = item
                file.write(f'{a},{b}\n')

        if i % 100 == 0:
            print(i)
