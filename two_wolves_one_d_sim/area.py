from __future__ import annotations
from typing import List
from two_wolves_one_d_sim.mark import Mark
from two_wolves_one_d_sim.den import Den

class Area:
    area: List[List[Wolf | Mark | Den]]
    
    def __init__(self, size: int) -> None:
        self.area = [[] for _ in range(size)]
        
    def put_wolf(self, wolf: Wolf, location: int) -> None:
        self.area[location].append(wolf)
    
    def put_den(self, den: Den, location: int) -> None:
        self.area[location].append(den)
    
    def put_mark(self, mark: Mark, location: int) -> None:
        self.area[location].append(mark)
    
    def remove_mark(self, mark: Mark, location: int) -> None:
        self.area[location].remove(mark)
    
    def move_wolf(self, wolf: Wolf, loc_before: int, loc_after: int) -> None:
        self.area[loc_before].remove(wolf)
        self.area[loc_after].append(wolf)
    
    def get_tile(self, loc: int) -> List[Wolf | Mark | Den]:
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
