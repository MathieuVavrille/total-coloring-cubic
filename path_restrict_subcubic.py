from math import log

results = {}

precision = 0.00000001

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
    for i in l:
        if i <= 0.0001:
            return 1000000
    xnm = -1
    xn = 1.5
    while abs(xnm - xn) > precision:
        xnm, xn = xn, xn - (1-powers(l, xn))/(coeff_powers(l, xn))
        if xn < 0:
            raise ValueError("Negative Value")
        if xn > 1000:
            return 100000000000
    return xn

def get_max_root(A, B, R, c, list_recurrence):
    """Find the maximum root of a list of recurrences"""
    global results
    r_max = 0
    i_max = 0
    l = list_recurrence(A, B, R, c)
    all_roots = []
    for i in range(len(l)):
        if False:
            root = results[l[i]]
        else:
            root = find_root(l[i])
        all_roots.append((root, i))
        if root > r_max:
            r_max = root
            i_max = i
    return r_max, sorted(all_roots), l

    
def min_yplus(D, allowed=[(0,0), (0,1), (1,0), (1,1)]):
    """min(axy-ax(y+1))"""
    val_min = None
    for (x,y) in allowed:
        if (x,y) == (1,0):
            current = D[x][y]
        else:
            current = D[x][y] - D[x][y+1]
        if val_min == None or current < val_min:
            val_min = current
    return val_min
    
def min_xplus(D, allowed=[(0,0), (0,1), (1,0), (1,1)]):
    """min(axy-a(x+1)y)"""
    val_min = None
    for (x,y) in allowed:
        if (x,y) == (0,1):
            current = D[x][y]
        else:
            current = D[x][y] - D[x+1][y]
        if val_min == None or current < val_min:
            val_min = current
    return val_min

def min_to_path(D, P):
    return min(D[0][0]-P[0][0], D[1][0], D[1][1])

def get_list_recurrence(A, B, R, c):
    #2nd comp = blue
    return ([(4*A[0][0]-2*A[1][0]-B[0][0], )*3+(4*A[0][0]-R[0][0]-2*A[0][1], )*3,            #a00/4*a00
            
            (R[0][0]+min_xplus(A)+min_to_path(A, B), )*2,                                    #r00
            (B[0][0]+min_to_path(A, R)+min_yplus(A), )*2,                                    #b00
            
            (A[1][0]+2*min_yplus(A), )+(A[1][0]+min_xplus(A)+min_to_path(A, B), )*2,         #a10 alone
            (A[0][1]+2*min_xplus(A), )+(A[0][1]+min_yplus(A)+min_to_path(A, R), )*2,         #a01 alone
            
            (3*A[0][0]+A[1][1]-A[1][0]+min_to_path(A, B), )*2+(3*A[0][0]+A[1][1]-A[0][1]+min_to_path(A, R), )*2+(3*A[0][0]+A[1][1]-2*min_yplus(A), 3*A[0][0]+A[1][1]-2*min_yplus(A)), 
            (2*A[0][0]+2*A[1][1]-A[0][1], )*2+(2*A[0][0]+2*A[1][1]-A[1][0], )*2+(2*A[0][0]+2*A[1][1]-R[0][0], )+(2*A[0][0]+2*A[1][1]-B[0][0], ),
            (A[0][0]+3*A[1][1], )*6,                                                         #a00/3*a11
            
            (2*A[1][1], )*2,                                                                 #a11/a11
            
            (c+2*min_xplus(A), )+(c+min_xplus(A)+min_yplus(A), )*2+(c+2*min_yplus(A), ),     #degree2
            (2*c+2*min_xplus(A), )+(2*c+min_xplus(A)+min_yplus(A), )*4+(2*c+2*min_yplus(A), )
            ])

"""Remarks
Cycles colored with the same color are done at the end
"""



def get_min_coeff_double(N, interval, starting_points):
    """Find the best coefficients such that the max root is the smallest"""
    r_min = 10000
    c_min = starting_points
    i_min = 0
    l_max = []
    for e1 in range(N+1):
        for e2 in range(N+1):
            for e3 in range(N+1):
                for e4 in range(2):
                    a00 = 1
                    a10 = e1/(N*interval)+starting_points[0]-1/(2*interval)
                    a11 = e2/(N*interval)+starting_points[1]-1/(2*interval)
                    b00 = e3/(N*interval)+starting_points[2]-1/(2*interval)
                    c   = 1
                    if c >= 1:
                        c = 1
                    A = [[0]*3 for j in range(3)]
                    B = [[0]*3 for j in range(3)]
                    R = [[0]*3 for j in range(3)]
                    A[0][0] = a00
                    A[1][0] = a10
                    A[0][1] = a10
                    A[1][1] = a11
                    B[0][0] = b00
                    R[0][0] = b00
                    if True:#0.99 > a01 and a01-0.01 >= a10 >= 0.01 and 0.99 >= b00 and b00-0.01 >= b01 >= 0.01 and 0.99 >= c00 and c00-0.01 >= c01 >= 0.01 and a01-0.01 >= b01:
                        root, index, l = get_max_root(A, B, R, c, get_list_recurrence)
                        if root < r_min:
                            r_min = root
                            c_min = (a10, a11, b00, a00)
                            i_min = index
                            l_max = l, A
    return r_min, c_min, i_min, l_max

def iterate(nb_steps, update_coeff, N, interval, starting):
    """Iterate to increase the precision of the best coefficients"""
    for i in range(nb_steps):
        print("Now finding at precision %d digits at starting points %s"%(log(interval, 10), str(starting)))
        r_min1, c_min1, i_min1, l_max = get_min_coeff_double(N, interval, starting)
        print("We got:")
        print("Root: %.5f. Giving a final algo in 2^(%.20f n)"%(r_min1, log(r_min1, 2)))
        print("With the coefficients %s"%(str(c_min1)))
        print("")
        starting = c_min1
        interval *= update_coeff
    r_min1, c_min1, i_min1, l_max = get_min_coeff_double(N, interval, starting)
    print(r_min1)
    print(c_min1)
    print(i_min1)
    #print(l_max[1])
    print(log(r_min1, 2))

iterate(20, 2, 5, 1, [0.5, 0.5, 0.5, 0.5])

#scp Bureau/stage/total-coloring-cubic/double_color.py  vavrille@chuck.mimuw.edu.pl:~/            (with -R for folder)

















































