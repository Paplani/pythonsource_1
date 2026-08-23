from sqlalchemy import create_engine, Numeric, String, DateTime, Identity, select
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, Session
from dotenv import load_dotenv
from typing import Optional
from datetime import datetime
import os

load_dotenv()
password = os.getenv("ORACLE_PASSWORD")
engine = create_engine(f"oracle+oracledb://python_user:{password}@localhost:1521/?service_name=xe", echo=True)


class Base(DeclarativeBase):
    pass

class Todo(Base):
    __tablename__ = "todo_list"

    todo_id:Mapped[int] = mapped_column(Numeric(10), Identity(start=1, increment=1), primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    is_done: Mapped[bool] = mapped_column(default=False)
    # Optional[datetime] : 값이 None 혹은 datetime
    created_at : Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.now)

    def __repr__(self):
        status = "완료" if self.is_done else "미완료"
        return f"{self.todo_id}. [{status}]{self.title} ({self.created_at})"


def ask_number(question: str):
    user_data = input(f"{question}")
    try:
        return int(user_data)
    except ValueError:
        print("에러 발생. 숫자를 입력해주세요.")
        return



# todo 추가 함수
def add_todo():
    # 할일 내용을 입력하세요 : 내용입력...
    #  등록되었습니다 보이게. 
    # 또한 db에 등록까지.
    input_todo = input("할 일을 입력해주세요.").strip()
    if not input_todo:
        print("아무것도 입력되지 않았습니다.")
        return 
    elif input_todo.isdigit():
        print("숫자만 입력되었습니다. 할 일을 입력해주세요")
        return 

    with Session(engine) as session:
        todo = Todo(title=input_todo)
        session.add(todo)
        session.commit()
        print(f"{todo.todo_id}. 등록되었습니다\n")


def list_todos():

    with Session(engine) as session:
        print("-"*20)
        # row 개수가 0이냐 아니냐 판단하는 것
        found = False
        stmt = select(Todo).order_by(Todo.todo_id)
        for todo in session.scalars(stmt):
            found = True
            print(todo)

        if not found:
            print("등록된 할 일이 없습니다.")

    # session.scalars(stmt)는 사실 리스트가 아니라 "결과를 하나씩 꺼내주는 이터레이터(ScalarResult)" 예요. 
    # .all()을 붙이면 그 순간 전체를 리스트로 한꺼번에 메모리에 올리는 거고, 이것처럼 .all() 없이 바로 for문 돌리면 한 건씩 꺼내면서(streaming) 처리해요.


def update_todo():

    user_choice = ask_number("완료 처리할 번호를 입력해주세요: ")

    if user_choice is None:
        return

    with Session(engine) as session:
        selected = session.get(Todo, user_choice)
        if selected is None:
            print("해당 번호의 할 일이 없습니다.")
            return
        selected.is_done = True
        session.commit()
        print("완료 처리되었습니다.\n")


    
def delete_todo():

    user_choice = ask_number("삭제 처리할 번호를 입력해주세요: ")

    if user_choice is None:
        return
    with Session(engine) as session:
        selected = session.get(Todo, user_choice)
        if selected is None:
            print("삭제할 번호의 할 일이 없습니다.")
            return
        session.delete(selected)
        session.commit()
        print("삭제되었습니다.")


def menu():
    while True:
        print("=== Todo")
        print("1. 추가 2.목록 3.완료처리 4.삭제 5.종료")

        choice = input("선택 : ")

        if choice == "1":
            add_todo()
        elif choice == "2":
            list_todos()
        elif choice == "3":
            update_todo()
        elif choice == "4":
            delete_todo()
        elif choice == "5":
            print("종료합니다.")
            break
        else:
            print("번호를 확인해주세요")

# 파이썬에서 "이 파일이 직접 실행됐을 때만 이 코드를 돌려라"는 뜻
# finally 는 try 안에서 어떤 일이 일어나도 무조건 실행되는 블록이다.
# 여기서는 이 게임이 어캐 끝나든 DB연결은 무조건 정리하라는 의미. 

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    menu()