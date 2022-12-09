def judge():
    n = int(input())
    x = []
    for i in range(n):
        x.append(int(input()))

    for i in range(n):
        for j in range(n - 1):
            if x[j] > x[j + 1]:
                x[j], x[j + 1] = x[j + 1], x[j]

    for i in x:
        print(i)


judge()
