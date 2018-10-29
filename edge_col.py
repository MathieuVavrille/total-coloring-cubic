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
    #print("beginning of Newton")
    #print(a, b)
    for i in l:
        if i <= 0.0001:
            return 1000000
    xnm = -1
    xn = 1.5
    while abs(xnm - xn) > precision:
        #print(xn)
        xnm, xn = xn, xn - (1-powers(l, xn))/(coeff_powers(l, xn))
        if xn < 0:
            raise ValueError("Negative Value")
        if xn > 1000:
            return 100000000000
    return xn

def get_max_root(A, list_recurrence):
    """Find the maximum root of a list of recurrences"""
    global results
    r_max = 0
    i_max = 0
    l = list_recurrence(A)
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
    return r_max, sorted(all_roots), l

    
def min_yplus(D, allowed=[(0,0), (0,1), (1,0), (1,1)]):
    """min(axy-ax(y+1))"""
    val_min = None
    for (x,y) in allowed:
        current = D[x][y] - D[x][y+1]
        if val_min == None or current < val_min:
            val_min = current
    return val_min
    
def min_xplus(D, allowed=[(0,0), (0,1), (1,0), (1,1)]):
    """min(axy-a(x+1)y)"""
    val_min = None
    for (x,y) in allowed:
        current = D[x][y] - D[x+1][y]
        if val_min == None or current < val_min:
            val_min = current
    return val_min

def get_list_recurrence(A):
    return ([(A[0][0]+2*min_yplus(A)+2*min_xplus(A), )*6,
            (A[1][0]+min_xplus(A, allowed = [(0,1), (1,0), (1,1)])+2*min_yplus(A, allowed = [(0,1), (1,0), (1,1)]), )*3,
            (A[1][0]+min_yplus(A, allowed = [(0,1), (1,0), (1,1)])+2*min_xplus(A, allowed = [(0,1), (1,0), (1,1)]), )*3,
            (4*A[1][1], )*2
            ])

"""Remarks
Cycles colored with the same color are done at the end
"""



def get_min_coeff_double(N, interval, starting_points):
    """Find the best coefficients such that the max root is the smallest"""
    r_min = 10000
    c_min = ()
    i_min = 0
    l_max = []
    for e1 in range(N+1):
        for e2 in range(N+1):
            a00 = 1
            a10 = e1/(N*interval)+starting_points[0]-1/(2*interval)
            a01 = a10
            a11 = e2/(N*interval)+starting_points[1]-1/(2*interval)
            A = [[0]*3 for j in range(3)]
            A[0][0] = a00
            A[1][0] = a10
            A[0][1] = a01
            A[1][1] = a11
            if True:#0.99 > a01 and a01-0.01 >= a10 >= 0.01 and 0.99 >= b00 and b00-0.01 >= b01 >= 0.01 and 0.99 >= c00 and c00-0.01 >= c01 >= 0.01 and a01-0.01 >= b01:
                root, index, l = get_max_root(A, get_list_recurrence)
                if root < r_min:
                    r_min = root
                    c_min = (a10, a11)
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
        print(i_min1)
        print(l_max[0])
        print("")
        starting = c_min1
        interval *= update_coeff
    r_min1, c_min1, i_min1, l_max = get_min_coeff_double(N, interval, starting)
    print(r_min1)
    print(c_min1)
    print(i_min1)
    #print(l_max[1])
    print(log(r_min1, 2))

iterate(20, 4, 50, 1, [0.5, 0.5, 0.5])
















































