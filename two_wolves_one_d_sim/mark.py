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
        
        self.intensity = 0
    
    def increase_intensity(self, intensity: float) -> None:
        self.intensity += intensity
    
    def get_intensity(self) -> float:
        return self.intensity
    
    def tick(self) -> None:
        self.intensity *= np.e**(-self.decay)
        
        if (self.intensity < 10**(-4)):     # ? chcem to takto?
            self.intensity = 0
            self.tag = ""    
        
    def get_tag(self) -> str:
        return self.tag
    
    def get_location(self) -> int:
        return self.location
    
    def change_tag(self, tag: str) -> None:
        self.tag = tag
    
    def __str__(self) -> str:
        return '.'
