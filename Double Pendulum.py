# Inits
import sympy as sym
import sympy.physics.mechanics as mech
mech.init_vprinting()
import numpy as np
import scipy
import scipy.integrate
import pygame
import sys
import math
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
running = True
num = 0

# Constants
m1,m2 = sym.symbols('m_1, m_2')
L1,L2 = sym.symbols('L_1, L_2')
t,g = sym.symbols('t, g')

the1 = sym.Function('theta_1')(t) # Angles, functions of time
the2 = sym.Function('theta_2')(t)

x1 = L1*sym.sin(the1) # Lengths, worked out using trigonometry
y1 = -L1*sym.cos(the1)
x2 = L1*sym.sin(the1)+L2*sym.sin(the2)
y2 = -L1*sym.cos(the1)-L2*sym.cos(the2)

vx1,vy1,vx2,vy2 = (xx.diff(t) for xx in (x1,y1,x2,y2)) # Differentials of cartesian coordinates
the1_d = sym.diff(the1,t) # Differentials of thetas
the2_d = sym.diff(the2,t)
the1_dd = sym.diff(the1,t,2)
the2_dd = sym.diff(the2,t,2)


# Formulae
T1 = m1/2*(vx1**2+vy1**2) # Kinetic energy
T2 = m2/2*(vx2**2+vy2**2)
T = T1+T2

V = g*(m1*y1+m2*y2) # GPE

L = T-V # Lagrangian
L=L.expand().simplify()

# Euler-Lagrange Equations
LE1 = sym.diff(L, the1) - sym.diff(sym.diff(L, the1_d), t).simplify()
LE2 = sym.diff(L, the2) - sym.diff(sym.diff(L, the2_d), t).simplify()

sols = sym.solve([LE1, LE2], (the1_dd, the2_dd),simplify=False, rational=False) # Solve Euler-Lagrange Equations

dz1dt_f = sym.lambdify((t,g,m1,m2,L1,L2,the1,the2,the1_d,the2_d), sols[the1_dd]) # Convert symbolic expressions to functions
dz2dt_f = sym.lambdify((t,g,m1,m2,L1,L2,the1,the2,the1_d,the2_d), sols[the2_dd])
dthe1dt_f = sym.lambdify(the1_d, the1_d)
dthe2dt_f = sym.lambdify(the2_d, the2_d)

# Solve ODEs
def dSdt(S, t, g, m1, m2, L1, L2): # Function to pass to odeint
    the1, z1, the2, z2 = S
    return [
        dthe1dt_f(z1),
        dz1dt_f(t, g, m1, m2, L1, L2, the1, the2, z1, z2),
        dthe2dt_f(z2),
        dz2dt_f(t, g, m1, m2, L1, L2, the1, the2, z1, z2),
    ]

tvar = int(input('Seconds of runtime: '))
gvar = float(input('Gravity: '))
m1var = float(input('Mass 1: '))
m2var = float(input('Mass 2: '))
l1var = float(input('Length 1: '))
l2var = float(input('Length 2: '))

t = np.linspace(0, tvar, ((tvar*25)+1)) # Define variables and pass to odeint
g = gvar
m1 = m1var
m2 = m2var
L1 = l1var
L2 = l2var
ans = scipy.integrate.odeint(dSdt, y0=[1, -3, -1, 5], t=t, args=(g,m1,m2,L1,L2)) #y0 = start positions of thetas and angular velocity

the1_ans = ans.T[0] # Take theta values from solved equation
the2_ans = ans.T[2]

def get_x1y1x2y2(t, the1_ans, the2_ans, L1, L2): # Get mass locations from theta values
    return (L1*np.sin(the1_ans),
            -L1*np.cos(the1_ans),
            L1*np.sin(the1_ans) + L2*np.sin(the2_ans),
            -L1*np.cos(the1_ans) - L2*np.cos(the2_ans))

x1, y1, x2, y2 = get_x1y1x2y2(t, ans.T[0], ans.T[2], L1, L2)

pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
alpha_surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
alpha_surf2 = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

while running:
    screen.fill(black)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = True
            running = False
            pygame.quit()
            sys.exit()
            exit()
            quit()
    clock.tick(25)
    alpha_surf.fill((255, 255, 255, 255), special_flags=pygame.BLEND_RGBA_MULT)    
    pygame.draw.circle(screen,white,(400,400),10)
    pygame.draw.line(screen,red,(400,400),((400+100*(x1[num])),(400-100*(y1[num]))),10)
    pygame.draw.circle(screen,white,((400+100*(x1[num])),(400-100*(y1[num]))),25)
    pygame.draw.circle(alpha_surf,blue,((400+100*(x1[num])),(400-100*(y1[num]))),5)
    pygame.draw.line(screen,red,((400+100*(x1[num])),(400-100*(y1[num]))),((400+100*(x2[num])),(400-100*(y2[num]))),10)
    pygame.draw.circle(screen,white,((400+100*(x2[num])),(400-100*(y2[num]))),25)
    pygame.draw.circle(alpha_surf,green,((400+100*(x2[num])),(400-100*(y2[num]))),5)
    pygame.draw.circle(alpha_surf2,(255,255,255,100),((400+100*(x2[num])),(400-100*(y2[num]))),5)
    screen.blit(alpha_surf2, (0, 0))
    screen.blit(alpha_surf, (0, 0))
    num+=1
    if num > (len(x1)-1):
        num = 0
        alpha_surf2.fill((255,255,255,255), special_flags=pygame.BLEND_RGBA_SUB)
        alpha_surf.fill((255,255,255,255), special_flags=pygame.BLEND_RGBA_SUB)
    pygame.display.update()

