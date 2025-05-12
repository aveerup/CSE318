import random, time, multiprocessing, os, csv
random.seed(12255)

def get_cut_weight_vertex(graph, v, y):
    if v == 0:
        return 0

    cut_weight = 0

    for i in y:
        cut_weight += graph[v].get(i, 0)

    return cut_weight

def get_cut_weight_partition(graph, x, y):
    cut_weight = 0
    
    for i in x:
        cut_weight += get_cut_weight_vertex(graph, i, y)

    return cut_weight

def Randomized_heuristic(graph, n):
    total_cut_weight = 0
    for i in range(n):
        
        x = []
        y = []

        for j in range(1,len(graph)):
            if random.random() >= 0.5:
                x.append(j)
            else:
                y.append(j)

        cut_weight = get_cut_weight_partition(graph, x, y)
        total_cut_weight += cut_weight

    average_cut_weight = total_cut_weight / n;

    return average_cut_weight

def Greedy_heuristic(graph):
    x = []
    y = []

    assigned = [False]*(total_vertices+1)

    x.append(graph[0][0])
    y.append(graph[0][1])

    assigned[graph[0][0]] = True
    assigned[graph[0][1]] = True

    for i in range(total_vertices+1):
        if i == 0 or assigned[i] == True:
            continue;

        w_x = get_cut_weight_vertex(graph, i, y)
        w_y = get_cut_weight_vertex(graph, i, x)

        if w_x > w_y :
            x.append(i)
        else:
            y.append(i)

        assigned[i] = True

    cut_weight = get_cut_weight_partition(graph, x, y)

    return x, y, cut_weight

def Semi_greedy_heuristic(graph):
    global repeat_check
    global semi_greedy_cut_weight
    x = []
    y = []

    assigned_vetices = 0
    assigned = [False]*(total_vertices+1)

    x.append(graph[0][0])
    y.append(graph[0][1])

    assigned_vetices += 2
    assigned[graph[0][0]] = True
    assigned[graph[0][1]] = True

    while assigned_vetices != total_vertices:
        candidate_list = {}

        max_sigma_x, max_sigma_y = -10000, -10000
        min_sigma_x, min_sigma_y = 10000, 10000 
        for i in range(1, total_vertices+1):
            if assigned[i]:
                continue

            sigma_x = get_cut_weight_vertex(graph, i, x)
            sigma_y = get_cut_weight_vertex(graph, i, y)

            candidate_list[i] = [sigma_x, sigma_y]

            max_sigma_x = max(max_sigma_x, sigma_x)
            max_sigma_y = max(max_sigma_y, sigma_y)

            min_sigma_x = min(min_sigma_x, sigma_x)
            min_sigma_y = min(min_sigma_y, sigma_y)

        w_max = max(max_sigma_x, max_sigma_y)
        w_min = max(min_sigma_x, min_sigma_y)

        mu = w_min + alpha*(w_max - w_min)

        rcl = []
        for key, value in candidate_list.items():
            sigma_x = value[0]
            sigma_y = value[1]

            greedy_value = max(sigma_x, sigma_y)

            if greedy_value > mu:
                rcl.append(key)

        if len(rcl) == 0:
            greedy_vertex = 0
            for key,value in candidate_list.items():
                greedy_vertex = key
                greedy_value = max(value[0], value[1])
                break

            for key, value in candidate_list.items():
                candidate_value = max(value[0], value[1])

                if candidate_value > greedy_value:
                    greedy_value = candidate_value                
                    greedy_vertex = key

            rcl.append(greedy_vertex)

        random_vertex = rcl[random.randint(0, len(rcl) - 1)]

        sigma_x = candidate_list[random_vertex][0]
        sigma_y = candidate_list[random_vertex][1]

        if sigma_x > sigma_y:
            y.append(random_vertex)
        else:
            x.append(random_vertex)

        assigned[random_vertex] = True
        assigned_vetices += 1

    cut_weight = get_cut_weight_partition(graph, x, y)
    if repeat_check == 0:
        semi_greedy_cut_weight = cut_weight

    return x, y, cut_weight

# def local_search(graph, x, y):
#     cut_weight = get_cut_weight_partition(graph, x, y)

#     while 1:
#         change_value = 0
#         change_vertex_index = 0
#         change_partition = 0

#         for i in range(len(x)):
#             change = get_cut_weight_vertex(graph, x[i], x) - get_cut_weight_vertex(graph, x[i], y) 
#             if change > change_value:
#                 change_value = change;
#                 change_vertex_index = i;
#                 change_partition = 0;

#         for i in range(len(y)):
#             change = get_cut_weight_vertex(graph, y[i], y) - get_cut_weight_vertex(graph, y[i], x) 
#             if change > change_value:
#                 change_value = change;
#                 change_vertex_index = i;
#                 change_partition = 1;

#         if  change > 0:
#             if change_partition == 0:
#                 y.append(x[change_vertex_index])
#                 x.pop(change_vertex_index)
#             else:
                # x.append(y[change_vertex_index])
                # y.pop(change_vertex_index)
#             cut_weight = cut_weight + change

#         else:
#             break

#     return x, y, cut_weight

def local_search(graph, x, y):
    global local_search_avg_cut_weight
    global local_search_iterations

    cut_weight = get_cut_weight_partition(graph, x, y)

    change_weight = {}
    for i in x:
        change_weight[i] = [get_cut_weight_vertex(graph, i, x), get_cut_weight_vertex(graph, i, y)]

    for i in y:
        change_weight[i] = [get_cut_weight_vertex(graph, i, x), get_cut_weight_vertex(graph, i, y)]
        
    while 1:
        change_value = 0
        change_vertex_index = 0
        change_partition = 0

        for i in range(len(x)):
            change = change_weight[x[i]][0] - change_weight[x[i]][1] 
            if change > change_value:
                change_value = change;
                change_vertex_index = i;
                change_partition = 0;

        for i in range(len(y)):
            change = change_weight[y[i]][1] - change_weight[y[i]][0] 
            if change > change_value:
                change_value = change;
                change_vertex_index = i;
                change_partition = 1;

        if  change_value > 0:
            if change_partition == 0:
                for i in range(1, total_vertices+1):
                    if i == x[change_vertex_index]:
                        continue

                    change_weight[i][0] -= graph[i].get(x[change_vertex_index], 0)
                    change_weight[i][1] += graph[i].get(x[change_vertex_index], 0)
                 
                y.append(x[change_vertex_index])
                x.pop(change_vertex_index)
                
            else:
                for i in range(1, total_vertices+1):
                    if i == y[change_vertex_index]:
                        continue

                    # print(change_weight, " ", i)
                    # print(1.1)
                    change_weight[i][0] += graph[i].get(y[change_vertex_index], 0)
                    # print(1.2)
                    change_weight[i][1] -= graph[i].get(y[change_vertex_index], 0)
                    # print(1.3)

                x.append(y[change_vertex_index])
                y.pop(change_vertex_index)

            cut_weight = cut_weight + change_value

            if repeat_check == 0:
                local_search_iterations += 1
                local_search_avg_cut_weight += cut_weight

        else:
            break

    if repeat_check == 0 and local_search_iterations != 0 :
        local_search_avg_cut_weight = local_search_avg_cut_weight / local_search_iterations

    return x, y, cut_weight

def GRASP(graph, iterations):
    global repeat_check
    global semi_greedy_cut_weight
    max_cut_weight = 0
    max_x = []
    max_y = []
    
    for i in range(iterations):
        
        x, y, cut_weight = Semi_greedy_heuristic(graph)
        x, y, cut_weight = local_search(graph, x, y)
        if local_search_iterations > 0:
            repeat_check += 1;
        else:
            semi_greedy_cut_weight = 0

        if i == 0:
            max_cut_weight = cut_weight
            max_x = x
            max_y = y
        else:
            if cut_weight > max_cut_weight:
                max_cut_weight = cut_weight
                max_x = x
                max_y = y
    
    return max_x, max_y, max_cut_weight

alpha = 0.5
no_of_vertices_edges = 0
total_vertices = 0
total_edges = 0
graph = {}
result = None
semi_greedy_cut_weight = 0
local_search_iterations = 0
local_search_avg_cut_weight = 0
grasp_search_iterations = 2
repeat_check = 0

def run_GRASP(file_name):

    print(f"processing {file_name}")
       
    global no_of_vertices_edges
    global total_vertices
    global total_edges
    global graph
    global repeat_check
    global semi_greedy_cut_weight
    global local_search_iterations
    global local_search_avg_cut_weight
    temp_result = {}

    with open(file_name, "r") as f:
        no_of_vertices_edges = list(map(int,f.readline().split()))
        total_vertices = no_of_vertices_edges[0]
        total_edges = no_of_vertices_edges[1]

        for i in range(total_vertices+1):
            graph[i] = {}

        graph[0] = [0, 0, 0]
        for i in range(total_edges):
            edges = list(map(int, f.readline().split()))
            graph[edges[0]][edges[1]] = edges[2]
            graph[edges[1]][edges[0]] = edges[2]

            if edges[2] > graph[0][2]:
                graph[0][0] = edges[0]
                graph[0][1] = edges[1]
                graph[0][2] = edges[2]

    file_no = int(file_name.split('/')[-1][1:-4])
    temp_result["file_no"] = file_no
    # print(file_no)

    random_cut_weight = Randomized_heuristic(graph, 10)
    print(f"Randomized heuristic cut weight {file_no}: ", random_cut_weight)
    temp_result["randomized_cut_weight"] = random_cut_weight

    greedy_x, greedy_y, greedy_cut_weight = Greedy_heuristic(graph)
    print(f"Greedy heuristic cut weight {file_no}: ", greedy_cut_weight)
    temp_result["greedy_cut_weight"] = greedy_cut_weight
    # print("x :", greedy_x)
    # print("y :", greedy_y)

    grasp_x, grasp_y, grasp_cut_weight = GRASP(graph, grasp_search_iterations)
    print(f"GRASP cut weight {file_no}: ", grasp_cut_weight)
    print(f"Semi-greedy cut weight {file_no}: ", semi_greedy_cut_weight )
    print(f"local search iterations {file_no}: ", local_search_iterations)
    print(f"local search avg cut weight {file_no}: ", local_search_avg_cut_weight)
    temp_result["grasp_cut_weight"] = grasp_cut_weight
    temp_result["local_search_iterations"] = local_search_iterations
    temp_result["local_search_avg_cut_weight"] = local_search_avg_cut_weight
    temp_result["semi_greedy_cut_weight"] = semi_greedy_cut_weight

    repeat_check = 0
    semi_greedy_cut_weight = 0
    local_search_avg_cut_weight = 0
    local_search_iterations = 0

    return temp_result

start_time = time.time()

input_files = []
for i in range(1,55):
    input_files.append("./graph_GRASP/set1/g"+str(i)+".rud")

# with multiprocessing.Pool(processes = 9) as pool:
#     result = pool.map(run_GRASP, input_files)

for _ in map(run_GRASP, input_files):
    pass

fieldnames = result[0].keys()
with open("results.csv", "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()  # writes column names
    writer.writerows(result)

end_time = time.time()
print("time needed :", end_time - start_time)

# print(graph)