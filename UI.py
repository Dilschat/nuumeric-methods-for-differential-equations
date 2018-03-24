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

START_SEGMENT = -1
END_SEGMENT = 1
Y_START_POINT = 4
STANDARD_STEP = 0.01


class UI(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setMinimumSize(QSize(640, 480))
        self.setWindowTitle('Numeric methods')
        self.button1 = QPushButton('Euler method', self, )
        self.button2 = QPushButton('Improved euler method', self)
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
    def __init__(self, title, main_window):
        super().__init__()
        self.left = 10
        self.top = 10
        self.title = title
        self.width = 1000
        self.height = 600
        self.window = main_window
        self.recalculate_button = QPushButton('Recalculate', self)
        self.text_area = QPlainTextEdit(self)
        self.text_area.move(500, 500)
        self.text_area.insertPlainText('new step value')
        self.recalculate_button.move(800, 500)
        self.recalculate_button.resize(200, 32)
        self.step = STANDARD_STEP
        self.recalculate_button.clicked.connect(self.recalculation)

    def initUI(self):
        text = self.window.text_area.toPlainText()
        if self.is_number(text):
            self.step = float(text)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        m = PlotCanvas(self, width=5, height=4)
        m.plot(self.title + ' method', self.step)
        m.move(0, 0)

        if "Real" not in self.title:
            error_canvas = PlotCanvas(self, width=5, height=4)
            error_canvas.plot_error(self.title + ' method error', m.solution)
            error_canvas.move(500, 0)

        self.show()

    def is_number(self, s):
        try:
            float(s)
            print(s)
            return True
        except ValueError:
            return False

    def recalculation(self):
        self.close()
        self.window = self
        self.initUI()


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.solution = [[], []]
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        # FigureCanvas.setSizePolicy(self,
        #                            QSizePolicy.Expanding,
        #                            QSizePolicy.Expanding)
        # FigureCanvas.updateGeometry(self)

        FigureCanvas.updateGeometry(self)

    def plot(self, title, step):
        solver = methods.Solver(START_SEGMENT, Y_START_POINT, END_SEGMENT)
        real_solution = solver.real_solution()
        if "Euler" in title:
            self.solution = solver.euler_method(step)
        elif "improved" in title:
            self.solution = solver.improved_euler_method(step)
        elif "Runge-kutta" in title:
            self.solution = solver.runge_kutta_method(step)
        elif "Real" in title:
            self.solution = solver.real_solution()
        else:
            raise IOError
        main_plot = self.figure.add_subplot(111)

        main_plot.plot(self.solution[0], self.solution[1], label=title)
        main_plot.plot(real_solution[0], real_solution[1], label='real solution')
        main_plot.legend(loc='upper left')
        main_plot.set_title(title)
        self.draw()

    def plot_error(self, title, solution):
        solver = methods.Solver(START_SEGMENT, Y_START_POINT, END_SEGMENT)
        error = solver.calculate_error(solution[0], solution[1])
        main_plot = self.figure.add_subplot(111)
        main_plot.plot(error[0], error[1])
        main_plot.set_title(title)
        self.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWidget = UI()
    euler_ui = methods_UI('Euler', myWidget)
    improved_euler_ui = methods_UI('Improved Euler', myWidget)
    runge_kutta_ui = methods_UI('Runge-kutta',  myWidget)
    real_solution_ui = methods_UI('Real solution', myWidget)
    myWidget.button1.clicked.connect(euler_ui.initUI)
    myWidget.button2.clicked.connect(improved_euler_ui.initUI)
    myWidget.button3.clicked.connect(runge_kutta_ui.initUI)
    myWidget.button5.clicked.connect(real_solution_ui.initUI)
    myWidget.button4.clicked.connect(app.exit)
    myWidget.show()
    app.exec_()
