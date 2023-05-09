from sad import SAD
from util import invert, powmod, getprimeover, isqrt
from CipherPub import CipherPub
from Ciphertext import Ciphertext
from Ciphertext1 import Ciphertext1
import time
import random
import math
import gmpy2 as _g


def compareTo(a, b):
    return ((a > b) - (a < b))


class SLT():
    def __init__(self,_VA,_VB,*args):

        self.a = CipherPub()
        self.b = CipherPub()

        self.a11 = CipherPub()
        self.b11 = CipherPub()
        self.a12 = CipherPub()
        self.b12 = CipherPub()
        self.b13 = CipherPub()
        self.l1 = CipherPub()
        self.l2 = CipherPub()

        self.CCC = 0
        self.U = CipherPub()
        self.EEone = CipherPub()
        self.FIN = CipherPub()

        self.a = _VA #对象
        self.b = _VB
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
        #self.time_start = time.time()
        self.a1 = self.PaillierPublicKey.N-1
        self.TWO = 2

        self.l = random.SystemRandom().randrange(1, 2**(self.PaillierPublicKey.N.bit_length()-1))
        self.EEone = self.PaillierPublicKey.raw_encrypt(1, self.pub)
        #print("a.t2",self.a.T2)
        self.a12.T1 = ((powmod(self.a.T1,self.TWO, self.PaillierPublicKey.N2))*self.EEone.T1)%self.PaillierPublicKey.N2
        self.a12.T2 = ((powmod(self.a.T2,self.TWO, self.PaillierPublicKey.N2))*self.EEone.T2)%self.PaillierPublicKey.N2

        self.a12.PUB = self.a.PUB

        self.b12.T1 = powmod(self.b.T1,self.TWO, self.PaillierPublicKey.N2)
        self.b12.T2 = powmod(self.b.T2,self.TWO, self.PaillierPublicKey.N2)
        self.b12.PUB = self.b.PUB

        self.RR1 = random.SystemRandom().randrange(1, 2**100)

        self.s = random.SystemRandom().randrange(1, 1000000) % 2

        if self.s == 1:
            self.b13.T1 = powmod(self.b12.T1, self.a1, self.PaillierPublicKey.N2)
            self.b13.T2 = powmod(self.b12.T2, self.a1, self.PaillierPublicKey.N2)
            self.b13.PUB = self.b12.PUB


            self.l2.T1 = self.a12.T1 * self.b13.T1
            self.l2.T2 = self.a12.T2 * self.b13.T2
            self.l2.PUB = self.a12.PUB

            self.l1.T1 = powmod(self.l2.T1, self.RR1, self.PaillierPublicKey.N2)
            self.l1.T2 = powmod(self.l2.T2, self.RR1, self.PaillierPublicKey.N2)
            self.l1.PUB = self.pub
        else:
            self.b13.T1 = powmod(self.a12.T1, self.a1, self.PaillierPublicKey.N2)
            self.b13.T2 = powmod(self.a12.T2, self.a1, self.PaillierPublicKey.N2)
            self.b13.PUB = self.a12.PUB

            self.l2.T1 = self.b12.T1 * self.b13.T1
            self.l2.T2 = self.b12.T2 * self.b13.T2
            self.l2.PUB = self.b12.PUB

            self.l1.T1 = powmod(self.l2.T1, self.RR1, self.PaillierPublicKey.N2)
            self.l1.T2 = powmod(self.l2.T2, self.RR1, self.PaillierPublicKey.N2)
            self.l1.PUB = self.pub

        self.m11 = self.PaillierPublicKey.AddPDec1(self.l1)
        #self.CCC = self.CCC + self.m11.T1.bit_length() + self.m11.T2.bit_length() + self.m11.T3.bit_length()

    def StepTwo(self):
        #self.m1 = 1
        self.m1 = self.PaillierPublicKey.AddPDec2(self.m11)
        if compareTo(self.m1,self.l) == 1:
            self.U.T1 = self.EEone.T1
            self.U.T2 = self.EEone.T2
            self.U.PUB = self.pub
        elif compareTo(self.m1,self.l) == -1:
            self.U.T1 = powmod(self.EEone.T1, 0, self.PaillierPublicKey.N2)  # 0
            self.U.T2 = powmod(self.EEone.T2, 0, self.PaillierPublicKey.N2)
            self.U.PUB = self.pub
        else:
            self.U = self.PaillierPublicKey.raw_encrypt(self.a1, self.pub)
        #self.CCC = self.CCC + self.U.T1.bit_length() + self.U.T2.bit_length()


    def StepThree(self):
        if self.s == 1 :
            self.FIN = self.U

        if self.s == 0:
            self.FIN.T1 = (self.EEone.T1 * (powmod(self.U.T1, self.a1, self.PaillierPublicKey.N2)))%(self.PaillierPublicKey.N2)
            self.FIN.T2 =  (self.EEone.T2 * (powmod(self.U.T2, self.a1, self.PaillierPublicKey.N2)))%(self.PaillierPublicKey.N2)
            self.FIN.PUB = self.pub
        #self.time_end = time.time()
        #print('time cost', self.time_end - self.time_start, 's')

class t(object):
    def __init__(self,key,value):
        self.key = key
        self.value = value


if __name__ == "__main__":

    a = 10
    b = 5
    K = 2
    Di = []
    PaillierPublicKey,PaillierPrivateKey = paillierT.generate_paillier_keypair(1024)
    B = 9
    B3 = 10
    a2 = 5
    a3 = 4
    ccc = [None] * PaillierPublicKey.beta
    ab = 16
    bb = 10
    E1 = PaillierPublicKey.Encrypt(B)


    E10 = PaillierPublicKey.Encrypt(B,None, PaillierPublicKey.H[1])
    t1= t('b',E10)

    # print("E10", E10)
    # C10 = paillier.AddPDec1(E10)
    # print("C10", C10)
    # C11 = paillier.AddPDec2(C10)
    # print("C11", C11)
    # for p in range(0, paillier.beta - 1):
    #     ccc[p] = paillier.WDecryption(E10, paillier.X[p])

    E20 = PaillierPublicKey.Encrypt(B3, None, PaillierPublicKey.H[2])
    t2 = t('c', E20)
    # print("new alo : ", C11)
    # print("E20: ", E20)
    # print("E20====", paillier.SDecryption(E20))
    # SK17 = SAD(E10, E20, paillier)
    # SK17.StepOne()
    # SK17.StepTwo()
    # SK17.StepThree()
    # print(paillier.SDecryption(E20))
    # print(SK17.FIN2)

    SK11 = SLT(t1.value.ciphertext(), t2.value.ciphertext(), PaillierPublicKey)
    SK11.StepOne()
    SK11.StepTwo()
    SK11.StepThree()




    #大小比较结果U=0 x>=y ,U=1 x<y 结果U=
    print(PaillierPrivateKey.SDecryption(SK11.FIN))