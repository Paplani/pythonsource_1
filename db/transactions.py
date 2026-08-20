import oracledb
from datetime import datetime

conn = oracledb.connect(user="python_user", password = "54321", dsn = "localhost/xe")
cursor = conn.cursor()

def add_transaction():
    input_add = input("추가하시고자 하는 내역을 입력해주세요. 수입/지출 여부, 금액, 어떤 내용인지 적어주세요. 각 항목은 반드시 쉼표로 구분해주세요.").split(",")
    input_add = [x.strip() for x in input_add]    # 쉽표로 나눈 리스트들의 앞뒤 공백 제거해서 다시 리스트로 넣어주기

    date = input('날짜를 입력하세요. (YYYY-MM-DD, 엔터시 오늘): ').strip()
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    if len(input_add) != 3:
        print("3가지 항목을 정확히 입력해주세요.")
        return

    # 공백도 걸러내주기 위해 
    if not all(input_add):
        print("모든 항목을 빠짐없이 입력해주세요.")
        return

    if input_add[0] not in ("수입", "지출"):
        print("수입인지 지출인지 다시 입력해주세요.")
        return
    elif not input_add[1].isdigit()  :
        print("금액은 양의 정수로 입력해주세요.")
        return

    try:
        sql = """insert into transactions (tx_type, amount, memo, reg_date) values(:1, :2, :3, :4)"""
        cursor.execute(sql, (input_add[0], input_add[1], input_add[2], date))
        conn.commit()
        if cursor.rowcount > 0:
            print("가계부에 추가되었습니다.\n")

    except oracledb.DatabaseError as e:
        (error_obj, ) = e.args
        print(error_obj.message)
        conn.rollback()


def list_transaction():
    # reg_date 순으로 나열
    # 번호 [지출] 300000원 - 용돈(2026-08-11)
    try:
        sql = """select * from transactions order by reg_date"""
        cursor.execute(sql)
        rows = cursor.fetchall()

        if not rows:
            print("등록된 내역이 없습니다.")
            return

        print("-"*50)

        for tx_id, tx_type, amount, memo, reg_date in rows:
            print(f"{tx_id} [{tx_type}] {amount}원 - {memo}({reg_date})")

    except oracledb.DatabaseError as e:
        (error_obj, ) = e.args
        print(error_obj.message)
        conn.rollback()


def monthly_summary():
    target_month = input("보고싶으신 년월을 입력하세요. (YYYY-MM)").strip()

    if len(target_month) !=7 or target_month[4] != "-":
        print("형식에 맞게 다시 입력해주세요. (예: 2026-03)")
        return
    
    try:
        sql = """select tx_type, sum(amount) from transactions
        where reg_date like :1
        group by tx_type
        """
        cursor.execute(sql, (target_month + "%", ))
        rows = cursor.fetchall()

        if not rows:
            print(f"{target_month}에 등록된 내역이 없습니다.\n")

        income = 0
        expense = 0
        for tx_type, total in rows:
            if tx_type == "수입":
                income = total
            elif tx_type == "지출":
                expense = total

        print("-"*50)
        print(f"{target_month}요약. 수입: {income}원, 지출: {expense}원, 순수익: {income - expense}원 ")

    except oracledb.DatabaseError as e:
        (error_obj, ) = e.args
        print(error_obj.message)
        conn.rollback()
        

def menu():
    # 1. 내역추가 2. 전체조회 3. 월별 합계  4.종료
    while True:
        print("=== budget book ===")
        print("1: 내역추가, 2: 전체조회, 3: 월별합계, 4: 종료")

        choice = input("원하시는 항목을 선택해주세요")

        if choice == "1":
            add_transaction()
        elif choice == "2":
            list_transaction()
        elif choice == "3":
            monthly_summary()
        elif choice == "4":
            print("가계부를 종료합니다.")
            break
        else:
            print("번호를 다시 입력해주세요.")


if __name__ == "__main__":
    try:
        menu()
    finally:
        cursor.close()
        conn.close()