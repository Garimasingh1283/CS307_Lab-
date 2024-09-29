import random

#function to generate random k sat
def generate_k_sat(k, m, n):
    clauses = []
    
    #to generate m clauses
    for _ in range(m):
        clause = set()  # no duplicate variables in a clause
        
        while len(clause) < k:
            var = random.randint(1, n)  
            negation = random.choice([True, False])  
            
            literal = -var if negation else var 
            clause.add(literal)  
        
        clauses.append(list(clause)) 
    
    return clauses

#display result as CNF
def print_ksat(clauses):
    formula = " ∧ ".join(
        "(" + " ∨ ".join([f"x{abs(lit)}" if lit > 0 else f"¬x{abs(lit)}" for lit in clause]) + ")"
        for clause in clauses
    )
    print(formula)



#parameters - given
k = 3  # Clause length
m = 5  # Number of clauses
n = 4  # Number of variables



clauses = generate_k_sat(k, m, n)
print_ksat(clauses)
