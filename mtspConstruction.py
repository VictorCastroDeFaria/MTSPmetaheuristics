from mtspHeuristic import *
import random

# Construção de inserção mais barata considerando todas as possíveis inserções, 
# mas com inserção inicial aleatória
def greedy_insertion_construction(distance_matrix, number_of_salesmen):
    cities_vector = [i for i in range(2,len(distance_matrix)+1)]
    shuffle(cities_vector)

    initial_cities = cities_vector[:number_of_salesmen]
    other_cities = cities_vector[number_of_salesmen:]

    initial_solutions = [[1,i,1] for i in initial_cities]
    route_to_increment_index = 0
    final_city = 0
    city_index_to_insert = 0
    max_distance = float("inf")
    for new_city in other_cities:
        #print("Building new solution...")
        for route_index in range(0,len(initial_solutions)): # Para cada rota
            #print("In route",route_index)
            route = initial_solutions[route_index]
            #print(route)
            #max_distance = float("inf")
            for city_index in range(1,len(route)): # Para cada cidade já inserida na dita rota
                city_in_route = route[city_index]
                city_before_in_route = route[city_index-1]
                insertion_cost = distance_matrix[city_in_route-1][new_city-1] + distance_matrix[new_city-1][city_before_in_route-1] - distance_matrix[city_in_route-1][city_before_in_route-1]
                #if city_index == 1:
                    #print("First insertion: ", insertion_cost)
                if insertion_cost < max_distance:
                    #print(route_to_increment_index)
                    max_distance = insertion_cost
                    route_to_increment_index = route_index
                    city_index_to_insert = city_index
                    final_city = new_city
                    #print("Found cheaper insertion of value",insertion_cost, 'at city',new_city,"in position",city_index_to_insert)
        city_to_insert = final_city
        #print("Solution built")
        #print("-----------------------------------------------------------------------------")
        #print(route_to_increment_index, city_to_insert, city_index_to_insert,max_distance)
        initial_solutions[route_to_increment_index] = insert_in_vector(initial_solutions[route_to_increment_index], city_to_insert, city_index_to_insert)
        # Reset das variáveis do problema
        route_to_increment_index = 0
        max_distance = float("inf")

    obj_function_vector = objective_function_vector_bf(initial_solutions, distance_matrix)
    initial_solutions = [route[1:-1] for route in initial_solutions]
    return initial_solutions, obj_function_vector

def random_construction(cities_vector, number_of_salesmen):
    cities_list = cities_vector
    shuffle(cities_list)
    indices = sample(range(1,len(cities_list)-1),number_of_salesmen-1)
    indices.sort()
    indices_len = len(indices)
    if(indices_len == 1):
        index = indices[0]
        return [(0,index),(index,-1)]
    splits = [(0,indices[0])] + [(indices[i],indices[i+1]) for i in range(0, indices_len-1)] #+ [(indices[-1],-1)]
    #return [list(split) for split in splits]
    return [cities_vector[p_a:p_b] for [p_a, p_b] in splits] + [cities_vector[indices[-1]:]]

# Heurística para construção de tours por inserção de uma cidade aleatória no final da rota
def cheapest_random_insertion_construction(distance_matrix, number_of_salesmen):
    cities_vector = [i for i in range(2,len(distance_matrix)+1)]
    shuffle(cities_vector)

    initial_cities = cities_vector[:number_of_salesmen]
    other_cities = cities_vector[number_of_salesmen:]

    initial_solutions = [[i] for i in initial_cities]
    for new_city in other_cities:
        max_distance = float("inf")
        for route in range(0,len(initial_solutions)):
            last_city = initial_solutions[route][-1]
            if distance_matrix[last_city-1][new_city-1] <= max_distance:
                max_distance = distance_matrix[last_city-1][new_city-1]
                route_to_increment = route
        initial_solutions[route_to_increment] = initial_solutions[route_to_increment] + [new_city]

    obj_function_vector = objective_function_vector_bf(initial_solutions, distance_matrix)
    return initial_solutions, obj_function_vector