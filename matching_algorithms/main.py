import random
import pulp
import numpy as np
import math
##Marriage Market Deferred Acceptance

def deferred_acceptance(men_preferences, women_preferences, men_propose=True):
    """
    Implements the Gale-Shapley deferred acceptance algorithm for stable matching.
    
    Args:
    men_preferences (dict): A dictionary where keys are men and values are lists of women in order of preference.
    women_preferences (dict): A dictionary where keys are women and values are lists of men in order of preference.
    men_propose (bool): If True, men propose to women. If False, women propose to men. Default is True.
    
    Returns:
    dict: A dictionary representing the stable matching, where keys are proposers and values are their matched partners.
    """
    
    if men_propose:
        proposers = list(men_preferences.keys())
        proposer_preferences = men_preferences
        acceptors = list(women_preferences.keys())
        acceptor_preferences = women_preferences
    else:
        proposers = list(women_preferences.keys())
        proposer_preferences = women_preferences
        acceptors = list(men_preferences.keys())
        acceptor_preferences = men_preferences
    
    # Initialize all proposers as free
    free_proposers = proposers.copy()
    engagements = {}
    
    # Continue while there are free proposers who still have acceptors to propose to
    while free_proposers:
        proposer = free_proposers.pop(0)
        
        # Get the proposer's preference list
        proposer_prefs = proposer_preferences[proposer]
        
        for acceptor in proposer_prefs:
            # If the acceptor is free, engage them
            if acceptor not in engagements.values():
                engagements[proposer] = acceptor
                break
            else:
                # Find the current partner of the acceptor
                current_partner = [p for p, a in engagements.items() if a == acceptor][0]
                
                # If the acceptor prefers this proposer to their current partner
                if acceptor_preferences[acceptor].index(proposer) < acceptor_preferences[acceptor].index(current_partner):
                    # Break the current engagement
                    del engagements[current_partner]
                    # Create the new engagement
                    engagements[proposer] = acceptor
                    # Add the previous partner back to free proposers
                    free_proposers.append(current_partner)
                    break
        else:
            # If the proposer has proposed to all acceptors and is still unmatched, add them back to free proposers
            free_proposers.append(proposer)
    
    return engagements

#------------------------------------------------------------------------------------------------------------
##School Choice Deferred Acceptance

def school_choice_da(schools, students, student_proposing=True):
    """
    Implements the deferred acceptance algorithm for school choice.
    
    Args:
    schools (dict): A dictionary where keys are school names and values are dictionaries containing:
                    'preferences': list of student names in order of preference
                    'quota': integer representing the school's capacity
    students (dict): A dictionary where keys are student names and values are lists of school names in order of preference
    student_proposing (bool): If True, students propose to schools. If False, schools propose to students. Default is True.
    
    Returns:
    dict: A dictionary representing the matching, where keys are school names and values are lists of assigned students
    """
    
    if student_proposing:
        proposers = list(students.keys())
        proposer_preferences = students
        receivers = list(schools.keys())
        receiver_preferences = {school: schools[school]['preferences'] for school in schools}
        receiver_quotas = {school: schools[school]['quota'] for school in schools}
    else:
        proposers = list(schools.keys())
        proposer_preferences = {school: schools[school]['preferences'] for school in schools}
        receivers = list(students.keys())
        receiver_preferences = students
        receiver_quotas = {school: schools[school]['quota'] for school in schools}
    
    # Initialize all proposers as unmatched and all receivers as empty
    unmatched_proposers = proposers.copy()
    assignments = {receiver: [] for receiver in receivers}
    
    while unmatched_proposers:
        proposer = unmatched_proposers.pop(0)
        proposer_prefs = proposer_preferences[proposer]
        
        for receiver in proposer_prefs:
            receiver_prefs = receiver_preferences[receiver]
            current_assignments = assignments[receiver]
            
            if student_proposing:
                quota = receiver_quotas[receiver]
            else:
                quota = 1  # When schools propose, each student can only be assigned to one school
            
            if len(current_assignments) < quota:
                # Receiver has capacity, assign proposer
                assignments[receiver].append(proposer)
                break
            else:
                # Receiver is at capacity, check if proposer is preferred over any current assignment
                worst_assigned = min(current_assignments, key=lambda x: receiver_prefs.index(x))
                if receiver_prefs.index(proposer) < receiver_prefs.index(worst_assigned):
                    # Replace worst assigned with current proposer
                    assignments[receiver].remove(worst_assigned)
                    assignments[receiver].append(proposer)
                    unmatched_proposers.append(worst_assigned)
                    break
        else:
            # Proposer couldn't be assigned to any receiver in their preference list
            unmatched_proposers.append(proposer)
    
    if not student_proposing:
        # Invert the assignments so that schools are keys and students are values
        inverted_assignments = {school: [] for school in schools}
        for student, assigned_schools in assignments.items():
            for school in assigned_schools:
                inverted_assignments[school].append(student)
        assignments = inverted_assignments
    
    return assignments


#------------------------------------------------------------------------------------------------------------
##Boston Mechanism
def boston_mechanism(students, schools):
    """
    Implements the Boston mechanism for school choice.
    
    Args:
    students (dict): A dictionary where keys are student names and values are lists of school preferences.
    schools (dict): A dictionary where keys are school names and values are dictionaries containing:
                    'capacity': integer representing the school's capacity
                    'priorities': list of student names in order of priority
    
    Returns:
    dict: A dictionary representing the matching, where keys are student names and values are assigned schools.
    """
    
    matching = {student: None for student in students}
    school_capacities = {school: schools[school]['capacity'] for school in schools}
    
    # Iterate through preference rounds
    for preference_level in range(max(len(prefs) for prefs in students.values())):
        # Collect students who are applying to schools in this round
        applications = {}
        for student, preferences in students.items():
            if matching[student] is None and preference_level < len(preferences):
                school = preferences[preference_level]
                if school not in applications:
                    applications[school] = []
                applications[school].append(student)
        
        # Process applications for each school
        for school, applicants in applications.items():
            available_seats = school_capacities[school]
            if available_seats > 0:
                # Sort applicants by priority
                sorted_applicants = sorted(applicants, key=lambda s: schools[school]['priorities'].index(s))
                
                # Assign seats to top priority applicants
                for student in sorted_applicants[:available_seats]:
                    matching[student] = school
                    school_capacities[school] -= 1
    
    return matching


#------------------------------------------------------------------------------------------------------------

##Top Trading Cycle(TTC)

def top_trading_cycles(students, schools):
    """
    Implements the Top Trading Cycles algorithm for school choice.
    
    Args:
    students (dict): A dictionary where keys are student names and values are lists of school preferences.
    schools (dict): A dictionary where keys are school names and values are dictionaries containing:
                    'priorities': list of student names in order of preference
                    'capacity': integer representing the school's capacity
                    
    
    Returns:
    dict: A dictionary representing the matching, where keys are student names and values are assigned schools.
    """
    
    # Initialize
    unassigned_students = set(students.keys())
    school_capacities = {school: schools[school]['capacity'] for school in schools}
    current_owners = {school: [] for school in schools}
    matching = {}

    while unassigned_students:
        # Step 1: Point to most preferred school/student
        student_pointers = {}
        school_pointers = {school: [] for school in schools}
        
        for student in unassigned_students:
            for school in students[student]:
                if school_capacities[school] > 0:
                    student_pointers[student] = school
                    break
        
        for school in schools:
            for student in schools[school]['priorities']:
                if student in unassigned_students:
                    school_pointers[school].append(student)
                    if len(school_pointers[school]) == school_capacities[school]:
                        break

        # Step 2: Identify cycles
        assigned_in_cycle = set()
        for student in unassigned_students:
            if student in assigned_in_cycle:
                continue
            
            cycle = [student]
            current = student
            while True:
                school = student_pointers[current]
                cycle.append(school)
                if not school_pointers[school]:
                    break
                current = school_pointers[school][0]
                if current in cycle:
                    cycle = cycle[cycle.index(current):]
                    for i in range(0, len(cycle), 2):
                        matching[cycle[i]] = cycle[i+1]
                        assigned_in_cycle.add(cycle[i])
                        school_capacities[cycle[i+1]] -= 1
                    break
                cycle.append(current)

        # Remove assigned students
        unassigned_students -= assigned_in_cycle

    return matching


#------------------------------------------------------------------------------------------------------------
##Serial Dictatorship
def serial_dictatorship(students, schools, student_order):
    """
    Implements the Serial Dictatorship algorithm for school choice.
    
    Args:
    students (dict): A dictionary where keys are student names and values are lists of school preferences.
    schools (dict): A dictionary where keys are school names and values are their capacities.
    student_order (list): List of student names in the order they should choose schools.
    
    Returns:
    dict: A dictionary representing the matching, where keys are student names and values are assigned schools.
    """
        
    # Initialize remaining capacities and matching
    remaining_capacity = schools.copy()
    matching = {}
    
    print("Student order:")
    for i, student in enumerate(student_order, 1):
        print(f"{i}. {student}")
    
    print("\nAssignment process:")
    # Let students choose in the given order
    for student in student_order:
        for school in students[student]:
            if remaining_capacity[school] > 0:
                matching[student] = school
                remaining_capacity[school] -= 1
                print(f"{student} chooses {school}")
                break
        else:
            # If no preferred school has capacity, assign to null school
            matching[student] = None
            print(f"{student} remains unassigned")
    
    return matching

#------------------------------------------------------------------------------------------------------------
##Random Serial Dictatorship
def random_serial_dictatorship(students, schools):
    """
    Implements the Random Serial Dictatorship algorithm for school choice.
    
    Args:
    students (dict): A dictionary where keys are student names and values are lists of school preferences.
    schools (dict): A dictionary where keys are school names and values are their capacities.
    
    Returns:
    dict: A dictionary representing the matching, where keys are student names and values are assigned schools.
    """
    
    # Create a random ordering of students
    student_order = list(students.keys())
    random.shuffle(student_order)
    
    # Initialize remaining capacities and matching
    remaining_capacity = schools.copy()
    matching = {}
    
    print("Random student order:")
    for i, student in enumerate(student_order, 1):
        print(f"{i}. {student}")
    
    print("\nAssignment process:")
    # Let students choose in the random order
    for student in student_order:
        for school in students[student]:
            if remaining_capacity[school] > 0:
                matching[student] = school
                remaining_capacity[school] -= 1
                print(f"{student} chooses {school}")
                break
        else:
            # If no preferred school has capacity, assign to null school
            matching[student] = None
            print(f"{student} remains unassigned")
    
    return matching

#------------------------------------------------------------------------------------------------------------
##Linear Programming Algorithms with Stability Constraints

##Stable Matching via Linear Programming
def stable_matching_lp(men_prefs, women_prefs):
    """
    Finds a stable matching using linear programming.
    
    Args:
    men_prefs (dict): A dictionary where keys are men and values are lists of women in order of preference.
    women_prefs (dict): A dictionary where keys are women and values are lists of men in order of preference.
    
    Returns:
    dict: A dictionary representing the stable matching, where keys are men and values are their matched women.
    """
    
    # Create the LP problem
    prob = pulp.LpProblem("Stable_Matching", pulp.LpMaximize)
    
    men = list(men_prefs.keys())
    women = list(women_prefs.keys())
    n = len(men)  # Assuming equal number of men and women
    
    # Create binary variables for each possible pairing
    x = pulp.LpVariable.dicts("match", ((m, w) for m in men for w in women), cat='Binary')
    
    # Objective function: maximize the number of matches (will always be n)
    prob += pulp.lpSum(x[m, w] for m in men for w in women)
    
    # Constraint: Each person is matched to exactly one partner
    for m in men:
        prob += pulp.lpSum(x[m, w] for w in women) == 1
    
    for w in women:
        prob += pulp.lpSum(x[m, w] for m in men) == 1
    
    # Stability constraints
    for m in men:
        for w in women:
            # Find indices of current pair in preference lists
            m_pref_index = men_prefs[m].index(w)
            w_pref_index = women_prefs[w].index(m)
            
            # Sum of x[m,w'] where m prefers w' to w
            m_preferred = pulp.lpSum(x[m, w_prime] for w_prime in men_prefs[m][:m_pref_index])
            
            # Sum of x[m',w] where w prefers m' to m
            w_preferred = pulp.lpSum(x[m_prime, w] for m_prime in women_prefs[w][:w_pref_index])
            
            # Stability constraint
            prob += x[m, w] + m_preferred + w_preferred >= 1
    
    # Solve the problem
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    
    # Extract the solution
    matching = {m: next(w for w in women if x[m, w].value() > 0.5) for m in men}
    
    return matching

#------------------------------------------------------------------------------------------------------------
##Egalitarian Stable Matching 

def egalitarian_stable_matching(men_preferences, women_preferences):
    prob = pulp.LpProblem("Egalitarian_Stable_Matching", pulp.LpMinimize)
    
    men = list(men_preferences.keys())
    women = list(women_preferences.keys())
    
    x = pulp.LpVariable.dicts("match", ((m, w) for m in men for w in women), lowBound=0, upBound=1, cat='Continuous')
    
    prob += pulp.lpSum(
        (men_preferences[m].index(w) + women_preferences[w].index(m)) * x[(m, w)]
        for m in men for w in women
    )
    
    for m in men:
        prob += pulp.lpSum(x[(m, w)] for w in women) == 1
    
    for w in women:
        prob += pulp.lpSum(x[(m, w)] for m in men) == 1
    
    for m in men:
        for w in women:
            prob += (
                x[(m, w)] +
                pulp.lpSum(x[(m, w2)] for w2 in women if men_preferences[m].index(w2) < men_preferences[m].index(w)) +
                pulp.lpSum(x[(m2, w)] for m2 in men if women_preferences[w].index(m2) < women_preferences[w].index(m))
                >= 1
            )
    
    prob.solve(pulp.PULP_CBC_CMD(msg=0))  # Suppress solver output
    
    matching = {}
    for m in men:
        for w in women:
            if x[(m, w)].value() > 0.5:
                matching[m] = w
    
    return matching

#------------------------------------------------------------------------------------------------------------
##Nash Stable Matching
def nash_stable_matching(men_valuations, women_valuations):
    """
    Calculates the Nash stable matching using linear programming.
    This matching maximizes the product of utilities among all stable matchings.
    
    Args:
    men_valuations (dict): A dictionary where keys are men and values are dictionaries of their valuations for each woman.
    women_valuations (dict): A dictionary where keys are women and values are dictionaries of their valuations for each man.
    
    Returns:
    dict: A dictionary representing the Nash stable matching, where keys are men and values are their matched women.
    """
    
    # Create the LP problem
    prob = pulp.LpProblem("Nash_Stable_Matching", pulp.LpMaximize)
    
    men = list(men_valuations.keys())
    women = list(women_valuations.keys())
    
    # Create binary variables for each possible pairing
    x = pulp.LpVariable.dicts("match", ((m, w) for m in men for w in women), cat='Binary')
    
    # Create continuous variables for the log of utilities
    log_utility = pulp.LpVariable.dicts("log_utility", ((m, w) for m in men for w in women), lowBound=None)
    
    # Objective function: maximize sum of log utilities (equivalent to maximizing product of utilities)
    prob += pulp.lpSum(log_utility[m, w] for m in men for w in women)
    
    # Constraint: Each person is matched to exactly one partner
    for m in men:
        prob += pulp.lpSum(x[m, w] for w in women) == 1
    
    for w in women:
        prob += pulp.lpSum(x[m, w] for m in men) == 1
    
    # Stability constraints
    for m in men:
        for w in women:
            for m2 in men:
                if m2 != m:
                    prob += x[m, w] + x[m2, w] + pulp.lpSum(x[m, w2] for w2 in women if men_valuations[m][w2] > men_valuations[m][w]) + \
                            pulp.lpSum(x[m2, w2] for w2 in women if women_valuations[w][m2] > women_valuations[w][m]) >= 1
    
    # Logarithmic utility constraints
    for m in men:
        for w in women:
            total_value = men_valuations[m][w] + women_valuations[w][m]
            if total_value > 0:
                prob += log_utility[m, w] <= math.log(total_value) + 1000 * (x[m, w] - 1)
                prob += log_utility[m, w] >= math.log(total_value) - 1000 * (1 - x[m, w])
            else:
                prob += log_utility[m, w] <= -1000 * (1 - x[m, w])
                prob += log_utility[m, w] >= -1000 * x[m, w]
    
    # Solve the problem
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    
    # Extract the solution
    matching = {m: next(w for w in women if x[m, w].value() > 0.5) for m in men}
    
    return matching
#------------------------------------------------------------------------------------------------------------
##Utilitarian Stable Matching
def utilitarian_stable_matching(men_valuations, women_valuations):
    """
    Calculates the utilitarian stable matching using linear programming.
    
    Args:
    men_valuations (dict): A dictionary where keys are men and values are dictionaries of their valuations for each woman.
    women_valuations (dict): A dictionary where keys are women and values are dictionaries of their valuations for each man.
    
    Returns:
    dict: A dictionary representing the utilitarian stable matching, where keys are men and values are their matched women.
    """
    
    # Create the LP problem
    prob = pulp.LpProblem("Utilitarian_Stable_Matching", pulp.LpMaximize)
    
    men = list(men_valuations.keys())
    women = list(women_valuations.keys())
    
    # Create binary variables for each possible pairing
    x = pulp.LpVariable.dicts("match", ((m, w) for m in men for w in women), cat='Binary')
    
    # Objective function: maximize total valuation
    prob += pulp.lpSum(men_valuations[m][w] * x[m, w] + women_valuations[w][m] * x[m, w] for m in men for w in women)
    
    # Constraint: Each person is matched to exactly one partner
    for m in men:
        prob += pulp.lpSum(x[m, w] for w in women) == 1
    
    for w in women:
        prob += pulp.lpSum(x[m, w] for m in men) == 1
    
    # Stability constraints
    for m in men:
        for w in women:
            for m2 in men:
                if m2 != m:
                    prob += x[m, w] + x[m2, w] + pulp.lpSum(x[m, w2] for w2 in women if men_valuations[m][w2] > men_valuations[m][w]) + \
                            pulp.lpSum(x[m2, w2] for w2 in women if women_valuations[w][m2] > women_valuations[w][m]) >= 1
    
    # Solve the problem
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    
    # Extract the solution
    matching = {m: next(w for w in women if x[m, w].value() > 0.5) for m in men}
    
    return matching

#------------------------------------------------------------------------------------------------------------
##Linear Programming Algorithms without Stability Constraints

##Egalitarian Matching
def egalitarian_matching(men_prefs, women_prefs):
    """
    Implements the Egalitarian matching algorithm without stability constraints.
    
    Args:
    men_prefs (dict): A dictionary where keys are men and values are lists of women in order of preference.
    women_prefs (dict): A dictionary where keys are women and values are lists of men in order of preference.
    
    Returns:
    dict: A dictionary representing the egalitarian matching, where keys are men and values are their matched women.
    """
    
    # Create the LP problem
    prob = pulp.LpProblem("Egalitarian_Matching", pulp.LpMinimize)
    
    men = list(men_prefs.keys())
    women = list(women_prefs.keys())
    
    # Create binary variables for each possible pairing
    x = pulp.LpVariable.dicts("match", ((m, w) for m in men for w in women), cat='Binary')
    
    # Objective function: minimize the sum of preference ranks
    prob += pulp.lpSum(men_prefs[m].index(w) * x[m, w] + women_prefs[w].index(m) * x[m, w] for m in men for w in women)
    
    # Constraint: Each person is matched to exactly one partner
    for m in men:
        prob += pulp.lpSum(x[m, w] for w in women) == 1
    
    for w in women:
        prob += pulp.lpSum(x[m, w] for m in men) == 1
    
    # Solve the problem
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    
    # Extract the solution
    matching = {m: next(w for w in women if x[m, w].value() > 0.5) for m in men}
    
    return matching
#------------------------------------------------------------------------------------------------------------

##Nash Matching
def nash_matching(men_valuations, women_valuations):
    """
    Calculates the Nash matching without stability constraints.
    This matching maximizes the product of utilities without enforcing stability.
    
    Args:
    men_valuations (dict): A dictionary where keys are men and values are dictionaries of their valuations for each woman.
    women_valuations (dict): A dictionary where keys are women and values are dictionaries of their valuations for each man.
    
    Returns:
    dict: A dictionary representing the Nash matching, where keys are men and values are their matched women.
    """
    
    # Create the LP problem
    prob = pulp.LpProblem("Nash_Matching_Without_Stability", pulp.LpMaximize)
    
    men = list(men_valuations.keys())
    women = list(women_valuations.keys())
    
    # Create binary variables for each possible pairing
    x = pulp.LpVariable.dicts("match", ((m, w) for m in men for w in women), cat='Binary')
    
    # Create continuous variables for the log of utilities
    log_utility = pulp.LpVariable.dicts("log_utility", ((m, w) for m in men for w in women), lowBound=None)
    
    # Objective function: maximize sum of log utilities (equivalent to maximizing product of utilities)
    prob += pulp.lpSum(log_utility[m, w] for m in men for w in women)
    
    # Constraint: Each person is matched to exactly one partner
    for m in men:
        prob += pulp.lpSum(x[m, w] for w in women) == 1
    
    for w in women:
        prob += pulp.lpSum(x[m, w] for m in men) == 1
    
    # Logarithmic utility constraints
    for m in men:
        for w in women:
            total_value = men_valuations[m][w] + women_valuations[w][m]
            if total_value > 0:
                prob += log_utility[m, w] <= math.log(total_value) + 1000 * (x[m, w] - 1)
                prob += log_utility[m, w] >= math.log(total_value) - 1000 * (1 - x[m, w])
            else:
                prob += log_utility[m, w] <= -1000 * (1 - x[m, w])
                prob += log_utility[m, w] >= -1000 * x[m, w]
    
    # Solve the problem
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    
    # Extract the solution
    matching = {m: next(w for w in women if x[m, w].value() > 0.5) for m in men}
    
    return matching

#------------------------------------------------------------------------------------------------------------
##Utilitarian Matching
def utilitarian_matching(men_valuations, women_valuations):
    """
    Calculates the utilitarian matching without stability constraints.
    This matching maximizes the sum of utilities for all matched pairs.
    
    Args:
    men_valuations (dict): A dictionary where keys are men and values are dictionaries of their valuations for each woman.
    women_valuations (dict): A dictionary where keys are women and values are dictionaries of their valuations for each man.
    
    Returns:
    dict: A dictionary representing the utilitarian matching, where keys are men and values are their matched women.
    """
    
    # Create the LP problem
    prob = pulp.LpProblem("Utilitarian_Matching", pulp.LpMaximize)
    
    men = list(men_valuations.keys())
    women = list(women_valuations.keys())
    
    # Create binary variables for each possible pairing
    x = pulp.LpVariable.dicts("match", ((m, w) for m in men for w in women), cat='Binary')
    
    # Objective function: maximize total valuation
    prob += pulp.lpSum(men_valuations[m][w] * x[m, w] + women_valuations[w][m] * x[m, w] for m in men for w in women)
    
    # Constraint: Each person is matched to exactly one partner
    for m in men:
        prob += pulp.lpSum(x[m, w] for w in women) == 1
    
    for w in women:
        prob += pulp.lpSum(x[m, w] for m in men) == 1
    
    # Solve the problem
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    
    # Extract the solution
    matching = {m: next(w for w in women if x[m, w].value() > 0.5) for m in men}
    
    return matching

#------------------------------------------------------------------------------------------------------------
##Helper Functions
import random

def generate_instance(num_agents, is_marriage_market=True, is_cardinal=False):
    """
    Generates random preference lists or valuations for a given number of agents in a matching market.
    For school choice, also generates random capacities and priorities for schools.
    
    Args:
    num_agents (int): Number of agents on each side of the market (or number of students for school choice)
    is_marriage_market (bool): If True, generates for marriage market. If False, generates for school choice.
    is_cardinal (bool): If True, generates cardinal valuations. If False, generates ordinal preferences.
    
    Returns:
    tuple: Two dictionaries (side1_preferences, side2_data)
    """
    
    # Generate lists of agents
    if is_marriage_market:
        side1 = [f'M{i+1}' for i in range(num_agents)]
        side2 = [f'W{i+1}' for i in range(num_agents)]
    else:
        side1 = [f'S{i+1}' for i in range(num_agents)]
        num_schools = max(1, num_agents // 2)  # Ensure at least 1 school
        side2 = [f'C{i+1}' for i in range(num_schools)]
    
    # Generate preferences or valuations for side1
    side1_preferences = {}
    for agent in side1:
        if is_cardinal:
            side1_preferences[agent] = {partner: random.uniform(0, 100) for partner in side2}
        else:
            side1_preferences[agent] = random.sample(side2, len(side2))
    
    # Generate preferences/priorities and capacities for side2
    side2_data = {}
    if is_marriage_market:
        for agent in side2:
            if is_cardinal:
                side2_data[agent] = {partner: random.uniform(1, 100) for partner in side1}
            else:
                side2_data[agent] = random.sample(side1, len(side1))
    else:
        total_capacity = random.randint(num_agents // 2, num_agents - 1)  # Ensure total capacity is less than num_agents
        remaining_capacity = total_capacity
        for school in side2:
            priorities = random.sample(side1, len(side1))
            if remaining_capacity > 0:
                capacity = random.randint(1, remaining_capacity)
                remaining_capacity -= capacity
            else:
                capacity = 0
            side2_data[school] = {
                "priorities": priorities,
                "capacity": capacity
            }
        # Assign any remaining capacity to the last school
        side2_data[side2[-1]]["capacity"] += remaining_capacity
    
    return side1_preferences, side2_data


def is_stable(matching, men_preferences, women_preferences):
    """
    Check if a given matching is stable under the given preferences.
    
    Args:
    matching (dict): A dictionary representing the matching, where keys are men and values are their matched women.
    men_preferences (dict): A dictionary where keys are men and values are lists of women in order of preference.
    women_preferences (dict): A dictionary where keys are women and values are lists of men in order of preference.
    
    Returns:
    bool: True if the matching is stable, False otherwise.
    """
    
    def prefers(person, new_partner, current_partner, preferences):
        """Helper function to check if a person prefers new_partner over current_partner."""
        return preferences[person].index(new_partner) < preferences[person].index(current_partner)
    
    for man, woman in matching.items():
        man_prefs = men_preferences[man]
        current_rank = man_prefs.index(woman)
        
        # Check if man prefers any woman over his current partner
        for preferred_woman in man_prefs[:current_rank]:
            preferred_woman_partner = next(m for m, w in matching.items() if w == preferred_woman)
            
            # If the preferred woman also prefers this man over her current partner, it's unstable
            if prefers(preferred_woman, man, preferred_woman_partner, women_preferences):
                print(f"Instability found: {man} and {preferred_woman} prefer each other over their current partners.")
                return False
    
    # If we've checked all pairs and found no instabilities, the matching is stable
    return True

