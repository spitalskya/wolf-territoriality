import random
from two_wolves_one_d_sim.wolf import Wolf
from two_wolves_one_d_sim.area import Area

class Simulation:
    wolf_a: Wolf
    wolf_b: Wolf
    wolf_c: Wolf
    area: Area
    
    def __init__(self, size: int, 
                 mark_duration: int = 10,
                 discomfort_constants: dict[str, float] | None = None,
                 murray_lewis_density_parameters: dict[str, float] | None = None) -> None:
        
        self.area = Area(size)
        den_location_a: int = random.randint(0, size - 3)
        den_location_b: int = random.randint(1, size - 2)
        den_location_c: int = random.randint(2, size - 1)
        while not (den_location_a < den_location_b < den_location_c):
            den_location_a = random.randint(0, size - 3)
            den_location_b = random.randint(1, size - 2)
            den_location_c = random.randint(2, size - 1)
        
        self.wolf_a = Wolf(area=self.area, tag='A', den_location=den_location_a, 
                           mark_duration=mark_duration,
                           discomfort_constants=discomfort_constants,
                           murray_lewis_density_parameters=murray_lewis_density_parameters)
        
        self.wolf_b = Wolf(area=self.area, tag='B', den_location=den_location_b, 
                           mark_duration=mark_duration,
                           discomfort_constants=discomfort_constants,
                           murray_lewis_density_parameters=murray_lewis_density_parameters)
        
        self.wolf_c = Wolf(area=self.area, tag='C', den_location=den_location_c, 
                           mark_duration=mark_duration,
                           discomfort_constants=discomfort_constants,
                           murray_lewis_density_parameters=murray_lewis_density_parameters)
    
    def tick(self) -> None:
        ticks = [self.wolf_a.tick, self.wolf_b.tick, self.wolf_c.tick]
        random.shuffle(ticks)
        for tick_wolf in ticks:
            tick_wolf()
            
    def __str__(self) -> str:
        return str(self.area)
