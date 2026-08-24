import matplotlib.pyplot as plt

# 계절별 서울/부산 지역 온도 데이터 정의
temperatures = [3.3, 34.5, 14.2, -10]
x = list(range(4))
x_labels = ['Spring', 'Summer', 'Fall', 'Winter']

# bar차트
plt.title("Bar Chart")
plt.bar(x, temperatures)
plt.xticks(x, x_labels)
plt.yticks(sorted(temperatures))
plt.xlabel("seasons")
plt.ylabel("temperatures")
plt.show() 