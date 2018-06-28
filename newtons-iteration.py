import numpy as np
from math import log

results = {}

precision = 0.00001

def powers(l, x):
    s = 0
    for c in l:
        s += x**(-c)
    return s

def coeff_powers(l, x):
    s = 0
    for c in l:
        s += c*x**(-c-1)
    return s

def find_root(l):
    """Uses Newton's iteration to find the biggest zero of the function"""
    #print("beginning of Newton")
    #print(a, b)
    for i in l:
        if i <= 0.0001:
            return 1000000
    xnm = -1
    xn = 1
    while abs(xnm - xn) > precision:
        #print(xn)
        xnm, xn = xn, xn - (1-powers(l, xn))/(coeff_powers(l, xn))
        if xn < 0:
            raise ValueError("Negative Value")
    return xn

def get_list_recurrence(l):
    a2 = l[0]
    a1 = l[1]
    return [(2-2*a2, 5-2*a2-a1), (2-2*a2, 4-a1), (2-2*a2, 3+2*a2-3*a1), (2-2*a2, 4-a2), (2-2*a2, 3+a2-a1), (2-2*a2, 3+a1), 
            (2-2*a2, 4-a1-a1), (2-2*a2, 3+a2-2*a1), (2-2*a2, 2+3*a2-2*a1), (2-2*a2, 3+a1), (2-2*a2, 2+2*a2), (2-2*a2, 2+a2+2*a1),
            (1-a1, 2+a2), (1-a1, 1+3*a2-a1), (1+3*a2, )*3, #15 
            (2-2*a2, 6-4*a2), (2-2*a2, 5-2*a2-a1), (2-2*a2, 4-2*a1), (2-2*a2, 3+2*a2-3*a1), #20
            (2-2*a2, 2+4*a2-4*a1), (3-2*a2+a1, 3-a2+a1, 5-3*a2+a1), (2-2*a2, 4-a2), (2-2*a2, 3+a2-a1), #24
            (2-2*a2, 2+3*a2-2*a1), (2-a2+2*a1, 2-a2+2*a1, 4+2*a1-2*a2), (2-a2+2*a1, 2-a2+2*a1, 3+a1), #27
            (2-2*a2, 2+2*a2), (2-a2+2*a1, 2-a2+2*a1, 3+3*a1-a2), (2-a2+2*a1, 2-a2+2*a1, 2+a2+2*a1), (2+4*a1,)*5, #31
            (1-a1, 2+2*a2-2*a1), (1-a1, 1+4*a2-3*a1), (1+a2+a1, 1+3*a2-a1), #34
            (1-a1, 2+a2), (1-a1, 1+3*a2-a1), (1+a2+a1, 1+2*a2+a1), #37
            (1+a2+a1, 1+a2+a1, 2+2*a1), (1+a2+a1, 1+a2+a1, 1+2*a2+a1), (1+a2+3*a1, 1+a2+3*a1, 1+a2+3*a1), #40
            (1+3*a1,)*3, (4*a2,)*2, (5*a2,)*5, (6*a2,)*5, (4*a2-2*a1, 7*a2-2*a1), #45
            (a2+2*a1, a2+2*a1), (2*a2+2*a1, 2*a2+2*a1), (2*a2, 3*a2)] #48

def get_list_recurrence_original_cut(l):
    a3 = l[0]
    a2 = l[1]
    a1 = l[2]
    return [(a3-a1, 2*a3+2*a2-2*a1), (a3-a1, a3+4*a2-3*a1), (a3-a1, a3+3*a2-a1), #2
            (a3-a1, a3+a2), (a3-a1, a3+3*a2-a1), (a3-a1, a3+2*a2+a1), #5
            (a3-a1, a3+2*a1), (a3-a1, a3+2*a2+a1), (a3-a1, a3+a2+3*a1), #5
            (a3+3*a1, a3+3*a1, a3+3*a1), #9
            (2*a2-2*a1, 4*a2-2*a1), (2*a2-2*a1, 3*a2), (2*a2-2*a1, 2*a2+2*a1)] #12

def get_list_recurrence_second2(l):
    b3 = l[0]
    b2 = l[1]
    a2 = l[2]
    a1 = l[3]
    return [ (b3+3*a2-2*a1, )*3, (b3+a2-b2-a1, b3+b2+3*a2-2*a1), #(b3+a2-b2-a1, b3+3*a2-b2-2*a1), (b3+a2-b2-a1, b3+b2+3*a2-2*a1), 
            (b3+a2-b2-a1, b3+4*a2-3*a1), (b3+a2-b2-a1, b3+3*a2-a1), (b3+3*a2+-2*a1, b3+3*a2+-2*a1, b3+3*a2+-2*a1), #4
            (2*b2+3*a2-a1, 2*b2+3*a2-a1), (b2+3*b2-2*a1, 2*b2+3*a2-a1), (b2+2*a2, 2*b2+3*a2+a1), #7
            (b2+3*a2-2*a1, b2+3*a2-2*a1), (b2+2*a2, b2+3*a2), (b2+2*a2+2*a1, b2+2*a2+2*a1), #10
            (b2+a2, 2*b2+2*a2+a1), (2*b2+a2+2*a1, 2*b2+a2+2*a1, 2*b2+a2+2*a1), #12
            (b2+a2, b2+2*a2), (b2+a2+2*a1, b2+a2+2*a1), (b2+2*a1, b2+2*a1), #15
            (2*a2-2*a1, 4*a2-2*a1), (2*a2, 3*a2), (2*a2+2*a1, 2*a2+2*a1)]

def generate_3colored_full2(l):
    b3 = l[0]
    b2 = l[1]
    a2 = l[2]
    a1 = l[3]
    ret = []
    for c3 in range(4):
        for c2 in range(4-c3):
            for u2 in range(4-c3-c2):
                u1 = 3-c3-c2-u2
                #print(c3, c2, u2, u1)
                ret.append((b3+3*a2+2*a1+b3-b2, )*c3+(b3+3*a2+2*a1+b2, )*c2+(b3+3*a2+2*a1+a2-a1, )*u2+(b3+3*a2+2*a1+a1, )*u1)
    return ret
                    
def generate_3colored_22(l):
    b3 = l[0]
    b2 = l[1]
    a2 = l[2]
    a1 = l[3]
    ret = []
    for c3 in range(3):
        for c2 in range(3-c3):
            for u2 in range(3-c3-c2):
                u1 = 2-c3-c2-u2
                #print(c3, c2, u2, u1)
                ret.append((b3+2*a2-a1, )+(b3+2*a2+b3-b2, )*c3+(b3+2*a2+b2, )*c2+(b3+2*a2+a2-a1, )*u2+(b3+3*a2+2*a1+a1, )*u1)
    return ret


def get_list_recurrence_second(l):
    b3 = l[0]
    b2 = l[1]
    a2 = l[2]
    a1 = l[3]
    #print(len(generate_3colored_full2(l)), len(generate_3colored_22(l)))
    return ([(b3+3*a2, b3+3*a2-a1, b3+3*a2-a1), (b3+2*a2+a1, )*3, (b3+3*a2-2*a1, b3+3*a2-a1, b3+3*a2-a1)] + #3, triangles
            generate_3colored_full2(l) + #22
            generate_3colored_22(l) + #32
            [(b3+2*a2+a1, )*3, (b3+3*a1, )*3, #34
            (2*b2+3*a2-a1, 2*b2+3*a2-a1), (b2+3*b2-2*a1, 2*b2+3*a2-a1), (b2+2*a2, 2*b2+3*a2+a1), #6
            (b2+3*a2-2*a1, b2+3*a2-2*a1), (b2+2*a2, b2+3*a2), (b2+2*a2+2*a1, b2+2*a2+2*a1), #9
            (b2+a2, 2*b2+2*a2+a1), (2*b2+a2+2*a1, 2*b2+a2+2*a1, 2*b2+a2+2*a1), #13
            (b2+a2, b2+2*a2), (b2+a2+2*a1, b2+a2+2*a1), (b2+2*a1, b2+2*a1), #14
            (a2+2*a1, a2+2*a1), (2*a2+2*a1, 2*a2+2*a1), (2*a2, 3*a2)])
            

def get_list_recurrence_edge_colored(a2, a1):
    return [()]
        
def get_max_root(l, list_recurrence):
    global results
    r_max = 0
    i_max = 0
    l = list_recurrence(l)
    all_roots = []
    for i in range(len(l)):
        if False:#l[i] in results.keys():
            root = results[l[i]]
        else:
            root = find_root(l[i])
            #results[l[i]] = root
        #print(i, root, l[i][0], l[i][1])
        all_roots.append((root, i))#, l[i]))
        if root > r_max:
            r_max = root
            i_max = i
    return r_max, sorted(all_roots)


def get_min_coeff(N):
    r_min1 = 10000
    c_min1 = ()
    i_min1 = 0
    r_min2 = 10000
    c_min2 = ()
    i_min2 = 0
    c = 0
    s = ""
    for e1 in range(1,N):
        for e2 in range(1,N):
            a2u = e2/N
            a1u = e1/N
            root1, index1 = get_max_root([a2u, a1u], get_list_recurrence)
            if root1 < r_min1:
                r_min1 = root1
                c_min1 = (a2u, a1u)
                i_min1 = index1
            for e3 in range(1,N):
                for e4 in range(1,N):
                    b3c = e4/N
                    b2c = e3/N
                    a2c = e2/N
                    a1c = e1/N
                    root2, index2 = get_max_root([b3c, b2c, a2c, a1c], get_list_recurrence_second)
                    #s += " (%f, %f, %.4f)"%(a1/100, a2/100, 1/root1) 
                    if a2c >= b3c:
                        coeff = a2c
                    else:
                        coeff = (3*a2c+b3c)/4
                    if root2**coeff < r_min2:
                        r_min2 = root2**coeff
                        c_min2 = (b3c, b2c, a2c, a1c)
                        i_min2 = index2
                        c = coeff
        s += "\n\n"
    return r_min1, c_min1, i_min1, s, r_min2, c_min2, i_min2, c

r_min1, c_min1, i_min1, s, r_min2, c_min2, i_min2, c = get_min_coeff(10)
print(r_min1, c_min1, i_min1)
print(r_min2, c_min2, i_min2, c)
print(log(r_min1, 2)+log(r_min2, 2))



'''print("""\\begin{figure}[ht]
\\centering
\\begin{tikzpicture}
\\begin{axis}[xlabel=a1, ylabel=a2, zlabel=1/work factor]
\\addplot3 [surf] coordinates
{ """)
print(s)
print("""};
\\end{axis}
\\end{tikzpicture}
\\caption{inverse of the work factor, depending on the coefficients a1 and a2}
\\label{fig:roots}
\\end{figure}""")'''


































