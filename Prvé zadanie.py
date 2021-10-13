import numpy as np

L_ = 2          # [m]
A_h = 3600/1e6  # [m^2]
A_d = 3500/1e6  # [m^2]
A_s = 2000/1e6  # [m^2]
F = 6           # [kN]
E = 210*1e6     # [kPa]

L = [L_/4, L_/2, L_/4]
A = [A_h**2, A_d**2, A_s**2]

n = len(L)

k_elem = []

for i in range(n):
    k = E * np.array([ [ A[i]/L[i], -A[i]/L[i] ], [ -A[i]/L[i] , A[i]/L[i] ] ])
    k_elem.append(k)

K = np.zeros( ( 4 , 4 ) )

for i in range(n):
    K_el = np.zeros( (4,4) )
    K_el[i:i+2, i:i+2] = k_elem[i]
    K += K_el

load = [0, 1*F, -1.5*F, 0]
print(load, "\n", 50*"-")

dof = [ 0, 3 ]
K = np.delete(K, dof, axis = 0)
K = np.delete(K, dof, axis = 1)
load = np.delete(load, dof, axis = 0)

K_inv = np.linalg.inv(K)
deformations = np.matmul( K_inv, load )

def_0 = [0, deformations[0]]
F_0 = np.matmul(k_elem[0], def_0)
print("F0 = ", F_0)

def_1 = [ deformations[0], deformations[1]]
F_1 = np.matmul(k_elem[1], def_1)
print("F1 = ", F_1)

def_2 = [ deformations[1], 0]
F_2 = np.matmul(k_elem[2], def_2)
print("F2 = ", F_2)
