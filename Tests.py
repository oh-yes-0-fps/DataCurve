from Main import curveKey, curveMath, dataCurve, interpMode, tangent
import matplotlib.pyplot as plt
import random

# RAND_LIST = [1.38, 0.28, 5.96, 5.38, 6.57, 2.51, 6.0, 1.89, 6.61, 5.91, 8.92]

CURVE_DATA = {  # key is distance
    13.0: {'angle': 10.8, 'height': 15},
    25.0: {'angle': 35.1, 'height': 12},
    27.0: {'angle': 49.9, 'height': 8}
}


def graph(curve: dataCurve, name: str, _min: float, _max: float, _step: float):
    x = []
    y = []
    for i in range(int(_min), int(_max), int(_step)):
        x.append(i/2)
        value = curve.eval(i/2)
        # print(f"{i} : {value}")
        y.append(value)
    plt.plot(x, y, label=name)


def generateRandomCurve(length: int, step: int) -> list[curveKey]:
    _keys = []
    for i in range(0, length, step):
        value = random.randint(1, 1000)/100
        # value = RAND_LIST[int(i/10)]
        _keys.append(curveKey(i, value, interpMode.CUBIC))
    return _keys


def generateCurve(field: str, curveDict: dict[float, dict[str, float]]) -> list[curveKey]:
    _keys = []
    for i in curveDict:
        value = curveDict[i][field]
        _keys.append(curveKey(i, value, interpMode.CUBIC))
    return _keys


if __name__ == '__main__':
    ang_curve = dataCurve()
    ang_curve.addKeys(*generateCurve('angle', CURVE_DATA))
    ang_curve.finalize()
    graph(ang_curve, 'Angle', 0, 60, 1)

    hei_curve = dataCurve()
    hei_curve.addKeys(*generateCurve('height', CURVE_DATA))
    hei_curve.finalize()
    graph(hei_curve, 'Height', 0, 60, 1)

    plt.legend()
    plt.show()
