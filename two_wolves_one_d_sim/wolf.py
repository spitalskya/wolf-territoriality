from __future__ import annotations
from typing import List
import random
from two_wolves_one_d_sim.mark import Mark
from two_wolves_one_d_sim.area import Area
from two_wolves_one_d_sim.den import Den


class Wolf:
        den: Den            # location of the den
        location: int       # location of the wolf
        tag: str            # distinct tag of the wolf
        marks: List[Mark]   # list of wolf's marks
        discomfort: int     # level of discomfort due to interactions
        area: Area          # reference to shared area
        on_way_back: bool   # if the wolf is returning to its den
        
        def __init__(self, area: Area, tag: str) -> None:
            self.area = area
            self.tag = tag
            self.discomfort = 0
            self.marks = []
            self.den = Den(self.tag.lower(), random.randint(0, len(self.area) - 1))
            self.location = self.den.get_location()
            self.on_way_back = False
            
            self.area.put_den(self.den, self.den.get_location())
            self.area.put_wolf(self, self.location)
        
        def tick(self) -> None:
            self.tick_marks()
            
            # if was on way back and is at den:
            if self.location == self.den.get_location():
                self.on_way_back = False
            
            # if is on way back, take step to den
            if self.on_way_back:
                self.move_on_way_back()
                return
            
            direction = random.choice([-1, 1])
            if self.look_ahead(direction):
                self.move(direction)
            else:
                self.move(-direction)
        
        def move(self, direction: int) -> None:
            dist_before = self.distance_from_den(self.location)
            
            # check if step is in boundaries, if not, walk back
            if 0 <= self.location + direction < len(self.area):
                if self.distance_from_den(self.location + direction) < dist_before:
                    # if takes step towards den
                    self.turn_back()
                
                self.area.move_wolf(self, self.location, self.location + direction)
                self.location += direction
            else:
                self.turn_back()
                self.area.move_wolf(self, self.location, self.location - direction)
                self.location -= direction 
        
        def move_on_way_back(self) -> None:                
            direction = -1 if self.location - self.den.get_location() > 0 else 1
            self.area.move_wolf(self, self.location, self.location + direction)
            self.location += direction                    
        
        def distance_from_den(self, location: int) -> int:
            return abs(location - self.den.get_location())
        
        def turn_back(self) -> None:
            # make a mark and start walking towards den
            self.on_way_back = True
            
            mark: Mark = Mark(self.tag.lower(), self.location, 9)
            self.area.put_mark(mark, self.location)
            self.marks.append(mark)
        
        def look_ahead(self, direction: int) -> bool:
            ahead: List[Wolf | Mark | Den] = self.area.get_tile(self.location + direction)
            obj: Wolf | Mark | Den
            for obj in ahead:
                if isinstance(obj, Wolf):
                    self.discomfort += 0.1
                    self.turn_back()
                    return False
                if isinstance(obj, Mark):
                    if obj.tag != self.tag.lower():
                        self.discomfort += 0.01
                        self.turn_back()
                        return False
            return True
            
        def tick_marks(self) -> None:
            mark: Mark
            for mark in self.marks:
                if mark.tick():
                    self.area.remove_mark(mark, mark.location)
                    self.marks.remove(mark)
        
        def __str__(self) -> str:
            return self.tag
