import numpy as np
import matplotlib.pyplot as plt
import aseeg as ag
import pandas as pd

from json import load

# ag.formatujPlik(r"mati.txt")
#dane = np.genfromtxt("mati.txt", delimiter = ',')

dane = pd.read_csv("mati3.txt",header=0)[2:]
#print(dane)

trigger = list(map(float,dane['b'].to_list()))

# Wyznaczyć tutaj początek zapisu i wpisać w data

start = 17050+2309

with open('emostim3.json') as f:
    emostim = {i:j for i,j in enumerate(load(f))} | {0:'0', -1:'-1'}

#print(df)

# #odczytanie i sygnału z każdej elektrody
Fpz = list(map(float, dane['e1'][start:].to_list())) #Cz
F4 = list(map(float, dane['e2'][start:].to_list()))
F3 = list(map(float, dane['e3'][start:].to_list()))
Fz = list(map(float, dane['e4'][start:].to_list()))
Cz = list(map(float, dane['e5'][start:].to_list()))
C4 = list(map(float, dane['e6'][start:].to_list()))
C3 = list(map(float, dane['e7'][start:].to_list()))
Pz = list(map(float, dane['e8'][start:].to_list()))

print(type(Fpz[0]))

trigger = list(map(float,dane['b'].to_list()))[start:]

val = 1
i = 0
trigger_new = []
while i<len(trigger):
    if trigger[i]==1 and trigger[i-1]==0:
        for _ in range(250*5):
            trigger_new.append(val)
            i += 1
        val += 1
    else:
        trigger_new.append(-round(trigger[i]))
        i += 1
trigger_new = [emostim[i] for i in trigger_new] 
#
# # trigger = dane[2:250*42+2,11]
# #
Fpz_filtr = ag.pasmowoprzepustowy(ag.pasmowozaporowy(Fpz, 250, 49, 51), 250, 2, 42)
print("filtr1")
F4_filtr = ag.pasmowoprzepustowy(ag.pasmowozaporowy(F4, 250, 49, 51), 250, 2, 42)
F3_filtr = ag.pasmowoprzepustowy(ag.pasmowozaporowy(F3, 250, 49, 51), 250, 2, 42)
Fz_filtr = ag.pasmowoprzepustowy(ag.pasmowozaporowy(Fz, 250, 49, 51), 250, 2, 42)
print("filtr4")
Cz_filtr = ag.pasmowoprzepustowy(ag.pasmowozaporowy(Cz, 250, 49, 51), 250, 2, 42)
C4_filtr = ag.pasmowoprzepustowy(ag.pasmowozaporowy(C4, 250, 49, 51), 250, 2, 42)
C3_filtr = ag.pasmowoprzepustowy(ag.pasmowozaporowy(C3, 250, 49, 51), 250, 2, 42)
Pz_filtr = ag.pasmowoprzepustowy(ag.pasmowozaporowy(Pz, 250, 49, 51), 250, 2, 42)
print("filtrkoniec")
mati = pd.DataFrame([Fpz_filtr, F4_filtr, F3_filtr, Fz_filtr, Cz_filtr, C4_filtr, C3_filtr, Pz_filtr, trigger_new]).transpose()
mati.to_csv('mati_calculated3.csv')

# mati = pd.DataFrame([Fpz_filtr, F4_filtr, F3_filtr]).transpose()

print(mati.head(10))
#
# #kolejność wyświetlanych bodzców
# wystapienia0 = [0, 4, 15, 16, 21, 25, 26, 32, 40, 41, 43, 47, 49, 51, 53, 54, 59, 63, 64, 65, 68, 69, 73, 76, 78, 82, 83, 99, 104, 108, 113, 115, 116, 118]
# wystapienia1 = [1, 6, 8, 12, 13, 20, 28, 31, 33, 34, 37, 39, 45, 52, 56, 60, 62, 66, 86, 87, 94, 96, 98, 100, 101, 106, 109, 119]
# wystapienia2 = [5, 9, 14, 19, 23, 27, 29, 30, 35, 36, 44, 46, 50, 55, 63, 67, 70, 71, 72, 74, 75, 77, 84, 90, 102, 103, 110, 111, 114, 117, 120]
# wystapienia3 = [2, 3, 7, 10, 11, 17, 18, 22, 24, 38, 42, 48, 53, 57, 58, 61, 79, 80, 81, 85, 88, 89, 91, 92, 93, 95, 97, 101, 105, 107, 112]
#
# ile_0 = len(wystapienia0)
# ile_1 = len(wystapienia1)
# ile_2 = len(wystapienia2)
# ile_3 = len(wystapienia3)
#
# print(ile_0, ile_1, ile_2, ile_3,)

# data_frames = []
# for i in range(1, 42*250):
#     if trigger[i] == 0 and trigger[i-1] == 1:
#         data_frames.append(Fpz_filtr[i:i+250])
#
# bodzce0 = [data_frames[0]]
# bodzcFpz = [data_frames[1]]
# bodzcF4 = [data_frames[5]]
# bodzcF3 = [data_frames[2]]
#
# print(len(data_frames[10]))
# print(len(bodzce0[0]))
# #sumowanie dla każdego bodźca
# for i in range(len(data_frames)):
#     if i == wystapienia0[1]:
#         for j in range(0, 250):
#             bodzce0[j] += data_frames[i][j]
#         wystapienia0.pop(1)
#     elif i == wystapienia1[1]:
#         for j in range(0, 250):
#             bodzcFpz[j] += data_frames[i][j]
#         wystapienia1.pop(1)
#     elif i == wystapienia2[1]:
#         for j in range(0, 250):
#             bodzcF4[j] += data_frames[i][j]
#         wystapienia1.pop(1)
#     elif i == wystapienia3[1]:
#         for j in range(0, 250):
#             bodzcF3[j] += data_frames[i][j]
#         wystapienia1.pop(1)
#
#
# # #uśrednianie
# # for i in range(len(bodzce0)):
# #     bodzce0[i] = bodzce0[i]/ile_0
# # for i in range(len(bodzce0)):
# #     bodzcFpz[i] = bodzcFpz[i]/ile_1
# # for i in range(len(bodzce0)):
# #     bodzcF4[i] = bodzcF4[i]/ile_2
# # for i in range(len(bodzce0)):
# #     bodzcF3[i] = bodzcF3[i]/ile_3
#
#
# #właściwy bodziec ma numer 1
# t=np.linspace(0, 1, 250)
# plt.plot(t, bodzce0)
# plt.plot(t, (bodzcFpz+bodzcF4+bodzcF3)/3)
# plt.legend(["target", "nontarget"])
# plt.xlabel("czas [s]")
# plt.ylabel("napięcie [uV]")
# plt.show()
