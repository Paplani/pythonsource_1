from sqlalchemy import create_engine, Numeric, String, DateTime, Identity, select, func, extract
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, Session
from dotenv import load_dotenv
from datetime import datetime
from typing import Optional
import os

load_dotenv()
password = os.getenv("ORACLE_PASSWORD")
engine = create_engine(f"oracle+oracledb://python_user:{password}@localhost:1521/?service_name=xe", echo=True)

class Base(DeclarativeBase):
    pass

class Transactions(Base):
    __tablename__ = "transactions"

    tx_id: Mapped[int] = mapped_column(Numeric(10), Identity(start=1, increment=1), primary_key=True)
    tx_type: Mapped[str] = mapped_column(String(20))
    amount: Mapped[int] = mapped_column(Numeric(20))
    memo: Mapped[str] = mapped_column(String(100))
    reg_date: Mapped[Optional[datetime]] = mapped_column(DateTime)

    def __repr__(self):
        return f"{self.tx_id} [{self.tx_type}] {self.amount}원 - {self.memo}({self.reg_date})"

def add_transaction():
    input_add = input("추가하시고자 하는 내역을 입력해주세요. 수입/지출 여부, 금액, 어떤 내용인지 적어주세요. 각 항목은 반드시 쉼표로 구분해주세요.").split(",")
    input_add = [x.strip() for x in input_add]    # 쉽표로 나눈 리스트들의 앞뒤 공백 제거해서 다시 리스트로 넣어주기

    date_input = input('날짜를 입력하세요. (YYYY-MM-DD, 엔터시 오늘): ').strip()
    if not date_input:
        reg_date = datetime.now()
    else:
        try:
            # reg_date 컬럼이 DateTime이라 문자열 그대로가 아니라 datetime 객체로 변환해서 넣어야 함
            reg_date = datetime.strptime(date_input, "%Y-%m-%d")
        except ValueError:
            print("날짜 형식이 올바르지 않습니다. (예: 2026-08-11)")
            return

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

    with Session(engine) as session:
        tx = Transactions(
            tx_type = input_add[0], 
            amount = int(input_add[1]),
            memo = input_add[2], 
            reg_date=reg_date,
        )
        session.add(tx)
        session.commit()
        print("가계부에 추가되었습니다.\n")

def list_transaction():
    # reg_date 순으로 나열
    # 번호 [지출] 300000원 - 용돈(2026-08-11)

    with Session(engine) as session:
        print("-"*50)
        found = False
        stmt = select(Transactions).order_by(Transactions.reg_date)

        for tx in session.scalars(stmt):
            found = True
            print(tx)
        if not found:
            print("등록된 내역이 없습니다.")



def monthly_summary():
    target_month = input("보고싶으신 년월을 입력하세요. (YYYY-MM)").strip()

    if len(target_month) !=7 or target_month[4] != "-":
        print("형식에 맞게 다시 입력해주세요. (예: 2026-03)")
        return

    year, month = target_month.split("-")

    with Session(engine) as session:
        # reg_date가 진짜 DateTime이라 문자열 like가 아니라 etract()로 년/월만 뽑아서 비교
        # extract("year", Transactions.reg_date) 이건 SQL의 EXTRACT(YEAR FROM reg_date) 로 변환됨 
        # 뭘 어느 컬럼에서 뽑을지.
        # reg_date가 문자열이면 Like로 하면 되지만
        # 지금은 DateTime 타입이라 extract()로 연/월 숫자 추출

        stmt = (select(Transactions.tx_type, func.sum(Transactions.amount))
               .where(extract("year", Transactions.reg_date) == int(year),
                     extract("month", Transactions.reg_date) == int(month),)
                     .group_by(Transactions.tx_type))
        rows = session.execute(stmt).all()

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
        print(f"{target_month}요약. 수입: {income}원, 지출: {expense}원, 순수익: {income - expense}원")
        

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
    Base.metadata.create_all(engine)
    menu()
