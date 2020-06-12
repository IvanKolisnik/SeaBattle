__author__ = 'Ivan_Kolisnik'

class Ship():
    '''
Клас Ship - реалізація поведінки об'єкта корабель для гри "Морський бій"
    властивість (вказується при створенні об'єкта): палубна (1 - 4)
    властивість (вказується при створенні об'єкта): розташування (0 - горизонтальне, 1 - вертикальне)
    властивість (вказується при створенні об'єкта): ключова точка (тег в форматі: "столбец_строка")
    властивість: масив зі статусами точок, який формується конструктором
    властивість: масив з координатами точок корабля, який формується конструктором
    властивість: координати точок навколо корабля
    властивість: статус загибелі корабля
    властивість (вказується при створенні об'єкта): префікс тега (для своїх кораблів буде, наприклад, "my", для чужих "nmy"
    метод-конструктор: зміна масиву зі статусами точок, наприклад [0,0,1,0]
    метод: shoot (координати точки), повертає 1 - якщо влучили, 2 - знищили, 0 - мимо
    '''

    # Властивості об'єктів, описані в класі
    # довжина
    length = 1
    # Масив зі статусами точок корабля
    status_map = []
    # Масив з координатами точок корабля
    coord_map = []
    # Точки навколо корабля
    around_map = []
    # Статус загибелі корабля
    death = 0
    # Префікс тега
    prefix = ""
    # Властивість: корабель був створений і не виходить за рамки поля
    ship_correct = 1

    # Метод-конструктор
    def __init__(self,length,rasp,keypoint):
        self.status_map = []
        self.around_map = []
        self.coord_map = []
        self.death = 0
        self.ship_correct = 1
        self.length = length
        #Перевизначити змінну self.prefix
        self.prefix = keypoint.split("_")[0]
        # Створити масиви status_map і coord_map (в залежності від напрямку)
        stroka = int(keypoint.split("_")[1])
        stolb = int(keypoint.split("_")[2])
        for i in range(length):
            self.status_map.append(0)
            # В залежності від напрямку генерувати нові точки корабля
            # 0 - горизонт (збільшувати стовпець), 1 - вертикаль (збільшувати рядок)
            if stolb + i > 9 or stroka + i > 9:
                self.ship_correct = 0
            if rasp == 0:
                self.coord_map.append(self.prefix+"_"+str(stroka)+"_"+str(stolb+i))
            else:
                self.coord_map.append(self.prefix+"_"+str(stroka+i)+"_"+str(stolb))
        for point in self.coord_map:
            ti = int(point.split("_")[1])
            tj = int(point.split("_")[2])
            for ri in range(ti-1,ti+2):
                for rj in range(tj-1,tj+2):
                    if ri>=0 and ri<=9 and rj>=0 and rj<=9:
                        if not(self.prefix+"_"+str(ri)+"_"+str(rj) in self.around_map) and not(self.prefix+"_"+str(ri)+"_"+str(rj) in self.coord_map):
                            self.around_map.append(self.prefix+"_"+str(ri)+"_"+str(rj))

    # постріл
    def shoot(self,shootpoint):
        #визначити номер точки і змінити її статус
        status = 0
        for point in range(len(self.coord_map)):
            if self.coord_map[point] == shootpoint:
                self.status_map[point] = 1
                status = 1
                break
        if not(0 in self.status_map):
            status = 2
            self.death = 1
        return status
