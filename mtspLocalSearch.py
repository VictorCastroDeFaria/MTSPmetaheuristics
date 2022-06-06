from mtspHeuristic import *

# Funções com First Imrpovement sem checagem de melhoria

def local_search_two_opt(solution,obj_function,distance_matrix):
    sum_OF = sum(obj_function)
    sol_copy = solution.copy()
    obj_function_copy = obj_function.copy() 
    amount_of_salesmen = len(solution)
    for route_index in range(amount_of_salesmen):
        route = sol_copy[route_index]
        obj_function_route = obj_function[route_index] 
        size_of_route = len(route)
        if size_of_route > 2:
            for point_a in range(size_of_route - 2):
                for point_b in range(point_a+2,size_of_route):
                    new_sol, new_obj_function = two_opt_intraroute(route,point_a,point_b,obj_function_route,distance_matrix)
                    obj_function_copy[route_index] = new_obj_function 
                    sum_OF_after = sum(obj_function_copy)
                    if sum_OF_after < sum_OF:
                        sol_copy[route_index] = new_sol
                        return sol_copy, obj_function_copy
                    sol_copy = solution.copy()
                    obj_function_copy = obj_function.copy()
    return solution, obj_function
    
def local_search_swap_intraroute(solution,obj_function,distance_matrix):
    sum_OF = sum(obj_function)
    sol_copy = solution.copy()
    obj_function_copy = obj_function.copy() 
    amount_of_salesmen = len(solution)
    for route_index in range(amount_of_salesmen):
        route = sol_copy[route_index]
        obj_function_route = obj_function[route_index] 
        size_of_route = len(route)
        if size_of_route > 1:
            for point_a in range(size_of_route - 1):
                for point_b in range(point_a+1,size_of_route):
                    new_sol, new_obj_function = swap_intraroute(route,point_a,point_b,obj_function_route,distance_matrix)
                    obj_function_copy[route_index] = new_obj_function 
                    sum_OF_after = sum(obj_function_copy)
                    if sum_OF_after < sum_OF:
                        sol_copy[route_index] = new_sol
                        return sol_copy, obj_function_copy
                    sol_copy = solution.copy()
                    obj_function_copy = obj_function.copy()
    return solution, obj_function  
    
def local_search_shift_intraroute(solution,obj_function,distance_matrix):
    sum_OF = sum(obj_function)
    sol_copy = solution.copy()
    obj_function_copy = obj_function.copy() 
    amount_of_salesmen = len(solution)
    for route_index in range(amount_of_salesmen):
        route = sol_copy[route_index]
        obj_function_route = obj_function[route_index] 
        size_of_route = len(route)
        if size_of_route > 1:
            for point_a in range(size_of_route):
                for point_b in range(size_of_route):
                        # Element > Target obrigatoriamente
                        # Move o elemento element para logo antes de target
                    new_sol, new_obj_function = shift_intraroute(route,point_b,point_a,obj_function_route,distance_matrix)
                    obj_function_copy[route_index] = new_obj_function 
                    sum_OF_after = sum(obj_function_copy)
                    if sum_OF_after < sum_OF:
                        sol_copy[route_index] = new_sol
                        return sol_copy, obj_function_copy
                    sol_copy = solution.copy()
                    obj_function_copy = obj_function.copy()
    return solution, obj_function
    
def local_search_swap_interroute(solution,obj_function,distance_matrix):
    sum_OF = sum(obj_function)
    sol_copy = solution.copy()
    obj_function_copy = obj_function.copy() 
    amount_of_salesmen = len(solution)
    for route_index_a in range(amount_of_salesmen):
        for route_index_b in range(route_index_a+1, amount_of_salesmen):
            size_of_route_a = len(solution[route_index_a])
            size_of_route_b = len(solution[route_index_b])
            for point_a in range(size_of_route_a):
                for point_b in range(size_of_route_b):
                    sol_copy, obj_function_copy = swap_interroute(sol_copy,route_index_a,route_index_b,point_a,point_b,obj_function_copy,distance_matrix)
                    sum_OF_after = sum(obj_function_copy)
                    if sum_OF_after < sum_OF:
                        return sol_copy, obj_function_copy
                    sol_copy = solution.copy()
                    obj_function_copy = obj_function.copy()
    return solution, obj_function

def local_search_shift_interroute(solution,obj_function,distance_matrix):
    sum_OF = sum(obj_function)
    sol_copy = solution.copy()
    obj_function_copy = obj_function.copy() 
    amount_of_salesmen = len(solution)
    
    # Ordem direta de pesquisa (do menor para o maior índice)
    for route_index_a in range(amount_of_salesmen):
        for route_index_b in range(route_index_a+1, amount_of_salesmen):
            size_of_route_a = len(solution[route_index_a])
            size_of_route_b = len(solution[route_index_b])
            if size_of_route_a > 2:
                for point_a in range(size_of_route_a):
                    for point_b in range(size_of_route_b):
                        sol_copy, obj_function_copy = shift_interroute(sol_copy,route_index_a,route_index_b,point_a,point_b,obj_function_copy,distance_matrix)
    # Na função, o shift realoca o elemento da primeira solução (first_sol) à segunda (second_sol) na posição second_element_index
                        sum_OF_after = sum(obj_function_copy)
            
                        if sum_OF_after < sum_OF:
                            return sol_copy, obj_function_copy
                        sol_copy = solution.copy()
                        obj_function_copy = obj_function.copy()

    # Ordem inversa de pesquisa (do maior para o menor índice)
    for route_index_a in reversed(range(amount_of_salesmen)):
        for route_index_b in reversed(range(route_index_a)):
            size_of_route_a = len(solution[route_index_a])
            size_of_route_b = len(solution[route_index_b])
            if size_of_route_a > 1:
                for point_a in range(size_of_route_a):
                    for point_b in range(size_of_route_b):
                        sol_copy, obj_function_copy = shift_interroute(sol_copy,route_index_a,route_index_b,point_a,point_b,obj_function_copy,distance_matrix)
                        sum_OF_after = sum(obj_function_copy)
            
                        if sum_OF_after < sum_OF:
                            return sol_copy, obj_function_copy
                        sol_copy = solution.copy()
                        obj_function_copy = obj_function.copy()
    return solution, obj_function

#Funções Best Improvement com checagem de melhoria

def local_search_two_opt_BI(solution,obj_function,distance_matrix):
    got_better_solution = False
    sum_OF = sum(obj_function)
    sol_copy = solution.copy()
    obj_function_copy = obj_function.copy()
    best_obj_function = obj_function.copy()
    amount_of_salesmen = len(solution)
    for route_index in range(amount_of_salesmen):
        route = sol_copy[route_index]
        obj_function_route = obj_function[route_index] 
        size_of_route = len(route)
        if size_of_route > 2:
            for point_a in range(size_of_route - 2):
                for point_b in range(point_a+2,size_of_route):
                    new_sol, new_obj_function = two_opt_intraroute(route,point_a,point_b,obj_function_route,distance_matrix)
                    obj_function_copy[route_index] = new_obj_function 
                    sum_OF_after = sum(obj_function_copy)
                    if sum_OF_after < sum_OF:
                        print(new_sol)
                        sum_OF = sum_OF_after
                        sol_copy[route_index] = new_sol
                        got_better_solution = True
                        best_obj_function = obj_function_copy.copy()
                        print(sol_copy)
                        print("____________________________________")

    return sol_copy, best_obj_function, got_better_solution

def local_search_swap_intraroute_BI(solution,obj_function,distance_matrix):
    got_better_solution = False
    best_obj_function = obj_function.copy()

    sum_OF = sum(obj_function)
    sol_copy = solution.copy()
    obj_function_copy = obj_function.copy() 
    amount_of_salesmen = len(solution)
    for route_index in range(amount_of_salesmen):
        route = sol_copy[route_index]
        obj_function_route = obj_function[route_index] 
        size_of_route = len(route)
        if size_of_route > 1:
            for point_a in range(size_of_route - 1):
                for point_b in range(point_a+1,size_of_route):
                    new_sol, new_obj_function = swap_intraroute(route,point_a,point_b,obj_function_route,distance_matrix)
                    obj_function_copy[route_index] = new_obj_function 
                    sum_OF_after = sum(obj_function_copy)
                    if sum_OF_after < sum_OF:
                        print(new_sol)
                        sum_OF = sum_OF_after
                        sol_copy[route_index] = new_sol
                        got_better_solution = True
                        best_obj_function = obj_function_copy.copy()
                        print(sol_copy)
                        print("____________________________________")

    return sol_copy, best_obj_function, got_better_solution

def local_search_shift_intraroute_BI(solution,obj_function,distance_matrix):
    got_better_solution = False
    best_obj_function = obj_function.copy()

    sum_OF = sum(obj_function)
    sol_copy = solution.copy()
    obj_function_copy = obj_function.copy() 
    amount_of_salesmen = len(solution)
    for route_index in range(amount_of_salesmen):
        route = sol_copy[route_index]
        obj_function_route = obj_function[route_index] 
        size_of_route = len(route)
        if size_of_route > 1:
            for point_a in range(size_of_route):
                for point_b in range(size_of_route):
                        # Element > Target obrigatoriamente
                        # Move o elemento element para logo antes de target
                    new_sol, new_obj_function = shift_intraroute(route,point_b,point_a,obj_function_route,distance_matrix)
                    obj_function_copy[route_index] = new_obj_function 
                    sum_OF_after = sum(obj_function_copy)
                    if sum_OF_after < sum_OF:
                        print(new_sol)
                        sol_copy[route_index] = new_sol
                        got_better_solution = True
                        best_obj_function = obj_function_copy.copy()
                        sum_OF = sum_OF_after


    return sol_copy, best_obj_function, got_better_solution
    got_better_solution = False
    best_obj_function = obj_function.copy()

    sum_OF = sum(obj_function)
    sol_copy = solution.copy()
    obj_function_copy = obj_function.copy() 
    amount_of_salesmen = len(solution)
    for route_index in range(amount_of_salesmen):
        route = sol_copy[route_index]
        obj_function_route = obj_function[route_index] 
        size_of_route = len(route)
        if size_of_route > 1:
            for point_a in range(size_of_route - 1):
                for point_b in range(point_a+1,size_of_route):
                        # Element > Target obrigatoriamente
                        # Move o elemento element para logo antes de target
                    new_sol, new_obj_function = shift_intraroute(route,point_b,point_a,obj_function_route,distance_matrix)
                    obj_function_copy[route_index] = new_obj_function 
                    sum_OF_after = sum(obj_function_copy)
                    if sum_OF_after < sum_OF:
                        sol_copy[route_index] = new_sol
                        got_better_solution = True
                        best_obj_function = obj_function_copy.copy()
                        sum_OF = sum_OF_after
                    sol_copy = solution.copy()
                    obj_function_copy = obj_function.copy()
    return sol_copy, best_obj_function, got_better_solution

def local_search_shift_interroute_BI(solution,obj_function,distance_matrix):
    got_better_solution = False
    best_obj_function = obj_function.copy()
    best_solution = solution.copy()
    sum_OF = sum(obj_function)
    sol_copy = solution.copy()
    obj_function_copy = obj_function.copy()

    amount_of_salesmen = len(solution)
    
    # Ordem direta de pesquisa (do menor para o maior índice)
    for route_index_a in range(amount_of_salesmen):
        for route_index_b in range(route_index_a+1, amount_of_salesmen):
            size_of_route_a = len(solution[route_index_a])
            size_of_route_b = len(solution[route_index_b])
            if size_of_route_a > 2:
                for point_a in range(size_of_route_a):
                    for point_b in range(size_of_route_b):
                        sol_copy, obj_function_copy = shift_interroute(sol_copy,route_index_a,route_index_b,point_a,point_b,obj_function_copy,distance_matrix)
    # Na função, o shift realoca o elemento da primeira solução (first_sol) à segunda (second_sol) na posição second_element_index
                        sum_OF_after = sum(obj_function_copy)
            
                        if sum_OF_after < sum_OF:
                            best_solution = sol_copy.copy()
                            best_obj_function = obj_function_copy.copy()
                            got_better_solution = True
                            sum_OF = sum_OF_after
                            print(best_solution)
                            print(best_obj_function)
                            print("_________________")
                        sol_copy = solution.copy()
                        obj_function_copy = obj_function.copy()

    # Ordem inversa de pesquisa (do maior para o menor índice)
    for route_index_a in reversed(range(amount_of_salesmen)):
        for route_index_b in reversed(range(route_index_a)):
            size_of_route_a = len(solution[route_index_a])
            size_of_route_b = len(solution[route_index_b])
            if size_of_route_a > 1:
                for point_a in range(size_of_route_a):
                    for point_b in range(size_of_route_b):
                        sol_copy, obj_function_copy = shift_interroute(sol_copy,route_index_a,route_index_b,point_a,point_b,obj_function_copy,distance_matrix)
                        sum_OF_after = sum(obj_function_copy)
            
                        if sum_OF_after < sum_OF:
                            best_solution = sol_copy.copy()
                            best_obj_function = obj_function_copy.copy()
                            got_better_solution = True
                            sum_OF = sum_OF_after
                            print(best_solution)
                            print(best_obj_function)
                            print("_________________")
                        sol_copy = solution.copy()
                        obj_function_copy = obj_function.copy()
    return best_solution, best_obj_function, got_better_solution

def local_search_swap_interroute_BI(solution,obj_function,distance_matrix):
    got_better_solution = False
    best_obj_function = obj_function.copy()
    best_solution = solution.copy()
    
    sum_OF = sum(obj_function)
    sol_copy = solution.copy()
    obj_function_copy = obj_function.copy() 
    amount_of_salesmen = len(solution)
    for route_index_a in range(amount_of_salesmen):
        for route_index_b in range(route_index_a+1, amount_of_salesmen):
            size_of_route_a = len(solution[route_index_a])
            size_of_route_b = len(solution[route_index_b])
            for point_a in range(size_of_route_a):
                for point_b in range(size_of_route_b):
                    sol_copy, obj_function_copy = swap_interroute(sol_copy,route_index_a,route_index_b,point_a,point_b,obj_function_copy,distance_matrix)
                    sum_OF_after = sum(obj_function_copy)
                    if sum_OF_after < sum_OF:
                        best_solution = sol_copy.copy()
                        best_obj_function = obj_function_copy.copy()
                        got_better_solution = True
                        sum_OF = sum_OF_after
                        print(best_solution)
                        print(best_obj_function)
                        print("_________________")
                    sol_copy = solution.copy()
                    obj_function_copy = obj_function.copy()
    return best_solution, best_obj_function, got_better_solution