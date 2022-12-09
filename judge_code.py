import sys
import os
import time
import math
import tracemalloc
from termcolor import colored

tracemalloc.start()

i = -1
out = ''

output_file = open('output.txt', 'w')
current_input = ''
test_output = ''
total_time = 0
total_memory = 0
times = []
max_total_score = 0
total_score = 0

wrong_answer = colored('WA', 'red')
accepted = colored('AC', 'green')


def dec_places(num):
    decimal_places = int(round(math.log(10 / num, 10))) + 2
    return f"{num:.{decimal_places}f}"


def print_mem(mem):
    mb = mem * 10 ** -3
    if mb > 1:
        return f"{mb:.2f} MB"
    else:
        return f"{mem:.2f} KB"


def input():
    global current_input
    test_input = current_input
    global i
    i += 1
    return test_input[i]


def main():
    n = int(input())
    for j in range(n):
        ab = input().split(" ")
        print(int(ab[0]) + int(ab[1]))


base_mem = 18720
for files in os.listdir('test_cases'):
    i = -1
    if files.endswith('.in'):
        tracemalloc.start()
        output_file = open('output.txt', 'w')
        current_input = open('test_cases/' + files, 'r').readlines()
        test_output = open('test_cases/' + files.replace('.in', '.out'), 'r').readlines()
        sys.stdout = output_file

        start_time = time.perf_counter()

        main()

        memory = tracemalloc.get_traced_memory()[1] - base_mem
        tracemalloc.stop()
        time_taken = time.perf_counter() - start_time

        total_memory += memory
        total_time += time_taken
        times.append(time_taken)
        output_file.close()
        sys.stdout = sys.__stdout__

        max_score = len(test_output)
        score = 0

        for i in range(len(test_output)):
            if test_output[i] == open('output.txt', 'r').readlines()[i]:
                score += 1

        max_total_score += max_score
        total_score += score

        if score == max_score:
            print(
                f"Test case {files.replace('.in' or '.out', '')}: {accepted} [{dec_places(time_taken)}s"
                f", {print_mem(memory)}] ({score}/{max_score})")
        else:
            print(
                f"Test case {files.replace('.in' or '.out', '')}: {wrong_answer} [{dec_places(time_taken)}s"
                f", {print_mem(memory)}] ({score}/{max_score})")

print(f"\nResources: {dec_places(total_time)}s, {print_mem(total_memory)}")
print(f"Maximum single-case runtime: {dec_places(max(times))}s")
print(f"Final score: {total_score}/{max_total_score}")
