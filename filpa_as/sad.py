#import Ent1.paillier as paillierT

from util import invert, powmod, getprimeover, isqrt
from CipherPub import CipherPub
from Ciphertext import Ciphertext
from Ciphertext1 import Ciphertext1
import random
import time
import math
import gmpy2 as _g


class SAD():
    def __init__(self,_VA,_VB,*args):
        # self.a11 = CipherPub()
        # self.b11 = CipherPub()
        # self.pub = 0
        self.ERR1 = CipherPub()
        self.ERR3 = CipherPub()
        self.ERR2 = CipherPub()
        self.EA = CipherPub()
        self.EB = CipherPub()
        self.m4 = CipherPub()
        self.EERR3 = Ciphertext()
        self.FIN = CipherPub()
        self.FIN2 = 0
        self.m11 = Ciphertext1()
        self.m12 = Ciphertext1()
        # self.paillier = PaillierT(1024)
        self.CCC = 0
        self.a1 = 0
        self.a11 = _VA
        self.b11 = _VB
        if args and len(args)>1:
            _pub = args[0]
            _paillier = args[1]
            self.pub = _pub
            self.PaillierPublicKey = _paillier
        else:
            _paillier = args[0]
            self.PaillierPublicKey = _paillier
            self.pub = self.PaillierPublicKey.Hsigma

    def StepOne(self):

        self.RR1 = random.SystemRandom().randrange(1, 2**100)
        self.RR2 = random.SystemRandom().randrange(1, 2**100)
        self.RR3 = self.RR1 + self.RR2
        self.a1 = self.PaillierPublicKey.N - 1
        self.ERR1 = self.PaillierPublicKey.raw_encrypt(self.RR1, self.a11.PUB)
        self.ERR2 = self.PaillierPublicKey.raw_encrypt(self.RR2, self.b11.PUB)

        self.ERR3 = self.PaillierPublicKey.raw_encrypt(self.RR3, self.pub)
        self.EA.T1 = self.a11.T1 * self.ERR1.T1
        self.EA.T2 = self.a11.T2 * self.ERR1.T2
        self.EA.PUB = self.a11.PUB

        self.EB.T1 = self.b11.T1 * self.ERR2.T1
        self.EB.T2 = self.b11.T2 * self.ERR2.T2
        self.EB.PUB = self.b11.PUB

        self.EERR3.T1 = powmod(self.ERR3.T1, self.a1, self.PaillierPublicKey.N2)
        self.EERR3.T2 = powmod(self.ERR3.T2, self.a1, self.PaillierPublicKey.N2)

        #self.m11 = self.PaillierPublicKey.AddPDec1(self.EA)
        #self.m12 = self.PaillierPublicKey.AddPDec1(self.EB)
        #self.CCC = self.CCC +self.m11.T1.bit_length() + self.m11.T2.bit_length() + self.m11.T3.bit_length() + self.m12.T1.bit_length() + self.m12.T2.bit_length() + self.m12.T3.bit_length()


    def StepTwo(self):
        #self.m1 = self.PaillierPublicKey.AddPDec2(self.m11)
        #self.m2 = self.PaillierPublicKey.AddPDec2(self.m12)
        #self.m1 = self.m1 + self.m2
        self.m4.T1 = self.EA.T1 * self.EB.T1
        self.m4.T2 = self.EA.T2 * self.EB.T2
        self.m4.T2 = self.EA.PUB
        #self.CCC = self.CCC + self.m4.T1.bit_length() + self.m4.T2.bit_length()

    def StepThree(self):
        self.FIN.T1 = self.m4.T1 * self.EERR3.T1
        self.FIN.T2 = self.m4.T2 * self.EERR3.T2
        self.FIN.PUB = self.pub
        # time_end = time.time()
        # print('time cost1-2', time_end - self.time_start, 's')
        #self.FIN2 = self.paillier.SDecryption(self.FIN)


if __name__ == "__main__":
    a = 10
    b = 5
    K = 2
    Di = []
    PaillierPublicKey,PaillierPrivateKey = paillierT.generate_paillier_keypair(1024)
    B = 5
    B3 = 8
    a2 = 5
    a3 = 4
    ccc = [None] * PaillierPublicKey.beta
    ab = 16
    bb = 10
    E1 = PaillierPublicKey.Encrypt(B)

    E10 = PaillierPublicKey.Encrypt(B, None, PaillierPublicKey.H[1])
    #print("E10---",E10)
    # E10.T1 = E10.T1
    # E10.T1 = E10.T1
    # print("E10", E10)
    # C10 = paillier.AddPDec1(E10)
    # # print("C10", C10)
    # C11 = paillier.AddPDec2(C10)
    #
    # print("C11", C11)
    # for p in range(0, paillier.beta - 1):
    #     ccc[p] = paillier.WDecryption(E10, paillier.X[p])
    E20 = PaillierPublicKey.Encrypt(B3, None,PaillierPublicKey.H[2])
    print(E20.ciphertext())
    # # print("new alo : ", C11)
    # # print("E20: ", E20)
    # # print("E20====", paillier.SDecryption(E20))
    SK17 = SAD(E10.ciphertext(), E20.ciphertext(), PaillierPublicKey)
    SK17.StepOne()
    SK17.StepTwo()
    SK17.StepThree()
    print(PaillierPrivateKey.SDecryption(SK17.FIN))
    print(SK17.FIN2)
