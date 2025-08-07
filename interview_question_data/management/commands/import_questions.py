import pandas as pd
import os
from django.core.management.base import BaseCommand
from interview_question_data.entity.interview_data import InterviewData


class Command(BaseCommand):
    help = '엑셀 파일에서 av_db로 면접 질문 데이터 가져오기'

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(os.path.abspath(__file__))   # 현재 파일 기준 디렉터리
        file_path = os.path.join(base_dir, '../../../merged_interview_questions.xlsx')
        file_path = os.path.abspath(file_path)   # 파일 정규화

        df = pd.read_excel(file_path)

        insert_count = 0
        skip_count = 0

        for _, row in df.iterrows():
            try:
                # 엑셀 컬럼: '직무', '회사 이름', '질문'
                category = str(row.get('직무', '')).strip()
                company_name = str(row.get('회사 이름', '')).strip()
                question = str(row.get('질문', '')).strip()

                if not question:
                    skip_count += 1
                    continue

                InterviewData.objects.create(
                    category=category,
                    companyName=company_name,
                    question=question,
                    source='엑셀 업로드'
                )
                insert_count += 1
            except Exception as e:
                print(f"🔥 row error: {e}")
                skip_count += 1

        self.stdout.write(self.style.SUCCESS(f'엑셀 데이터 저장 완료! (성공: {insert_count}, 건너뜸: {skip_count})'))