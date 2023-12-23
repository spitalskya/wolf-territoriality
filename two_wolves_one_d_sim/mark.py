import numpy as np
from two_wolves_one_d_sim.interfaces import MarkInterface

class Mark(MarkInterface):
    decay: float
    tag: str
    location: int
    
    def __init__(self, tag: str, location: int, decay: float) -> None:
        self.decay = decay
        self.location = location
        self.tag = tag
        
        self.intensity = 1
    
    def tick(self) -> bool:
        self.intensity *= np.e**(-self.decay)
        
        if (self.intensity < 10**(-4)):     # ? chcem to takto?
            self.intensity = 0
            
        if self.intensity == 0:
            return True
        return False
    
    def get_tag(self) -> str:
        return self.tag
    
    def get_location(self) -> int:
        return self.location
    
    def __str__(self) -> str:
        return '.'
