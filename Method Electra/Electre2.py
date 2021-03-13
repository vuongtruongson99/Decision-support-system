from collections import defaultdict
import queue

alternatives = []
weight_crit = []

# Formated output alternative
def print_alternative(alternatives):
    row_format = "{:^15} |" + "{:^18} | " * (len(alternatives[0][1]) + len(alternatives[0][2]))
    for alternative in alternatives:
        al = [alternative[i][j] for i in range(len(alternative)) for j in range(len(alternative[i]))]
        print(row_format.format(*al))

def input_data():
    fa = open("data/input.txt", "r")
    for line in fa:
        alter = []
        alternative = line.strip("\n").split("|")
        for criterion in alternative:
            alter.append(criterion.split(";"))
        alternatives.append(alter)

    fw = open("data/weight.txt", "r")
    for line in fw:
        w = line.strip("\n").split("|")
        for criterion in w:
            weight_crit.append(criterion.split(";"))

def cal_D(alternatives):
    c_alternatives = alternatives.copy()
    tag = c_alternatives.pop(0)
    D = [[0 for x in range(len(c_alternatives))] for y in range(len(c_alternatives))]
    
    for i in range(0, len(c_alternatives)):
        for j in range(0, len(c_alternatives)):
            P = 0
            N = 0
            if i == j:
                continue
            for pos_criterion in range(len(c_alternatives[i][1])):
                if float(c_alternatives[i][1][pos_criterion]) > float(c_alternatives[j][1][pos_criterion]):
                    P += float(weight_crit[0][pos_criterion])
                elif float(c_alternatives[i][1][pos_criterion]) < float(c_alternatives[j][1][pos_criterion]):
                    N += float(weight_crit[0][pos_criterion])

            for neg_criterion in range(len(c_alternatives[i][2])):
                if float(c_alternatives[i][2][neg_criterion]) < float(c_alternatives[j][2][neg_criterion]):
                    P += float(weight_crit[1][neg_criterion])     
                elif float(c_alternatives[i][2][neg_criterion]) > float(c_alternatives[j][2][neg_criterion]):
                    N += float(weight_crit[1][neg_criterion])
                    
            if N == 0:
                continue
            elif P == 0:
                D[i][j] = float("inf")
            
            if P/N < 1:
                continue
            else:
                D[i][j] = P/N
    return D

def get_graph(mD, C):
    G = defaultdict(list)
    V = len(mD)

    for i in range(0, len(mD)):
        for j in range(0, len(mD[0])):
            if mD[i][j] > C:
                G[i].append(j)
    return G

def cyclic(g):
    path = set()
    visited = set()

    def visit(vertex):
        if vertex in visited:
            return False
        visited.add(vertex)
        path.add(vertex)
        for neighbour in g.get(vertex, ()):
            if neighbour in path or visit(neighbour):
                return True
        path.remove(vertex)
        return False

    return any(visit(v) for v in g)

def remove_circle(mD):
    lst = []
    for i in range(len(D)):
        for j in range(len(D[0])):
            if D[i][j] > 0:
                lst.append(D[i][j])
    lst = sorted(lst)

    for i in lst:
        graph = get_graph(D, i)
        
        if cyclic(graph) == True:
            continue
        else:
            return graph

def level_graph(G, V, x):
    level = [None] * V
    que = queue.Queue()
    que.put(x)
    level[x] = 0

    while(not que.empty()):
        x = que.get()
        for i in range(len(G[x])):
            b = G[x][i]
            que.put(b)
            level[b] = level[x] + 1
    ans = []
    for i in range(V):
        l = []
        l.append(alternatives[i+1][0])
        l.append(level[i])
        ans.append(l)
    ans.sort(key = lambda x : x[1])
    return ans


input_data()
D = cal_D(alternatives)
g = remove_circle(D)
ans = level_graph(g, 8, 0)

print("Alternatives: ")
print_alternative(alternatives)
print("\n")
print("Final result:")
for index, alternative in enumerate(ans):
    print(str(index + 1) + " - " + alternative[0][0])