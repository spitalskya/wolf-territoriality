from two_wolves_one_d_sim.interfaces import MarkInterface

class Mark(MarkInterface):
    duration: int
    tag: str
    location: int
    
    def __init__(self, tag: str, location: int, duration: int) -> None:
        self.duration = duration
        self.location = location
        self.tag = tag
    
    def tick(self) -> bool:
        self.duration -= 1
        if self.duration == 0:
            return True
        return False
    
    def get_tag(self) -> str:
        return self.tag
    
    def get_location(self) -> int:
        return self.location
    
    def __str__(self) -> str:
        return ''
