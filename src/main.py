from a_star import a_star
from grid_gen import grid
from theta_star import theta_star
from interface import *

def algo_choice(file_path):
    run = True
    while run:
        algo = input("Enter 'a' for A* or 'theta' for Theta* or 'stop' to end the program: ")
        if algo == 'a':
            star_a = a_star(file_path)
            print("Source node is: {}".format(star_a.start))
            print("Goal node is: {}".format(star_a.end))
            print("Path from A* is:")
            graph(star_a)
        elif algo == 'theta':
            star_theta = theta_star(file_path)
            print("Source node is: {}".format(star_theta.start))
            print("Goal node is: {}".format(star_theta.end))
            print("Path from Theta* is:")
            graph(star_theta)
        elif algo == 'stop':
            run = False
        else:
            print("Incorrect input")

print("For random grid, type '1'")
print("To input a custom grid, type '2'")
inp = input("Choose the input method: ")
if inp == '1':
    val_x = input("Enter an X dimension: ")
    val_y = input("Enter a Y dimension: ")
    grid([int(val_x), int(val_y)])
    algo_choice("test.txt")
elif inp == '2':
    path = input("Enter your file path: ")
    algo_choice(path)
else:
    print("Incorrect input")
