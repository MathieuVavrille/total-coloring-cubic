import sys

def order(e1, e2):
    """reordering of elements such that they have always the same order"""
    if e2 < e1:
        return e2, e1
    return e1, e2

def edge_name(e1, e2):
    """generale identifier of an edge in a dictionnary"""
    e1, e2 = order(e1, e2)
    return (e1,e2)

def compare(e1, e2):
    """comparison between elements, used to have an order in nodes+edges"""
    if type(e1) == type(e2) == type((2,3)):
        return e1 < e2
    elif type(e1) == type((2,3)):
        return True
    elif type(e2) == type((2,3)):
        return False
    else:
        return e1 < e2

def project_dict(full_col, base):
    """extract the coloration of the base in the full coloration full_col"""
    res = {}
    for (k, v) in full_col.items():
        if k in base:
            res[k] = v
    return res

def project_enum(enumeration, base):
    """get all the possibilities of coloration of the base, given an enumeration of colorations"""
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
    
    def allowed_colors_node(self, e):
        """return the list of allowed colors for a node"""
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
        """return the list of allowed colors for an edges"""
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
        """return the list of allowed colors for an element"""
        if type(elt) == type("a"):
            return self.allowed_colors_node(elt)
        else:
            e1, e2 = elt
            return self.allowed_colors_edge(e1, e2)
    
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
    
    def find_blank(self):
        """find an element that is not colored"""
        current_best = ""
        for (k, v) in self.color.items():
            if v == -1 and (compare(k, current_best) or current_best == ""):
                current_best = k
        if current_best != "":
            return current_best
    
    def enumerate_coloration(self):
        """enumerate all the possible colorations of the graph"""
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
simple = ColoredGraph()
simple2 = ColoredGraph()



for n in ["a", "b", "c", "e", "f", "g"]:#, "k", "l", "m", "n"]:
    simple.add_node(n)
    
for n in ["a", "b", "c", "e", "f", "g"]:#, "k", "l", "m", "n"]:
    simple2.add_node(n)

for n in ["a", "b", "c", "d", "e", "f"]:#, "k", "l", "m", "n"]:
    test.add_node(n)



test.add_edge("a", "b")
test.add_edge("b", "c")
test.add_edge("b", "d")
test.add_edge("c", "d")
test.add_edge("c", "e")
test.add_edge("d", "e")
test.add_edge("e", "f")

simple.add_edge("a", "c")
simple.add_edge("b", "c")
simple.add_edge("e", "f")
simple.add_edge("e", "g")

simple2.add_edge("a", "c")
simple2.add_edge("b", "c")
simple2.add_edge("c", "e")
simple2.add_edge("e", "f")
simple2.add_edge("e", "g")


max_found = 0
total = 0
test.add_coloration_node("a", 0)
test.add_coloration_edge("a","b", 1)
#simple.add_coloration_node("a", 0)
#simple.add_coloration_edge("a","c", 1)
for i in range(4):
    test.add_coloration_node("f", i)
    for j in test.allowed_colors_edge("f", "e"):
        test.add_coloration_edge("f", "e", j)
        res = test.enumerate_coloration()
        if len(res) == 0:
            print(j, i)
        test.add_coloration_edge("f", "e", -1)
"""for i in range(4):
    test.add_coloration_node("b", i)
    simple.add_coloration_node("b", i)
    simple2.add_coloration_node("b", i)
    for j in test.allowed_colors_edge("b", "c"):
        test.add_coloration_edge("b", "c", j)
        simple.add_coloration_edge("b", "c", j)
        simple2.add_coloration_edge("b", "c", j)
        for k in range(4):
            test.add_coloration_node("f", k)
            simple.add_coloration_node("f", k)
            simple2.add_coloration_node("f", k)
            for l in test.allowed_colors_edge("f", "e"):
                test.add_coloration_edge("f", "e", l)
                simple.add_coloration_edge("f", "e", l)
                simple2.add_coloration_edge("f", "e", l)
                for m in range(4):
                    test.add_coloration_node("g", m)
                    simple.add_coloration_node("g", m)
                    simple2.add_coloration_node("g", m)
                    for n in test.allowed_colors_edge("e", "g"):
                        total += 1
                        test.add_coloration_edge("e", "g", n)
                        simple.add_coloration_edge("e", "g", n)
                        simple2.add_coloration_edge("e", "g", n)
                        res = test.enumerate_coloration()
                        res2 = simple.enumerate_coloration()
                        res3 = simple2.enumerate_coloration()
                        if len(res) != 0 and  len(res3) != 0:
                            print(i ,j, k, l, "ttttttttt")
                            max_found += 1
                        test.add_coloration_edge("e", "g", -1)
                        simple.add_coloration_edge("e", "g", -1)
                        simple2.add_coloration_edge("e", "g", -1)
                    test.add_coloration_node("g", -1)
                    simple.add_coloration_node("g", -1)
                    simple2.add_coloration_node("g", -1)
                test.add_coloration_edge("f", "e", -1)
                simple.add_coloration_edge("f", "e", -1)
                simple2.add_coloration_edge("f", "e", -1)
            test.add_coloration_node("f", -1)
            simple.add_coloration_node("f", -1)
            simple2.add_coloration_node("f", -1)
        test.add_coloration_edge("b", "c", -1)
        simple.add_coloration_edge("b", "c", -1)
        simple2.add_coloration_edge("b", "c", -1)"""
print(max_found)
print(total)

































