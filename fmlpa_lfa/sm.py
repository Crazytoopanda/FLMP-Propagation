from util import invert, powmod, getprimeover, isqrt
from CipherPub import CipherPub
from Ciphertext import Ciphertext
from Ciphertext1 import Ciphertext1
import random
import time
import math
import gmpy2 as _g

class SM():
    def __init__(self,_VA,_VB,*args):
        self.FIN = CipherPub()
        if isinstance(_VA,int):
            self._VA = _VB
            self._VB = _VA
        else:
            self._VA = _VA
            self._VB = _VB
        _paillier = args[0]
        self.public_key = _paillier
        self.pub = self.public_key.Hsigma


    def StepOne(self):

        self.FIN.T1 = powmod(self._VA.T1, self._VB, self.public_key.N2)
        self.FIN.T2 = self._VA.T2
        self.FIN.PUB = self._VA.PUB