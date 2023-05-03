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
data_list = []
class SystemL:
    
    def __init__(self, t, axiom, width, length, angle,iterations):
        self.iterations = iterations
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

    def add_rules(self, rules):  # на вход подавать кортеж содержащий кортежи-правила
        for rule in rules:
            self.rules[rule[0]] = rule[1]

    def generate_path(self, iter):
        for n in range(iter):
            # self.length = self.length / iter
            for key, value in self.rules.items():
                # заменяем F на правило, при этом понижаем регистр, чтобы при большом количестве правил они не наслаивались
                self.state = self.state.replace(key, value.lower())

            self.state = self.state.upper()

    def draw_turtle(self, start_pos, start_angle):
        podlist = []
        # границы
        # устанавливаем скоростной режим черепашки
        self.t.up()
        self.t.setpos(start_pos)
        self.t.seth(start_angle)
        self.t.down()
        podlist.append(self.t.pos())
        turtle_stack = []
        for part in self.state:
            if part == 'F':
                self.t.forward(self.length)
                #self.t.dot(10)
                podlist.append(self.t.pos())
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

        data_list.append(podlist)

def analizys():
    '''
    for i in range(len(data_list)):
        print("iteration = ", i+1)
        print(data_list[i])
        print()
    '''
    for i in range(len(data_list)):
        xd,yd = 0,0
        count = 0
        for x,y in data_list[i]:
            xd+=x
            yd+=y
            count+=1
        xd/=count
        yd/=count
        print("центр фрактала = ",xd,yd)
    return (xd,yd)


@Repeater()
def Do_Fract(iterations, speed, f_len, angle, axiom, rules, start_pos=(0, 0), start_angle=0,pen_width = 1):
    #time.sleep(sleep)
    turtle.tracer(speed, 0)
    l_sys = SystemL(t, axiom, pen_width, f_len, angle,iterations)
    l_sys.add_rules(rules)
    l_sys.t.pencolor(colors[iterations%9])
    l_sys.generate_path(iterations)
    data.write("iteration:"+str(iterations))
    l_sys.draw_turtle(start_pos, start_angle)
    centre = analizys()
    l_sys.t.penup()
    l_sys.t.goto(*centre)
    l_sys.t.dot(5,'red')

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
# ================= 
# базовые параметры
width = 1920
height = 1080
screen = turtle.Screen()
screen.setup(width, height, 0, 0)
t = turtle.Turtle()
t.ht()

# ================= основное тело
fractal = fract_info['{0}'.format(fract_list[index])]
#print(fractal)
#print(*fractal)
#print(*fractal.values())

sleep = 5

Do_Fract(iterations,speed,f_len,*fractal.values())

# ================= не закрывает окно
turtle.done()

data.close()
# key_re = re.sub(r"([a-z]+)([, ]*)", lambda m: r"([-+]?\b\d+(?:\.\d+)?\b)" + m.group(2), key_re)
