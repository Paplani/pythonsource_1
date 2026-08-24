import pickle

f = open('setting.txt', 'rb')
setting = pickle.load(f, encoding='utf-8')
f.close()

print(setting)