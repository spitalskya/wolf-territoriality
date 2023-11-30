import random
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

with open('two_wolves_one_d_sim/loc_start.csv', 'w') as file:
    file.write('A,B\n')
with open('two_wolves_one_d_sim/loc_end.csv', 'w') as file:
    file.write('A,B\n')


for i in range(10):
    simulation = Simulation(40)
    with open('two_wolves_one_d_sim/loc_start.csv', 'a') as file:
        file.write(f'{simulation.wolf_a.location},{simulation.wolf_b.location}\n')
    for _ in range(100000):
        simulation.tick()
        
        """
        print(simulation)
        print(simulation.wolf_a.discomfort, simulation.wolf_a.pressure)
        print(simulation.wolf_b.discomfort, simulation.wolf_b.pressure)
        """
    with open('two_wolves_one_d_sim/loc_end.csv', 'a') as file:
        file.write(f'{simulation.wolf_a.location},{simulation.wolf_b.location}\n')
    print(i)