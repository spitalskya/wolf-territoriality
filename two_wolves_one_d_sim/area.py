from __future__ import annotations
from typing import List
from two_wolves_one_d_sim.interfaces import WolfInterface, MarkInterface, DenInterface


class Area:
    area: List[List[WolfInterface | MarkInterface | DenInterface]]
    
    def __init__(self, size: int) -> None:
        self.area = [[] for _ in range(size)]
        
    def put_wolf(self, wolf: WolfInterface, location: int) -> None:
        self.area[location].append(wolf)
    
    def put_den(self, den: DenInterface, location: int) -> None:
        self.area[location].append(den)
    
    def put_mark(self, mark: MarkInterface, location: int) -> None:
        self.area[location].append(mark)
    
    def remove_mark(self, mark: MarkInterface, location: int) -> None:
        self.area[location].remove(mark)
    
    def move_wolf(self, wolf: WolfInterface, loc_before: int, loc_after: int) -> None:
        self.area[loc_before].remove(wolf)
        self.area[loc_after].append(wolf)
    
    def move_den(self, den: DenInterface, loc_before: int, loc_after: int) -> None:
        self.area[loc_before].remove(den)
        self.area[loc_after].append(den)
    
    def get_tile(self, loc: int) -> List[WolfInterface | MarkInterface | DenInterface]:
        if loc < 0 or loc >= len(self.area):
            return []
        return self.area[loc]
    
    def __len__(self) -> int:
        return len(self.area)
    
    def __str__(self) -> str:
        state: str = ''
        for tile in self.area:
            if tile == [] or all(isinstance(item, MarkInterface) for item in tile):
                state += '_'
            else:
                for obj in tile:
                    if isinstance(obj, MarkInterface): continue
                    state += str(obj)
                    break
            state += '|'
        return state[:-1]
