import pygame
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtMultimedia
import sys
import requests

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
        vbox = QVBoxLayout()   # создаю лейауты
        hbox2 = QHBoxLayout()
        
        menubar = self.menuBar()
        filemenu = menubar.addMenu('Меню')   # создаю меню
        filemenu.addAction(self.Coords())
        filemenu.addAction(self.Size())
        filemenu.addAction(self.exitAction())
        
        centralWidget = QWidget()
        centralWidget.setLayout(vbox)
        self.setCentralWidget(centralWidget)
        
        self.show()

    def Coords(self):                             #создаю вкладки для Меню
        fileAc = QAction('Задать координаты',self)
        fileAc.setShortcut('Q')
        fileAc.triggered.connect(self.new_Coords)
        return fileAc

    def Size(self):
        infoAc = QAction('Задати масштаб',self)
        infoAc.setShortcut('W')
        infoAc.triggered.connect(self.new_Size)
        return infoAc

    def exitAction(self):
        exitAc = QAction('Выход',self)
        exitAc.setShortcut('R')
        exitAc.triggered.connect(self.Exit)
        return exitAc
    def Exit(self): #Закрытие програмы
        Sys.exit()

    def new_Coords(self):                                                   #Функция ищущая песню в БД и добавляющая найденную песни в плейлист
        p, ok_pressed = QInputDialog.getText(self, "Координаты", 
                                                "Введите координаты ")

        if ok_pressed:
            mp.lat = p.split(' ')[0]
            mp.lon = p.split(' ')[1]
     

    def new_Size(self):                                                   #Функция ищущая песню в БД и добавляющая найденную песни в плейлист
        p, ok_pressed = QInputDialog.getText(self, "Масштаб", 
                                                "Введите Масштаб")

        if ok_pressed:
            mp.zoom = int(p)
        

def ll(x, y):
    return "{0},{1}".format(x, y)

pygame.init()
pygame.event.set_blocked(None)
pygame.event.set_allowed((pygame.QUIT, pygame.KEYDOWN))
pygame.event.clear()
size = w,h = 600, 450
screen = pygame.display.set_mode(size)
screen.fill(-1)



class MapParams(object):
    def __init__(self):
        self.lat = 55.729738  # Координаты центра карты на старте.
        self.lon = 37.664777
        self.zoom = 15  # Масштаб карты на старте.
        self.type = "map"  # Тип карты на старте.


    def ll(self):
        return ll(self.lon, self.lat)

def load_map(mp):
    map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&l=map".format(ll=mp.ll(),
                                                                                    z=mp.zoom)
                                                                                    #type=mp.type
    #if mp.search_result:
       # map_request += "&pt={0},{1},pm2grm".format(mp.search_result.point[0],
                          #                         mp.search_result.point[1])

    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запишем полученное изображение в файл.
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)

    return map_file

mp = MapParams()
running = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        map_file = load_map(mp)

        screen.blit(pygame.image.load(map_file), (0, 0))

        pygame.display.flip()
    sys.exit(app.exec_())
