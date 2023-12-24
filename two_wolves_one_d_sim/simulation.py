import random
from two_wolves_one_d_sim.wolf import Wolf
from two_wolves_one_d_sim.area import Area

class Simulation:
    wolf_a: Wolf
    wolf_b: Wolf
    area: Area
    
    def __init__(self, size: int, 
                 mark_decay: float,
                 mark_intensity_increase: float,
                 den_intensity_increase: float,
                 discomfort_constants: dict[str, float] | None = None,
                 murray_lewis_density_parameters: dict[str, float] | None = None) -> None:
        
        self.area = Area(size=size, mark_decay=mark_decay)
        
        den_location_a: int = random.randint(0, size - 2)
        den_location_b: int = random.randint(1, size - 1)
        while den_location_a >= den_location_b:
            den_location_a = random.randint(0, size - 2)
            den_location_b = random.randint(1, size - 1)
        
        self.wolf_a = Wolf(area=self.area, tag='A', den_location=den_location_a, 
                           mark_decay=mark_decay,
                           mark_intensity_increase=mark_intensity_increase,
                           den_intensity_increase=den_intensity_increase,
                           discomfort_constants=discomfort_constants,
                           murray_lewis_density_parameters=murray_lewis_density_parameters)
        
        self.wolf_b = Wolf(area=self.area, tag='B', den_location=den_location_b, 
                           mark_decay=mark_decay,
                           mark_intensity_increase=mark_intensity_increase,
                           den_intensity_increase=den_intensity_increase,
                           discomfort_constants=discomfort_constants,
                           murray_lewis_density_parameters=murray_lewis_density_parameters)
    
    def tick(self) -> None:
        self.area.tick()
        
        ticks = [self.wolf_a.tick, self.wolf_b.tick]
        random.shuffle(ticks)
        for tick_wolf in ticks:
            tick_wolf()
            
    def __str__(self) -> str:
        return str(self.area)
