import thorpy
import pygame
from PIL import ImageFont
import sys
import math
import re
import os

def get_pil_text_size(text, font_size, font_name):
    font = ImageFont.truetype(font_name, font_size)
    size = font.getlength(text)
    return size

normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
super_s = "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾"

    
def get_super(x):    
    res = x.maketrans(''.join(normal), ''.join(super_s))
    return x.translate(res)

def un_super(x):
    res = x.maketrans(''.join(super_s), ''.join(normal))
    return x.translate(res)

pygame.init()
screen = pygame.display.set_mode((652, 300))
pygame.display.set_caption('Scientific Calculator')

painter1 = thorpy.painters.roundrect.RoundRect(size=(85.14,36),color=(218,220,224),radius=0.3)
painter2 = thorpy.painters.roundrect.RoundRect(size=(36,36),color=(218,220,224),radius=0)
painter3 = thorpy.painters.roundrect.RoundRect(size=(85.14,36),color=(241,243,244),radius=0.3)
painter4 = thorpy.painters.roundrect.RoundRect(size=(85.14,36),color=(66,133,244),radius=0.3)
painter5 = thorpy.painters.basicframe.BasicFrame(size=(616.22,32),color=(255,255,255))
painter6 = thorpy.painters.basicframe.BasicFrame(size=(576.22,20),color=(255,255,255))

coords = True
answer = ""
clearvar = False
running = True
symlist = ['x','÷','+','-']
numlist = ['1','2','3','4','5','6','7','8','9','0','.']
invvar = False
superscript = False
prev_ans = 'Ans = 0'
temp_prev_ans = 'Ans = 0'

answerfield = thorpy.Element(answer)
answerfield.set_painter(painter5)
answerfield.finish()
answerfield.set_topleft((17.89,40))
answerfield.set_font("Calibri")
answerfield.set_font_size(30)

prevanswerfield = thorpy.Element(prev_ans)
prevanswerfield.set_painter(painter6)
prevanswerfield.finish()
prevanswerfield.set_topleft((57.89,20))
prevanswerfield.set_font("Calibri")
prevanswerfield.set_font_size(15)
prevanswerfield.set_font_color((92,97,102))

def answer_update():
    global answer
    global prev_ans
    textlen = (get_pil_text_size(answer, 30, 'calibri.ttf'))
    prevtextlen = (get_pil_text_size(prev_ans, 15, 'calibri.ttf'))
    answerfield.set_topleft((((17.89+616.22)-textlen-(308.11-(textlen/2))),40))
    prevanswerfield.set_topleft((((57.89+576.22)-prevtextlen-(288.11-(prevtextlen/2))),20))
    if textlen > 616.22:
        answer = answer[:-1]
    answerfield.set_text(answer)
    answerfield.update()
    answerfield.unblit_and_reblit()
    prevanswerfield.set_text(prev_ans)
    prevanswerfield.update()
    prevanswerfield.unblit_and_reblit()

def invert_calcs():
    global invvar
    if invvar == False:
        invvar = True
        sin.set_text('sin⁻¹')
        sin.set_font_color_hover((0,0,0))
        cos.set_text('cos⁻¹')
        cos.set_font_color_hover((0,0,0))
        tan.set_text('tan⁻¹')
        tan.set_font_color_hover((0,0,0))
        ln.set_text('eˣ')
        ln.set_font_color_hover((0,0,0))
        log.set_text('10ˣ')
        log.set_font_color_hover((0,0,0))
        sqrt.set_text('x²')
        sqrt.set_font_color_hover((0,0,0))
        xy.set_text('ʸ√x')
        xy.set_font_color_hover((0,0,0))
    elif invvar == True:
        invvar = False
        sin.set_text('sin')
        sin.set_font_color_hover((0,0,0))
        cos.set_text('cos')
        cos.set_font_color_hover((0,0,0))
        tan.set_text('tan')
        tan.set_font_color_hover((0,0,0))
        ln.set_text('ln')
        ln.set_font_color_hover((0,0,0))
        log.set_text('log')
        log.set_font_color_hover((0,0,0))
        sqrt.set_text('√')
        sqrt.set_font_color_hover((0,0,0))
        xy.set_text('xʸ')
        xy.set_font_color_hover((0,0,0))

def raddeg():
    global coords
    if coords == True:
        deg.set_font_color((0,0,0))
        deg.set_font_color_hover((0,0,0))
        deg.update()
        deg.unblit_and_reblit()
        rad.set_font_color((92,97,102))
        rad.set_font_color_hover((92,97,102))
        rad.update()
        rad.unblit_and_reblit()
        coords = False
    elif coords == False:
        rad.set_font_color((0,0,0))
        rad.set_font_color_hover((0,0,0))
        rad.update()
        rad.unblit_and_reblit()
        deg.set_font_color((92,97,102))
        deg.set_font_color_hover((92,97,102))
        deg.update()
        deg.unblit_and_reblit()
        coords = True

def sin_func(x):
    global coords
    if coords == True:
        return math.sin(x)
    elif coords == False:
        return math.sin(math.radians(x))
    else:
        return 'ERROR'

def cos_func(x):
    global coords
    if coords == True:
        return math.cos(x)
    elif coords == False:
        return math.cos(math.radians(x))
    else:
        return 'ERROR'

def tan_func(x):
    global coords
    if coords == True:
        return math.tan(x)
    elif coords == False:
        return math.tan(math.radians(x))
    else:
        return 'ERROR'

def asin_func(x):
    global coords
    if coords == True:
        return math.asin(x)
    elif coords == False:
        return math.asin(math.radians(x))
    else:
        return 'ERROR'

def acos_func(x):
    global coords
    if coords == True:
        return math.acos(x)
    elif coords == False:
        return math.acos(math.radians(x))
    else:
        return 'ERROR'

def atan_func(x):
    global coords
    if coords == True:
        return math.atan(x)
    elif coords == False:
        return math.atan(math.radians(x))
    else:
        return 'ERROR'

def press(x,inverse=None):
    global answer
    global clearvar
    global invvar
    global superscript
    global prev_ans
    global temp_prev_ans
    if invvar == True and inverse != None:
        x = inverse
    if x in symlist and answer[-1] in symlist:
        answer = answer
    elif x == 'E':
        if len(answer) == 1 and answer[0] == '0':
            answer = answer
        elif answer[-1] not in numlist:
            answer = answer
        else:
            answer += str(x)
            answer_update()
    elif superscript == True:
        if str(x) in numlist:
            answer = answer.replace('□',str(get_super(str(x))))
        elif x not in numlist:
            superscript = False
    elif x == 'root':
        answer += '√'
        answer = re.sub(r'([\w]+)√', r'□√\1', answer)
        superscript = True
    else:
        if len(answer) == 1 and answer[0] == '0':
            answer = answer[:-1]
        if answer == 'ERROR':
            answer = ''
        if clearvar == True:
            if x not in symlist:
                answer = ''
            clearvar = False
            prev_ans = temp_prev_ans
            ce.set_text("CE")
            ce.set_font_color_hover((0,0,0))
            ce.update()
            ce.unblit_and_reblit()
        if x == '□' or x == 'e□' or x == '10□':
            superscript = True
        answer += str(x)
    answer_update()

def clear():
    global answer
    global clearvar
    global prev_ans
    global temp_prev_ans
    if clearvar == False:
        if answer == 'ERROR':           
            answer = ''
            answer += '0'
        answer = answer[:-1]
        if len(answer) == 0:
            answer += '0'
        answer_update()
    elif clearvar == True:
        answer = ''
        answer += '0'
        clearvar = False
        prev_ans = temp_prev_ans
        ce.set_text("CE")
        ce.set_font_color_hover((0,0,0))
        ce.update()
        ce.unblit_and_reblit()
        answer_update()

def calc():
    global answer
    global clearvar
    global coords
    global superscript
    global prev_ans
    global temp_prev_ans
    prev_ans = str(answer)+' ='
    answercalc = answer.replace('x','*')
    answercalc = answercalc.replace('÷','/')
    answercalc = answercalc.replace('%','/100')
    answercalc = answercalc.replace('π','math.pi')
    #answercalc = answercalc.replace('e','math.e')
    answercalc = answercalc.replace('sin⁻¹','asn_func')
    answercalc = answercalc.replace('cos⁻¹','acs_func')
    answercalc = answercalc.replace('tan⁻¹','atn_func')
    answercalc = answercalc.replace('sin','sin_func')
    answercalc = answercalc.replace('cos','cos_func')
    answercalc = answercalc.replace('tan','tan_func')
    answercalc = answercalc.replace('sn','sin')
    answercalc = answercalc.replace('cs','cos')
    answercalc = answercalc.replace('tn','tan')
    answercalc = re.sub(r'([\w]+)math.pi', r'\1*math.pi', answercalc)
    answercalc = re.sub(r'([\w]+)math.e', r'\1*math.e', answercalc)
    rootre = re.match(r'([\w]+)√([\w]+)', answercalc)
    if rootre != None:
        answercalc = answercalc.replace(rootre.group(1)+'√'+rootre.group(2),str(rootre.group(2)+'**'+str(1/int(un_super(rootre.group(1))))))
    answercalc = re.sub(r'([\w]+)√', r'\1*√', answercalc)
    answercalc = re.sub(r'√([\w]+)', r'math.sqrt(\1)', answercalc)
    answercalc = re.sub(r'log\(([\w]+)\)', r'math.log(\1,10)', answercalc)
    #answercalc = answercalc.replace('ln','math.log')
    answercalc = re.sub(r'([\w]+)!|\((.+?)\)!', r'math.factorial(\1\2)', answercalc)
    for i in answercalc:
        if i in super_s:
            answercalc = answercalc.replace(i,'**'+un_super(i))
    try:
        print(answercalc)
        answer = str(eval(answercalc))
        temp_prev_ans = 'Ans = '+answer
        if (get_pil_text_size(answer, 30, 'calibri.ttf')) > 616.22:
            answer = "{:E}".format(float(answer))
        answer = answer.replace('e','E')
    except:
        answer = 'ERROR'
        temp_prev_ans = 'Ans = 0'
    clearvar = True
    ce.set_text("AC")
    ce.set_font_color_hover((0,0,0))
    ce.update()
    ce.unblit_and_reblit()
    superscript = False
    answer_update()
    
rad = thorpy.make_button("Rad",raddeg)
mid = thorpy.make_button("|",raddeg)
deg = thorpy.make_button("Deg",raddeg)
inv = thorpy.make_button("Inv",invert_calcs)
pi = thorpy.make_button("π",press,params={"x":'π'})
e = thorpy.make_button("e",press,params={"x":'e'})
ans = thorpy.make_button("Ans")
sin = thorpy.make_button("sin",press,params={"x":'sin(',"inverse":'sin⁻¹('})
cos = thorpy.make_button("cos",press,params={"x":'cos(',"inverse":'cos⁻¹('})
tan = thorpy.make_button("tan",press,params={"x":'tan(',"inverse":'tan⁻¹('})
exp = thorpy.make_button("EXP",press,params={"x":'E'})
fact = thorpy.make_button("x!",press,params={"x":'!'})
ln = thorpy.make_button("ln",press,params={"x":'ln(',"inverse":'e□'})
log = thorpy.make_button("log",press,params={"x":'log(',"inverse":'10□'})
sqrt = thorpy.make_button("√",press,params={"x":'√',"inverse":'²'})
xy = thorpy.make_button("xʸ",press,params={"x":'□',"inverse":'root'})
left = thorpy.make_button("(",press,params={"x":'('})
num7 = thorpy.make_button("7",press,params={"x":7})
num4 = thorpy.make_button("4",press,params={"x":4})
num1 = thorpy.make_button("1",press,params={"x":1})
num0 = thorpy.make_button("0",press,params={"x":0})
right = thorpy.make_button(")",press,params={"x":')'})
num8 = thorpy.make_button("8",press,params={"x":8})
num5 = thorpy.make_button("5",press,params={"x":5})
num2 = thorpy.make_button("2",press,params={"x":2})
numdot = thorpy.make_button(".",press,params={"x":'.'})
percent = thorpy.make_button("%",press,params={"x":'%'})
num9 = thorpy.make_button("9",press,params={"x":9})
num6 = thorpy.make_button("6",press,params={"x":6})
num3 = thorpy.make_button("3",press,params={"x":3})
equals = thorpy.make_button("=",calc)
ce = thorpy.make_button("CE",clear)
divide = thorpy.make_button("÷",press,params={"x":'÷'})
multiply = thorpy.make_button("x",press,params={"x":'x'})
minus = thorpy.make_button("-",press,params={"x":'-'})
plus = thorpy.make_button("+",press,params={"x":'+'})

elements1 = [rad,deg,inv,pi,e,ans,sin,cos,tan,exp,fact,ln,log,sqrt,xy,left,right,percent,ce,divide,multiply,minus,plus]
elements2 = [num7,num4,num1,num0,num8,num5,num2,numdot,num9,num6,num3]
elements = []

for i in elements1:
    i.set_painter(painter1)
    i.finish()
    elements.append(i)

for i in elements2:
    i.set_painter(painter3)
    i.finish()
    elements.append(i)
    
rad.set_topleft((4,84))
deg.set_topleft((97.14,84))
inv.set_topleft((4,128))
pi.set_topleft((4,172))
e.set_topleft((4,216))
ans.set_topleft((4,260))
sin.set_topleft((97.14,128))
cos.set_topleft((97.14,172))
tan.set_topleft((97.14,216))
exp.set_topleft((97.14,260))
fact.set_topleft((190.28,84))
ln.set_topleft((190.28,128))
log.set_topleft((190.28,172))
sqrt.set_topleft((190.28,216))
xy.set_topleft((190.28,260))
left.set_topleft((283.42,84))
num7.set_topleft((283.42,128))
num4.set_topleft((283.42,172))
num1.set_topleft((283.42,216))
num0.set_topleft((283.42,260))
right.set_topleft((376.56,84))
num8.set_topleft((376.56,128))
num5.set_topleft((376.56,172))
num2.set_topleft((376.56,216))
numdot.set_topleft((376.56,260))
percent.set_topleft((469.7,84))
num9.set_topleft((469.7,128))
num6.set_topleft((469.7,172))
num3.set_topleft((469.7,216))
ce.set_topleft((562.84,84))
divide.set_topleft((562.84,128))
multiply.set_topleft((562.84,172))
minus.set_topleft((562.84,216))
plus.set_topleft((562.84,260))

for i in elements:
    i.set_font('Calibri')
    i.set_font_size(15)
    i.set_font_color_hover((0,0,0))

deg.set_font_color((92,97,102))
deg.set_font_color_hover((92,97,102))

mid.set_painter(painter2)
mid.finish()
mid.set_font("Arial Bold")
mid.set_font_size(28)
mid.set_font_color((165,168,173))
mid.set_font_color_hover((165,168,173))
mid.set_topleft((75.14,84))
elements.append(mid)

numdot.set_font("Arial Bold")
numdot.set_font_size(30)
numdot.set_font_color_hover((0,0,0))

equals.set_painter(painter4)
equals.finish()
equals.set_font("Arial Bold")
equals.set_font_size(30)
equals.set_font_color((255,255,255))
equals.set_font_color_hover((255,255,255))
equals.set_topleft((469.7,260))
elements.append(equals)

divide.set_font("Arial Bold")
multiply.set_font("Arial Bold")
minus.set_font("Arial Bold")
plus.set_font("Arial Bold")
divide.set_font_size(28)
multiply.set_font_size(20)
minus.set_font_size(30)
plus.set_font_size(25)
divide.set_font_color_hover((0,0,0))
multiply.set_font_color_hover((0,0,0))
minus.set_font_color_hover((0,0,0))
plus.set_font_color_hover((0,0,0))

elements.append(answerfield)
elements.append(prevanswerfield)

background = thorpy.Background(color=(255, 255, 255), elements=elements)

answer += '0'
answer_update()

menu = thorpy.Menu(background)

screen.fill((255,255,255))

def blit_all():
    for element in menu.get_population():
        element.surface = screen
        element.blit()

blit_all()
pygame.display.flip()

while running == True:
    screen.fill((255,255,255))
    blit_all()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                clear()
            elif event.key == pygame.K_RETURN:
                calc()
            elif event.key == pygame.K_SLASH:
                press('÷')
            elif event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                None
            else:
                press(event.unicode)
                answer_update()
        menu.react(event)
        pygame.display.update()


