data = open('runtime.txt').read().split('\n')
with open('runtime.txt','w') as f:
    f.write(' '.join(data))