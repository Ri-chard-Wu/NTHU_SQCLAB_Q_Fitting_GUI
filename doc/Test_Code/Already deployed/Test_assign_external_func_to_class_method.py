

def func():
    print("test")

class PM():
    def __init__(self):
        self.func = func
        #self.func()

pm = PM()
