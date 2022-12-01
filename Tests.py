from Main import tang_tension, curveKey, curveMath, dataCurve, interpMode, tangent
import matplotlib.pyplot as plt
import random

RAND_LIST = [0.03, 6.6, 1.9, 8.28, 2.44, 0.41, 6.22, 1.43, 2.23, 9.63, 5]

CURVE_DATA = {  # key is distance
    13.0: {'angle': 10.8, 'height': 15},
    25.0: {'angle': 35.1, 'height': 12},
    27.0: {'angle': 49.9, 'height': 8}
}

MODE = interpMode.CUBIC


def graph(curve: dataCurve, name: str, _min: float, _max: float, _step: float):
    x = []
    y = []
    for i in range(int(_min), int(_max), int(_step)):
        x.append(i)
        value = curve.eval(i)
        # print(f"{i} : {value}")
        y.append(value)
    plt.plot(x, y, label=name)


def generateRandomCurve(length: int, step: int) -> list[curveKey]:
    _keys = []
    x = []
    y = []
    for i in range(0, length, step):
        # value = random.randint(1, 1000)/100
        value = RAND_LIST[int(i/100)]
        _keys.append(curveKey(i, value, MODE))
        x.append(i)
        y.append(value)
    plt.scatter(x, y, label='random scatter', color='red')
    return _keys


def generateCurve(field: str, curveDict: dict[float, dict[str, float]]) -> list[curveKey]:
    _keys = []

    for i in curveDict:
        value = curveDict[i][field]
        _keys.append(curveKey(i, value, MODE))

    return _keys


if __name__ == '__main__':
    curve = dataCurve()
    curve.addKeysList(generateRandomCurve(1000, 100))
    curve.finalize(0)
    graph(curve, "Random Curve=", 0, 1000, 1)

    # ang_curve = dataCurve()
    # ang_curve.addKeys(*generateCurve('angle', CURVE_DATA))
    # ang_curve.finalize()
    # graph(ang_curve, 'Angle', 0, 60, 1)

    # hei_curve = dataCurve()
    # hei_curve.addKeys(*generateCurve('height', CURVE_DATA))
    # hei_curve.finalize()
    # graph(hei_curve, 'Height', 0, 60, 1)

    plt.legend()
    plt.show()
