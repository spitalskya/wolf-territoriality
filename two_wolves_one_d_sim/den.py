from two_wolves_one_d_sim.interfaces import DenInterface

class Den(DenInterface):
    tag: str
    location: int
    
    def __init__(self, tag: str, location: int) -> None:
        self.tag = tag
        self.location = location
    
    def get_location(self) -> int:
        return self.location
    
    def set_location(self, loc: int) -> None:
        self.location = loc
    
    def __str__(self) -> str:
        return self.tag
