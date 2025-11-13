import matplotlib.pyplot as plt 
import numpy as np

IGx = []
IGy = []
IGnodes = []
IGRx = []
IGRy = []
IGRnodes = []
NWIGx = []
NWIGy = []
NWIGnodes = []

def insert_data(line_data):
    if line_data[0] == 'IG':
        IGx.insert(len(IGx), int(line_data[1]))
        IGy.insert(len(IGy), float(line_data[2])*100)
        IGnodes.insert(len(IGnodes), int(line_data[3]))
    elif line_data[0] == 'IGR':
        IGRx.insert(len(IGRx), int(line_data[1]))
        IGRy.insert(len(IGRy), float(line_data[2])*100)
        IGRnodes.insert(len(IGRnodes), int(line_data[3]))
    elif line_data[0] == 'NWIG':
        NWIGx.insert(len(NWIGx), int(line_data[1]))
        NWIGy.insert(len(NWIGy), float(line_data[2])*100)
        NWIGnodes.insert(len(NWIGnodes), int(line_data[3]))


line_no = 0
with open('plot_data.txt', 'r') as file:
    for line in file:
        if line_no == 0:
            line_no += 1;
            continue;
        else:
            line_data = line.strip(" ").replace('\n', '').split(",")
            insert_data(line_data)
            line_no += 1;

# print(IGx, IGRx, NWIGx)
# print(IGy, IGRy, NWIGy)
# print(IGnodes, IGRnodes, NWIGnodes)

plt.figure(1)
plt.plot(IGx, IGy, marker = 'o', color = 'red')
plt.xlabel('IG_max_depth')
plt.ylabel('IG_accuracy')
plt.grid(True)
plt.savefig("IG_acc_vs_depth.png")

plt.figure(2)
plt.plot(IGRx, IGRy, marker = 'o', color = 'red')
plt.xlabel('IGR_max_depth')
plt.ylabel('IGR_accuracy')
plt.grid(True)
plt.savefig("IGR_acc_vs_depth.png")

plt.figure(3)
plt.plot(NWIGx, NWIGy, marker = 'o', color = 'red')
plt.xlabel('NWIG_max_depth')
plt.ylabel('NWIG_accuracy')
plt.grid(True)
plt.savefig("NWIG_acc_vs_depth.png")

plt.figure(4)
plt.plot(IGx, IGy, marker = 'o', color = 'blue', label = 'IG')
plt.plot(IGRx, IGRy, marker = 'o', color = 'orange', label = 'IGR')
plt.plot(NWIGx, NWIGy, marker = 'o', color = 'green', label = 'NWIG')
plt.xlabel('max_depth')
plt.ylabel('accuracy')
plt.grid(True)
plt.legend()
plt.savefig("acc_vs_depth.png")

plt.figure(5)
plt.plot(IGx, IGnodes, marker = 'o', color = 'red')
plt.xlabel('IG_max_depth')
plt.ylabel('IG_nodes')
plt.grid(True)
plt.savefig("IG_nodes_vs_depth.png")

plt.figure(6)
plt.plot(IGRx, IGRnodes, marker = 'o', color = 'red')
plt.xlabel('IGR_max depth')
plt.ylabel('IGR_nodes')
plt.grid(True)
plt.savefig("IGR_nodes_vs_depth.png")

plt.figure(7)
plt.plot(NWIGx, NWIGnodes, marker = 'o', color = 'red')
plt.xlabel('NWIG_max_depth')
plt.ylabel('NWIG_nodes')
plt.grid(True)
plt.savefig("NWIG_nodes_vs_depth.png")

plt.figure(8)
plt.plot(IGx, IGnodes, marker = 'o', color = 'blue', label = 'IG')
plt.plot(IGRx, IGRnodes, marker = 'o', color = 'orange', label = 'IGR')
plt.plot(NWIGx, NWIGnodes, marker = 'o', color = 'green', label = 'NWIG')
plt.xlabel('max_depth')
plt.ylabel('nodes')
plt.grid(True)
plt.legend()
plt.savefig("nodes_vs_depth.png")