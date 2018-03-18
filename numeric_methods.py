import numpy


class Solver(object):
    def __init__(self, x0, y0, X):
        self.x0 = x0
        self.y0 = y0
        self.X = X

    def real_solution(self):
        x = numpy.linspace(self.x0, self.X, 100)
        y = self.calculate_function(x)
        return [x, y]

    def euler_method(self, h):
        list_of_x = [self.x0]
        list_of_y = [self.y0]
        last_x = list_of_x[-1]
        while last_x + h <= self.X:
            last_x = list_of_x[-1]
            last_y = list_of_y[-1]
            list_of_y.append(last_y + h * self.calculate_derivative(last_x, last_y))
            list_of_x.append(last_x + h)
        return [list_of_x, list_of_y]

    def improved_euler_method(self, h):
        list_of_x = [self.x0]
        list_of_y = [self.y0]
        last_x = list_of_x[-1]
        while last_x + h <= self.X:
            last_x = list_of_x[-1]
            last_y = list_of_y[-1]
            list_of_y.append(last_y +
                             h * self.calculate_derivative(last_x + h / 2, last_y + (h / 2)
                                                           * self.calculate_derivative(last_x, last_y)))
            list_of_x.append(last_x + h)
        return [list_of_x, list_of_y]

    def runge_kutta_method(self, h):
        list_of_x = [self.x0]
        list_of_y = [self.y0]
        last_x = list_of_x[-1]
        while last_x + h <= self.X:
            last_x = list_of_x[-1]
            last_y = list_of_y[-1]
            k1 = self.calculate_derivative(last_x, last_y)
            k2 = self.calculate_derivative(last_x + h / 2, last_y + h * k1 / 2)
            k3 = self.calculate_derivative(last_x + h / 2, last_y + h * k2 / 2)
            k4 = self.calculate_derivative(last_x + h, last_y + h * k3)
            list_of_y.append(last_y + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4))
            list_of_x.append(last_x + h)
        return [list_of_x, list_of_y]

    def calculate_derivative(self, x, y):
        return x * numpy.power(y, 1.5) + x * y

    def calculate_function(self, x):
        return numpy.power(numpy.e, (numpy.power(x, 2) / 2)) / numpy.power((
            1.5 * numpy.power(numpy.e, 1 / 4) - numpy.power(numpy.e, numpy.power(x, 2) / 4)), 2)

    def calculate_error(self, x, y):
        error_y = list()
        error_y = numpy.abs(numpy.subtract(y, self.calculate_function(x)))
        return [x, error_y]
