from __future__ import annotations
from typing import List, Optional
import random
from math import e
from two_wolves_one_d_sim.interfaces import WolfInterface, MarkInterface, DenInterface
from two_wolves_one_d_sim.mark import Mark
from two_wolves_one_d_sim.area import Area
from two_wolves_one_d_sim.den import Den
# from two_wolves_one_d_sim.murray_lewis_wolf_density.wolf_density_n_zero import get_step


class Wolf(WolfInterface):
    den: DenInterface               # location of the den
    location: int                   # location of the wolf
    tag: str                        # distinct tag of the wolf
    
    marks: List[MarkInterface]      # list of wolf's marks
    mark_tag: str                   # identifier of the mark
    mark_duration: int              # how long will mark last
    
    discomfort: float               # level of discomfort due to interactions
    pressure: int                   # direction of more interactions
    area: Area                      # reference to shared area
    on_way_back: bool               # if the wolf is returning to its den
    
    def __init__(self, area: Area, tag: str, den_location: int,
                 mark_duration: int, mark_tag: Optional[str] = None) -> None:
        self.area = area
        self.tag = tag
        self.discomfort = 0
        self.pressure = 0
        
        self.marks = []
        self.mark_tag = self.tag.lower() if mark_tag is None else mark_tag
        self.mark_duration = mark_duration
        
        self.den = Den(self.tag.lower(), den_location)
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
        
        self.move_den()
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
        
        if not self.on_way_back and self.direction_towards_den(direction):
            if self.decide_whether_to_return():
                self.on_way_back = True
                self.mark()
        
        new_location: int = self.location + direction
        if new_location < 0 or new_location >= len(self.area):
            self.pressure += direction
            self.discomfort += 0.01
            self.on_way_back = True
            new_location = self.location
            
        self.area.move_wolf(self, self.location, new_location)
        self.location = new_location
        
        if self.location == self.den.get_location():
            self.on_way_back = False
    
    
    def get_direction(self) -> int:
        """Gets direction based on some generator"""
        return self.murray_lewis_direction_generator()
    
    def uniform_direction_generator(self) -> int:
        """Returns uniform random direction"""
        return random.choice([-1, 1])
    
    def linear_direction_generator(self) -> int:
        if self.location == self.den.get_location():
            return self.uniform_direction_generator()
        
        distance_from_den: int = abs(self.location - self.den.get_location())
        if random.random() < distance_from_den/10:
            return self.get_direction_towards_den()
        return -self.get_direction_towards_den()
    
    def murray_lewis_direction_generator(self) -> int:
        return get_step(self.location, self.den.get_location())
    
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
        return False
    
    
    def look_for_wolves(self, direction: int) -> bool:
        """Looks one tile in direction dir
        if there is another wolf, returns True
        """
        tile: List[WolfInterface | MarkInterface | DenInterface]
        tile = self.area.get_tile(self.location + 2 * direction)
        tile = self.area.get_tile(self.location + direction) if tile == [] else tile
        
        for item in tile:
            if isinstance(item, WolfInterface):
                self.discomfort += 0.1
                self.pressure += direction
                return True
            if isinstance(item, DenInterface):
                if item != self.den:
                    self.discomfort += 0.1
                    self.pressure += direction
                    return True
        return False
    
    def look_for_marks(self, direction: int) -> bool:
        """Looks one tile in direction
        if there is mark of another wolf, returns True
        """
        tile: List[WolfInterface | MarkInterface | DenInterface] 
        tile = self.area.get_tile(self.location + direction)
        
        item: WolfInterface | MarkInterface | DenInterface
        for item in tile:
            if isinstance(item, MarkInterface):
                if item.get_tag() != self.mark_tag:
                    self.discomfort += 0.01
                    self.pressure += direction
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
    
    
    def move_den(self) -> None:
        if random.random() > self.discomfort:
            return
        
        loc_before: int = self.den.get_location()
        if self.pressure > 0:
            # pressure from the right
            if loc_before > 0:
                self.area.move_den(self.den, loc_before, loc_before - 1)
                self.den.set_location(loc_before - 1)
        elif self.pressure < 0:
            if loc_before < len(self.area) - 1:
                self.area.move_den(self.den, loc_before, loc_before + 1)
                self.den.set_location(loc_before + 1)
        self.discomfort = 0
        self.pressure = 0
    
    
    def __str__(self) -> str:
        return self.tag

def probability_density(x, x_u):
    global c_u, d_u, beta, A
    return A / (cosh(beta*(x - x_u)))**((c_u)/(beta*d_u))

def cosh(x) -> int:
    return (e**x + e**(-x)) / 2

def get_step(current_location, den_location) -> int:
    prob_left = probability_density(current_location - 1, den_location)
    prob_right = probability_density(current_location + 1, den_location)

    # Normalize probabilities to ensure they sum to 1
    total_prob = prob_left + prob_right
    prob_left /= total_prob
    prob_right /= total_prob

    # Generate a random step based on the normalized probabilities
    # step = random.choice([-1, 1], p=[prob_left, prob_right])
    step = -1 if random.random() < prob_left else 1
    return step

c_u = 1
d_u = 0.3
beta = 0.05
A = 0.1622579 