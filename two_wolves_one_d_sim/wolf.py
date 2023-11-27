from __future__ import annotations
from typing import List, Optional
import random
from two_wolves_one_d_sim.interfaces import WolfInterface, MarkInterface
from two_wolves_one_d_sim.mark import Mark
from two_wolves_one_d_sim.area import Area
from two_wolves_one_d_sim.den import Den


class Wolf(WolfInterface):
    den: Den                        # location of the den
    location: int                   # location of the wolf
    tag: str                        # distinct tag of the wolf
    
    marks: List[MarkInterface]      # list of wolf's marks
    mark_tag: str                   # identifier of the mark
    mark_duration: int              # how long will mark last
    
    discomfort: int                 # level of discomfort due to interactions
    area: Area                      # reference to shared area
    on_way_back: bool               # if the wolf is returning to its den
    
    def __init__(self, area: Area, tag: str, mark_duration: int,
                    mark_tag: Optional[str] = None) -> None:
        self.area = area
        self.tag = tag
        self.discomfort = 0
        
        self.marks = []
        self.mark_tag = self.tag.lower() if mark_tag is None else mark_tag
        self.mark_duration = mark_duration
        
        self.den = Den(self.tag.lower(), random.randint(0, len(self.area) - 1))
        self.location = self.den.get_location()
        self.on_way_back = False
        
        self.area.put_den(self.den, self.den.get_location())
        self.area.put_wolf(self, self.location)
    
    def tick(self) -> None:
        """
        zostarnú marks
        rozhodne sa direction
            ak je v nore, tak uz sa nevracia
            ak sa vracia, tak sa vracia
        pozrie sa dopredu kvoli vlkom
        pozrie sa dopredu kvoli znackam
        ak sa zacne vracat, oznackuje
        pohne sa
        """
        
        self.tick_marks()
        
        direction: int
        if self.on_way_back:
            direction = self.get_direction_towards_den()
            self.move(direction, False, False)
            return

        direction = self.get_direction()
            
        wolf_ahead: bool = self.look_for_wolves(direction)
        mark_ahead: bool = self.look_for_marks(direction)
            
        self.move(direction, wolf_ahead, mark_ahead)
        
    
    def move(self, direction: int, wolf_ahead: bool, mark_ahead: bool) -> None:
        """Moves the wolf
        
        if there is wolf/mark ahead, marks the spot and starts to return
        if not and direction is towards den, decides, if the wolf return to den
        takes the step
        stops returning towards den if is at den
        """
        if wolf_ahead or mark_ahead:
            self.on_way_back = True
            self.mark()
            direction *= -1
        
        if self.direction_towards_den(direction):
            if self.decide_whether_to_return():
                self.on_way_back = True
                self.mark()
        
        new_location: int = self.location + direction
        if new_location < 0 or new_location >= len(self.area):
            new_location = self.location
        self.area.move_wolf(self, self.location, new_location)
        self.location = new_location
        
        if self.location == self.den.get_location():
            self.on_way_back = False
    
    
    def get_direction(self) -> int:
        """Gets direction based on some generator"""
        return self.linear_direction_generator()
    
    def uniform_direction_generator(self) -> int:
        """Returns uniform random direction"""
        return random.choice([-1, 1])
    
    def linear_direction_generator(self) -> int:
        # ! too much RLU
        if self.location == self.den.get_location():
            return self.uniform_direction_generator()
        
        distance_from_den: int = abs(self.location - self.den.get_location())
        if random.random() < distance_from_den/10:
            return self.get_direction_towards_den()
        return -self.get_direction_towards_den()
    
    def direction_towards_den(self, direction: int) -> bool:
        """Returns whether given direction is towards den"""
        dir_before: int = abs(self.location - self.den.get_location())
        dir_after: int = abs((self.location + direction) - self.den.get_location())
        return dir_after < dir_before
    
    def get_direction_towards_den(self) -> int:
        """Gets direction towards den"""
        return 1 if self.direction_towards_den(1) else -1
    
    def decide_whether_to_return(self) -> bool:
        """Decides, if the wolf should return to den"""
        return True
    
    
    def look_for_wolves(self, direction: int) -> bool:
        """Looks one tile in direction dir
        if there is another wolf, returns True
        """
        tile: List[WolfInterface | MarkInterface | Den]
        tile = self.area.get_tile(self.location + 2 * direction)
        tile = self.area.get_tile(self.location + direction) if tile == [] else tile
        
        if any(isinstance(item, WolfInterface) for item in tile):
            return True
        return False
    
    def look_for_marks(self, direction: int) -> bool:
        """Looks one tile in direction
        if there is mark of another wolf, returns True
        """
        tile: List[WolfInterface | MarkInterface | Den] 
        tile = self.area.get_tile(self.location + direction)
        
        item: WolfInterface | MarkInterface | Den
        for item in tile:
            if isinstance(item, MarkInterface):
                if item.get_tag() != self.mark_tag:
                    return True
        return False
    
    
    def mark(self) -> None:
        mark: MarkInterface = Mark(self.mark_tag, self.location, self.mark_duration)
        self.marks.append(mark)
        self.area.put_mark(mark, self.location)
    
    def tick_marks(self) -> None:
        """Ticks all the marks, removes expired marks"""
        mark: MarkInterface
        for mark in self.marks:
            if mark.tick():
                self.area.remove_mark(mark, mark.get_location())
                self.marks.remove(mark)
    
    def __str__(self) -> str:
        return self.tag
