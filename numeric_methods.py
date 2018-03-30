import numpy


class Solver(object):
    def __init__(self, x0, y0, X):
        self.x0 = x0
        self.y0 = y0
        self.X = X
        self.c = self.calculateConstant(self.x0, self.y0)

    def calculate_real_solution(self):
        """ This function calculates x and y values for exact solution of given diff.equation"""
        x = numpy.linspace(self.x0, self.X, 100)
        y = self.calculate_function(x, self.c)
        return [x, y]

    def calculate_by_euler_method(self, h):
        """ This function calculates approximated solution of given diff. equation using euler method """
        list_of_x = [self.x0]
        list_of_y = [self.y0]
        last_x = list_of_x[-1]
        while last_x + h <= self.X:
            last_x = list_of_x[-1]
            last_y = list_of_y[-1]
            list_of_y.append(last_y + h * self.calculate_derivative(last_x, last_y))
            list_of_x.append(last_x + h)
        return [list_of_x, list_of_y]

    def calculate_by_improved_euler_method(self, h):
        """ This function calculates approximated solution of given diff. equation using improved euler method """
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

    def calculate_by_runge_kutta_method(self, h):
        """ This function calculates approximated solution of given diff. equation using runge-kutta method """
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
        """ Calculates value of derivative for given d.e."""
        return x * numpy.power(y, 1.5) + x * y

    def calculate_function(self, x, c):
        """ Calculates value of exact solution of d.e."""
        return numpy.power(numpy.e, (numpy.power(x, 2) / 2)) / numpy.power((
            c - numpy.power(numpy.e, numpy.power(x, 2) / 4)), 2)

    def calculateConstant(self, x0, y0):
        """ Calculates constant value for solution of d.e."""
        return numpy.power(numpy.e, numpy.power(x0, 2) / 4) + numpy.power(
            numpy.power(numpy.e, numpy.power(x0, 2) / 2) / y0, 0.5)

    def calculate_local_error(self, x, y):
        """ Calculates local trancation error """
        error_y = numpy.abs(numpy.subtract(y, self.calculate_function(x, self.c)))
        return [x, error_y]

    def calculate_global_error(self):
        """ Calculates global trancation error"""
        x = numpy.linspace(0.0001, 0.2, 3000)
        euler_solution = list()
        improved_euler_solution = list()
        runge_kutta_solution = list()
        for i in x:
            euler_solution.append(self.calculate_by_euler_method(i))
            improved_euler_solution.append(self.calculate_by_improved_euler_method(i))
            runge_kutta_solution.append(self.calculate_by_runge_kutta_method(i))
        euler_error = self.calculate_max_local_error(euler_solution)
        improved_euler_error = self.calculate_max_local_error(improved_euler_solution)
        runge_cutta_error = self.calculate_max_local_error(runge_kutta_solution)
        dictionary = {'euler': euler_error, 'improved euler': improved_euler_error, 'runge-kutta': runge_cutta_error}
        return [x, dictionary]

    def calculate_max_local_error(self,solution):
        error = list()
        for i in solution:
            error.append(max((self.calculate_local_error(i[0], i[1]))[1]))
        return error
