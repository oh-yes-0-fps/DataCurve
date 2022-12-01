from Main import curveKey, curveMath, dataCurve, interpMode, tangent
import matplotlib.pyplot as plt
import random

# RAND_LIST = [1.38, 0.28, 5.96, 5.38, 6.57, 2.51, 6.0, 1.89, 6.61, 5.91, 8.92]


def graph(curve, _min: float, _max: float, _step: float):
    x = []
    y = []
    for i in range(int(_min), int(_max), int(_step)):
        x.append(i)
        value = curve.eval(i)
        # print(f"{i} : {value}")
        y.append(value)
    plt.plot(x, y)
    plt.show()


def generateRandomCurve(length: int, step: int) -> list[curveKey]:
    _keys = []
    for i in range(0, length, step):
        value = random.randint(1, 1000)/100
        # value = RAND_LIST[int(i/10)]
        _keys.append(curveKey(i, value, interpMode.CUBIC))
    return _keys


if __name__ == '__main__':
    curve = dataCurve()
    curve.addKeys(*generateRandomCurve(100, 10))
    curve.finalize()
    graph(curve, 0, 100, 1)
