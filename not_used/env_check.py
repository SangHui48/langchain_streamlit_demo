env_set = set()

with open('requirements.txt','r') as f:
    lines = f.readlines()
    for line in lines:
        env_set.add(line.rstrip())
    
with open('requirements2.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        env_set.add(line.rstrip())
print(env_set)
with open('requirements3.txt', 'w') as f:
    for item in env_set:
        f.write(item+'\n')