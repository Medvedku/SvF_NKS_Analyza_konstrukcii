import numpy as np

np.set_printoptions(precision=2)

spiel = True

class Node:
    num_of_nodes = 0
    def __init__(self, xz: list, alfa_ = 0):
        self.nd_id    = Node.num_of_nodes
        self.v        = Node.num_of_nodes*2 + 0
        self.fi       = Node.num_of_nodes*2 + 1
        self.coor     = xz

        Node.num_of_nodes += 1

class Element:
    num_of_elements = 0
    def __init__(self, start_, end_, b_, h_, E = 29*1e6,):
        self.el_id       = Element.num_of_elements
        self.start       = start_.nd_id
        self.end         = end_.nd_id
        self.start_coor  = start_.coor
        self.end_coor    = end_.coor
        self.E           = E
        self.I           = (1/12) * b_ * (h_**3)

        self.c_n = [ start_.v, start_.fi, end_.v, end_.fi]

        self.Lx = self.end_coor[0] - self.start_coor[0]
        self.Ly = self.end_coor[1] - self.start_coor[1]
        self.L = ( (self.Lx**2) + (self.Ly**2) )**(1/2)
        assert (self.L!=0), "Element s nulovou dlzkou"

        Element.num_of_elements += 1

        self.k_elem = (self.E * self.I) * np.array(
        [   [ + 12/(self.L**3) , - 6 /(self.L**2) , - 12/(self.L**3) , - 6 /(self.L**2) ],
            [ - 6 /(self.L**2) , + 4 /(self.L**1) , + 6 /(self.L**2) , + 2 /(self.L**1) ],
            [ - 12/(self.L**3) , + 6 /(self.L**2) , + 12/(self.L**3) , + 6 /(self.L**2) ],
            [ - 6 /(self.L**2) , + 2 /(self.L**1) , + 6 /(self.L**2) , + 4 /(self.L**1) ] ]
            )


# >>>>>>>>>>>> Definicia konstrukcie <<<<<<<<<<<<<<<<<<<
# >>>>>>>>>>>> Výpočet               <<<<<<<<<<<<<<<<<<<
# Definícia uzlov
Nodes = []
Nodes.append(Node([ 0.0, 0.0 ]))                         # 0
Nodes.append(Node([ 3.2, 0.0 ]))                         # 1
Nodes.append(Node([ (3.2+1.92), 0.0 ]))                  # 2
Nodes.append(Node([ (3.2+1.92+2.56), 0.0 ]))             # 3

# Definícia elementov
Elements = []
Elements.append(Element( Nodes[0], Nodes[1], 0.25, 0.25))
Elements.append(Element( Nodes[1], Nodes[2], 0.25, 0.25))
Elements.append(Element( Nodes[2], Nodes[3], 0.25, 0.25))

n = Elements[-1].el_id+1                                # počet elementov

# for i in Elements:
#     print(i.k_elem)

# >>>>>>>>>>>> Výpočet               <<<<<<<<<<<<<<<<<<<

# Skladanie globálnej matice tuhosti
K = np.zeros( (Nodes[-1].fi+1, Nodes[-1].fi+1) )
for i in Elements:
    K_temp = np.zeros( (Nodes[-1].fi+1, Nodes[-1].fi+1) )
    for j in range(4):
        for k in range(4):
            K_temp[i.c_n[j],i.c_n[k]] = i.k_elem[j,k]
    K += K_temp

# Definícia zaťažovacieho vektora
load    = [ 0 for i in range(Nodes[-1].fi+1)]
load[2] = -75
load[4] = -50

# Definícia indexov deformácii
indexes = list(range(Nodes[-1].fi+1))

# Aplikovanie okrajových podmienok
deleto = [ 0, 1, -1, -2]
K       = np.delete(K, deleto, axis = 0)
K       = np.delete(K, deleto, axis = 1)
load    = np.delete(load, deleto, axis = 0)
indexes = np.delete(indexes, deleto, axis = 0)

# Výpočet matice poddajnosti
delta = np.linalg.inv(K)

# Výpočet deformácii
r_tot = np.matmul( delta, load )

# Definícia vektorov deformácii pre jednotlivé elementy
r_el = []
for i in Elements:
    r_e = []
    for j in i.c_n:
        if j in list(indexes):
            coor_ = list(indexes).index(j)
            r_e.append( r_tot[coor_] )
        else:
            r_e.append( 0 )
    r_el.append(r_e)

# Výpočet vnútorných síl po prvkoch
F_ = [ np.matmul(Elements[i].k_elem, r_el[i]) for i in range(n) ]

# Výsledky
if spiel:
    for i in range(n):
        print("Element: {}".format(i))
        print("Ohybový moment na začiaku elementu = {} kNm".format( format(F_[i][1], ".6g") ))
        print("Ohybový moment na konci elementu   = {} kNm".format( format(-F_[i][-1], ".6g") ))
        print("Priečna sila na začiatku elementu  = {} kN ".format( format(F_[i][0], ".6g") ))
        print("Priečna sila na konci elementu     = {} kN ".format( format(-F_[i][2], ".6g") ))
        print("Zvislý posun na začiaktu elementu  = {} mm ".format( format(-F_[i][2], ".6g") ))
        print(50*"-")
