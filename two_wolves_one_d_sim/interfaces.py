from __future__ import annotations
from abc import ABC, abstractmethod


class WolfInterface(ABC):
    pass


class MarkInterface(ABC):
    
    @abstractmethod
    def tick(self) -> None:
        pass
    
    @abstractmethod
    def increase_intensity(self, intensity: float) -> None:
        pass
    
    @abstractmethod
    def get_intensity(self) -> float:
        pass
    
    @abstractmethod
    def get_tag(self) -> str:
        pass

    @abstractmethod
    def get_location(self) -> int:
        pass
    
    @abstractmethod
    def change_tag(self, tag: str) -> None:
        pass
