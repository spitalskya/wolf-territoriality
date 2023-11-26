class Mark:
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
    
    def __str__(self) -> str:
        return str(self.duration)
