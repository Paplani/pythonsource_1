# 영어타자 프로그램

# word.txt 읽어서 문제 섞어서 보여줌
# random.shuffle()
# 임의로 하나 추출 : choice()

# Q1) then
# input()
# input으로 입력한 값이 정답인지 오답인지 출력

# start = time.time()
# 문제 5문제 출제
# 정답 개수
# end = time.time()

# 게임시간 출력
# 출력문 => 게임시간 : 10초, 정답개수 : 3개
# 3개이상 정답인 경우 합격

# 처음에 내가 적은거
import time 
import random

with open("./data/word.txt", "r", encoding="utf-8") as f:
    contents = [line.strip() for line in f.readlines()]
    # random.shuffle() 은 반환값이 없기 때문에 그냥 섞어줘야함
    random.shuffle(contents)
    pickedList = contents[:5]
    start = time.time()
    trueAnswer = 0
    while pickedList :
        pickedOne = random.choice(pickedList)
        print(f"Q: {pickedOne}")
        answer = input("단어를 입력해주세요")
        # 여기도 remove()는 반환값이 없기 때문에 그냥 제거만 해야함
        # pickedList = pickedlist.remove(pickedOne) 해주면 안됨
        pickedList.remove(pickedOne)
        if answer == pickedOne:
            print("정답!!!")  
            trueAnswer += 1
        else:
            print("오타!!!")

end = time.time()
et = end - start
et = format(et, ".3f")

if trueAnswer >= 3:
    result = "합격"
else:
    result = "불합격"

print(f"게임시간 : {et}, 정답개수 : {trueAnswer}, 합격여부 : {result}")


# count쓰는걸 제미나이한테 아이디어를 얻은 후
with open("./data/word.txt", "r", encoding = "utf-8") as f:
    contents = [line.strip() for line in f.readlines()]
    # choices는 중복을 허용해서 뽑음. 이럴때는 sample(contents, 5)를 사용하는게 더 좋음
    contentList = random.choices(contents, k = 5)
    start = time.time()
    trueAnswer = 0
    count = 0
    while count < 5:
        pickedOne = contentList[count]   
        print(f"Q{count+1} : {pickedOne}")
        answer = input("단어 입력해")
        count += 1
        if answer == pickedOne:
            print("정답!!!")  
            trueAnswer += 1
        else:
            print("오타!!!")

end = time.time()
et = end - start
et = format(et, ".3f")


if trueAnswer >= 3:
    result = "합격"
else:
    result = "불합격"

print(f"게임시간 : {end - start}, 정답개수 : {trueAnswer}, 합격여부 : {result}")
        