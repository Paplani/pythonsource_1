# 사용자 정의 모듈
# 함수 2개 정의
def add(a,b):
    return a + b

def sub(a,b):
    return a - b

PI = 3.145192

class Math:
    def solv(self, r):
        return PI * (r**2)

# 테스트
if __name__ == "__main__":
    print(add(9,5))
    print(sub(9,5))
    m = Math()
    print(m.solv(6))