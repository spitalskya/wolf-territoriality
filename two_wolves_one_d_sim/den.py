class Den:
    tag: str
    location: int
    
    def __init__(self, tag: str, location: int) -> None:
        self.tag = tag
        self.location = location
    
    def get_location(self) -> int:
        return self.location
    
    def __str__(self) -> str:
        return self.tag
