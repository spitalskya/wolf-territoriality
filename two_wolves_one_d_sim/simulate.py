import multiprocessing
from two_wolves_one_d_sim.simulation import Simulation


def run_simulation(simulation: Simulation) -> tuple[int, int]:
    output: list[tuple[int, int]] = []
    # print(simulation.wolf_a.location, simulation.wolf_b.location)
    for _ in range(100000):
        simulation.tick()
        output.append((simulation.wolf_a.location, simulation.wolf_b.location))
    print('Done')
    #return output
    return (simulation.wolf_a.den.get_location(), simulation.wolf_b.den.get_location())

if __name__ == "__main__":
    with open('two_wolves_one_d_sim/loc_end_murray_lewis.csv', 'w', encoding='utf-8') as file:
        file.write('A,B\n')
    
    for i in range(25):
        with multiprocessing.Pool(processes=4) as pool:        
            outputs = pool.map(run_simulation, [Simulation(30) for _ in range(4)])
    
        with open('two_wolves_one_d_sim/loc_end_murray_lewis.csv', 'a', encoding='utf-8') as file:
            for item in outputs:
                a, b = item
                file.write(f'{a},{b}\n')
