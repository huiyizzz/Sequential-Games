import random

def instance(path, name, num, cap, refill, fun, goal, count):
    file = str(name).zfill(2)+'_'+str(count)+'.dzn'
    filename = path+file
    with open(filename,'w') as f:
        f.write('num = '+str(num)+';\n')
        f.write('cap = '+str(cap)+';\n')
        f.write('refill = '+str(refill)+';\n')
        f.write('fun = '+str(fun)+';\n')
        f.write('goal = '+str(goal)+';\n')

def change_num():
    path = './change_num/'
    for num in range(4,11):
        instance(path, num, num, 5, 2, [i for i in range(num, 0, -1)], 0, 1)
        instance(path, num, num, 5, 2, [i for i in range(1, num+1)], 0, 2)
        instance(path, num, num, 5, 2, [i for i in range(num, 0, -1)], 150, 3)
        instance(path, num, num, 5, 2, [i for i in range(1, num+1)], 150, 4)

def random_instances():
    path = './random_instances/'
    for num in range(4,11):
        for t in range(1,3):
            cap = random.randint(3, 10)
            refill = random.randint(1, cap)
            fun = [random.randint(-10, 10) for i in range(num)]
            goal = random.randint(-100, 1000)
            instance(path, num, num, cap, refill, fun, goal, t)


#change_num()
#random_instances()