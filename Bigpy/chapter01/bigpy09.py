import matplotlib.pyplot as plt
# uv pip install matplotlib

'''
x=[a for a in range(0,11)]
y = list(range(0,11))

print('x축', x)
print('y축', y)

# 출력
plt.plot(x,y)
plt.show()
'''


# 2차원 함수 => f(x) = x^2
f = lambda x:x**2
x=[x for x in range(-10, 11)]
y=[f(y) for y in x]

print('x축', x)
print('y축',y)

plt.plot(x,y)
plt.show()