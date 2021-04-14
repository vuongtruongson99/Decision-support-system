import operator
from copy import copy, deepcopy

fa = open("data/function1.txt")

minmax = str(fa.readline().replace("\n", ""))
C = list(map(int, fa.readline().split()))
B = list(map(int, fa.readline().split()))
A = []
for f in fa:
    A.append(list(map(int, f.split())))

if minmax == "MIN":
    print("-------------------")
    for i in range(0, len(C)):
        C[i] = (-1) * C[i]


print(C)

Cb = [0] * len(A)   
F = [None] * (len(C))
Q = 0

Basic = []
Non_basic = []
for i in range(len(C)):
    Non_basic.append("x" + str(i + 1))

for i in range(len(A)):
    Basic.append("x" + str(i + len(C) + 1))


def printTable(Basic, Non_basic, C, B, A, Cb, F, Q):
    print("\t C", end="\t")
    for c in C:
        print(c, end="\t")
    print()
    print("Cb \t\t", end ="")
    for non_basic in Non_basic:
        print(non_basic, end="\t")
    print("B")

    for i in range(len(A)):
        print(Cb[i], end="\t")
        print(Basic[i], end="\t")
        for j in range(len(C)):
            print(A[i][j], end="\t")
        print(B[i])

    print("\t F", end = "\t")
    for f in F:
        print(f, end = "\t")
    print(Q)

print("Starting Table:")
printTable(Basic, Non_basic, C, B, A, Cb, F, Q)

for f in range(len(F)):
    a = list(map(operator.itemgetter(f), A))
    S = 0
    for i in range(len(Cb)):
        S += (Cb[i] * a[i])
    F[f] = S - C[f]

for i in range(len(Cb)):
    Q += (Cb[i] * B[i])


iter = 1
check2 = False
while(True):

    print("----------------------------------")
    print("Iteration :", iter)
    printTable(Basic, Non_basic, C, B, A, Cb, F, Q)
    Q_old = Q

    for f in range(len(F)):
        a = list(map(operator.itemgetter(f), A))
        S = 0
        for i in range(len(Cb)):
            S += (Cb[i] * a[i])
        F[f] = S - C[f]

    for i in range(len(Cb)):
        Q += (Cb[i] * B[i])

    printIter = False
    for f in F:
        if f < 0:
            printIter = True

    if not printIter:
        Q = Q_old
        break

    min_f = min(F)
    print("Pivot Column: " + Non_basic[F.index(min_f)])

    r_min = float("inf")
    row = 0
    check = False
    for i in range(0, len(A)):
        if A[i][F.index(min_f)] == 0:
            continue
        else:
            r = B[i] / A[i][F.index(min_f)]
            #print(r)
            if (r > 0 and r < r_min):
                r_min = r
                row = i
                check = True
    if check == False:
        print("Cannot solve this problem!")
        check2 = True
        break

    print("Pivot Row: " + Basic[row])
    print("Pivot Element: " + str(A[row][F.index(min_f)]))

    # Swap basic and non-basic of pivot row and col
    c_old = C[F.index(min_f)]
    C[F.index(min_f)] = Cb[row]
    Cb[row] = c_old

    non_basic_old = Non_basic[F.index(min_f)]
    Non_basic[F.index(min_f)] = Basic[row]
    Basic[row] = non_basic_old

    A_new = deepcopy(A)
    B_new = B.copy()
    pivot_ele = A[row][F.index(min_f)]

    # Calculate new matrix
    for i in range(0, len(A)):
        for j in range(0, len(A[0])):
            if i == row:
                if j == F.index(min_f):
                    A[i][j] = 1 / pivot_ele
                else:
                    A[i][j] = A_new[i][j] / pivot_ele
            elif j == F.index(min_f):
                A[i][j] = -1 * (A_new[i][j] / pivot_ele)
            else:
                A[i][j] = (A_new[i][j] * pivot_ele) - (A_new[i][F.index(min_f)] * A_new[row][j])
                A[i][j] /= pivot_ele

        if i == row:
            B[i] = B_new[i] / pivot_ele
        else:
            B[i] = (B_new[i] * pivot_ele) - (A_new[i][F.index(min_f)] * B_new[row])
            B[i] /= pivot_ele

    F_new = F.copy()
    for i in range(len(F)):
        if i == F_new.index(min_f):
            F[i] = -1 * (F_new[i] / pivot_ele)
        else:
            F[i] = (F_new[i] * pivot_ele) - (A_new[row][i] * F_new[F_new.index(min_f)])
            F[i] /= pivot_ele

    Q = 0
    for i in range(len(Cb)):
        Q += (Cb[i] * B[i])

    iter += 1

if check2 == False:
    print("----------------------------------")
    print("Final Table reached in", iter, "iterations")
    print("Coefficients: ")
    for i in range(len(Basic)):
        if Cb[i] != 0:
            print("\t" + Basic[i] + ": " + str(B[i]))
    print("Optimal value: " + str(Q))