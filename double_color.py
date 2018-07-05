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

def get_max_root(A, B, C, list_recurrence):
    global results
    r_max = 0
    i_max = 0
    l = list_recurrence(A, B, C)
    all_roots = []
    for i in range(len(l)):
        if False:#l[i] in results.keys():
            root = results[l[i]]
        else:
            root = find_root(l[i])
            #results[l[i]] = root
        #print(i, root, l[i][0], l[i][1])
        all_roots.append((root, i, l[i]))
        if root > r_max:
            r_max = root
            i_max = i
    return r_max, sorted(all_roots), l

def min_a_b(A,B, allowed=[(0,0), (0,1), (1,0)]):
    val_min = None
    for (x,y) in allowed:
        current = A[x][y] - B[x][y]
        if val_min == None or current < val_min:
            val_min = current
    return val_min
    
def min_yplus(D, allowed=[(0,0), (0,1), (1,0)]):
    """D is either A or C"""
    val_min = None
    for (x,y) in allowed:
        current = D[x][y] - D[x][y+1]
        if val_min == None or current < val_min:
            val_min = current
    return val_min
    
def min_xplus(D, allowed=[(0,0), (0,1), (1,0)]):
    val_min = None
    for (x,y) in allowed:
        current = D[x][y] - D[x+1][y]
        if val_min == None or current < val_min:
            val_min = current
    return val_min

def get_list_recurrence(A, B, C):
    return [(A[1][0]+min_a_b(A, B)+min_yplus(A), )*2, #a10
            (A[0][1]+2*min_a_b(A, B), A[0][1]+min_a_b(A, B)+min_yplus(A), A[0][1]+min_a_b(A, B)+min_yplus(A)), 
            (A[0][1]+2*min_a_b(A, C), A[0][1]+min_a_b(A, B)+min_yplus(A), A[0][1]+min_a_b(A, B)+min_yplus(A))
            (B[0][0]+2*min_yplus(A), B[0][0]+min_a_b(A, B)+min_xplus(A) , B[0][0]+min_a_b(A, B)+min_xplus(A)), 
            (B[0][1]+min_yplus(A), B[0][1]+min_a_b(A, B)), 
            (B[0][1]+min_yplus(A), B[0][1]+min_a_b(A, C)), 
            (2*C[0][0]+min_a_b(A, B)+min_yplus(A), 2*C[0][0]+min_a_b(A, B)+min_yplus(A), 2*C[0][0]+2*min_xplus(A), 2*C[0][0]+2*min_yplus(A)), 
            (C[0][0]+C[0][1]+min_a_b(A, B), C[0][0]+C[0][1]+min_yplus(A), C[0][0]+C[0][1]+min_xplus(A))]










def get_min_coeff_double(N, interval, starting_points):
    r_min = 10000
    c_min = ()
    i_min = 0
    l_max = []
    for e1 in range(N+1):
        for e2 in range(N+1):
            for e3 in range(N+1):
                for e4 in range(N+1):
                    for e5 in range(N+1):
                        for e6 in range(N+1):
                            a00 = 1
                            a10 = e1/(N*interval)+starting_points[0]-1/(2*interval)
                            if a10 >1:
                                a10=1
                            a01 = e1/(N*interval)+starting_points[1]-1/(2*interval)
                            if a01 >1:
                                a01=1
                            b00 = e3/(N*interval)+starting_points[2]-1/(2*interval)
                            if b00 >1:
                                b00=1
                            b10 = 0
                            b01 = e4/(N*interval)+starting_points[3]-1/(2*interval)
                            if b01 >1:
                                b01=1
                            c00 = e5/(N*interval)+starting_points[4]-1/(2*interval)
                            if c00 >1:
                                c00=1
                            c10 = 0
                            c01 = e5/(N*interval)+starting_points[5]-1/(2*interval)
                            if c01 >1:
                                c01=1
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
                            if True:#0.99 > a01 and a01-0.01 >= a10 >= 0.01 and 0.99 >= b00 and b00-0.01 >= b01 >= 0.01 and 0.99 >= c00 and c00-0.01 >= c01 >= 0.01 and a01-0.01 >= b01:
                                root, index, l = get_max_root(A, B, C, get_list_recurrence)
                                if root < r_min:
                                    r_min = root
                                    c_min = (a10, a01, b00, b01, c00, c01)
                                    i_min = index
                                    l_max = (l, A, B, C)
    return r_min, c_min, i_min, l_max

def iterate(nb_steps, update_coeff, N, interval, starting):
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
    for l in l_max:
        print(l)
    print(log(r_min1, 2))

iterate(10, 4, 4, 5, [0.5, 0.9, 0.76, 0.65, 0.7, 0.3])

#scp Bureau/stage/total-coloring-cubic/double_color.py  vavrille@chuck.mimuw.edu.pl:~/            (with -R for folder)

















































