# training_sample/utils/merge_answers_data.py

import os
import pandas as pd

def merge_answer_excels(folder_path: str, output_file: str):
    combined_df = pd.DataFrame()
    total_files = 0
    total_rows = 0

    for file in os.listdir(folder_path):
        if file.endswith('.xlsx') or file.endswith('.xls'):
            file_path = os.path.join(folder_path, file)
            try:
                df = pd.read_excel(file_path)

                # ✅ 'question_id' + 'answer' 기반으로 병합하도록 수정
                if 'question_id' not in df.columns or 'answer' not in df.columns:
                    print(f"⚠️ 컬럼 누락: {file}")
                    continue

                combined_df = pd.concat([combined_df, df[["question_id", "answer"]]], ignore_index=True)
                total_files += 1
                total_rows += len(df)

            except Exception as e:
                print(f"❌ 파일 오류({file}): {e}")

    if not combined_df.empty:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        combined_df.to_excel(output_file, index=False)
        print(f"✅ 병합 완료: {total_files}개 파일, {total_rows}개 행 → {output_file}")
    else:
        print("⚠️ 병합할 데이터가 없습니다.")
