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

def get_max_root(a01, a11, r, d, rd, sd, list_recurrence):
    """Find the maximum root of a list of recurrences"""
    global results
    r_max = 0
    i_max = 0
    l = list_recurrence(a01, a11, r, d, rd, sd)
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

def get_list_recurrence(a01, a11, r, d, rd, sd):
    #2nd comp = blue
    return ([(1+2*min(1-a01, a01-a11, a11, r, 1-rd, sd, rd-d)+min(1-r, a01, a11, r, 1-sd, sd, rd), )*6, #a00 surrounded by anything. The first min is for the normal edge colored, the second one is for the edge colored with the same color as the vertex
            (r+min(a01-a11, a11, r, 1-rd, sd, rd-d)+min(a01, a11, r, 1-sd, sd, rd), )*2, #r
            (a01+2*min(a01-a11, a11, 1-rd, sd, rd-d), )+(a01+min(a01-a11, a11, 1-rd, sd, rd-d)+min(a01, a11, r, 1-sd, sd, rd), )*2, #a01
            (a11+min(a11, 1-rd, sd, rd-d), )*2,
            (d, )*2
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
                for e4 in range(N+1):
                    for e5 in range(N+1):
                        for e6 in range(N+1):
                            a01 = e1/(N*interval)+starting_points[0]-1/(2*interval)
                            a11 = e2/(N*interval)+starting_points[1]-1/(2*interval)
                            r   = e3/(N*interval)+starting_points[2]-1/(2*interval)
                            d   = e4/(N*interval)+starting_points[3]-1/(2*interval)
                            rd  = e5/(N*interval)+starting_points[4]-1/(2*interval)
                            sd  = e6/(N*interval)+starting_points[5]-1/(2*interval)
                            root, index, l = get_max_root(a01, a11, r, d, rd, sd, get_list_recurrence)
                            if root < r_min:
                                r_min = root
                                c_min = (a01, a11, r, d, rd, sd)
                                i_min = index
                                l_max = l, (a01, a11, r, d, rd, sd)
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

iterate(20, 1.5, 4, 1, [0.5, 0.5, 0.5, 0.5, 0.5, 0.5])

#scp Bureau/stage/total-coloring-cubic/double_color.py  vavrille@chuck.mimuw.edu.pl:~/            (with -R for folder)

















































