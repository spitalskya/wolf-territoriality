from __future__ import annotations
from typing import List
from two_wolves_one_d_sim.interfaces import WolfInterface, MarkInterface
from two_wolves_one_d_sim.mark import Mark

class Area:
    area: List[List[WolfInterface | MarkInterface]]
    marks: List[MarkInterface]
    
    def __init__(self, size: int, mark_decay: float) -> None:
        # create area of given size and all mark spots
        
        self.marks = [Mark(tag="", location=i, decay=mark_decay)
                      for i in range(size)]
        
        self.area = [
            [self.marks[i]] 
            for i in range(size)
            ]
    
    def tick(self) -> None:
        for mark in self.marks:
            mark.tick()
    
    def put_wolf(self, wolf: WolfInterface, location: int) -> None:
        self.area[location].append(wolf)
     
    def put_mark(self, mark: MarkInterface, location: int) -> None:
        self.area[location].append(mark)
    
    def remove_mark(self, mark: MarkInterface, location: int) -> None:
        self.area[location].remove(mark)
    
    def move_wolf(self, wolf: WolfInterface, loc_before: int, loc_after: int) -> None:
        self.area[loc_before].remove(wolf)
        self.area[loc_after].append(wolf)
    
    def get_tile(self, loc: int) -> List[WolfInterface | MarkInterface]:
        if loc < 0 or loc >= len(self.area):
            return []
        return self.area[loc]
    
    def __len__(self) -> int:
        return len(self.area)
    
    def __str__(self) -> str:
        state: str = ''
        for tile in self.area:
            tmp = ''
            for obj in tile:
                tmp += str(obj)
            state += f'{tmp:<{12}}'
            state += '|'
        return state[:-1]
