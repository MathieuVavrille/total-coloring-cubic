import numpy as np

precision = 0.000001

def find_root(a, b):
    """Uses Newton's iteration to find the biggest zero of the function"""
    #print("beginning of Newton")
    #print(a, b)
    if a > b:
        a,b = b,a
    xnm = 2
    xn = 1
    while xnm - xn > precision:
        #print(xn)
        xnm, xn = xn, xn - (1-xn**(-b) - xn**(-a))/(a*xn**(a+1) + b*xn**(b+1))
    return xn

def get_list_recurrence(a2, a1):
    return [(2-2*a2, 6-4*a2), (2-2*a2, 5-2*a2-a1), (2-2*a2, 4-2*a1), (2-2*a2, 3+2*a2-3*a1), #4
            (2-2*a2, 2+4*a2-4*a1), (2-2*a2, 5-3*a2+a1), (2-2*a2, 4-a2), (2-2*a2, 3+a2-a1), #7
            (2-2*a2, 2+3*a2-2*a1), (2-2*a2, 4+2*a1-2*a2), (2-2*a2, 3+a1), #10
            (2-2*a2, 2+2*a2), (2-2*a2, 3+3*a1-a2), (2-2*a2, 2+a2+2*a1), (2-2*a2, 2+4*a1), #14
            (1-a1, 2-2*a2+2*a1), (1-a1, 1+4*a2-3*a1), (1-a1, 2+a2), (1-a1, 1+3*a2-a1), (1-a1, 2+2*a1), (1-a1, 1+2*a2+a1), (1-a1, 1+3*a1),
            (2*a2-2*a1, 4*a2-2*a1), (2*a2-2*a1, 3*a2), (2*a2-2*a1, 2*a2+2*a1)]
        
def get_max_root(a2, a1):
    r_max = 0
    i_max = 0
    l = get_list_recurrence(a2, a1)
    all_roots = []
    for i in range(len(l)):
        root = find_root(l[i][0], l[i][1])
        #print(i, root, l[i][0], l[i][1])
        all_roots.append((root, i))
        if root > r_max:
            r_max = root
            i_max = i
    return r_max, sorted(all_roots)


def get_min_coeff(N):
    r_min = 100
    c_min = ()
    i_min = 0
    s = ""
    for e2 in range(N):
        for e1 in range(N):
            a2 = e2/N
            a1 = e1/N
            if a2 > a1:
                root, index = get_max_root(a2, a1)
            else:
                root, index = 10000, []
            s += " (%f, %f, %.4f)"%(a1/100, a2/100, 1/root) 
            if root**((1+3*a2)/4) < r_min:
                r_min = root**((1+3*a2)/4)
                c_min = (a2, a1)
                i_min = index
        s += "\n\n"
    return r_min, c_min, i_min, s

r_min, c_min, i_min, s = get_min_coeff(10)
print(r_min, c_min, i_min)

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


































