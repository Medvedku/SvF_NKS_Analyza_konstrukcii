import numpy as np
np.set_printoptions(precision=3)

L_ = 5          # [m]
H_ = 3          # [m]
A_ = 3500/1e6   # [m^2]
E = 210*1e6     # [kPa]
F = 12          # [kN]

coor = [ [L_, 0], [L_, -0.8*H_], [L_, -1.2*H_], [-L_, 0], [-L_, -0.8*H_], [-L_, -1.2*H_]  ]

L = [ ( (i[0]**2) + (i[1]**2) )**(1/2) for i in coor]

alfa = []
for i in coor:
    if i[0] >= 0:
        alfa.append( 2*np.pi + np.arctan( (i[1]/i[0])) )
    else:
        alfa.append( 1*np.pi + np.arctan( (i[1]/i[0])) )

# for i in alfa:
#     print(np.rad2deg(i))

n = len(L)

k_elem = []
for i in range(n):
    k = ((E*A_)/L[i])* np.array([   [ +(np.cos(alfa[i]))**2,                 +(np.cos(alfa[i]))*(np.sin(alfa[i])),  -(np.cos(alfa[i]))**2,                 -(np.cos(alfa[i]))*(np.sin(alfa[i]))  ],
                                    [ +(np.cos(alfa[i]))*(np.sin(alfa[i])),  +(np.sin(alfa[i]))**2,                 -(np.cos(alfa[i]))*(np.sin(alfa[i])),  -(np.sin(alfa[i]))**2                 ],
                                    [ -(np.cos(alfa[i]))**2,                 -(np.cos(alfa[i]))*(np.sin(alfa[i])),  +(np.cos(alfa[i]))**2,                 +(np.cos(alfa[i]))*(np.sin(alfa[i]))  ],
                                    [ -(np.cos(alfa[i]))*(np.sin(alfa[i])),  -(np.sin(alfa[i]))**2,                 +(np.cos(alfa[i]))*(np.sin(alfa[i])),  +(np.sin(alfa[i]))**2                 ] ])
    k_elem.append(k)

K = np.zeros( (2,2) )

for i in range(n):
    K += k_elem[i][0:2, 0:2]

load = [0, -1*F]

delta = np.linalg.inv(K)
deformations = np.matmul( delta, load )
deformations = [deformations[0], deformations[1], 0, 0]

F_gcs = [np.matmul(k_elem[i], deformations) for i in range(n)]
print("F_gcs", F_gcs)
A = []
for i in range(n):
    a = np.array([  [ +np.cos(alfa[i]),   +np.sin(alfa[i]),                 0,                 0  ],
                    [ -np.sin(alfa[i]),   +np.cos(alfa[i]),                 0,                 0  ],
                    [                0,                  0,  +np.cos(alfa[i]),   +np.sin(alfa[i]) ],
                    [                0,                  0,  -np.sin(alfa[i]),   +np.cos(alfa[i]) ] ])
    A.append(a)

F_lcs = []
for i in range(n):
    f = np.matmul( A[i], F_gcs[i] )
    F_lcs.append(f)

N = [F_lcs[i][2] for i in range(n)]
print(N)
