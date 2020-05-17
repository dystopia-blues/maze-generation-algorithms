import random

height = 4
width = 5
cell_list = set()
for i in range(width):
    for j in range(height):
        cell_list.add((i,j))

print(cell_list)

random.seed(1)

selected = random.sample(cell_list, 1)[0]
print(selected)

selected = random.sample(cell_list, 1)[0]
print(selected)

selected = random.sample(cell_list, 1)[0]
print(selected)
