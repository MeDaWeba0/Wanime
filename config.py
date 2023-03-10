import sys, os, platform, time
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QIcon, QPixmap

# Variables globales

dirG = os.getcwd()

if platform.system() == "Windows":
    br = "\\"
else:
    br = "/"

dirUI = dirG + br + "bin" + br + "gui" + br + "config.ui"
dirIco = dirG + br + "bin" + br + "icon.png"

class ClGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(dirUI, self)
        self.fondo_inicio()
        self.select_background()
        self.fondo.currentTextChanged.connect(self.select_background)
        self.guardar.clicked.connect(self.guardarfn)

    def guardarfn(self):
        todo = (self.nombre.text().replace("\n","")).upper()+";;"+(self.link.text().replace("\n","")).upper()+";;"+ (self.dia.currentText().replace("\n","")).upper()
        todo = todo.replace("\n","")
        dirU = dirG + br + "bin" + br + "local_saves" + br + "animes.sv"
        try:
            f = open(dirU, "a", encoding="utf-8")
        except:
            f = open(dirU, "w", encoding="utf-8")
        f2 = open(dirU, "r", encoding="utf-8")
        dataNOW = f2.read()
        if dataNOW.replace("\n","").replace(" ","") == "":
            f.write(todo)
        else:
            f.write("/*/"+todo)
        f.close()

    def fondo_inicio(self):
        dirU = dirG + br + "bin" + br + "local_saves" + br + "background_select.sv"
        try:
            f = open(dirU, "r")
            dataU = f.read()
            f.close()
            boolneed = True
        except:
            boolneed = False
        if boolneed == True:
            new_item = dataU
            current_index = self.fondo.currentIndex()
            current_item = self.fondo.itemText(current_index)
                
            if new_item != current_item:
                new_index = self.fondo.findText(new_item)
                    
                if new_index != -1:
                    self.fondo.setCurrentIndex(new_index)
                else:
                    self.fondo.addItem(new_item)
                    self.fondo.setCurrentIndex(self.fondo.count() - 1)

    def select_background(self):
        def save_background(dirU,data):
            f = open(dirU, "w", encoding="utf-8")
            f.write(data)
            f.close()
        def obtn(ruta_carpeta):
            # Obtener la lista de archivos en la carpeta
            lista_archivos = os.listdir(ruta_carpeta)

            # Filtrar solo los archivos con extensiones .jpeg, .png o .jpg
            lista_archivos_filtrados = [archivo for archivo in lista_archivos if archivo.endswith(('.jpeg', '.png', '.jpg'))]

            # Devolver la lista de archivos filtrados
            return lista_archivos_filtrados

        lista = obtn(dirG + br + "bin" + br + "background")
        # Obtener los elementos actuales de la QComboBox
        current_items = [self.fondo.itemText(i) for i in range(self.fondo.count())]
        # Agregar los elementos que no estén presentes en la QComboBox
        for item in set(lista):
            if item not in current_items:
                self.fondo.addItem(item)
        # Cargar la imagen y establecerla como fondo
        dirU = dirG + br + "bin" + br + "local_saves" + br + "background_select.sv"
        if self.fondo.currentText() != "Sin fondo" and self.fondo.currentText() != None:
            dirBK = dirG + br + "bin" + br + "background" + br + self.fondo.currentText()
            save_background(dirU,str(self.fondo.currentText()))
            pixmap = QPixmap(dirBK)
            self.imagen_de_fondo.setPixmap(pixmap)
            self.imagen_de_fondo.setScaledContents(True)  # Escalar la imagen para que se ajuste al tamaño del widget
            self.setStyleSheet("background-color: none;")  # Establecer el color de fondo como transparente
        else:
            save_background(dirU,str(self.fondo.currentText()))
            pixmap = QPixmap(1, 1)
            pixmap.fill(Qt.transparent)
            self.imagen_de_fondo.setPixmap(pixmap)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = ClGUI()
    GUI.setWindowTitle("Wamine")
    GUI.setWindowIcon(QIcon(dirIco))
    GUI.show()
    sys.exit(app.exec_())
