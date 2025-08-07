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

        for _, row in df.iterrows():
            try:
                print("row:", row)  # 👈 추가
                raw_id = row.get('id', '')
                id_value = int(raw_id) if pd.notnull(raw_id) and str(raw_id).strip() != '' else None

                if id_value is None:
                    print("❌ ID 없음 - 건너뜀")
                    continue

                category = str(row.get('직무', '') or '')
                companyName = str(row.get('회사 이름', '') or '')
                question = str(row.get('질문', '') or '')
                #source = row.get('source', '')

                if not question.strip():  # 질문 없으면 무시
                    continue

                print(f"✅ inserting: id={id_value}, category={category}, company={companyName}")

                InterviewData.objects.create(
                    category=category,
                    companyName=companyName,
                    question=question,
                    source='엑셀 업로드'  # 혹은 빈 문자열 ''
                )
            except Exception as e:
                print(f"🔥 row error: {e}")

        self.stdout.write(self.style.SUCCESS('엑셀 데이터가 av_db에 성공적으로 저장되었습니다.'))
