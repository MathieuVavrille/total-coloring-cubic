from math import log

results = {}

precision = 0.000001

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

def min_a_b(A,B):
    val_min = None
    for x in range(2):
        for y in range(2):
            current = A[x][y] - B[x][y]
            if val_min == None or current < val_min:
                val_min = current
    return val_min
    
def min_d_yplus(D):
    """D is either A or C"""
    val_min = None
    for x in range(2):
        for y in range(2):
            current = D[x][y] - D[x][y+1]
            if val_min == None or current < val_min:
                val_min = current
    return val_min
    
def min_d_xplus(D):
    val_min = None
    for x in range(2):
        for y in range(2):
            current = A[x][y] - A[x+1][y]
            if val_min == None or current < val_min:
                val_min = current
    return val_min

def get_list_recurrence(A, B, C):
    return [(A[1][0]+min_a_b(A, B)+min_d_yplus(A), )*2, #a10
            (A[0][1]+2*min_a_b(A, B), A[0][1]+min_a_b(A, B)+min_d_yplus(A), A[0][1]+min_a_b(A, B)+min_d_yplus(A)), 
            (B[0][0]+2*min_d(A), B[0][0]+min_a_b(A, B)+min_d_xplus(A) , B[0][0]+min_a_b(A, B)+min_d_xplus(A)), 
            (B[0][1]+min_d_yplus(A), B[0][1]+min_a_b(A, B)), 
            (C[0][0]+min_d_yplus(A)+min_d_yplus(C), C[0][0]+min_a_b(A, B)+min_d_xplus(C), C[0][0]+min_d_xplus(A)+min_d_xplus(C)), 
            (C[0][1]+min_d_yplus(C), C[0][1]+min_d_xplus(C))]










def get_min_coeff_double(N, interval, starting_points):
    r_min = 10000
    c_min = ()
    i_min = 0
    for e1 in range(N+1):
        for e2 in range(N+1):
            for e3 in range(N+1):
                for e4 in range(N+1):
                    for e5 in range(N+1):
                        for e6 in range(N+1):
                            a00 = 1
                            a10 = e1/(N*interval)+starting_points[0]-1/(2*interval)
                            a01 = e1/(N*interval)+starting_points[1]-1/(2*interval)
                            b00 = e3/(N*interval)+starting_points[2]-1/(2*interval)
                            b10 = 0
                            b01 = e4/(N*interval)+starting_points[3]-1/(2*interval)
                            c00 = e5/(N*interval)+starting_points[4]-1/(2*interval)
                            c10 = 0
                            c01 = e5/(N*interval)+starting_points[5]-1/(2*interval)
                            A = [[0]*3 for j in range(3)]
                            B = [[0]*3 for j in range(3)]
                            C = [[0]*3 for j in range(3)]
                            A[0][0] = a00
                            A[1][0] = a10
                            A[0][1] = a01
                            B[0][0] = b00
                            B[1][0] = b10
                            B[0][1] = b01
                            C[0][0] = c00
                            C[1][0] = c10
                            C[0][1] = c01
                            root, index = get_max_root(A, B, C, get_list_recurrence)
                            if root < r_min:
                                r_min = root
                                c_min = (a10, a01, b00, b01, c00, c01)
                                i_min = index
    return r_min, c_min, i_min

def iterate(nb_steps, update_coeff, N, interval, starting_points):
    for i in range(nb_steps):
        print("Now finding at precision %d digits at starting points %s"%(log(interval, 10), str(starting)))
        r_min1, c_min1, i_min1, s = get_min_coeff_double(6, interval, starting)
        print("We got:")
        print("Root: %.5f. Giving a final algo in 2^(%.20f n)"%(r_min1, log(r_min1, 2)))
        print("With the coefficients %s"%(str(c_min1)))
        print("")
        starting = c_min1
        interval *= update_coeff
    r_min1, c_min1, i_min1, s = get_min_coeff_double(8, interval, starting)
    print(r_min1, c_min1, i_min1)
    print(log(r_min1, 2))




















































