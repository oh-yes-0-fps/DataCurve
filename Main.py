from enum import Enum, EnumMeta
from msilib import PID_KEYWORDS
from typing import Union, Any


ONETHIRD: float = 1/3

tang_tension = 0
TANG_MULTIPLIER = 2


class interpMode(Enum):
    LINEAR = 0
    MANUAL = 1
    CUBIC = 2
    CONSTANT = 3
    LAGRANGE = 4
    QUADRATIC = 5

    @staticmethod
    def fromStr(string: str):
        if string in interpMode.__members__:
            return interpMode[string]
        else:
            raise ValueError(f"Invalid interpMode: {string}")


class tangent:
    def __init__(self, _arrive: float = 0, _leave: float = 0):
        self.arrive = _arrive
        self.leave = _leave

    def fromTuple(self, _inTuple: tuple):
        if len(_inTuple) != 2:
            self.arrive = 0
            self.leave = 0
        else:
            self.arrive = _inTuple[0]
            self.leave = _inTuple[1]
        return self

    def fromFloat(self, _inFloat: float):
        self.arrive = _inFloat
        self.leave = _inFloat
        return self

    def autoCalc(self, PrevTime: float, PrevPoint: float, CurTime: float, CurPoint: float, NextTime: float, NextPoint: float, Tension: float):
        tang = curveMath.AutoCalcTangent(
            PrevTime, PrevPoint, CurTime, CurPoint, NextTime, NextPoint, Tension)
        self.arrive = tang
        self.leave = tang

    def __repr__(self) -> str:
        return f"(a:{self.arrive}, l:{self.leave})"


class curveKey:
    # just for sorting
    @staticmethod
    def getValue(key) -> float:
        return key.value

    @staticmethod
    def getTime(key) -> float:
        return key.time

    def __init__(self, _time: float, _value: float, _mode: interpMode, _tangents: Union[tangent, tuple] = (0, 0)) -> None:
        self.time = _time
        self.value = _value
        self.mode = _mode
        if isinstance(_tangents, tuple):
            self.tangent: tangent = tangent().fromTuple(_tangents)
        else:
            self.tangent = _tangents

    def setMode(self, _mode: Union[str, interpMode]):
        if isinstance(_mode, str):
            self.mode = interpMode.fromStr(_mode)
        else:
            self.mode = _mode

    def __repr__(self) -> str:
        return f"({self.time}, {self.value}, {self.mode.name}, {self.tangent})"


class curveMath:
    @staticmethod
    def AutoCalcTangent(PrevTime: float, PrevPoint: float, CurTime: float, CurPoint: float, NextTime: float, NextPoint: float, Tension: float) -> float:
        outTan: float = (1 - Tension) * \
            ((CurPoint-PrevPoint) + (NextPoint-CurPoint))
        PrevToNextTimeDiff = max(0.1, NextTime - PrevTime)
        print(f'{outTan} / {PrevToNextTimeDiff} = {outTan/PrevToNextTimeDiff}')
        return (outTan/PrevToNextTimeDiff) * TANG_MULTIPLIER

    @staticmethod
    def __Lerp(A: float, B: float, T: float) -> float:
        return A + (B-A)*T

    @staticmethod
    def __QuadInterp(Value1: float, Value2: float, Tangent1: float, Tangent2: float, T: float) -> float:
        # A = P0, B = P1, C = P2, T = 0-1
        # figure out C using the tangents
        C = curveMath.__Lerp(Value2, Value1, T) - \
            curveMath.__Lerp(Tangent2, Tangent1, T)

        return curveMath.__Lerp(curveMath.__Lerp(Value1, Value2, T), C, T)

    @staticmethod
    def __CubicInterp(Value1: float, Value2: float, Tangent1: float, Tangent2: float, T: float) -> float:
        # cubic bezier interpolation

        # calculate the two control points
        C1 = Value1 + Tangent1 * ONETHIRD
        C2 = Value2 - Tangent2 * ONETHIRD

        # calculate the two intermediate points
        I1 = curveMath.__Lerp(Value1, C1, T)
        I2 = curveMath.__Lerp(C1, C2, T)
        I3 = curveMath.__Lerp(C2, Value2, T)

        # calculate the final point
        return curveMath.__Lerp(I1, I2, T) + curveMath.__Lerp(I2, I3, T)

    @staticmethod
    def lagrangeInterp(_keyList: list, _time: float) -> float:
        outValue: float = 0
        for i in range(len(_keyList)):
            curKey: curveKey = _keyList[i]
            curValue: float = curKey.value
            curTime: float = curKey.time
            curWeight: float = 1
            for j in range(len(_keyList)):
                if i != j:
                    otherKey: curveKey = _keyList[j]
                    otherTime: float = otherKey.time
                    curWeight *= (_time - otherTime) / (curTime - otherTime)
            outValue += curValue * curWeight
        return outValue

    @staticmethod
    def linInterp(_Key1: curveKey, _Key2: curveKey, timeIn: float) -> float:
        diff = _Key2.time - _Key1.time
        timeOffset = (timeIn - _Key1.time) / diff
        return curveMath.__Lerp(_Key1.value, _Key2.value, timeOffset)

    @staticmethod
    def quadInterp(_Key1: curveKey, _Key2: curveKey, timeIn: float) -> float:
        diff = _Key2.time - _Key1.time
        timeOffset = (timeIn - _Key1.time) / diff
        return curveMath.__QuadInterp(_Key1.value, _Key2.value, _Key1.tangent.leave, _Key2.tangent.arrive, timeOffset)

    @staticmethod
    def cubicInterp(_Key1: curveKey, _Key2: curveKey, timeIn: float) -> float:
        diff = _Key2.time - _Key1.time
        timeOffset = (timeIn - _Key1.time) / diff

        # return curveMath.__CubicInterp(_Key1.value, _Key2.value, _Key1.tangents.leave, _Key2.tangents.arrive, timeOffset)

        point0 = _Key1.value
        point1 = _Key1.value + (_Key1.tangent.leave * diff * ONETHIRD)
        point2 = _Key2.value - (_Key2.tangent.arrive * diff * ONETHIRD)
        point3 = _Key2.value

        p01 = curveMath.__Lerp(point0, point1, timeOffset)
        p12 = curveMath.__Lerp(point1, point2, timeOffset)
        p23 = curveMath.__Lerp(point2, point3, timeOffset)
        p012 = curveMath.__Lerp(p01, p12, timeOffset)
        p123 = curveMath.__Lerp(p12, p23, timeOffset)
        p0123 = curveMath.__Lerp(p012, p123, timeOffset)
        return p0123


class dataCurve:
    def __init__(self, *args: curveKey):
        self.keys: list[curveKey] = []
        for i in args:
            if isinstance(i, curveKey):
                self.keys.append(i)
        self.keys.sort(key=curveKey.getTime)

    def addKeys(self, *args: curveKey):
        for i in args:
            if isinstance(i, curveKey):
                self.keys.append(i)
        return sorted(self.keys, key=curveKey.getTime)

    def addKeysList(self, _inList: list[curveKey]):
        return self.addKeys(*_inList)

    def finalize(self, tension = 0):
        for i in range(len(self.keys)):
            _Ky = self.keys[i]
            if _Ky.mode == interpMode.CUBIC:
                if i == len(self.keys)-1 or i == 0:
                    # _Ky.tangent.leave = 0
                    # _Ky.tangent.arrive = 0
                    continue
                p_Ky = self.keys[i-1]
                n_Ky = self.keys[i+1]
                _Ky.tangent.autoCalc(
                    p_Ky.time, p_Ky.value, _Ky.time, _Ky.value, n_Ky.time, n_Ky.value, tension)

    def eval(self, timeIn: float) -> float:
        for i in range(len(self.keys)):
            _Ky = self.keys[i]
            if _Ky.time > timeIn:
                p_Ky = self.keys[i-1]
                if _Ky.mode == interpMode.LINEAR:
                    return curveMath.linInterp(p_Ky, _Ky, timeIn)
                elif _Ky.mode == interpMode.CUBIC or _Ky.mode == interpMode.MANUAL:
                    return curveMath.cubicInterp(p_Ky, _Ky, timeIn)
                elif _Ky.mode == interpMode.LAGRANGE:
                    return curveMath.lagrangeInterp(self.keys, timeIn)
                elif _Ky.mode == interpMode.QUADRATIC:
                    return curveMath.quadInterp(p_Ky, _Ky, timeIn)
                else:
                    return p_Ky.value
        return self.keys[-1].value

    def getTimeRange(self) -> tuple[float, float]:
        return self.keys[0].time, self.keys[-1].time
