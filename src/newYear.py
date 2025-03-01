import random
import sys
import time

list_2024 = [
"  ██████╗  ██████╗  ██████╗ ██████╗ ██████╗ ██╗   ██╗███████╗    ██████╗  ██████╗ ██████╗ ██╗  ██╗██╗ ",
" ██╔════╝ ██╔═══██╗██╔═══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝██╔════╝    ╚════██╗██╔═████╗╚════██╗██║  ██║██║ ",
" ██║  ███╗██║   ██║██║   ██║██║  ██║██████╔╝ ╚████╔╝ █████╗       █████╔╝██║██╔██║ █████╔╝███████║██║ ",
" ██║   ██║██║   ██║██║   ██║██║  ██║██╔══██╗  ╚██╔╝  ██╔══╝      ██╔═══╝ ████╔╝██║██╔═══╝ ╚════██║╚═╝ ",
" ╚██████╔╝╚██████╔╝╚██████╔╝██████╔╝██████╔╝   ██║   ███████╗    ███████╗╚██████╔╝███████╗     ██║██╗ ",
"  ╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝ ╚═════╝    ╚═╝   ╚══════╝    ╚══════╝ ╚═════╝ ╚══════╝     ╚═╝╚═╝ "
]

list_2025 = [
"          ██╗  ██╗███████╗██╗     ██╗      ██████╗     ██████╗  ██████╗ ██████╗ ███████╗██╗           ",
"          ██║  ██║██╔════╝██║     ██║     ██╔═══██╗    ╚════██╗██╔═████╗╚════██╗██╔════╝██║           ",
"          ███████║█████╗  ██║     ██║     ██║   ██║     █████╔╝██║██╔██║ █████╔╝███████╗██║           ",
"          ██╔══██║██╔══╝  ██║     ██║     ██║   ██║    ██╔═══╝ ████╔╝██║██╔═══╝ ╚════██║╚═╝           ",
"          ██║  ██║███████╗███████╗███████╗╚██████╔╝    ███████╗╚██████╔╝███████╗███████║██╗           ",
"          ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝ ╚═════╝     ╚══════╝ ╚═════╝ ╚══════╝╚══════╝╚═╝           "
]
template = "                                                                                                      "
result = [template]*6


def update_lines(log_lines, status, processes):
    processes += 1
    combined = log_lines + [""] + status
    num_lines = len(combined)
    if num_lines > processes:
        for i in range(num_lines - processes):
            print("")
    for i in range(num_lines):
        i = num_lines - i -1
        sys.stdout.write('\033[F')
        if i < num_lines - 1:
            sys.stdout.write('\033[F')
        sys.stdout.write('\033[K')
        print(combined[i])
    for i in range(num_lines-1):
        sys.stdout.write('\033[B')

displayNewYear = False
update_lines([], result, 0)
for i in range(len(template)):
    for j in range(len(result)):
        result[j] = list_2024[j][:i] + template[i:]
    update_lines([], result, 6)
    time.sleep(0.02)
time.sleep(2)
for i in range(len(template)):
    for j in range(len(result)):
        result[j] = list_2025[j][:i] + list_2024[j][i:]
    update_lines([], result, 6)
    time.sleep(0.02)