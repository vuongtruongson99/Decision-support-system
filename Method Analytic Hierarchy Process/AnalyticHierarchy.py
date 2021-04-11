import json

RCI_TABLE = [0.00, 0.00, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49, 1.51, 1.48, 1.56, 1.57, 1.59]

f = open("data/city.json")
data = json.load(f)

criteria = data["criteria"]
alternatives = data["alternatives"]
preferenceMatrices = data["preferenceMatrices"]

def print_table():
    for index, key in enumerate(preferenceMatrices):
        if index == 0:
            row_format = "{:^15} |" + "{:^20} |" * len(criteria)
            print(row_format.format(key, *criteria))
            for index, val in enumerate(preferenceMatrices[key]):
                print(row_format.format(criteria[index], *val))
            print("-"*127)         
        else:
            row_format = "{:^15} |" + "{:^20} |" * len(alternatives)
            print(row_format.format(key, *alternatives))
            for index, val in enumerate(preferenceMatrices[key]):
                print(row_format.format(alternatives[index], *val))
            print("-"*127)  

def cal_priority_vector():
    ans = []
    for key, vals in preferenceMatrices.items():
        S = 0
        W = []
        V = []
        for val in vals:
            x = 1
            for v in val:
                x *= v
            x = pow(x, (1/len(val)))
            S += x
            V.append(x)
        for index, val in enumerate(vals):
            w = V[index] / S
            W.append(w)
        ans.append(W)
    return ans

def check_acceptable():
    ans = []
    for index, key in enumerate(preferenceMatrices):
        lamda = 0
        for j in range(len(preferenceMatrices[key][0])):
            S = 0
            for i in range(len(preferenceMatrices[key])):
                S += preferenceMatrices[key][i][j]
            P = S * W[index][j]
            lamda += P
        IC = (lamda - len(preferenceMatrices[key])) / (len(preferenceMatrices[key]) - 1)
        OC = IC / RCI_TABLE[4]
        ans.append(OC)
   
    check = False
    for index, val in enumerate(ans):
        if val > 0.1:
            check = True
            for indexM, val in enumerate(preferenceMatrices):
                if index == indexM:
                    print("Matrix " + val + " is not acceptable! Please change value of matrix!")
    if check:
        return True


print_table()
W = cal_priority_vector()
priority = []
if not check_acceptable():
    print("All matrix are acceptable!")
    for i in range(len(W[1])):
        w = 0
        for j in range(len(W[0])):
            w += W[0][j] * W[j + 1][i]    
        priority.append(w)

    for index, key in enumerate(alternatives):
        print(key + " has priority: " + str(priority[index]))
    