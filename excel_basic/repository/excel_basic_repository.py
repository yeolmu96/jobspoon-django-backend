from abc import ABC, abstractmethod


class ExcelBasicRepository(ABC):

    @abstractmethod
    def createMany(self, excelDictionary):
        pass

    @abstractmethod
    def list(self):
        pass
