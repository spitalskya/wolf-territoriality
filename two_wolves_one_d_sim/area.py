from __future__ import annotations
from typing import List
from two_wolves_one_d_sim.interfaces import WolfInterface, MarkInterface
from two_wolves_one_d_sim.den import Den

class Area:
    area: List[List[WolfInterface | MarkInterface | Den]]
    
    def __init__(self, size: int) -> None:
        self.area = [[] for _ in range(size)]
        
    def put_wolf(self, wolf: WolfInterface, location: int) -> None:
        self.area[location].append(wolf)
    
    def put_den(self, den: Den, location: int) -> None:
        self.area[location].append(den)
    
    def put_mark(self, mark: MarkInterface, location: int) -> None:
        self.area[location].append(mark)
    
    def remove_mark(self, mark: MarkInterface, location: int) -> None:
        self.area[location].remove(mark)
    
    def move_wolf(self, wolf: WolfInterface, loc_before: int, loc_after: int) -> None:
        self.area[loc_before].remove(wolf)
        self.area[loc_after].append(wolf)
    
    def get_tile(self, loc: int) -> List[WolfInterface | MarkInterface | Den]:
        if loc < 0 or loc >= len(self.area):
            return []
        return self.area[loc]
    
    def __len__(self) -> int:
        return len(self.area)
    
    def __str__(self) -> str:
        state: str = ''
        for tile in self.area:
            if tile == []:
                state += '_'
            else:
                for obj in tile:
                    state += str(obj)
            state += '|'
        return state[:-1]
