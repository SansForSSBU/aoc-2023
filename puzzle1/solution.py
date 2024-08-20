total = 0
with open("input") as f:
    lines=f.read().split("\n")
    for line in lines:
        first = "0"
        last = "0"
        for i in range(len(line)):
            if line[i].isdigit():
                first = line[i]
                break

        for i in range(len(line)):
            if line[-(i+1)].isdigit():
                last = line[-(i+1)]
                break
        num = int(first+last)
        print(line)
        print(num)
        total += num

print(total)