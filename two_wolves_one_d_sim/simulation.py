import random
import multiprocessing
from two_wolves_one_d_sim.wolf import Wolf
from two_wolves_one_d_sim.area import Area

class Simulation:
    wolf_a: Wolf
    wolf_b: Wolf
    area: Area
    
    def __init__(self, size: int) -> None:
        self.area = Area(size)
        den_location_a: int = random.randint(0, size - 2)
        den_location_b: int = random.randint(1, size - 1)
        while den_location_a >= den_location_b:
            den_location_b = random.randint(1, size - 1)
        
        self.wolf_a = Wolf(area=self.area, tag='A', den_location=den_location_a, mark_duration=10)
        self.wolf_b = Wolf(area=self.area, tag='B', den_location=den_location_b, mark_duration=10)
    
    def tick(self) -> None:
        ticks = [self.wolf_a.tick, self.wolf_b.tick]
        random.shuffle(ticks)
        for tick_wolf in ticks:
            tick_wolf()
            
    def __str__(self) -> str:
        return str(self.area)


def run_simulation(simulation: Simulation) -> tuple[int, int]:
    for _ in range(100000):
        simulation.tick()
    return (simulation.wolf_a.den.get_location(), simulation.wolf_b.den.get_location())

if __name__ == "__main__":
    with open('two_wolves_one_d_sim/loc_end.csv', 'w', encoding='utf-8') as file:
        file.write('A,B\n')
    for i in range(1):
        with multiprocessing.Pool() as pool:        
            outputs = pool.map(run_simulation, [Simulation(30) for _ in range(8)])
        with open('two_wolves_one_d_sim/loc_end.csv', 'a', encoding='utf-8') as file:
            for item in outputs:
                a, b = item
                file.write(f'{a},{b}\n')
