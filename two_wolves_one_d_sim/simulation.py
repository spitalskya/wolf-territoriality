from two_wolves_one_d_sim.wolf import Wolf
from two_wolves_one_d_sim.area import Area

class Simulation:
    wolf_A: Wolf
    wolf_B: Wolf
    area: Area
    
    def __init__(self, size: int) -> None:
        self.area = Area(size)
        self.wolf_A = Wolf(self.area, 'A')
        self.wolf_B = Wolf(self.area, 'B')
    
    def tick(self) -> None:
        self.wolf_A.tick()
        self.wolf_B.tick()
    
    def __str__(self) -> str:
        return str(self.area)


simulation = Simulation(20)

for _ in range(15):
    simulation.tick()
    print(simulation)
    print(simulation.wolf_A.discomfort)
    print(simulation.wolf_B.discomfort)