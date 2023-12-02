import multiprocessing
from two_wolves_one_d_sim.simulation import Simulation


def run_simulation(simulation: Simulation) -> tuple[int, int]:
    for _ in range(100000):
        simulation.tick()
    return (simulation.wolf_a.den.get_location(), simulation.wolf_b.den.get_location())

if __name__ == "__main__":
    with open('two_wolves_one_d_sim/loc_end_murray_lewis.csv', 'w', encoding='utf-8') as file:
        file.write('A,B\n')
    
    for _ in range(3750):
        with multiprocessing.Pool(processes=16) as pool:        
            outputs = pool.map(run_simulation, [Simulation(30) for _ in range(16)])
    
        with open('two_wolves_one_d_sim/loc_end_murray_lewis.csv', 'a', encoding='utf-8') as file:
            for item in outputs:
                a, b = item
                file.write(f'{a},{b}\n')
