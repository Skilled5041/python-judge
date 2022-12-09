import sys
import os
import time
import math
import tracemalloc
import json
from termcolor import colored

tracemalloc.start()

config = json.load(open("config.json"))
code_file = config["test_code"]
cases = config["test_cases_directory"]
memory_limit = config["memory_limit"]
time_limit = config["time_limit"]

i = -1
out = ''

output_file = open('output.txt', 'w')
current_input = ''
test_output = ''
total_time = 0
total_memory = []
times = []
max_total_score = 0
total_score = 0

wrong_answer = colored('WA', 'red')
accepted = colored('AC', 'green', attrs=['bold'])
timeout = colored('TLE', 'grey')
over_memory = colored('MLE', 'yellow', attrs=['bold'])


def dec_places(num):
    decimal_places = int(round(math.log(10 / num, 10))) + 2
    return f"{num:.{decimal_places}f}"


def print_mem(mem):
    mb = mem * 10 ** -3
    if mb > 1:
        return f"{mb:.2f} MB"
    else:
        return f"{mem:.2f} KB"


def input(*args):
    global current_input
    test_input = current_input
    global i
    i += 1
    return test_input[i]


def judge_code():
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


base_mem = 18720
print()
for files in os.listdir(cases):
    i = -1
    if files.endswith('.in'):
        tracemalloc.start()
        output_file = open('output.txt', 'w')
        current_input = open(f'{cases}/' + files, 'r').readlines()
        test_output = open(f'{cases}/' + files.replace('.in', '.out'), 'r').readlines()
        sys.stdout = output_file

        start_time = time.perf_counter()

        judge_code()

        memory = tracemalloc.get_traced_memory()[1] - base_mem
        tracemalloc.stop()
        time_taken = time.perf_counter() - start_time

        total_memory.append(memory)
        total_time += time_taken
        times.append(time_taken)
        output_file.close()
        sys.stdout = sys.__stdout__

        max_score = len(test_output)
        score = 0

        for i in range(len(test_output)):
            try:
                if test_output[i] == open('output.txt', 'r').readlines()[i]:
                    score += 1
            except IndexError:
                break

        max_total_score += max_score
        total_score += score

        if score == max_score and memory * 10 ** -3 < memory_limit and time_taken < time_limit:
            print(
                f"Test case {files.replace('.in' or '.out', '')}: {accepted} [{dec_places(time_taken)}s"
                f", {print_mem(memory)}] ({score}/{max_score})")
        elif score == max_score and memory * 10 ** -3 > memory_limit:
            print(
                f"Test case {files.replace('.in' or '.out', '')}: {over_memory} [{dec_places(time_taken)}s"
                f", {print_mem(memory)}] ({score}/{max_score})")
        elif score == max_score and time_taken > time_limit:
            print(
                f"Test case {files.replace('.in' or '.out', '')}: {timeout} [{dec_places(time_taken)}s"
                f", {print_mem(memory)}] ({score}/{max_score})")
        else:
            print(
                f"Test case {files.replace('.in' or '.out', '')}: {wrong_answer} [{dec_places(time_taken)}s"
                f", {print_mem(memory)}] ({score}/{max_score})")

print(f"\nResources: {dec_places(total_time)}s, {print_mem(max(total_memory))}")
print(f"Maximum single-case runtime: {dec_places(max(times))}s")
print(f"Final score: {total_score}/{max_total_score}\n")
