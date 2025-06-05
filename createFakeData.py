from abc import ABC, abstractmethod

class CreateFakeData(ABC):
    @abstractmethod
    def openConnectonDB(self) : pass
    
    @abstractmethod
    def closeConnectionDB(self) : pass
    
    @abstractmethod
    def openCursorDB(self) : pass
    
    @abstractmethod
    def closeCursorDB(self) : pass