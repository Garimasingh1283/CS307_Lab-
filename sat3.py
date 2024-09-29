import random
from typing import List, Tuple

# Helper function to generate a random 3-SAT instance
def generate_3sat_instance(n: int, m: int) -> List[List[int]]:
    clauses = []
    for _ in range(m):
        clause = set()
        while len(clause) < 3:
            var = random.randint(1, n)
            # Randomly decide to negate the variable or not
            if random.random() < 0.5:
                var = -var
            clause.add(var)
        clauses.append(list(clause))
    return clauses

# Hill Climbing algorithm
def hill_climbing(clauses: List[List[int]], n: int, max_steps: int = 1000) -> Tuple[List[int], bool]:
    current = [random.choice([True, False]) for _ in range(n)]
    for _ in range(max_steps):
        satisfied = sum(any((lit > 0) == current[abs(lit) - 1] for lit in clause) for clause in clauses)
        if satisfied == len(clauses):
            return current, True
        
        # Generate neighbors
        neighbors = []
        for i in range(n):
            neighbor = current[:]
            neighbor[i] = not neighbor[i]
            neighbors.append(neighbor)
        
        # Select the best neighbor
        next_state = max(neighbors, key=lambda neighbor: sum(any((lit > 0) == neighbor[abs(lit) - 1] for lit in clause) for clause in clauses))
        current = next_state
    
    return current, False

# Beam Search algorithm
def beam_search(clauses: List[List[int]], n: int, beam_width: int, max_steps: int = 1000) -> Tuple[List[int], bool]:
    population = [[random.choice([True, False]) for _ in range(n)] for _ in range(beam_width)]
    for _ in range(max_steps):
        new_population = []
        for individual in population:
            satisfied = sum(any((lit > 0) == individual[abs(lit) - 1] for lit in clause) for clause in clauses)
            if satisfied == len(clauses):
                return individual, True
            
            # Generate neighbors
            for i in range(n):
                neighbor = individual[:]
                neighbor[i] = not neighbor[i]
                new_population.append(neighbor)
        
        # Select the best individuals
        population = sorted(new_population, key=lambda ind: sum(any((lit > 0) == ind[abs(lit) - 1] for lit in clause) for clause in clauses), reverse=True)[:beam_width]
    
    return population[0], False

# Variable Neighborhood Descent
def variable_neighborhood_descent(clauses: List[List[int]], n: int, max_steps: int = 1000) -> Tuple[List[int], bool]:
    current = [random.choice([True, False]) for _ in range(n)]
    
    for _ in range(max_steps):
        satisfied = sum(any((lit > 0) == current[abs(lit) - 1] for lit in clause) for clause in clauses)
        if satisfied == len(clauses):
            return current, True
        
        # Explore different neighborhoods
        for i in range(n):
            neighbor = current[:]
            neighbor[i] = not neighbor[i]
            if sum(any((lit > 0) == neighbor[abs(lit) - 1] for lit in clause) for clause in clauses) > satisfied:
                current = neighbor
    
    return current, False

# Run experiment based on user input
def run_experiment(n: int, m: int, beam_width: int):
    clauses = generate_3sat_instance(n, m)
    
    print("Running Hill Climbing...")
    hc_solution, hc_success = hill_climbing(clauses, n)
    print("Hill Climbing:", "Satisfiable" if hc_success else "Not Satisfiable")
    
    print("Running Beam Search...")
    bs_solution, bs_success = beam_search(clauses, n, beam_width)
    print("Beam Search:", "Satisfiable" if bs_success else "Not Satisfiable")
    
    print("Running Variable Neighborhood Descent...")
    vnd_solution, vnd_success = variable_neighborhood_descent(clauses, n)
    print("Variable Neighborhood Descent:", "Satisfiable" if vnd_success else "Not Satisfiable")

# Main function to take input from the user
if __name__ == "__main__":  # Corrected here
    n = int(input("Enter the number of variables (n): "))
    m = int(input("Enter the number of clauses (m): "))
    beam_width = int(input("Enter the beam width for Beam Search (e.g., 3 or 4): "))
    
    print(f"\nExperiment with n={n}, m={m}, Beam Width={beam_width}:")
    run_experiment(n, m, beam_width) 
