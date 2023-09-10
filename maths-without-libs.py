pi = 0

def fact(x): #Factorial - iteration
    count = 1
    for i in range(1,x+1):
        count *= i
    return count

def sqrt(x): #Square root - Newton-Raphson method
    x0 = x
    for i in range(1000):
        x0 -= (((x0**2))-x)/(2*x0)
    return x0

def root(num,root): #Root - Newton-Raphson method
    x0 = num
    for i in range(1000):
        x0 -= (((x0**root))-num)/(root*(x0**(root-1)))
    return x0

def sqrt2(x): #Square root - Newton-Raphson method (simplified)
    x0 = x
    for i in range(1000):
        x0 = (x0+(x/x0))/2
    return x0

def madhava(): #Pi - Madhava series
    global pi
    count = 0
    for i in range(1000):
        if i % 2 == 0:
            count += 1/(((i*2)+1)*(3**i))
        else:
            count -= 1/(((i*2)+1)*(3**i))
    pi = count*sqrt(12)
    return pi

def ramanujan(): #Pi - Ramanujan-Sato series
    global pi
    count = 0
    for i in range(100):
        count += (fact(4*i)*(1103+(26390*i)))/((((fact(i))**4))*((396**(4*i))))
    pi = 9801/(count*2*sqrt(2))
    return pi

def chudnovsky(): #Pi - Chudnovsky algorithm
    global pi
    count = 0
    C = 426880*sqrt(10005)
    for i in range(10):
        M = (fact(6*i))/((fact(3*i))*((fact(i))**3))
        L = (545140134*i)+13591409
        X = ((-262537412640768000)**i)
        count += (M*L)/X
    pi = C/count
    return pi
        
def sin(x): #Sin - Maclaurin expansion
    global pi
    if x%180 == 0:
        x = 0
    else:
        x = (x%360)*(pi/180)
    count = x
    for i in range(1,30):
        answer = (((x**((i*2)+1)))/fact((i*2)+1))
        if i % 2 != 0:
            count -= answer
        else:
            count += answer  
    return count
