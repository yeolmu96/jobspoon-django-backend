from company_job.entity.company_job import CompanyJob
from company_job.repository.company_job_repository import CompanyJobRepository

import pandas as pd


class CompanyJobRepositoryImpl(CompanyJobRepository):
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

    def createMany(self, jobDataList):
        jobObjects = []
        for data in jobDataList:
            job = CompanyJob(**data)
            job.save()
            jobObjects.append(job)
        return jobObjects

    def findAll(self) -> pd.DataFrame:
        jobList = CompanyJob.objects.all().values()
        return pd.DataFrame(jobList)
