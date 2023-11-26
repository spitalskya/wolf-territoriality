from two_wolves_one_d_sim.wolf import Wolf
from two_wolves_one_d_sim.area import Area

class Simulation:
    wolf_A: Wolf
    wolf_B: Wolf
    area: Area
    
    def __init__(self, size: int) -> None:
        self.area = Area(size)
        self.wolf_A = Wolf(self.area, 'A', 10)
        self.wolf_B = Wolf(self.area, 'B', 10)
    
    def tick(self) -> None:
        self.wolf_A.tick()
        self.wolf_B.tick()
    
    def __str__(self) -> str:
        return str(self.area)


simulation = Simulation(100)

for i in range(10000):
    simulation.tick()
    if i % 1000 == 0:
        print(simulation)
    continue
    print(simulation)
    print(simulation.wolf_A.discomfort)
    print(simulation.wolf_B.discomfort)
print()
for i in range(10):
    simulation.tick()
    if i % 1000 == 0 or True:
        print(simulation)
    continue
    print(simulation)
    print(simulation.wolf_A.discomfort)
    print(simulation.wolf_B.discomfort)
