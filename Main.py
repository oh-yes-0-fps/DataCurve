from enum import Enum
from typing import Union

ONETHIRD:float = 1/3

class interpMode(Enum):
    LINEAR = 0
    MANUAL = 1
    CUBIC_H = 2
    CUBICL = 3
    CONSTANT = 4

    @staticmethod
    def fromStr(string:str) -> int:
        return interpMode.__getattribute__(string)


class tangent:
    def __init__(self, _arrive:float = 0, _leave:float = 0):
        self.arrive = _arrive
        self.leave = _leave

    def fromTuple(self, _inTuple:tuple) -> tangent:
        if len(tuple) != 2:
            self.arrive = 0
            self.leave = 0
        else:
            self.arrive = _inTuple[0]
            self.leave = _inTuple[1]
        return self

class curveKey:
    #just for sorting
    @staticmethod
    def getValue(key) -> float:
        return key.value
    @staticmethod
    def getTime(key) -> float:
        return key.time

    def __init__(self, _time:float, _value:float, _mode:Union[str, int] = 0, _tangents:Union[tangent, tuple] = tangent()) -> None:
        self.time = _time
        self.value = _value
        if isinstance(_mode, str):
            self.mode = interpMode.fromStr(_mode)
        else:
            self.mode = _mode
        if isinstance(_tangents, tuple):
            self.tangents:tangent = tangent().fromTuple(_tangents)
        else:
            self.tangents = _tangents

    def modeName(self) -> str:
        if self.mode == 0:
            return 'LINEAR'
        elif self.mode == 1:
            return 'MANUAL'
        elif self.mode == 2:
            return 'CUBIC_H'
        elif self.mode == 3:
            return 'CUBIC_L'
        elif self.mode == 4:
            return 'CONSTANT'





class dataCurve:

    hasBeenFinalized:bool = False

    def __init__(self, *args:curveKey):
        self.keys = []
        for i in args:
            if isinstance(i, curveKey):
                self.keys.append(i)
        self.keys.sort(key=curveKey.getTime)

    #class properties being immutable besides addkeys is best
    def __setattr__(self, __name: str, __value: Any) -> None:
        pass

    def addKeys(self, *args:curveKey):
        if self.hasBeenFinalized:return
        f_keys = []
        for i in args:
            if isinstance(i, curveKey):
                f_keys.append(i)
        return sorted(self.keys.extend(f_keys), key = curveKey.getTime)

    def finalize(self):
        self.hasBeenFinalized = True
        

    

    def linInterp(key1:curveKey, key2:curveKey, timeIn:float) -> float:
        offset = (timeIn-key1.time)/(key2.time) * (key2.value - key1.value)
        return key1.value + offset



