fa = open("data/function1.txt")

minmax = str(fa.readline().replace("\n", ""))
C = list(map(int, fa.readline().split()))
B = list(map(int, fa.readline().split()))
A = []
for f in fa:
    A.append(list(map(int, f.split())))

print(minmax == "MIN")
print("MIN")