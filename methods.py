import json
from sympy import *
import csv

class Newtons:
    def __init__(self):
        with open('config.json') as f:
            config = json.load(f)

        self.func_str = config['f(x)']
        if config['Iteration'] == 0:
            self.xi = config['xi']
        else:
            self.xi = config['xi+1']
        self.eps = config['Eps']
        self.Rest = config['Rest']
        self.Method = config['Method']
        self.criteria = config['Stop_Criteria']
        self.number_iteration = config['Number of Iteration']
        self.iteration = config['Iteration']

        x = symbols('x')
        self.func_expr = sympify(self.func_str)
        self.f_val = self.func_expr.subs('x', self.xi).evalf()
        self.f_prime = self.find_derivative(self.func_expr)
        self.f_sec_prime = self.find_derivative(self.f_prime)
        self.tangent = self.find_tanget()

    def find_derivative(self, func_expr):
        x = symbols('x')  
        func_prime = diff(func_expr, x)
        return func_prime
    
    def find_tanget(self):
        x = symbols('x')  
        tanget = self.f_prime.subs('x', self.xi).evalf()*(x-self.xi)+ self.func_expr.subs('x', self.xi).evalf()
        return tanget
    
    def Iteration(self):
        if not self.criteria:
            x = self.xi
            f_prime_val = self.f_prime.subs('x', x).evalf()
            self.xi = x - self.f_val / f_prime_val
            if abs(x-self.xi)<self.eps or self.iteration > self.number_iteration:
                self.criteria = True

    def update_config(self):
        with open('config.json', "r") as f:
            config = json.load(f)

        if config['Iteration'] == 0: 
            config['dx'] = str(self.f_prime)
            config['d2x'] = str(self.f_sec_prime)
            config['f(xi)'] = float(self.f_val)
        else:
            config['xi'] = config['xi+1']
            config['f(xi)'] = config['f(xi+1)']

        #config['xi-1'] = config['xi']
        config['xi+1'] = float(self.xi)
        config['tangent'] = str(self.tangent)
        config['f(xi+1)'] = float(self.func_expr.subs('x', self.xi).evalf())
        config['Rest'] = self.Rest
        config['Iteration'] += 1
        config['Stop_Criteria'] = self.criteria

        with open('config.json', "w") as f:
            json.dump(config, f)

        with open('data.csv', 'a', newline='') as csvfile:
            # Create a CSV writer object
            writer = csv.writer(csvfile)

            # Write the data row
            writer.writerow([config['xi'], 0])
            writer.writerow([config['xi'],config['f(xi)']])
            

def root_search():
    methods = {
        "Newtons": Newtons,
    }
    with open('config.json', "r") as f:
        config = json.load(f)

    Num_method = methods[config['Method']]()
    Num_method.Iteration()
    Num_method.update_config()
    
root_search()