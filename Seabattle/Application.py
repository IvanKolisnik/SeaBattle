__author__ = 'Ivan_Kolisnik'

from random import randrange
from time import time
from tkinter import *
from Ship import *
from tkinter.messagebox import *
import _thread

class Application(Frame):
    '''
    Додаток. Успадковує клас Frame. Створення вікна, полотна і всіх функцій для реалізації програми
    '''
    # Ширина робочого поля
    width = 800
    # Висота робочого поля
    height = 400
    # Колір фону полотна
    bg = "white"
    # Відступ між осередками
    indent = 2
    # Розмір однієї зі сторін квадратної комірки
    gauge = 32
    # Зміщення по y (відступ зверху)
    offset_y = 40
    # Зміщення по x призначеного для користувача поля
    offset_x_user = 30
    # Зміщення по x поля комп'ютера
    offset_x_comp = 430
    # Час генерації флоту
    fleet_time = 0
    # Комп'ютерний флот
    fleet_comp = []
    # Наш флот
    fleet_user = []
    # Масив точок, в які стріляв комп'ютер
    comp_shoot = []

   #Додавання полотна на вікно
    def createCanvas(self):
        self.canv = Canvas(self)
        self.canv["height"] = self.height
        self.canv["width"] = self.width
        self.canv["bg"] = self.bg
        self.canv.pack()
        #клик по холсту вызывает функцию play
        self.canv.bind("<Button-1>",self.userPlay)

    def new_game(self):
        self.canv.delete('all')
        # Додавання ігрових полів користувача і комп'ютера
        # Створення поля для користувача
        # Перебір рядків
        for i in range(10):
            # Перебір стовпців
            for j in range(10):
                xn = j*self.gauge + (j+1)*self.indent + self.offset_x_user
                xk = xn + self.gauge
                yn = i*self.gauge + (i+1)*self.indent + self.offset_y
                yk = yn + self.gauge
                # Додавання прямокутника на полотно з тегом в форматі:
                # префікс_рядок_стовпчик
                self.canv.create_rectangle(xn,yn,xk,yk,tag = "my_"+str(i)+"_"+str(j))

        # Створення поля для комп'ютера
        # Перебір рядків
        for i in range(10):
            #перебор столбцов
            for j in range(10):
                xn = j*self.gauge + (j+1)*self.indent + self.offset_x_comp
                xk = xn + self.gauge
                yn = i*self.gauge + (i+1)*self.indent + self.offset_y
                yk = yn + self.gauge
                # Додавання прямокутника на полотно з тегом в форматі:
                # префікс_рядок_стовпчик
                self.canv.create_rectangle(xn,yn,xk,yk,tag = "nmy_"+str(i)+"_"+str(j),fill="gray")

        # Додавання букв і цифр
        for i in reversed(range(10)):
            # Цифри користувача
            xc = self.offset_x_user - 15
            yc = i*self.gauge + (i+1)*self.indent + self.offset_y + round(self.gauge/2)
            self.canv.create_text(xc,yc,text=str(i+1))
            # Цифри комп'ютера
            xc = self.offset_x_comp - 15
            yc = i*self.gauge + (i+1)*self.indent + self.offset_y + round(self.gauge/2)
            self.canv.create_text(xc,yc,text=str(i+1))
        # букви
        symbols = "АБВГДЕЖЗИК"
        for i in range(10):
            
            # Букви користувача
            xc = i*self.gauge + (i+1)*self.indent + self.offset_x_user + round(self.gauge/2)
            yc = self.offset_y - 15
            self.canv.create_text(xc,yc,text=symbols[i])

            # Букви комп'ютера
            xc = i*self.gauge + (i+1)*self.indent + self.offset_x_comp + round(self.gauge/2)
            yc = self.offset_y - 15
            self.canv.create_text(xc,yc,text=symbols[i])

        self.fleet_time = time()

       # Генерація кораблів противника
        _thread.start_new_thread(self.createShips,("nmy",))
        # self.createShips("nmy")
        # Генерація своїх кораблів
        self.createShips("my")

    def createShips(self, prefix):
        # Функція генерації кораблів на поле
        # Кількість згенерованих кораблів
        count_ships = 0
        while count_ships < 10:
            # Масив зайнятих кораблями точок
            fleet_array = []
            # Обнулити кількість кораблів
            count_ships = 0
            # Масив з флотом
            fleet_ships = []
            # Генерація кораблів (length - палубність корабля)
            for length in reversed(range(1,5)):
                # Генерація необхідної кількості кораблів необхідної довжини
                for i in range(5-length):
                    # Генерація точки з випадковими координатами, поки туди не встановиться корабель
                    try_create_ship = 0
                    while 1:
                        try_create_ship += 1
                        # Якщо кількість спроб перевищило 50, почати все заново
                        if try_create_ship > 50:
                            break
                        # Генерація точки з випадковими координатами
                        ship_point = prefix+"_"+str(randrange(10))+"_"+str(randrange(10))
                        # Випадкове розташування корабля (або горизонтальне, або вертикальне)
                        orientation = randrange(2)
                        # Створити екземпляр класу Ship
                        new_ship = Ship(length,orientation,ship_point)
                        # Якщо корабель може бути поставлений коректно і його точки не перетинаються з вже зайнятими точками поля
                        # Перетин безлічі зайнятих точок поля і точок корабля:
                        intersect_array = list(set(fleet_array) & set(new_ship.around_map+new_ship.coord_map))
                        if new_ship.ship_correct == 1 and len(intersect_array) == 0:
                            # Додати в масив з усіма зайнятими точками точки навколо корабля і точки самого корабля
                            fleet_array += new_ship.around_map + new_ship.coord_map
                            fleet_ships.append(new_ship)
                            count_ships += 1
                            break
        print(prefix,time() - self.fleet_time,"секунд")
        # Сортування кораблів
        if prefix == "nmy":
            self.fleet_comp = fleet_ships
        else:
            self.fleet_user = fleet_ships
            self.paintShips(fleet_ships)

    #метод для отрисовки кораблій
    def paintShips(self,fleet_ships):
        #отрисовка кораблій
        for obj in fleet_ships:
            for point in obj.coord_map:
                self.canv.itemconfig(point,fill="gray")

    # Метод малювання в осередку хреста на білому тлі
    def paintCross(self,xn,yn,tag):
        xk = xn + self.gauge
        yk = yn + self.gauge
        self.canv.itemconfig(tag,fill="white")
        self.canv.create_line(xn+2,yn+2,xk-2,yk-2,width="3")
        self.canv.create_line(xk-2,yn+2,xn+2,yk-2,width="3")

    # Метод малювання промаху
    def paintMiss(self,point):
       # Знайти координати
        new_str = int(point.split("_")[1])
        new_stlb = int(point.split("_")[2])
        if point.split("_")[0] == "nmy":
            xn = new_stlb*self.gauge + (new_stlb+1)*self.indent + self.offset_x_comp
        else:
            xn = new_stlb*self.gauge + (new_stlb+1)*self.indent + self.offset_x_user
        yn = new_str*self.gauge + (new_str+1)*self.indent + self.offset_y
        # Додати прямокутник
        # Пофарбувати в білий
        self.canv.itemconfig(point,fill="white")
        self.canv.create_oval(xn+13,yn+13,xn+17,yn+17,fill="gray")

    # Метод перевірки фінішу
    def checkFinish(self,type):
        '''type - вказівка, від чийого імені йде звернення'''
        status = 0
        if type == "user":
            for ship in self.fleet_comp:
                status += ship.death
        else:
            for ship in self.fleet_user:
                status += ship.death
        return status

    # Метод гри комп'ютера
    # Параметр step - крок, з яким відбувається постріл,
    # Якщо він 0 - значить постріл є першим після промаху
    # Якщо 1 - значить треба стріляти поруч з останнім пострілом
    def compPlay(self,step = 0):
        print(step)
        # Якщо step = 0, то генерувати випадкові точки
        if step == 0:
            # Генерувати випадкові точки, поки не буде знайдена пара, якої не було в списку пострілв
            while 1:
                i = randrange(10)
                j = randrange(10)
                if not("my_"+str(i)+"_"+str(j) in self.comp_shoot):
                    break
        else:
            # Взяти передостанню точку, вибрати будь-яку точку навколо (по горизонталі або вертикалі)
            # Масив точок навколо
            points_around = []
            i = int(self.comp_shoot[-1].split("_")[1])
            j = int(self.comp_shoot[-1].split("_")[2])
            for ti in range(i-1,i+2):
                for tj in range(j-1,j+2):
                    if ti>=0 and ti<=9 and tj>=0 and tj<=9 and ti != tj and (ti == i or tj == j) and not(ti == i and tj == j) and not("my_"+str(ti)+"_"+str(tj) in self.comp_shoot):
                        points_around.append([ti,tj])
            
            # Cлучайное точка з масиву
            select = randrange(len(points_around))
            i = points_around[select][0]
            j = points_around[select][1]
        xn = j*self.gauge + (j+1)*self.indent + self.offset_x_user
        yn = i*self.gauge + (i+1)*self.indent + self.offset_y
        hit_status = 0
        for obj in self.fleet_user:
            # Якщо координати точки збігаються з координатою корабля, то викликати метод пострілу
            if "my_"+str(i)+"_"+str(j) in obj.coord_map:
                # Змінити статус попадання
                hit_status = 1
                # Ми влучили, тому треба намалювати хрест
                self.paintCross(xn,yn,"my_"+str(i)+"_"+str(j))
                # Додати точку в список пострілів комп'ютера
                self.comp_shoot.append("my_"+str(i)+"_"+str(j))
                # Якщо метод повернув двійку, значить, корабель знищений
                if obj.shoot("my_"+str(i)+"_"+str(j)) == 2:
                    hit_status = 2
                    # Змінити статус корабля
                    obj.death = 1
                    # Всі поля навколо корабля зробити точками, в які ми вже стріляли
                    for point in obj.around_map:
                        # Намалювати промахи
                        self.paintMiss(point)
                        # Додати точки навколо корабля в список пострілів комп'ютера
                        self.comp_shoot.append(point)
                break
        # Якщо статус попадання залишився рівним нулю - значить, ми промахнулися, передати управління комп'ютеру
        # Інакше дати користувачеві стріляти
        print("hit_status",hit_status)
        if hit_status == 0:
            #додати точку в список пострілів
            self.comp_shoot.append("my_"+str(i)+"_"+str(j))
            self.paintMiss("my_"+str(i)+"_"+str(j))
        else:
            # Перевірити виграш, якщо його немає - передати управління комп'ютеру
            if self.checkFinish("comp") < 10:
                if hit_status == 1:
                    step += 1
                    if step > 4:
                        self.compPlay()
                    else:
                        self.compPlay(step)
                else:
                    self.compPlay()
            else:
                showinfo("Морський бій", "Ви програли!")

    # Метод для гри користувача
    def userPlay(self,e):
        for i in range(10):
            for j in range(10):
                xn = j*self.gauge + (j+1)*self.indent + self.offset_x_comp
                yn = i*self.gauge + (i+1)*self.indent + self.offset_y
                xk = xn + self.gauge
                yk = yn + self.gauge
                if e.x >= xn and e.x <= xk and e.y >= yn and e.y <= yk:
                    # Перевірити чи потрапили ми в корабель
                    hit_status = 0
                    for obj in self.fleet_comp:
                        #якщо координати точки збігаються з координатою корабля, то викликати метод пострілу
                        if "nmy_"+str(i)+"_"+str(j) in obj.coord_map:
                            # Змінити статус попадання
                            hit_status = 1
                            # Ми влучили, тому треба намалювати хрест
                            self.paintCross(xn,yn,"nmy_"+str(i)+"_"+str(j))
                            #якщо метод повернув двійку, значить, корабель знищений
                            if obj.shoot("nmy_"+str(i)+"_"+str(j)) == 2:
                                # Змінити статус корабля
                                obj.death = 1
                                #всі поля навколо корабля зробити точками, в які ми вже стріляли
                                for point in obj.around_map:
                                    #намалювати промахи
                                    self.paintMiss(point)
                            break
                    #якщо статус попадання залишився рівним нулю - значить, ми промахнулися, передати управління комп'ютеру
                    # Інакше дати користувачеві стріляти
                    if hit_status == 0:
                        self.paintMiss("nmy_"+str(i)+"_"+str(j))
                        #перевірити виграш, якщо його немає - передати управління комп'ютера
                        if self.checkFinish("user") < 10:
                            self.compPlay()
                        else:
                            showinfo("Морський бій", "Вы виграли!")
                    break

    def __init__(self, master=None):
        #ініціалізація вікна
        Frame.__init__(self, master)
        self.pack()

        #ініціалізація меню
        self.m = Menu(master)
        master.config(menu = self.m)
        self.m_play = Menu(self.m)
        self.m.add_cascade(label = "Гра",menu = self.m_play)
        self.m_play.add_command(label="Почати нову гру", command = self.new_game)
        #виклик функції створення полотна
        self.createCanvas()
