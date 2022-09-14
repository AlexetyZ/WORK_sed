import os
import random
print(len(os.listdir()))
print(random.Random().seed(os.listdir()))

num = [2, 4, 6, 8, 10, 12]
print(num[::-1])
for i in range(2):
    with open(f'autoself{i}.py', 'w') as file:
        file.write('#!/usr/bin/python;\nimport os\nprint(os.listdir())\nos.remove(__file__)')