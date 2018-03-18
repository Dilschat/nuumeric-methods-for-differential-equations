import random
import sys
import numeric_methods as methods

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
    QPushButton, QPlainTextEdit
from PyQt5.QtGui import QIcon

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class UI(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setMinimumSize(QSize(640, 480))
        self.setWindowTitle('Numeric methods')
        self.button1 = QPushButton('Euler method', self, )
        self.button2 = QPushButton('Improved Euler method', self)
        self.button3 = QPushButton('Runge-Kutta method', self)
        self.button4 = QPushButton('Exit', self)
        self.button5 = QPushButton('Real solution', self)
        self.button1.move(50, 50)
        self.button2.move(50, 80)
        self.button2.resize(200, 32)
        self.button3.move(50, 110)
        self.button3.resize(200, 32)
        self.button4.move(50, 170)
        self.button5.resize(200, 32)
        self.button5.move(50, 140)
        self.text_area = QPlainTextEdit(self)
        self.text_area.resize(100, 50)
        self.text_area.move(300, 50)
        self.text_area.insertPlainText('Print size of step here')


class methods_UI(QMainWindow):
    def __init__(self, title, graph, error_graph):
        super().__init__()
        self.left = 10
        self.top = 10
        self.title = title
        self.width = 1000
        self.height = 600
        self.graph = graph
        self.error_graph = error_graph

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        m = PlotCanvas(self, width=5, height=4)
        m.plot(self.graph,self.title+' method')
        m.move(0, 0)
        error_canvas = PlotCanvas(self, width=5, height=4)
        error_canvas.plot(self.error_graph, self.title+' method error')
        error_canvas.move(500, 0)
        self.show()


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        # FigureCanvas.setSizePolicy(self,
        #                            QSizePolicy.Expanding,
        #                            QSizePolicy.Expanding)
        # FigureCanvas.updateGeometry(self)

        print('sf')
        FigureCanvas.updateGeometry(self)


    def plot(self,solution,title):
        main_plot = self.figure.add_subplot(111)
        main_plot.plot(solution[0], solution[1])
        main_plot.set_title(title)
        self.draw()

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWidget = UI()
    solver = methods.Solver(-1, 4, 1)
    euler_solution = solver.euler_method(0.01)
    euler_error = solver.calculate_error(euler_solution[0], euler_solution[1])
    improved_euler_solution = solver.improved_euler_method(0.01)
    improved_euler_error = solver.calculate_error(improved_euler_solution[0], improved_euler_solution[1])
    runge_kutta_solution = solver.improved_euler_method(0.01)
    runge_kutta_error = solver.calculate_error(runge_kutta_solution[0], runge_kutta_solution[1])
    real_solution = solver.real_solution()
    euler_ui = methods_UI('Euler', euler_solution, euler_error)
    improved_euler_ui = methods_UI('Improved Euler', improved_euler_solution, improved_euler_error)
    runge_kutta_ui = methods_UI('Runge-kutta', euler_solution, euler_error)
    real_solution_ui = methods_UI('Real solution', real_solution,[[],[]])
    myWidget.button1.clicked.connect(euler_ui.initUI)
    myWidget.button2.clicked.connect(improved_euler_ui.initUI)
    myWidget.button3.clicked.connect(runge_kutta_ui.initUI)
    myWidget.button5.clicked.connect(real_solution_ui.initUI)
    myWidget.button4.clicked.connect(app.exit)
    myWidget.show()
    app.exec_()
