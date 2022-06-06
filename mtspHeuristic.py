from random import shuffle, randint, sample

#Impressão linha a linha da sequência de rotas para cada viajante
def print_routes(route_vector):
    for route in route_vector:
        print(route)

# Função para inserção de um elemento em um vetor numa dada posição
def insert_in_vector(vector, element, index):
    return vector[:index] + [element] + vector[index:]

# Função de cálculo da distância de uma lista de sequências de viagens a visitar
def calc_tour_length(solution, distance_matrix):
    if len(solution) == 0:
        return 0
    if len(solution) == 1:
        return distance_matrix[0][solution[0]-1] + distance_matrix[solution[0]-1][0]
    start_index = solution[0]
    end_index = solution[-1]
    total = distance_matrix[0][start_index-1] + distance_matrix[end_index-1][0]
    for i in range(1, len(solution)):
        total += distance_matrix[solution[i-1]-1][solution[i]-1]
    return total

def objective_function_vector_bf(routes, distance_matrix):
    obj_function_vector = [0 for route in routes]
    for i in range(0,len(routes)):
        obj_function_vector[i] = calc_tour_length(routes[i],distance_matrix)
    return obj_function_vector

def objective_function_minsum(obj_function_vector):
    return sum(obj_function_vector)

def two_opt_intraroute(route_vector,point_a,point_b,obj_function, distance_matrix):
    #point_a, point_b = min([point_a, point_b]), max([point_a, point_b])
    new_vector = [1] + route_vector[:point_a] + route_vector[point_a:point_b][::-1] + route_vector[point_b:] + [1]
    point_a += 1
    point_b += 1
    obj_function = obj_function - distance_matrix[new_vector[point_a-1]-1][new_vector[point_b-1]-1] 
    obj_function = obj_function - distance_matrix[new_vector[point_a]-1][new_vector[point_b]-1]
    obj_function = obj_function + distance_matrix[new_vector[point_a-1]-1][new_vector[point_a]-1] 
    obj_function = obj_function + distance_matrix[new_vector[point_b-1]-1][new_vector[point_b]-1]
    return new_vector[1:-1], obj_function

def shift_intraroute(route_vector,point_element,point_target,obj_function,distance_matrix):
    element = route_vector[point_element]
    new_vector = [1] + route_vector + [1]
    point_element += 1
    point_target += 1
    new_vector = [i - 1 for i in new_vector]
    # Mudança nos cálculos de acordo com a posição alvo
    if point_target < point_element: 
        obj_function = obj_function - distance_matrix[new_vector[point_target-1]][new_vector[point_target]] - distance_matrix[new_vector[point_element-1]][new_vector[point_element]] - distance_matrix[new_vector[point_element]][new_vector[point_element+1]]
        obj_function = obj_function + distance_matrix[new_vector[point_target-1]][new_vector[point_element]] + distance_matrix[new_vector[point_element]][new_vector[point_target]] + distance_matrix[new_vector[point_element-1]][new_vector[point_element+1]]
    
    elif point_target > point_element:
        obj_function = obj_function - distance_matrix[new_vector[point_target+1]][new_vector[point_target]] - distance_matrix[new_vector[point_element-1]][new_vector[point_element]] - distance_matrix[new_vector[point_element]][new_vector[point_element+1]]
        obj_function = obj_function + distance_matrix[new_vector[point_target+1]][new_vector[point_element]] + distance_matrix[new_vector[point_element]][new_vector[point_target]] + distance_matrix[new_vector[point_element-1]][new_vector[point_element+1]]
   
    new_vector = [i + 1 for i in new_vector]
    new_vector = new_vector[:point_element] + new_vector[point_element+1:]
    new_vector = insert_in_vector(new_vector, element, point_target)

    return new_vector[1:-1], obj_function

def shift_interroute(solutions,first_sol_index,second_sol_index,first_element_index,second_element_index,obj_function_vector,distance_matrix):
    # O shift realoca o elemento da primeira solução (first_sol) à segunda (second_sol) na posição second_element_index
    first_element_index += 1
    second_element_index += 1
    
    first_route = [1] + solutions[first_sol_index] + [1]
    second_route = [1] + solutions[second_sol_index] + [1]

    element_to_shift = first_route[first_element_index]
    delta_first = distance_matrix[first_route[first_element_index-1]-1][first_route[first_element_index+1]-1] - distance_matrix[first_route[first_element_index-1]-1][first_route[first_element_index]-1] - distance_matrix[first_route[first_element_index]-1][first_route[first_element_index+1]-1]
    delta_second = -1*distance_matrix[second_route[second_element_index]-1][second_route[second_element_index-1]-1] + distance_matrix[second_route[second_element_index-1]-1][first_route[first_element_index]-1] + distance_matrix[second_route[second_element_index]-1][first_route[first_element_index]-1]

    obj_function_vector[first_sol_index] += delta_first
    obj_function_vector[second_sol_index] += delta_second

    first_route = first_route[:first_element_index] + first_route[first_element_index+1:]
    second_route = second_route[:second_element_index] + [element_to_shift] + second_route[second_element_index:]
    solutions[first_sol_index] = first_route[1:-1]
    solutions[second_sol_index] = second_route[1:-1]
    return solutions, obj_function_vector

def swap_intraroute(route_vector,point_a,point_b,obj_function,distance_matrix):
    new_vector = [1] + route_vector + [1]
    point_a += 1
    point_b += 1
    # Retirada dos pesos das arestas do trajeto antes da mudança 
    obj_function = obj_function - distance_matrix[new_vector[point_a-1]-1][new_vector[point_a]-1] - distance_matrix[new_vector[point_a]-1][new_vector[point_a+1]-1]
    obj_function = obj_function - distance_matrix[new_vector[point_b-1]-1][new_vector[point_b]-1] - distance_matrix[new_vector[point_b]-1][new_vector[point_b+1]-1]
    # Movimento de mudança do trajeto
    new_vector[point_a], new_vector[point_b] = new_vector[point_b], new_vector[point_a]
    # Adição dos pesos das novas arestas após a mudança
    obj_function = obj_function + distance_matrix[new_vector[point_a-1]-1][new_vector[point_a]-1] + distance_matrix[new_vector[point_a]-1][new_vector[point_a+1]-1]
    obj_function = obj_function + distance_matrix[new_vector[point_b-1]-1][new_vector[point_b]-1] + distance_matrix[new_vector[point_b]-1][new_vector[point_b+1]-1]

    return new_vector[1:-1], obj_function

def swap_interroute(solutions,first_sol_index,second_sol_index,first_element_index,second_element_index,obj_function_vector,distance_matrix):
    first_element_index += 1
    second_element_index += 1
    
    first_route = [1] + solutions[first_sol_index] + [1]
    second_route = [1] + solutions[second_sol_index] + [1]

    delta_first = distance_matrix[first_route[first_element_index-1]-1][second_route[second_element_index]-1] + distance_matrix[first_route[first_element_index+1]-1][second_route[second_element_index]-1] - distance_matrix[first_route[first_element_index]-1][first_route[first_element_index-1]-1] - distance_matrix[first_route[first_element_index]-1][first_route[first_element_index+1]-1] 
    delta_second = distance_matrix[second_route[second_element_index-1]-1][first_route[first_element_index]-1] + distance_matrix[second_route[second_element_index+1]-1][first_route[first_element_index]-1] - distance_matrix[second_route[second_element_index]-1][second_route[second_element_index-1]-1] - distance_matrix[second_route[second_element_index]-1][second_route[second_element_index+1]-1]

    obj_function_vector[first_sol_index] += delta_first
    obj_function_vector[second_sol_index] += delta_second

    first_route[first_element_index], second_route[second_element_index] = second_route[second_element_index], first_route[first_element_index]
    solutions[first_sol_index] = first_route[1:-1]
    solutions[second_sol_index] = second_route[1:-1]
    return solutions, obj_function_vector

def random_movement(solutions,objective_function_vector,distance_matrix):
    main_movement_mode = randint(0,1)
    # Se o modo principal for 0, o movimento será somente intrarrota
    if main_movement_mode == 0: 
        second_movement_mode = randint(0,2)
        solution_index = randint(0,len(solutions)-1)

        # Bloco para evitar seleção de rotas curtas 
        while len(solutions[solution_index]) <= 2:
            solution_index = randint(0,len(solutions)-1)

        if second_movement_mode == 0: # 2-opt
            pointA, pointB = 0, 0
            while pointB - pointA < 2:
                pointA = randint(0,len(solutions[solution_index])-1)
                pointB = randint(0,len(solutions[solution_index])-1)
            # def two_opt_intraroute(route_vector,point_a,point_b,obj_function, distance_matrix):
            solutions[solution_index], objective_function_vector[solution_index] = two_opt_intraroute(solutions[solution_index],pointA,pointB,objective_function_vector[solution_index],distance_matrix)
            #print("2-opt INTRAroute")
            return solutions, objective_function_vector

        elif second_movement_mode == 1: # Swap
            pointA, pointB = 0, 0
            while pointB == pointA:
                pointA = randint(0,len(solutions[solution_index])-1)
                pointB = randint(0,len(solutions[solution_index])-1)
            # def swap_intraroute(route_vector,point_a,point_b,obj_function,distance_matrix):
            solutions[solution_index], objective_function_vector[solution_index] = swap_intraroute(solutions[solution_index],pointA,pointB,objective_function_vector[solution_index],distance_matrix)
            #print("Swap INTRAroute")
            return solutions, objective_function_vector

        #Shift
        point_target = randint(0,len(solutions[solution_index])-1)
        point_element = randint(0,len(solutions[solution_index])-1)
        # def shift_intraroute(route_vector,point_element,point_target,obj_function,distance_matrix):
        solutions[solution_index], objective_function_vector[solution_index] = shift_intraroute(solutions[solution_index],point_element,point_target,objective_function_vector[solution_index],distance_matrix)
        #print("Shift INTRAroute")
        return solutions, objective_function_vector

    # Se o modo principal for 1, o movimento será interrota
    second_movement_mode = randint(0,1)

    if second_movement_mode == 0: # Swap
        first_solution_index, second_solution_index = 0, 0
        # Condições para selecionar índices: índices diferentes e a primeira solução ter tamanho maior que 1
 
        while first_solution_index == second_solution_index or len(solutions[first_solution_index]) < 1:
            first_solution_index = randint(0,len(solutions)-1)
            second_solution_index = randint(0,len(solutions)-1)
        first_element_index = randint(0, len(solutions[first_solution_index])-1)
        second_element_index = randint(0, len(solutions[second_solution_index])-1) 
        # def swap_interroute(solutions,first_sol_index,second_sol_index,first_element_index,second_element_index,obj_function_vector,distance_matrix):
        solutions, objective_function_vector = swap_interroute(solutions,first_solution_index,second_solution_index,first_element_index,second_element_index,objective_function_vector,distance_matrix)
        #print("Swap INTERroute with solutions %d and %d and points %d and %d" % (first_solution_index, second_solution_index, first_element_index, second_element_index))
        return solutions, objective_function_vector
    
    # Shift
    first_solution_index, second_solution_index = 0, 0
    # Condições para selecionar índices: índices diferentes, a primeira solução ter tamanho maior que 2 e a segunda solução não ser vazia
    while first_solution_index == second_solution_index or len(solutions[first_solution_index]) < 2 or len(solutions[second_solution_index]) < 1:
        first_solution_index = randint(0,len(solutions)-1)
        second_solution_index = randint(0,len(solutions)-1)
    first_element_index = randint(0, len(solutions[first_solution_index])-1)
    second_element_index = randint(0, len(solutions[second_solution_index])-1) 
    #                                   shift_interroute(solutions,first_sol_index,second_sol_index,first_element_index,second_element_index,obj_function_vector,distance_matrix)
    solutions, objective_function_vector = shift_interroute(solutions,first_solution_index,second_solution_index,first_element_index,second_element_index,objective_function_vector,distance_matrix)
    #print("Shift INTERroute with solutions %d and %d and points %d and %d" % (first_solution_index, second_solution_index, first_element_index, second_element_index))
    return solutions, objective_function_vector

def generate_random_neighbor_shift_interroute(solutions,objective_function_vector,distance_matrix):
    first_solution_index, second_solution_index = 0, 0
    # Condições para selecionar índices: índices diferentes, a primeira solução ter tamanho maior que 2 e a segunda solução não ser vazia
    while first_solution_index == second_solution_index or len(solutions[first_solution_index]) < 2 or len(solutions[second_solution_index]) < 1:
        first_solution_index = randint(0,len(solutions)-1)
        second_solution_index = randint(0,len(solutions)-1)
    first_element_index = randint(0, len(solutions[first_solution_index])-1)
    second_element_index = randint(0, len(solutions[second_solution_index])-1) 
    #                                   shift_interroute(solutions,first_sol_index,second_sol_index,first_element_index,second_element_index,obj_function_vector,distance_matrix)
    solutions_neighbor, objective_function_neighbor = shift_interroute(solutions,first_solution_index,second_solution_index,first_element_index,second_element_index,objective_function_vector,distance_matrix)
    #print("Shift INTERroute with solutions %d and %d and points %d and %d" % (first_solution_index, second_solution_index, first_element_index, second_element_index))
    return solutions_neighbor, objective_function_neighbor

def generate_random_neighbor_swap_interroute(solutions,objective_function_vector,distance_matrix):
    first_solution_index, second_solution_index = 0, 0
    # Condições para selecionar índices: índices diferentes e a primeira solução ter tamanho maior que 1
 
    while first_solution_index == second_solution_index or len(solutions[first_solution_index]) < 1:
        first_solution_index = randint(0,len(solutions)-1)
        second_solution_index = randint(0,len(solutions)-1)
    first_element_index = randint(0, len(solutions[first_solution_index])-1)
    second_element_index = randint(0, len(solutions[second_solution_index])-1) 
    # def swap_interroute(solutions,first_sol_index,second_sol_index,first_element_index,second_element_index,obj_function_vector,distance_matrix):
    solutions_neighbor, objective_function_neighbor = swap_interroute(solutions,first_solution_index,second_solution_index,first_element_index,second_element_index,objective_function_vector,distance_matrix)
    #print("Swap INTERroute with solutions %d and %d and points %d and %d" % (first_solution_index, second_solution_index, first_element_index, second_element_index))
    return solutions_neighbor, objective_function_neighbor


def generate_random_neighbor_shift_intraroute(solutions,objective_function_vector,distance_matrix):
    solution_index = randint(0,len(solutions)-1)
    while len(solutions[solution_index]) <= 2:
        solution_index = randint(0,len(solutions)-1)
    
    point_element, point_target = 0, 0
    point_target = randint(0,len(solutions[solution_index])-1)
    point_element = randint(0,len(solutions[solution_index])-1)
    solutions_neighbor, objective_function_neighbor = solutions.copy(), objective_function_vector.copy()
    # def shift_intraroute(route_vector,point_element,point_target,obj_function,distance_matrix):
    solutions_neighbor[solution_index], objective_function_neighbor[solution_index] = shift_intraroute(solutions[solution_index],point_element,point_target,objective_function_vector[solution_index],distance_matrix)
    #print("Shift INTRAroute")
    return solutions_neighbor, objective_function_neighbor


def generate_random_neighbor_swap_intraroute(solutions,objective_function_vector,distance_matrix):
    solution_index = randint(0,len(solutions)-1)
    while len(solutions[solution_index]) <= 2:
        solution_index = randint(0,len(solutions)-1)
    
    pointA, pointB = 0, 0
    while pointB == pointA:
        pointA = randint(0,len(solutions[solution_index])-1)
        pointB = randint(0,len(solutions[solution_index])-1)
    # def swap_intraroute(route_vector,point_a,point_b,obj_function,distance_matrix):
    solutions_neighbor, objective_function_neighbor = solutions.copy(), objective_function_vector.copy()
    solutions_neighbor[solution_index], objective_function_neighbor[solution_index] = swap_intraroute(solutions[solution_index],pointA,pointB,objective_function_vector[solution_index],distance_matrix)
    #print("Swap INTRAroute")
    return solutions_neighbor, objective_function_neighbor


def generate_random_neighbor_two_opt(solutions,objective_function_vector,distance_matrix):
    solution_index = randint(0,len(solutions)-1)
    while len(solutions[solution_index]) <= 2:
        solution_index = randint(0,len(solutions)-1)

    pointA, pointB = 0, 0
    while pointB - pointA < 2:
        pointA = randint(0,len(solutions[solution_index])-1)
        pointB = randint(0,len(solutions[solution_index])-1)
    solutions_neighbor, objective_function_neighbor = solutions.copy(), objective_function_vector.copy()
    # def two_opt_intraroute(route_vector,point_a,point_b,obj_function, distance_matrix):
    solutions_neighbor[solution_index], objective_function_neighbor[solution_index] = two_opt_intraroute(solutions[solution_index],pointA,pointB,objective_function_vector[solution_index],distance_matrix)
    #print("2-opt INTRAroute")
    return solutions_neighbor, objective_function_neighbor