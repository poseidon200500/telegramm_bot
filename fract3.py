import turtle
import time
import re
from decorators import *
from fractal_dict import fract_info
'''
кодовые обозначения

F - идти вперёд, параметр: длина
K - идти вперёд, не рисуя: длина
U - поднять перо, параметров нет
D - опустить перо, параметров нет
+ - поворот налево, параметр: угол поворота
- - поворот направо, параметр: угол поворота
[ - начало повторяемой части
] - конец повторяемой части

'''
colors = ['yellow', 'cyan', 'red', 'light blue', 'pink', 'blue', 'purple', 'green', 'orange']
data = open("data.txt",'w')

def min_and_max(now,minx,miny,maxx,maxy):
    if now[0] > maxx:
        maxx = now[0]
    if now[0] < minx:
        minx = now[0]
    if now[1] > maxy:
        maxy = now[1]
    if now[1] < miny:
        miny = now[1]
    return [now,minx,miny,maxx,maxy]

def draw_rect(t,now,minx,miny,maxx,maxy):
    t.penup()
    t.goto(minx,miny)
    t.pendown()
    t.pencolor('red')
    t.goto(minx,maxy)
    t.goto(maxx,maxy)
    t.goto(maxx,miny)
    t.goto(minx,miny)
    t.penup()
    t.goto(*now)
    t.pendown()

def set_start_pos(fractal,index):
    if index == 1-1:
        fractal['start_pos'] = (0-(3**iterations * f_len/2)/2,0-(3**iterations * f_len/2)/2)
    if index == 6-1:
        fractal['start_pos'] = (0-(2**(iterations))*f_len,0-(2**iterations)*f_len/(3**0.5))
    if index == 9-1:
        fractal['start_pos'] = (0-(f_len*(2**iterations-1)/2),0+(f_len*(2**iterations-1)/2))

class SystemL:
    
    def __init__(self, t, axiom, width, length, angle,):
        # массив с набором команд (F,+,-)
        self.state_list = list(axiom.split())
        self.state = axiom
        self.width = width                  # толщина линии рисования
        self.length = length                # длина одного линейного сигмента
        self.angle = angle                  # фиксированный угол поворота
        self.t = t                          # черепашка
        self.rules = {}                     # словарь правил
        self.t.pensize(self.width)          # установка толщины пера

    def set_turtle(self, x, y, angle, width):
        self.width = width
        self.t.penup()
        self.t.goto(x, y)
        self.t.pendown()
        self.t.seth(angle)
        self.t.pensize(self.width)
        self.key_re_list = [] #список шаблонов комманд

    def add_rules(self, rules):  # на вход подавать кортеж содержащий кортежи-правила
        for rule in rules:
            key,value = rule[0],rule[1]
            key_re = ""
            if not isinstance(value,str):
                key_re = key.replace("(",r"\(")
                key_re = key_re.pelace(")",r"\(")
                key_re = re.sub(r"([a-z]+)([,]*)", lambda m: r"([-+]?\b\d+(?:\.\d+)?\b)" + m.group(2),key_re)
                self.key_re_list.append(key_re)

            self.rules[key] = (value,key_re)

    def update_param_cmd(self,m):
        if not self.function_key:
            return ""

        args = list(map(float,m.groups))
        return self.function_key(*args).lower()

    def generate_path(self, iter):
        for n in range(iter):
            # self.length = self.length / iter
            for key, values in self.rules.items():
                # заменяем F на правило, при этом понижаем регистр, чтобы при большом количестве правил они не наслаивались
                if isinstance(values[0], str):
                    self.state = self.state.replace(key, values[0].lower())
                else:
                    self.function_key = values[0]
                    self.state = re.sub(values[1],self.update_param_cmd,self.state)
                    self.function_key = None


            self.state = self.state.upper()

    def draw_turtle(self, start_pos, start_angle):
        # границы
        # устанавливаем скоростной режим черепашки
        self.t.up()
        self.t.setpos(start_pos)
        self.t.seth(start_angle)
        self.t.down()
        turtle_stack = []
        position_list = [start_pos,start_pos[0],start_pos[1],start_pos[0],start_pos[1]]
        #data.write()
        for part in self.state:
            if part == 'F':
                self.t.forward(self.length)

            elif part == 'U':
                self.t.penup()
            elif part == 'D':
                self.t.pendown()
            elif part == '+':
                self.t.left(self.angle)
            elif part == '-':
                self.t.right(self.angle)
            # ветвление
            elif part == '[':
                turtle_stack.append(
                    (self.t.xcor(), self.t.ycor(), self.t.heading(), self.t.pensize()))
            elif part == ']':
                x, y, angle, w = turtle_stack.pop()
                self.set_turtle(x, y, angle, w)

            # специфичные значения
            elif part == 'K':
                self.t.penup()
                self.t.forward(self.length)
                self.t.pendown()
            position_list[0] = (self.t.xcor(),self.t.ycor())
            position_list = min_and_max(*position_list)
        #draw_rect(self.t,*position_list)

@Repeater()
def Do_Fract(iterations, speed, f_len, angle, axiom, rules, start_pos=(0, 0), start_angle=0,pen_width = 1):
    #time.sleep(sleep)
    turtle.tracer(speed, 0)
    l_sys = SystemL(t, axiom, pen_width, f_len, angle)
    l_sys.add_rules(rules)
    l_sys.t.pencolor(colors[iterations%9])
    l_sys.generate_path(iterations)
    #data.write("iteration:",iterations)
    l_sys.draw_turtle(start_pos, start_angle)
    return 0

    # возле каждого фрактала помечено рекомендуемое число итераций
    # простые фракталы

# ================= ввод данных
fract_list = list(fract_info.keys())
for fract in range(len(fract_list)):
    print(str(fract+1)+'.',fract_list[fract])
print("выберите фрактал и введите его номер")
index = int(input()) - 1 

print("Теперь выберите количество итераций, масштаб и скорость прорисовки")
iterations,f_len,speed = map(int,input().split())
fractal = fract_info['{0}'.format(fract_list[index])]
set_start_pos(fractal,index)
# ================= 
# базовые параметры
width = 1920
height = 1080
screen = turtle.Screen()
screen.setup(width, height, 0, 0)
t = turtle.Turtle()
t.ht()
# ================= основное тело
sleep = 5
Do_Fract(iterations,speed,f_len,*(fractal.values()))
#t.penup()
#t.goto(0,0)
#t.dot(10)
# ================= не закрывает окно
turtle.done()
data.close()
# key_re = re.sub(r"([a-z]+)([, ]*)", lambda m: r"([-+]?\b\d+(?:\.\d+)?\b)" + m.group(2), key_re)
