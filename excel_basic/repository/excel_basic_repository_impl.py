from excel_basic.entity.excel_basic_employee import ExcelBasicEmployee
from excel_basic.repository.excel_basic_repository import ExcelBasicRepository


class ExcelBasicRepositoryImpl(ExcelBasicRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def createMany(self, excelDictionary):
        employeeDictionary = [
            ExcelBasicEmployee(
                name=excelElement['Name'],
                age=excelElement['Age'],
                city=excelElement['City'],
                score=excelElement['Score'],
                department=excelElement['Department']
            )
            for excelElement in excelDictionary
        ]

        ExcelBasicEmployee.objects.bulk_create(employeeDictionary)

    def list(self):
        return ExcelBasicEmployee.objects.all()
    