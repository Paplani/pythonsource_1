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
import random

conn =  oracledb.connect(user="python_user", password = "54321", dsn="localhost/xe")
cursor = conn.cursor()

def load_words_from_csv():
    '''csv 파일을 읽어서 튜플 리스트로 반환'''
    # [(wife, 아내), (apple, 사과)]
    words_list = []
    with open("./words.csv", "r", encoding="utf-8") as f:
        contents = f.readlines()
        for content in contents[1:]:
            # 영어, 한글   꼴로 그냥 보여짐. content는 리스트가 아님. contents가 리스트 + content는 그 안의 문자열
            word, meaning = content.strip().split(",")
            words_list.append((word, meaning))
        return words_list

        # 이건 클로드가 추천하는 방식. DicReader는 첫 줄을 필드명으로 인식해서 알아서 건너뛰어줌
        # reader = csv.DictReader(f)   # 첫 줄을 자동으로 헤더로 인식, 알아서 건너뜀
        # return [(row["word"], row["meaning"]) for row in reader]


def seed_words_if_empty():
    '''words 테이블이 비어 있으면 csv파일 내용을 읽어서 넣기'''
    # insert 하기
    sql = """select * from words"""
    cursor.execute(sql)
    words_table = cursor.fetchall()

    if not words_table:
        load_words = load_words_from_csv()
        sql = """insert into words (word, meaning) values (:1, :2)"""
        # executemany() : 튜플리스트를 통채로 넘기면 각 튜플이 하나씩 자동적으로 insert된다.
        cursor.executemany(sql, load_words)
        # for word, meaning in words_list:
        #     cursor.execute(sql, (word, meaning))
        conn.commit()

def run_quiz(num_problems = 5):
    '''
    1) all_words = words 테이블 읽기
    2) 무작위 문제 추출 random.sample()
    3) all_words 문제를 제외한 내용을 섞은 후 거기서 틀린 답 3개 뽑기
    4) 답변 입력받은 후 정답 맞는지 확인
    5) 최종 결과 입력
    '''
    sql = """select word, meaning from words"""
    cursor.execute(sql)
    all_words = cursor.fetchall()    # 리스트로 반환

    question_list = random.sample(all_words, num_problems)     #리스트 형태로 돌려줌
    filtered = [row for row in all_words if row not in question_list]    # 오답 후보군들 걸러내기

    is_correct = 0

    for i in range(num_problems):
        print(f"Question {i+1} : '{question_list[i][0]}'의 뜻은?\n")
        correct_answer = question_list[i][1]       # correct_answer는 그저 문자열

        distractor = random.sample(filtered, 3)
        distractor = [row[1] for row in distractor]     # 3개 튜플에서 각각 meaning 만 가져오기.
        options = distractor + [correct_answer]
        random.shuffle(options)             #shuffle 은 반환값 없으므로 그냥 실행해주면 알아서 섞어짐
        print(f"1:{options[0]}\n 2:{options[1]}\n 3:{options[2]}\n 4:{options[3]}\n")
        
        # 이건 내가 짠 코드 
        # input_answer = input("답안을 적어주세요")
        # if not input_answer.isdigit() or input_answer not in ("1", "2", "3", "4"):
        #     print("1,2,3,4 사이의 숫자를 다시 입력해주세요.")
        #     return

        # 1,2,3,4 숫자를 잘 입력하는지 계속 확인
        while True:
            input_answer = input("답안을 입력해주세요.")
            if input_answer in ("1", "2", "3", "4"):
                break
            print("1,2,3,4 사이의 숫자를 다시 입력해주세요.")

        selected_choice = options[int(input_answer) - 1]
        if selected_choice == correct_answer:
            print("정답입니다.")
            is_correct += 1
        else:
            print(f"오답입니다. 정답은 {correct_answer}입니다.") 

    print(f"{num_problems}개의 문제중 {is_correct}개를 맞추셨습니다.")
    save_quiz_list(num_problems, is_correct)


def save_quiz_list(total, correct):

    # regdate는 date 타입임.
    now = datetime.now()
    sql = """insert into quiz_records(total, correct, regdate) values(:1, :2, :3)"""
    cursor.execute(sql, (total, correct, now))
    conn.commit()


if __name__ == "__main__":
    try:
        seed_words_if_empty()
        run_quiz()
    finally:
        cursor.close()
        conn.close()