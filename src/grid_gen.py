import random
import math
from telnetlib import DM


class grid:
    
    def __init__(self, dimension): 
        self.generate(dimension)
    
    def generate(self, dimension):
        start = [random.randint(1, dimension[0]+1), random.randint(1, dimension[1]+1)]
        end = [random.randint(1, dimension[0]+1), random.randint(1, dimension[1]+1)]

        count = math.ceil(int((dimension[0]*dimension[1])*0.1))
        blocked = []
        for i in range(count):
           x,y = random.randint(1, dimension[0]), random.randint(1, dimension[1])
           blocked.append([x,y])
        
        with open('test.txt', 'w') as f:
            f.write(str(start[0]) + " " + str(start[1]) + '\n')
            f.write(str(end[0]) + " " + str(end[1]) + '\n')
            f.write(str(dimension[0]) + " " + str(dimension[1]) + '\n')

            for x in range(1, dimension[0]+1):
                for y in range(1, dimension[1]+1):
                    line = ""
                    line = line + str(x) + " " + str(y) + " "
                    if [x,y] in blocked:
                        line = line + "1\n"
                    else:
                        line = line + "0\n"
                    f.write(line)


    

