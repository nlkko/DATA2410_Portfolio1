import inspect

def foo(hei, hei2):
    print("Hei:")

argins = len(inspect.getfullargspec(foo).args)
x = lambda argins: argins if argins == 0 else "Større enn 0"
print(argins)