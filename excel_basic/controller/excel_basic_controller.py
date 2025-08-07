from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, status

from excel_basic.service.excel_basic_service_impl import ExcelBasicServiceImpl


class ExcelBasicController(viewsets.ViewSet):
    excelBasicService = ExcelBasicServiceImpl.getInstance()

    def requestCreateExcelInfo(self, request):
        isSuccess = self.excelBasicService.createExcelToDatabase()

        return JsonResponse({"isSuccess": isSuccess}, status=status.HTTP_200_OK)

    def requestDatabaseToExcel(self, request):
        isSuccess = self.excelBasicService.createDatabaseToExcel()

        return JsonResponse({"isSuccess": isSuccess}, status=status.HTTP_200_OK)
