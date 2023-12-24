from __future__ import annotations
from typing import List, Optional
import random
from math import e
from two_wolves_one_d_sim.interfaces import WolfInterface, MarkInterface
from two_wolves_one_d_sim.area import Area
# from two_wolves_one_d_sim.murray_lewis_wolf_density.wolf_density_n_zero import get_step


class Wolf(WolfInterface):
    location: int                   # location of the wolf
    tag: str                        # distinct tag of the wolf
    
    den_location: int               # location of the den
    den_intensity_increase: float   # mark intensity increase in the den
    
    marks: List[MarkInterface]      # list of wolf's marks
    mark_tag: str                   # identifier of the mark
    mark_decay: float               # how long will mark last
    mark_intensity_increase: float  # how much will intensity of a mark increase upon marking
    
    discomfort: float               # level of discomfort due to interactions
    pressure: int                   # direction of more interactions
    area: Area                      # reference to shared area
    on_way_back: bool               # if the wolf is returning to its den
    
    discomfort_constants: dict[str, float]
    
    murray_lewis_density_parameters: dict[str, float] | None
    
    def __init__(self, area: Area, tag: str, den_location: int,
                 mark_decay: float, mark_intensity_increase: float,
                 den_intensity_increase: float,
                 murray_lewis_density_parameters: dict[str, float] | None,
                 mark_tag: Optional[str] = None,
                 discomfort_constants: dict[str, float] | None = None) -> None:
        
        self.area = area
        self.tag = tag
        self.discomfort = 0
        self.pressure = 0
        
        self.mark_tag = self.tag.lower() if mark_tag is None else mark_tag
        self.mark_decay = mark_decay
        self.mark_intensity_increase = mark_intensity_increase
        
        self.den_location = den_location
        self.den_intensity_increase = den_intensity_increase
        
        self.location = self.den_location
        self.on_way_back = False
        
        self.mark(self.location)    # initial marking of the den
        
        if discomfort_constants:
            self.discomfort_constants = discomfort_constants
        else:
            self.discomfort_constants = {
                'wolf': 0.1,
                'den': 0.1,
                'mark': 0.01,
                'boundary': 0.01
            }
        
        self.murray_lewis_density_parameters = murray_lewis_density_parameters

        self.area.put_wolf(self, self.location)

    def tick(self) -> None:
        """
        rozhodne sa direction
            ak je v nore, tak uz sa nevracia
            ak sa vracia, tak sa vracia
        pozrie sa dopredu kvoli vlkom
        pozrie sa dopredu kvoli znackam
        ak sa zacne vracat, oznackuje
        pohne sa
        """
        
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
            self.mark(self.location)
            direction *= -1
        
        new_location: int = self.location + direction
        if new_location < 0 or new_location >= len(self.area):
            self.pressure += direction
            self.discomfort += self.discomfort_constants['boundary']
            self.on_way_back = True
            new_location = self.location
            
        self.area.move_wolf(self, self.location, new_location)
        self.location = new_location
        
        if self.location == self.den_location:
            self.mark(self.location)
            self.on_way_back = False
    
    
    def get_direction(self) -> int:
        """Gets direction based on murray lewis generator"""
        return self.murray_lewis_direction_generator()
    
    def murray_lewis_direction_generator(self) -> int:
        return get_step(self.location, self.den_location, self.murray_lewis_density_parameters)
    
    def direction_towards_den(self, direction: int) -> bool:
        """Returns whether given direction is towards den"""
        dir_before: int = abs(self.location - self.den_location)
        dir_after: int = abs((self.location + direction) - self.den_location)
        return dir_after < dir_before
    
    def get_direction_towards_den(self) -> int:
        """Gets direction towards den"""
        return 1 if self.direction_towards_den(1) else -1
    
    
    def look_for_wolves(self, direction: int) -> bool:
        """Looks one tile in direction dir
        if there is another wolf, returns True
        """
        tile: List[WolfInterface | MarkInterface]
        tile = self.area.get_tile(self.location + 2 * direction)
        tile = self.area.get_tile(self.location + direction) if tile == [] else tile
        
        for item in tile:
            if isinstance(item, WolfInterface):
                self.discomfort += self.discomfort_constants['wolf']
                self.pressure += direction
                return True
            
        return False
    
    def look_for_marks(self, direction: int) -> bool:
        """Looks one tile in direction
        if there is mark of another wolf, returns True
        """
        tile: List[WolfInterface | MarkInterface] 
        tile = self.area.get_tile(self.location + direction)
        
        item: WolfInterface | MarkInterface
        for item in tile:
            if isinstance(item, MarkInterface):
                # check if it is own mark
                if item.get_tag() == self.mark_tag or item.get_tag() == "":
                    return False

                # if not own mark, decide, whether to return or overmark
                if random.random() > item.get_intensity():
                    self.mark(self.location + direction)
                    return False
                self.discomfort += self.discomfort_constants['mark']
                self.pressure += direction
                return True
        return False
    
    
    def mark(self, location: int) -> None:
        tile: List[WolfInterface | MarkInterface] = self.area.get_tile(location)
        for item in tile:
            if not isinstance(item, MarkInterface):
                continue
            
            # cancel previous markings, if they are not your own
            if item.get_tag() != self.mark_tag:
                item.increase_intensity(-item.get_intensity())
                item.change_tag(self.mark_tag)
            
            if location == self.den_location:
                item.increase_intensity(self.den_intensity_increase)
            else:
                item.increase_intensity(self.mark_intensity_increase)
    
    
    def move_den(self) -> None:
        # ! REDO
        
        if random.random() > self.discomfort:
            return
        
        loc_before: int = self.den_location
        if self.pressure > 0:
            # pressure from the right
            if loc_before > 0:
                self.den_location = loc_before - 1
        elif self.pressure < 0:
            if loc_before < len(self.area) - 1:
                self.den_location = loc_before
        
        self.mark(self.den_location)
        self.discomfort = 0
        self.pressure = 0
    
    
    def __str__(self) -> str:
        return self.tag
    
    
def probability_density(x, x_u, density_parameters):
    c_u = density_parameters['c_u']
    d_u = density_parameters['d_u']
    beta = density_parameters['beta']
    a = density_parameters['A']
    
    return a / (cosh(beta*(x - x_u)))**((c_u)/(beta*d_u))

def cosh(x) -> int:
    return (e**x + e**(-x)) / 2

def get_step(current_location, den_location, density_parameters) -> int:
    prob_left = probability_density(current_location - 1, den_location, density_parameters)
    prob_right = probability_density(current_location + 1, den_location, density_parameters)

    # Normalize probabilities to ensure they sum to 1
    total_prob = prob_left + prob_right
    prob_left /= total_prob
    prob_right /= total_prob

    # Generate a random step based on the normalized probabilities
    # step = random.choice([-1, 1], p=[prob_left, prob_right])
    step = -1 if random.random() < prob_left else 1
    return step
