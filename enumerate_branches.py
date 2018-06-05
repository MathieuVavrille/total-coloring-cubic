import sys

def order(e1, e2):
    if e2 < e1:
        return e2, e1
    return e1, e2

def edge_name(e1, e2):
    e1, e2 = order(e1, e2)
    return (e1,e2)

def compare(e1, e2):
    if type(e1) == type(e2) == type((2,3)):
        return e1 < e2
    elif type(e1) == type((2,3)):
        return True
    elif type(e2) == type((2,3)):
        return False
    else:
        return e1 < e2

def project_dict(d, base):
    res = {}
    for (k, v) in d.items():
        if k in base:
            res[k] = v
    return res

def project_enum(enumeration, base):
    l = []
    for d in enumeration:
        pruned = project_dict(d, base)
        if not pruned in l:
            l.append(pruned)
    return l

class ColoredGraph():
    
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.color = {}
    
    def add_node(self, e):
        if e in self.nodes.keys():
            raise ValueError("Node " + e + " already existing")
        self.nodes[e] = []
        self.color[e] = -1
    
    def add_edge(self, e1, e2):
        self.edges.append(edge_name(e1, e2))
        self.nodes[e1].append(e2)
        self.nodes[e2].append(e1)
        self.color[edge_name(e1, e2)] = -1
    
    def add_coloration_node(self, e, col):
        if col < 0 or col in self.allowed_colors_node(e):
            self.color[e] = col
        else:
            raise ValueError("Color illegal")
    
    def add_coloration_edge(self, e1, e2, col):
        if col < 0 or col in self.allowed_colors_edge(e1, e2):
            self.color[edge_name(e1, e2)] = col
        else:
            raise ValueError("Color illegal")
    
    def allowed_colors_node(self, e):
        l = []
        for i in range(4):
            allowed = True
            for f in self.nodes[e]:
                if self.color[f] == i:
                    allowed = False
                if self.color[edge_name(e, f)] == i:
                    allowed = False
            if allowed:
                l.append(i)
        return l
    
    def allowed_colors_edge(self, e1, e2):
        l = []
        for i in range(4):
            allowed = True
            for f in self.nodes[e1]:
                if self.color[edge_name(e1, f)] == i:
                    allowed = False
            for f in self.nodes[e2]:
                if self.color[edge_name(e2, f)] == i:
                    allowed = False
            if self.color[e1] == i or self.color[e2] == i:
                allowed = False
            if allowed:
                l.append(i)
        return l
    
    def allowed_colors(self, elt):
        if type(elt) == type("a"):
            return self.allowed_colors_node(elt)
        else:
            e1, e2 = elt
            return self.allowed_colors_edge(e1, e2)
    
    def find_blank(self):
        current_best = ""
        for (k, v) in self.color.items():
            if v == -1 and (compare(k, current_best) or current_best == ""):
                current_best = k
        if current_best != "":
            return current_best
    
    def enumerate_coloration(self):
        s = self.find_blank()
        if s == None:
            return [self.color.copy()]
        else:
            rec_res = []
            for col in self.allowed_colors(s):
                self.color[s] = col
                rec_res += self.enumerate_coloration()
            self.color[s] = -1
            return rec_res





test = ColoredGraph()
for n in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p"]:
    test.add_node(n)

test.add_edge("a", "b")
test.add_edge("a", "c")
test.add_edge("c", "d")
test.add_edge("c", "e")
test.add_edge("e", "f")
test.add_edge("e", "g")
test.add_edge("g", "h")
test.add_edge("g", "i")
test.add_edge("i", "j")
test.add_edge("i", "k")
test.add_edge("k", "l")
test.add_edge("k", "m")
test.add_edge("m", "n")
#test.add_edge("m", "o")
#test.add_edge("o", "p")
max_found = 0
l = []
test.add_coloration_node("b", 0)
test.add_coloration_edge("a","b", 1)
for i in range(4):
    test.add_coloration_node("n", i)
    for j in test.allowed_colors_edge("m", "n"):
        test.add_coloration_edge("m", "n", j)
        res = test.enumerate_coloration()
        proj = project_enum(res, ["c", edge_name("c","d"), "e", edge_name("e","f"), "g", edge_name("g", "h"), "i", edge_name("i", "j"), "k", edge_name("k", "l")])
        print(len(proj))
        l.append(len(proj))
        if len(proj) > max_found:
            max_found = len(proj)
        test.add_coloration_edge("m","n", -1)
print(max_found)
"""
Maximize p = 0a0 + 0am + 3a1 + 3.322a2 + 3.585a3 + 5.17b1 + 6.13b2 + 6.4b3 + 8.54g3 + 10.574g4 + 12.5822g5 + 3.585d1 + 3.322d21 + 6.4d22 + 3.585d31 + 5.9542d32 + 8.54d33 subject to
d1 + d21 + 2d22 + d31 + 2d32 + 3d33 + 3g3 + 4g4 + 5g5 - am = 0
d1 + d21 + d22 + d31 + d32 + d33 - a0 = 0
a1 + b1 + d21 + d32 + 2d31 - am <= 0
2a3 + a2 + 2b3 + b2 - a0 <= 0
am + a0 + a1 + a2 + a3 + 2b1 + 2b2 + 2b3 = 1

Maximize p = 0am + 3a + 5.17b + 7.11c + 9.077d + 11.69e + 14.5843g6 subject to
2b + 3c + 4d + 5e + 6g6 - am = 0
2a + b + c + d + e - am <= 0
am + a = 1

Maximize p = 0am + 3a + 5.17b + 7.11c + 9.077d + 12.582142g5 subject to
2b + 3c + 4d + 5g5 - am = 0
2a + b + c + d - am <= 0
am + a = 1

Maximize p = 3a + 5.17b + 7.11c + 9.077d + 11.69e + 13.81f + 16.585g7 subject to
f - 7g7 <= 0
e - 6f - 7g7 <= 0
d - 5e - 6f - 7g7 <= 0
c - 4d - 5e - 6f - 7g7 <= 0
b - 3c - 4d - 5e - 6f - 7g7 <= 0
2a - 2b - 3c - 4d - 5e - 6f - 7g7 <= 0
a + 2b + 3c + 4d + 5e + 6f + 7g7 = 1

Maximize p = 3a + 5.17b + 7.11c + 9.077d + 11.69e + 13.81f + 15.81g7 + 16.585g8 subject to
g7 - 8g8 <= 0
f - 7g7 - 8g8 <= 0
e - 6f - 7g7 - 8g8 <= 0
d - 5e - 6f - 7g7 - 8g8 <= 0
c - 4d - 5e - 6f - 7g7 - 8g8 <= 0
b - 3c - 4d - 5e - 6f - 7g7 - 8g8 <= 0
2a - 2b - 3c - 4d - 5e - 6f - 7g7 - 8g8 <= 0
a + 2b + 3c + 4d + 5e + 6f + 7g7 + 8g8 = 1

Maximize p = 0y + 0z + 3a1 + 5.17a2 + 7.11a3 + 9.077a4 + 11.69a5 + 13.807a6 + 3.322b1 + 5.7b2 + 7.78b3 + 9.8b4 + 11.806b5 + 13.807b6 + 3.585c1 + 6.4c2 + 8.54c3 + 10.574c4 + 12.58c5 + 14.584c6 + 3.585ch3 + 6.4ch4 + 8.54ch5 + 10.574ch6 + 16.5848d subject to
ch3 + ch4 + ch5 + ch6 - y = 0
1.5b2 + 2.5b3 + 3.5b4 + 4.5b5 + 5.5b6 + 2c2 + 3c3 + 4c4 + 5c5 + 6c6 + 7d + ch3 + 2ch4 + 3ch5 + 4ch6 - z = 0
2c1 + 2c2 + 2c3 + 2c4 + 2c5 + 2c6 + b1 + b2 + b3 + b4 + b5 + b6 - 2y <= 0
a6 - z <= 0
a5 - z - 5a6 <= 0
a4 - z - 5a6 - 4a5 <= 0
a3 - z - 5a6 - 4a5 -3a4 <= 0
a2 - z - 5a6 - 4a5 -3a4 -2a3 <= 0
2a1 - z - 5a6 - 4a5 -3a4 -2a3 - a2 <= 0
y + z + b1 + c1 + a1 + 2a2 + 3a3 + 4a4 + 5a5 + 6a6 = 1

Maximize p = 0y + 0z + 3a1 + 5.17a2 + 7.11a3 + 9.077a4 + 11.69a5 + 13.807a6 + 3.322b1 + 5.7b2 + 7.78b3 + 9.8b4 + 11.806b5 + 3.585c1 + 6.4c2 + 8.54c3 + 10.574c4 + 12.58c5 + 3.585ch3 + 6.4ch4 + 8.54ch5 + 10.574ch6 + 16.5848d subject to
ch3 + ch4 + ch5 + ch6 - y = 0
4c1 + 2c2 + 2c3 + 2c4 + 2c5 + 2c6  b1 + b2 + b3 + b4 + b5 - y <= 0
7d + ch3 + 2ch4 + 3ch5 + 4ch6 + 2c2 + 3c3 + 4c4 + 5c5 + 6c6 - z = 0
b5 - 2z <= 0
b4 - 2z - 9b5 <= 0
b3 - 2z - 9b5 - 7b4 <= 0
b2 - 2z - 9b5 - 7b4 - 5b3 <= 0
2b1 - 2z - 9b5 - 7b4 - 5b3 - 3b2 <= 0
0.5b1 + 1.5b2 + 2.5b3 + 3.5b4 + 4.5b5 - z2 = 0
a6 - z2 <= 0
a5 - z2 - 5a6 <= 0
a4 - z2 - 5a6 - 4a5 <= 0
a3 - z2 - 5a6 - 4a5 -3a4 <= 0
a2 - z2 - 5a6 - 4a5 -3a4 -2a3 <= 0
2a1 - z2 - 5a6 - 4a5 -3a4 -2a3 - a2 <= 0
y + z + b1 + 2b2 + 3b3 + 4b4 + 5b5 + c1 + a1 + 2a2 + 3a3 + 4a4 + 5a5 + 6a6 = 1

Maximize p = 0y + 0z + 0z2 + 3a1 + 5.17a2 + 7.11a3 + 9.077a4 + 11.69a5 + 13.807a6 + 3.322b1 + 5.7b2 + 7.78b3 + 9.8b4 + 11.806b5 + 3.585c1 + 6.4c2 + 8.54c3 + 10.574c4 + 12.58c5 + 3.585ch3 + 6.4ch4 + 8.54ch5 + 10.574ch6 + 16.5848d + 3e3 + 3.7e4 + 6.644e5 + 8.155e6 subject to
ch3 + ch4 + ch5 + ch6 - y = 0
4c1 + 2c2 + 2c3 + 2c4 + 2c5 + 2c6 + b1 + b2 + b3 + b4 + b5 - y <= 0
7d + ch3 + 2ch4 + 3ch5 + 4ch6 + 2c2 + 3c3 + 4c4 + 5c5 + 6c6 + 3e3 + 4e4 + 5e5 + 6e6 - z = 0
b5 - 2z <= 0
b4 - 2z - 9b5 <= 0
b3 - 2z - 9b5 - 7b4 <= 0
b2 - 2z - 9b5 - 7b4 - 5b3 <= 0
2b1 - 2z - 9b5 - 7b4 - 5b3 - 3b2 <= 0
0.5b1 + 1.5b2 + 2.5b3 + 3.5b4 + 4.5b5 - z2 = 0
a6 - z2 <= 0
a5 - z2 - 5a6 <= 0
a4 - z2 - 5a6 - 4a5 <= 0
a3 - z2 - 5a6 - 4a5 -3a4 <= 0
a2 - z2 - 5a6 - 4a5 -3a4 -2a3 <= 0
2a1 - z2 - 5a6 - 4a5 -3a4 -2a3 - a2 <= 0
y + z + b1 + 2b2 + 3b3 + 4b4 + 5b5 + c1 + a1 + 2a2 + 3a3 + 4a4 + 5a5 + 6a6 = 1


Maximize p = 0y + 0z + 0z2 + 3a1 + 5.17a2 + 7.11a3 + 9.077a4 + 11.69a5 + 13.807a6 + 3.322b1 + 5.7b2 + 7.78b3 + 9.8b4 + 11.806b5 + 3.585c1 + 6.4c2 + 8.54c3 + 10.574c4 + 12.58c5 + 3.585ch3 + 6.4ch4 + 8.54ch5 + 10.574ch6 + 16.5848d + 3e3 + 3.7e4 + 6.644e5 + 8.155e6 subject to
ch3 + ch4 + ch5 + ch6 - y = 0
4c1 + 2c2 + 2c3 + 2c4 + 2c5 + 2c6 + b1 + b2 + b3 + b4 + b5 - y <= 0
7d + ch3 + 2ch4 + 3ch5 + 4ch6 + 2c2 + 3c3 + 4c4 + 5c5 + 6c6 + 3e3 + 4e4 + 5e5 + 6e6 - z = 0
b5 - 2z <= 0
b4 - 2z - 9b5 <= 0
b3 - 2z - 9b5 - 7b4 <= 0
b2 - 2z - 9b5 - 7b4 - 5b3 <= 0
2b1 - 2z - 9b5 - 7b4 - 5b3 - 3b2 <= 0
0.5b1 + 1.5b2 + 2.5b3 + 3.5b4 + 4.5b5 - z2 = 0
a6 - z2 <= 0
a5 - z2 - 2.5a6 <= 0
a4 - z2 - 2.5a6 - 2a5 <= 0
a3 - z2 - 5a6 - 2a5 - 1.5a4 <= 0
a2 - z2 - 5a6 - 4a5 - 1.5a4 - 1.5a3 <= 0
2a1 - z2 - 5a6 - 4a5 - 3a4 - 2a3 - 0.5a2 <= 0
y + z + b1 + 2b2 + 3b3 + 4b4 + 5b5 + c1 + a1 + 2a2 + 3a3 + 4a4 + 5a5 + 6a6 = 1

Optimal Solution: p = 2377/921; y = 4/809, z = 8/809, z2 = 10/809, a1 = 150/809, a2 = 200/809, a3 = 0, a4 = 0, a5 = 35/809, a6 = 10/809, b1 = 0, b2 = 0, b3 = 4/809, b4 = 0, b5 = 0, c1 = 0, c2 = 0, c3 = 0, c4 = 0, c5 = 0, ch3 = 0, ch4 = 4/809, ch5 = 0, ch6 = 0, d = 0, e3 = 0, e4 = 0, e5 = 0, e6 = 0

Maximize p = 0y + 0z + 0z2 + 3a1 + 5.17a2 + 7.11a3 + 9.077a4 + 11.69a5 + 13.807a6 + 15.807a7 + 3.322b1 + 5.7b2 + 7.78b3 + 9.8b4 + 11.806b5 + 13.807b6+ 3.585c1 + 6.4c2 + 8.54c3 + 10.574c4 + 12.58c5 + 3.585ch3 + 6.4ch4 + 8.54ch5 + 10.574ch6 + 12.58ch7 + 17.8d + 3e3 + 3.7e4 + 6.644e5 + 8.155e6 subject to
ch3 + ch4 + ch5 + ch6 +ch7 - y = 0
4c1 + 2c2 + 2c3 + 2c4 + 2c5 + 2c6 + b1 + b2 + b3 + b4 + b5 + b6 - y <= 0
8d + ch3 + 2ch4 + 3ch5 + 4ch6 + 5ch7 + 2c2 + 3c3 + 4c4 + 5c5 + 6c6 + 3e3 + 4e4 + 5e5 + 6e6 - z = 0
b6 - 2z <= 0
b5 - 2z - 11b6 <= 0
b4 - 2z - 11b6 - 9b5 <= 0
b3 - 2z - 11b6 - 9b5 - 7b4 <= 0
b2 - 2z - 11b6 - 9b5 - 7b4 - 5b3 <= 0
2b1 - 2z - 11b6 - 9b5 - 7b4 - 5b3 - 3b2 <= 0
0.5b1 + 1.5b2 + 2.5b3 + 3.5b4 + 4.5b5 + 5.5b6 + z - z2 = 0
a7 - z2 <= 0
a6 - z2 - 6a7 <= 0
a5 - z2 - 6a7 - 5a6 <= 0
a4 - z2 - 6a7 - 5a6 - 4a5 <= 0
a3 - z2 - 6a7 - 5a6 - 4a5 - 3a4 <= 0
a2 - z2 - 6a7 - 5a6 - 4a5 - 3a4 - 2a3 <= 0
2a1 - z2 - 6a7 - 5a6 - 4a5 - 3a4 - 2a3 - a2 <= 0
y + z + b1 + 2b2 + 3b3 + 4b4 + 5b5 + 6b6 + c1 + a1 + 2a2 + 3a3 + 4a4 + 5a5 + 6a6 + 7a7 = 1


"""



























