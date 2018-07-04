import numpy as np
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

def generate_recurrence(x1, y1, x2, y2, l):
    rec = []
    if y1 != 2 and y2 != 2:
        rec.append(l[x1][y1] + l[x2][y2] - l[x1][y1+1] - l[x2][y2+1])
    rec.append(l[x1][y1] + l[x2][y2] - l[x1+1][y1] - l[x2+1][y2])
    if x1 == 0 and x2 == 0:
        rec.append(l[x1][y1] + l[x2][y2] - l[x1+1][y1] - l[x2+1][y2])
    return rec

def get_list_double_node(l, verbose = False):
    ret = []
    count = 0
    for x1 in [0,1]:
        for y1 in range(3-x1):
            for x2 in [0,1]:
                for y2 in range(3-x2):
                    if verbose:
                        print(count, x1, y1, x2, y2)
                    count += 1
                    ret.append(generate_recurrence(x1, y1, x2, y2, l))
    return ret

#get_list_double_node([[0,0,0,0]]*3, True)

def get_list_double(l):
    a = l[0]
    b = l[1]
    c = l[2]
    d2 = l[3]
    d1 = l[4]
    return [(b-d2, a-c, a-c), #baa
            (b-d2, 2*b-2*c, a-c), #bab
            (b, a+d1), #bad1
            (b+d2-2*d1, a+d2-d1), #bad2
            (b, 2*b-c), #bbd1
            (b+d2-2*d1, 2*b+d2-d1-c), #bbd2
            (2*a+c-d1-b, )*4, #caa 6
            (2*a+2*c-b, )*2, #cac
            (3*a+d2-d1-2*b, 2*a+d2-b-2*d1)*2, #d2aa
            (3*a+d1-2*b, 2*a-b, 2*a-b)]#




def rec_for_grph33(s1, s2, s3, s4, a2, a1):
    nb_deg = [0,0,0,0]
    nb_deg[s1] += 1
    nb_deg[s2] += 1
    nb_deg[s3] += 1
    nb_deg[s4] += 1
    return (2-2*a2, 2+nb_deg[3]*(1-a2)+nb_deg[2]*(a2-a1)+nb_deg[1]*a1)

def generate_33(a2, a1):
    count = 15
    rec = []
    for s1 in range(1, 4):
        for s2 in range(1, 4):
            for s3 in range(1, 4):
                for s4 in range(1, 4):
                    rec.append(rec_for_grph33(s1, s2, s3, s4, a2, a1))
                    count += 1
    return rec

def rec_for_grph32(s1, s2, sdeg2, a2, a1):
    dec = [0, a1, a2-a1, 1-a2]
    dele = [0, a1, a2, 1]
    nb_deg = [0,0,0,0]
    nb_deg[s1] += 1
    nb_deg[s2] += 1
    nb_deg[sdeg2] += 1
    if sdeg2 == 1:
        return (1+a1, 1+a2+a1+dec[s1]+dec[s2])
    elif s1 == 1 or s2 == 1:
        return (1+a2+dec[max(s1, s2)], 1+a2+a1+dec[sdeg2]+dec[max(s1, s2)], 1+a2+dele[max(s1, s2)])
    return (1-a1, 1+a2+dec[s1]+dec[s2]+dec[sdeg2])

def generate_32(a2, a1):
    count = 96
    rec = []
    for s1 in range(1, 3):
        for s2 in range(1, 3):
            for sdeg2 in range(1, 4):
                if count == 1070:
                    print(count, s1, s2, sdeg2)
                rec.append(rec_for_grph32(s1, s2, sdeg2, a2, a1))
                count += 1
    return rec

def get_list_generated(l):
    a2 = l[0]
    a1 = l[1]
    return ([(2-2*a2, 5-2*a2-a1), (2-2*a2, 4-a1), (2-2*a2, 3+2*a2-3*a1), (2-2*a2, 4-a2), (2-2*a2, 3+a2-a1), (2-2*a2, 3+a1), 
            (2-2*a2, 4-a1-a1), (2-2*a2, 3+a2-2*a1), (2-2*a2, 2+3*a2-2*a1), (2-2*a2, 3+a1), (2-2*a2, 2+2*a2), (2-2*a2, 2+a2+2*a1),
            (1-a1, 2+a2), (1-a1, 1+3*a2-a1), (1+3*a2, )*3] +#14
            generate_33(a2, a1) + generate_32(a2, a1) + 
            [(1+3*a1,)*3, (4*a2,)*2, (5*a2,)*5, (6*a2,)*5, (4*a2-2*a1, 7*a2-2*a1), #45
            (a2+2*a1, a2+2*a1), (2*a2+2*a1, 2*a2+2*a1), (2*a2, 3*a2)]) #48






def get_list_recurrence(l):
    a2 = l[0]
    a1 = l[1]
    return ([(2-2*a2, 5-2*a2-a1), (2-2*a2, 4-a1), (2-2*a2, 3+2*a2-3*a1), (2-2*a2, 4-a2), (2-2*a2, 3+a2-a1), (2-2*a2, 3+a1), 
            (2-2*a2, 4-a1-a1), (2-2*a2, 3+a2-2*a1), (2-2*a2, 2+3*a2-2*a1), (2-2*a2, 3+a1), (2-2*a2, 2+2*a2), (2-2*a2, 2+a2+2*a1),
            (1-a1, 2+a2), (1-a1, 1+3*a2-a1), (1+3*a2, )*3, #15 
            (2-2*a2, 6-4*a2), (2-2*a2, 5-2*a2-a1), (2-2*a2, 4-2*a1), (2-2*a2, 3+2*a2-3*a1), #20
            (2-2*a2, 2+4*a2-4*a1), (3-2*a2+a1, 3-a2+a1, 5-3*a2+a1), (2-2*a2, 4-a2), (2-2*a2, 3+a2-a1), #24
            (2-2*a2, 2+3*a2-2*a1), (2-a2+2*a1, 2-a2+2*a1, 4+2*a1-2*a2), (2-a2+2*a1, 2-a2+2*a1, 3+a1), #27
            (2-2*a2, 2+2*a2), (2-a2+2*a1, 2-a2+2*a1, 3+3*a1-a2), (2-a2+2*a1, 2-a2+2*a1, 2+a2+2*a1), (2+4*a1,)*5, #31
            (1-a1, 2+2*a2-2*a1), (1-a1, 1+4*a2-3*a1), (1+a2+a1, 1+3*a2-a1), #34
            (1-a1, 2+a2), (1-a1, 1+3*a2-a1), (1+a2+a1, 1+2*a2+a1), #37
            (1+a2+a1, 1+a2+a1, 2+2*a1), (1+a2+a1, 1+a2+a1, 1+2*a2+a1), (1+a2+3*a1, )*3, #40
            (1+3*a1,)*3, (4*a2,)*2, (5*a2,)*5, (6*a2,)*5, (4*a2-2*a1, 7*a2-2*a1), #45
            (a2+2*a1, a2+2*a1), (2*a2+2*a1, 2*a2+2*a1), (2*a2, 3*a2)]) #48

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
        all_roots.append((root, i, l[i]))
        if root > r_max:
            r_max = root
            i_max = i
    return r_max, sorted(all_roots)


def get_min_coeff(N, interval, starting_points):
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
            a2u = e2/(N*interval)+starting_points[0]-1/(2*interval)
            a1u = e1/(N*interval)+starting_points[1]-1/(2*interval)
            root1, index1 = get_max_root([a2u, a1u], get_list_generated)
            if root1 < r_min1:
                r_min1 = root1
                c_min1 = (a2u, a1u)
                i_min1 = index1
            for e3 in range(1,N):
                for e4 in range(1,N):
                    b3c = e4/(N*interval)+starting_points[2]-1/(2*interval)
                    b2c = e3/(N*interval)+starting_points[3]-1/(2*interval)
                    a2c = e2/(N*interval)+starting_points[4]-1/(2*interval)
                    a1c = e1/(N*interval)+starting_points[5]-1/(2*interval)
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

def get_min_coeff_double(N, interval, starting_points):
    r_min = 10000
    c_min = ()
    i_min = 0
    s = ""
    for e1 in range(N+1):
        for e2 in range(N+1):
            for e3 in range(N+1):
                for e4 in range(N+1):
                    for e5 in range(N+1):
                        a  = 1#e1/(N*interval)+starting_points[0]-1/(2*interval)
                        b  = e2/(N*interval)+starting_points[1]-1/(2*interval)
                        c  = e3/(N*interval)+starting_points[2]-1/(2*interval)
                        d2 = e4/(N*interval)+starting_points[3]-1/(2*interval)
                        d1 = e5/(N*interval)+starting_points[4]-1/(2*interval)
                        root, index = get_max_root([a, b, c, d2, d1], get_list_double)
                        if root**a < r_min and a > 0.1 and b > 0.1 and c >= 0 and d2 >= 0 and d1 >= 0:
                            r_min = root**a
                            c_min = (a, b, c, d2, d1)
                            i_min = index
        s += "\n\n"
    return r_min, c_min, i_min, s

def get_min_coeff_double_node(N, interval, starting_points):
    r_min = 10000
    c_min = ()
    i_min = 0
    s = ""
    for e1 in range(N+1):
        for e2 in range(N+1):
            for e3 in range(N+1):
                for e4 in range(N+1):
                    a  = e1/(N*interval)+starting_points[0]-1/(2*interval)
                    b  = e2/(N*interval)+starting_points[1]-1/(2*interval)
                    c  = e3/(N*interval)+starting_points[2]-1/(2*interval)
                    d = e4/(N*interval)+starting_points[3]-1/(2*interval)
                    root, index = get_max_root([[1,a,b,0], [c,d,0], [0,0]], get_list_double_node)
                    if root < r_min:
                        r_min = root
                        c_min = (a, b, c, d)
                        i_min = index
        s += "\n\n"
    return r_min, c_min, i_min, s

"""interval = 3
starting = [0.7, 0.4, 0.5, 0.3, 0.3, 0.2]
print(starting)
for i in range(10):
    print("Now finding at precision %d digits at starting points %s"%(log(interval, 10), str(starting)))
    r_min1, c_min1, i_min1, s, r_min2, c_min2, i_min2, c = get_min_coeff(8, interval, starting)
    print("We got:")
    print("Roots: %.5f, %.5f. Giving a final algo in 2^(%.20f n)"%(r_min1, r_min2, log(r_min1, 2)+log(r_min2, 2)))
    print("With the coefficients %s"%(str(c_min1) + str(c_min2)))
    print("")
    starting = c_min1+c_min2
    interval *= 1.8

#r_min1, c_min1, i_min1, s, r_min2, c_min2, i_min2, c = get_min_coeff(10, interval, starting)
print(r_min1, c_min1, i_min1)
print(r_min2, c_min2, i_min2, c)
print(log(r_min1, 2)+log(r_min2, 2))"""

interval = 1
starting = [0.5, 0.5, 0.5, 0.5, 0.5]
for i in range(20):
    #print("Now finding at precision %d digits at starting points %s"%(log(interval, 10), str(starting)))
    r_min1, c_min1, i_min1, s = get_min_coeff_double(6, interval, starting)
    print("We got:")
    print("Root: %.5f. Giving a final algo in 2^(%.20f n)"%(r_min1, log(r_min1, 2)))
    print("With the coefficients %s"%(str(c_min1)))
    print("")
    starting = c_min1
    interval *= 2
r_min1, c_min1, i_min1, s = get_min_coeff_double(8, interval, starting)
print(r_min1, c_min1, i_min1)
print(log(r_min1, 2))


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


































