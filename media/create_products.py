import os

from company_report.entity.company_data_total import CompanyDataTotal
from company_report.entity.company_report import CompanyReport

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "av_db.settings")

import random

import django

django.setup()


PRICE = range(0, 501, 50)


def create_product(path):
    productName = path.split(".png")[0]
    productPrice = random.choice(PRICE)
    productImage = path
    content = CompanyDataTotal.objects.filter(company_name=productName).values('business_summary')
    print(productName,content)

    CompanyReport.objects.create(
        companyReportName=productName,
        companyReportPrice=productPrice,
        companyReportTitleImage=productImage,
        companyReportCategory='IT',
        content=content
    )


def run():
    print("Creating products...")
    paths = os.listdir("media/image")
    for path in paths:
        create_product(path)
    print("Products created!")
