from two_wolves_one_d_sim.wolf import Wolf
from two_wolves_one_d_sim.area import Area

class Simulation:
    wolf_a: Wolf
    wolf_b: Wolf
    area: Area
    
    def __init__(self, size: int) -> None:
        self.area = Area(size)
        self.wolf_a = Wolf(self.area, 'A', 10)
        self.wolf_b = Wolf(self.area, 'B', 10)
    
    def tick(self) -> None:
        self.wolf_a.tick()
        self.wolf_b.tick()
    
    def __str__(self) -> str:
        return str(self.area)


simulation = Simulation(50)

for _ in range(20):
    simulation.tick()
    print(simulation)
    
