import itertools
import tkinter
from tkinter import filedialog

root = tkinter.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()
answer_path = filedialog.asksaveasfilename(filetypes=(("CSV Files", "*.csv"), ("All", "*.*")), defaultextension=".csv")

if not file_path:
    raise SystemExit

matrix_adjacency = []
with open(file_path, "r", errors='ignore') as f:
    for line in f:
        matrix_adjacency.append([int(x) for x in line.split()])

answer_file = None
if answer_path:
    answer_file = open(answer_path, "w")

sets_vertex = [set([x for x in range(1, len(matrix_adjacency) + 1)])]
k = 1
while k < len(matrix_adjacency):
    done = False
    all_bound_vertex = []
    all_unbound_vertex = []
    for set_vertex in itertools.combinations(set(itertools.chain(*sets_vertex)), k):
        answer_str = ""
        for c in set_vertex:
            answer_str = answer_str + str(c) + "\t"
        current_bound_vertex = []
        current_unbound_vertex = []
        for vertex in set_vertex:
            bound_vertex = []
            unbound_vertex = []
            for i in range(0, len(matrix_adjacency)):
                if i != vertex - 1:
                    if matrix_adjacency[vertex - 1][i] == 1:
                        bound_vertex.append(i + 1)
                    else:
                        unbound_vertex.append(i + 1)
            current_bound_vertex.append(bound_vertex)
            current_unbound_vertex.append(unbound_vertex)
        for c in set(itertools.chain(*current_bound_vertex)) - set(set_vertex):
            answer_str = answer_str + str(c) + ","
        answer_str = answer_str[0:-1]
        answer_str = answer_str + "\t"
        for c in set(itertools.chain(*current_unbound_vertex)) - set(itertools.chain(*current_bound_vertex)) - set(set_vertex):
            answer_str = answer_str + str(c) + ","
        answer_str = answer_str[0:-1]
        answer_str = answer_str + "\t"
        print(answer_str)
        if answer_file:
            answer_file.write(answer_str + "\n")
        all_bound_vertex.append(set(itertools.chain(*current_bound_vertex)))
        all_unbound_vertex.append(set(itertools.chain(*current_unbound_vertex)))
        if len(sets_vertex[0] - set(itertools.chain(*current_bound_vertex)) - set(set_vertex)) == 0:
            done = True
    sets_vertex.append(set(itertools.chain(*all_bound_vertex)))
    print()
    if done:
        raise SystemExit
    k += 1

