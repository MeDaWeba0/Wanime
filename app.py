import sys, os, platform, datetime, webbrowser
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

dirUI = dirG + br + "bin" + br + "gui" + br + "gui.ui"
dirIco = dirG + br + "bin" + br + "icon.png"


def diaD():
    fecha_actual = datetime.date.today()
    dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    dia_semana = dias_semana[fecha_actual.weekday()]
    return dia_semana.capitalize()


class ClGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(dirUI, self)
        self.fondo_inicio()
        self.select_background()
        self.cargar()
        self.fondo.currentTextChanged.connect(self.select_background)
        self.ir.clicked.connect(self.irfn)
        self.eliminar.clicked.connect(self.eliminarfn)
    
    def comprobar_data(self,data: str) -> bool:
        if "/*/" in data:
            return True
        else:
            return False

    def buscar_elementoN(self,search, listaU):
        for i, elemento in enumerate(listaU):
            if search in elemento:
                return i
        return None

    
    def buscar_elemento(self,search, listaU):
        for elemento in listaU:
            if search in elemento:
                return elemento
        return None
   

    def fondo_inicio(self):
        dirU = dirG + br + "bin" + br + "local_saves" + br + "background_select.sv"
        try:
            f = open(dirU, "r", encoding="utf-8")
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

    def irfn(self):
        dirU = dirG + br + "bin" + br + "local_saves" + br + "animes.sv"
        f = open(dirU, "r", encoding="utf-8")
        data = f.read()
        if self.comprobar_data(data) == True:
            data = data.split("/*/")
            search = self.anime_seleccionado.currentText()
            dataU = self.buscar_elemento(search,data)
            data = dataU
        f.close()
        dataU = str(data).split(";;")
        link = str(dataU[1]).lower()
        webbrowser.open(link)

    def eliminarfn(self):
        def chapuza(cadena):
            if cadena.endswith("/*/"):
                cadena = cadena[:-3]
            return cadena

        dirU = dirG + br + "bin" + br + "local_saves" + br + "animes.sv"
        def eliminar(dirU, wdata):
            f = open(dirU, "r", encoding="utf-8")
            data = f.read()
            f.close()

            data = data.split("/*/")

            numR = self.buscar_elementoN(self.anime_seleccionado.currentText(),data)
            Nl = int(len(data)) -1 ; i = -1 ; todo = ''

            while Nl != i:
                i += 1
                if i != numR:
                    todo += data[i]
                    if Nl != i:
                        todo += "/*/"
            f = open(dirU, "w", encoding="utf-8")
            f.write(chapuza(todo))
            f.close()
        eliminar(dirU,str(self.anime_seleccionado.currentText()))
        index = self.anime_seleccionado.findText(self.anime_seleccionado.currentText())
        if index >= 0:
            self.anime_seleccionado.removeItem(index)
        self.cargar()




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

    def cargar(self):
        dirU = dirG + br + "bin" + br + "local_saves" + br + "animes.sv" ; todo = [] ; todo2 = ''
        dia = diaD()   

        try:
            f = open(dirU, "r", encoding="utf-8")
            data = f.read()
            f.close()
            if (data.replace(" ","")).replace("\n","") != "":
                boolneed = True
            else:
                boolneed = False
        except:
            boolneed = False
        if boolneed == True:
            if self.comprobar_data(data) == True:
                data = data.split("/*/")
                Nl = int(len(data)) - 1 ; i = -1
                while Nl != i:
                    i += 1
                    a = data[i]
                    b = str(a.split(";;")[2]) 
                    if b == diaD().upper():
                        c = str(a.split(";;")[0])
                        todo.append(c) ; todo2 += c + "\n"
            else:
                a = str(data.split(";;")[2])
                if a == diaD().upper():
                    b = str(data.split(";;")[0])
                    todo.append(b) ; todo2 = b
        self.animess.setPlainText(todo2)
        self.anime_seleccionado.clear()
        self.anime_seleccionado.addItems(set(todo))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = ClGUI()
    GUI.setWindowTitle("Wamine")
    GUI.setWindowIcon(QIcon(dirIco))
    GUI.show()
    sys.exit(app.exec_())
