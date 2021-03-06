import os
import sys
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import Qt

SCREEN_SIZE = [900, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.x, self.y = 37.530887, 55.703118
        self.m, self.n = 0.002, 0.002
        self.style_map = 'map'
        self.getImage()
        self.initUI()


    def getImage(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.x},{self.y}&spn={self.m},{self.n}&l={self.style_map}"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        return response.content

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setFixedSize(900, 450)
        self.setWindowTitle('Отображение карты')

        #########
        self.chg_map = QPushButton(f'Сменить стиль: Схема', self)
        self.chg_map.move(620, 15)
        self.chg_map.resize(260, 50)
        self.chg_map.setFocusPolicy(Qt.NoFocus)
        self.chg_map.clicked.connect(self.change_style_map)
        #########

        ## Изображение
        self.pixmap = QPixmap()
        self.pixmap.loadFromData(self.getImage())
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def change_style_map(self):
        if self.style_map == 'map':
            self.style_map = 'sat'
            self.chg_map.setText('Сменить стиль: Спутник')
        elif self.style_map == 'sat':
            self.chg_map.setText('Сменить стиль: Гибрид')
            self.style_map = 'sat,skl'
        else:
            self.chg_map.setText('Сменить стиль: Схема')
            self.style_map = 'map'
        self.update_map()


    def update_map(self):
        self.pixmap.loadFromData(self.getImage())
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_PageUp:
            self.m /= 2
            self.n /= 2
            self.n = max(self.n, 0.0005)
            self.m = max(self.m, 0.0005)
            self.update_map()

        elif event.key() == Qt.Key_PageDown:
            self.m *= 2
            self.n *= 2
            self.m = min(self.m, 65.536)
            self.n = min(self.n, 65.536)
            self.update_map()

        elif event.key() == Qt.Key_Up:
            self.y += self.n
            self.update_map()

        elif event.key() == Qt.Key_Down:
            self.y -= self.n
            self.update_map()

        elif event.key() == Qt.Key_Left:
            self.x -= self.n
            self.update_map()

        elif event.key() == Qt.Key_Right:
            self.x += self.n
            self.update_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
