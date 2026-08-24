import pickle
# pickle 모듈은 파이썬 객체를 파일로 저장하고 읽어들임
# 저장된 상태에서 프로그램이 종료되면 객체는 자동 소멸됨
# 파이썬 객체를 바이트 형태로 직렬화(serialize)해서 파일로 저장하고, 나중에 그대로 복원(deserialize)할 수 있게 해주는 파이썬 표준 라이브러리입니다.
# 직렬화(dump): 메모리에 있는 파이썬 객체(리스트, 딕셔너리, DataFrame, 학습된 모델 등) → 파일(바이트열)
# 역직렬화(load): 파일(바이트열) → 원래의 파이썬 객체로 복원

'''
f=open('setting.txt', 'wb')
setting=[{'title':'python program'}, {'author':'soldesk'}]
pickle.dump(setting, f)
f.close()
'''

f=open('setting2.txt', 'wb')
try:
    setting=[{'title':'python program'}, {'author':'soldesk'}]
    pickle.dump(setting, f)
except Exception as e:
    print(e)
finally:
    f.close()