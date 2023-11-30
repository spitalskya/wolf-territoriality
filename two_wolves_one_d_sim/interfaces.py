from __future__ import annotations
from abc import ABC, abstractmethod


class WolfInterface(ABC):
    pass


class MarkInterface(ABC):
    
    @abstractmethod
    def tick(self) -> bool:
        pass
    
    @abstractmethod
    def get_tag(self) -> str:
        pass

    @abstractmethod
    def get_location(self) -> int:
        pass

class DenInterface(ABC):
    
    @abstractmethod
    def get_location(self) -> int:
        pass
    
    @abstractmethod
    def set_location(self, loc: int) -> None:
        pass
