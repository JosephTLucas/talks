from dataclasses import dataclass
import numpy as np

def f(x):
    return np.exp(3 * x)

@dataclass
class RemoteConnection:
    path: str = ''
    key: str = ''
    
    def get_data(self, *args, **kwargs):
        x_tr = np.linspace(0., 2, 200)
        y_tr = f(x_tr)
        x = np.array([0, .1, .2, .5, .8, .9, 1])
        y = f(x) + 2 * np.random.randn(len(x))
        return x_tr, y_tr, x, y
    
def save_to_s3(path='', obj=''):
    return True