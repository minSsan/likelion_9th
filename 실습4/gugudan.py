def gugudan1():
    for i in range(1, 10):
        print("%d X %d = %d"%(1, i, 1*i))

def gugudan2():
    for i in range(1, 10):
        print("%d X %d = %d"%(2, i, 2*i))

def gugudan3():
    for i in range(1, 10):
        print("%d X %d = %d"%(3, i, 3*i))

def gugudan4():
    for i in range(1, 10):
        print("%d X %d = %d"%(4, i, 4*i))

def gugudan5():
    for i in range(1, 10):
        print("%d X %d = %d"%(5, i, 5*i))

def gugudan6():
    for i in range(1, 10):
        print("%d X %d = %d"%(6, i, 6*i))

def gugudan7():
    for i in range(1, 10):
        print("%d X %d = %d"%(7, i, 7*i))

def gugudan8():
    for i in range(1, 10):
        print("%d X %d = %d"%(8, i, 8*i))

def gugudan9():
    for i in range(1, 10):
        print("%d X %d = %d"%(9, i, 9*i))

num = int(input("1 ~ 9 사이 숫자를 입력해주세요: "))

if num == 1:
    gugudan1()
elif num == 2:
    gugudan2()
elif num == 3:
    gugudan3()
elif num == 4:
    gugudan4()
elif num == 5:
    gugudan5()
elif num == 6:
    gugudan6()
elif num == 7:
    gugudan7()
elif num == 8:
    gugudan8()
elif num == 9:
    gugudan9()
else:
    print("잘못된 입력값입니다.")
