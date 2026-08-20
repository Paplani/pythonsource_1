# csv 파일의 내용을 테이블에 insert 하기 (단, 테이블이 비어 있는 경우만 삽입)

# 테이블의 내용을 읽어서 섞은 후 문제내기 (sample쓰면 간단하고 좋음)
# Question 1: 'apple' 의 뜻은?
# 1. 버스
# 2. 남편
# 3. 수줍은
# 4. 항구
# words.csv에서 뜻만 무작위로 3개 뽑아서 보기로 같이 제시하기

# 결과 : 3 / 5
# 결과를 테이블에 저장하기
# total, correct, regdate

import oracledb
from datetime import datetime

conn =  oracledb.connect(user="python_user", password = "54321", dsn="localhost/xe")
cursor = conn.cursor()

words_list = []
def load_words_from_csv():
    '''csv 파일을 읽어서 튜플 리스트로 반환'''
    # [(wife, 아내), (apple, 사과)]

    with open("./words.csv", "r", encoding="utf-8") as f:
        contents = f.readlines()
        for content in contents:
            # 영어, 한글   꼴로 그냥 보여짐. content는 리스트가 아님. contents가 리스트 + content는 그 안의 문자열
            word, meaning = content.strip().split(",")
            words_list.append((word, meaning))
        return words_list




def seed_words_if_empty():
    '''words 테이블이 비어 있으면 csv파일 내용을 읽어서 넣기'''
    # insert 하기


def run_quiz():
    '''
    1) all_words = words 테이블 읽기
    2) 무작위 문제 추출 random.sample()
    3) all_words 문제를 제외한 내용을 섞은 후 거기서 틀린 답 3개 뽑기
    4) 답변 입력받은 후 정답 맞는지 확인
    5) 최종 결과 입력
    '''


if __name__ == "__main__":
    try:
        seed_words_if_empty()
        run_quiz()
    finally:
        cursor.close()
        conn.close()