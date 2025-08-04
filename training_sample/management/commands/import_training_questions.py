from django.core.management.base import BaseCommand
import pandas as pd
from training_sample.service.training_sample_service_impl import TrainingSampleServiceImpl

class Command(BaseCommand):
    help = 'GPT 학습용 질문을 엑셀에서 DB에 저장합니다.'

    def handle(self, *args, **kwargs):
        file_path = 'training_sample/data/training_questions.xlsx'
        df = pd.read_excel(file_path)

        service = TrainingSampleServiceImpl.getInstance()
        service.import_questions(df)

        self.stdout.write(self.style.SUCCESS("✅ 질문 저장 완료"))
