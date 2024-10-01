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
    next_to_propose = {proposer: 0 for proposer in proposers}
    
    # Continue while there are free proposers who still have acceptors to propose to
    while free_proposers:
        proposer = free_proposers.pop(0)
        
        # Get the proposer's preference list
        proposer_prefs = proposer_preferences[proposer]
        
        # Check if the proposer has already proposed to everyone
        if next_to_propose[proposer] >= len(proposer_prefs):
            continue
        
        acceptor = proposer_prefs[next_to_propose[proposer]]
        next_to_propose[proposer] += 1
        
        # If the acceptor is free, engage them
        if acceptor not in engagements.values():
            engagements[proposer] = acceptor
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
            else:
                # If rejected, add the proposer back to free proposers
                free_proposers.append(proposer)

    return engagements

#------------------------------------------------------------------------------------------------------------
##School Choice Deferred Acceptance
def school_choice_da(students, schools, student_proposing=True):
    """
    Implements the deferred acceptance algorithm for school choice.
    
    Args:
    schools (dict): A dictionary where keys are school names and values are dictionaries containing:
                    'priorities': list of student names in order of priority
                    'capacity': integer representing the school's capacity
    students (dict): A dictionary where keys are student names and values are lists of school names in order of preference
    student_proposing (bool): If True, students propose to schools. If False, schools propose to students. Default is True.
    
    Returns:
    dict: A dictionary representing the matching, where keys are school names and values are lists of assigned students
    """
    
    # Expand schools with capacity > 1 into multiple "slots"
    expanded_schools = {}
    for school, info in schools.items():
        for i in range(info['capacity']):
            expanded_schools[f"{school}_{i+1}"] = {'priorities': info['priorities'], 'capacity': 1}
    
    # Adjust student preferences to include the new "slots"
    expanded_students = {}
    for student, prefs in students.items():
        expanded_prefs = []
        for school in prefs:
            expanded_prefs.extend([f"{school}_{i+1}" for i in range(schools[school]['capacity'])])
        expanded_students[student] = expanded_prefs
    
    if student_proposing:
        proposers = list(expanded_students.keys())
        proposer_preferences = expanded_students
        receivers = list(expanded_schools.keys())
        receiver_priorities = {school: expanded_schools[school]['priorities'] for school in expanded_schools}
    else:
        proposers = list(expanded_schools.keys())
        proposer_preferences = {school: expanded_schools[school]['priorities'] for school in expanded_schools}
        receivers = list(expanded_students.keys())
        receiver_priorities = expanded_students
    
    # Initialize all proposers as free
    free_proposers = proposers.copy()
    engagements = {}
    next_to_propose = {proposer: 0 for proposer in proposers}
    
    # Continue while there are free proposers who still have receivers to propose to
    while free_proposers:
        proposer = free_proposers.pop(0)
        
        # Get the proposer's preference list
        proposer_prefs = proposer_preferences[proposer]
        
        # Check if the proposer has already proposed to everyone
        if next_to_propose[proposer] >= len(proposer_prefs):
            continue
        
        receiver = proposer_prefs[next_to_propose[proposer]]
        next_to_propose[proposer] += 1
        
        # If the receiver is free, engage them
        if receiver not in engagements.values():
            engagements[proposer] = receiver
        else:
            # Find the current partner of the receiver
            current_partner = [p for p, r in engagements.items() if r == receiver][0]
            
            # If the receiver prefers this proposer to their current partner
            if receiver_priorities[receiver].index(proposer) < receiver_priorities[receiver].index(current_partner):
                # Break the current engagement
                del engagements[current_partner]
                # Create the new engagement
                engagements[proposer] = receiver
                # Add the previous partner back to free proposers
                free_proposers.append(current_partner)
            else:
                # If rejected, add the proposer back to free proposers
                free_proposers.append(proposer)

    # Combine the assignments for schools with multiple "slots"
    final_assignments = {}
    for proposer, receiver in engagements.items():
        if student_proposing:
            school = receiver.rsplit('_', 1)[0]
            if school not in final_assignments:
                final_assignments[school] = []
            final_assignments[school].append(proposer)
        else:
            student = receiver
            school = proposer.rsplit('_', 1)[0]
            if school not in final_assignments:
                final_assignments[school] = []
            final_assignments[school].append(student)
    
    return final_assignments

#------------------------------------------------------------------------------------------------------------
##Boston Mechanism
def boston_mechanism(students, schools):
    """
    Implements the Boston mechanism for school choice.
    
    Args:
    students (dict): A dictionary where keys are student names and values are lists of school preferences.
    schools (dict): A dictionary where keys are school names and values are dictionaries containing:
                    'priorities': list of student names in order of priority
                    'capacity': integer representing the school's capacity
    
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
    
    # Let students choose in the given order
    for student in student_order:
        for school in students[student]:
            if remaining_capacity[school] > 0:
                matching[student] = school
                remaining_capacity[school] -= 1
                break
        else:
            # If no preferred school has capacity, assign to null school
            matching[student] = None
    
    return matching

#------------------------------------------------------------------------------------------------------------
##Random Serial Dictatorship
import random

def random_serial_dictatorship(students, schools):
    """
    Implements the Random Serial Dictatorship algorithm for school choice.
    
    Args:
    students (dict): A dictionary where keys are student names and values are lists of school preferences.
    schools (dict): A dictionary where keys are school names and values are their capacities.
    
    Returns:
    dict: A dictionary representing the matching, where keys are student names and values are assigned schools.
    """
    
    # Create a random order of students
    student_order = list(students.keys())
    random.shuffle(student_order)
    
    # Initialize remaining capacities and matching
    remaining_capacity = schools.copy()
    matching = {}
    
    # Let students choose in the random order
    for student in student_order:
        for school in students[student]:
            if remaining_capacity[school] > 0:
                matching[student] = school
                remaining_capacity[school] -= 1
                break
        else:
            # If no preferred school has capacity, assign to None (unassigned)
            matching[student] = None
    
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
    prob = pulp.LpProblem("Stable_Matching_LP", pulp.LpMaximize)
    
    men = list(men_prefs.keys())
    women = list(women_prefs.keys())
    n = len(men)  # Assuming equal number of men and women
    
    # Create variables
    x = pulp.LpVariable.dicts("match", ((m, w) for m in men for w in women), lowBound=0, upBound=1)
    
    # Objective function
    prob += pulp.lpSum(x[m, w] for m in men for w in women)
    
    # Constraints
    # Each person is fully matched
    for m in men:
        prob += pulp.lpSum(x[m, w] for w in women) == 1
    
    for w in women:
        prob += pulp.lpSum(x[m, w] for m in men) == 1
    
    # Stability constraints
    for m in men:
        for w in women:
            prob += (x[m, w] + 
                     pulp.lpSum(x[m2, w] for m2 in men if women_prefs[w].index(m2) < women_prefs[w].index(m)) + 
                     pulp.lpSum(x[m, w2] for w2 in women if men_prefs[m].index(w2) < men_prefs[m].index(w))) >= 1
    
    # Solve the problem
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    
    # Extract the solution
    matching = {}
    for m in men:
        for w in women:
            if x[m, w].value() > 0.5:  # We consider a match if x[m, w] > 0.5
                matching[m] = w
                break
    
    return matching

#------------------------------------------------------------------------------------------------------------
##Egalitarian Stable Matching 

def egalitarian_stable_matching(men_prefs, women_prefs):
    """
    Calculates the Egalitarian Stable Matching.
    
    Args:
    men_prefs (dict): A dictionary where keys are men and values are lists of women in order of preference.
    women_prefs (dict): A dictionary where keys are women and values are lists of men in order of preference.
    
    Returns:
    dict: A dictionary representing the Egalitarian Stable Matching, where keys are men 
          and values are their matched women.
    """
    
    # Create the LP problem
    prob = pulp.LpProblem("Egalitarian_Stable_Matching", pulp.LpMinimize)
    
    men = list(men_prefs.keys())
    women = list(women_prefs.keys())
    
    # Create variables
    x = pulp.LpVariable.dicts("match", ((m, w) for m in men for w in women), lowBound=0, upBound=1)
    
    # Helper function to get rank
    def get_rank(prefs, a, b):
        return prefs[a].index(b) + 1
    
    # Objective function
    prob += pulp.lpSum((get_rank(men_prefs, m, w) + get_rank(women_prefs, w, m)) * x[m, w] 
                       for m in men for w in women)
    
    # Constraints
    # Each participant is matched exactly once
    for m in men:
        prob += pulp.lpSum(x[m, w] for w in women) == 1
    
    for w in women:
        prob += pulp.lpSum(x[m, w] for m in men) == 1
    
    # Stability constraints
    for m in men:
        for w in women:
            prob += (x[m, w] + 
                     pulp.lpSum(x[m, w2] for w2 in women if get_rank(men_prefs, m, w2) < get_rank(men_prefs, m, w)) + 
                     pulp.lpSum(x[m2, w] for m2 in men if get_rank(women_prefs, w, m2) < get_rank(women_prefs, w, m))) >= 1
    
    # Solve the problem
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    
    # Extract the solution
    matching = {m: max(women, key=lambda w: x[m, w].value()) for m in men}
    
    return matching

#------------------------------------------------------------------------------------------------------------
##Nash Stable Matching
def nash_stable_matching(men_valuations, women_valuations):
    """
    Calculates the Nash Stable Matching.
    
    Args:
    men_valuations (dict): A dictionary where keys are men and values are 
                           dictionaries of their valuations for each woman.
    women_valuations (dict): A dictionary where keys are women and values are 
                             dictionaries of their valuations for each man.
    
    Returns:
    dict: A dictionary representing the Nash Stable Matching, where keys are men 
          and values are their matched women.
    """
    
    # Create the LP problem
    prob = pulp.LpProblem("Nash_Stable_Matching", pulp.LpMaximize)
    
    men = list(men_valuations.keys())
    women = list(women_valuations.keys())
    
    # Create variables
    x = pulp.LpVariable.dicts("match", ((m, w) for m in men for w in women), lowBound=0, upBound=1)
    
    # Objective function (logarithmic transformation)
    prob += pulp.lpSum(x[m, w] * (math.log(men_valuations[m][w]) + math.log(women_valuations[w][m])) 
                       for m in men for w in women)
    
    # Constraints
    # Each participant is matched exactly once
    for m in men:
        prob += pulp.lpSum(x[m, w] for w in women) == 1
    
    for w in women:
        prob += pulp.lpSum(x[m, w] for m in men) == 1
    
    # Stability constraints
    for m in men:
        for w in women:
            prob += (x[m, w] + 
                     pulp.lpSum(x[m, w2] for w2 in women if men_valuations[m][w2] > men_valuations[m][w]) + 
                     pulp.lpSum(x[m2, w] for m2 in men if women_valuations[w][m2] > women_valuations[w][m])) >= 1
    
    # Solve the problem
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    
    # Extract the solution
    matching = {m: max(women, key=lambda w: x[m, w].value()) for m in men}
    
    return matching
#------------------------------------------------------------------------------------------------------------
##Utilitarian Stable Matching
def utilitarian_stable_matching(men_valuations, women_valuations):
    """
    Calculates the Utilitarian Stable Matching.
    
    Args:
    men_valuations (dict): A dictionary where keys are men and values are 
                           dictionaries of their valuations for each woman.
    women_valuations (dict): A dictionary where keys are women and values are 
                             dictionaries of their valuations for each man.
    
    Returns:
    dict: A dictionary representing the Utilitarian Stable Matching, where keys are men 
          and values are their matched women.
    """
    
    # Create the LP problem
    prob = pulp.LpProblem("Utilitarian_Stable_Matching", pulp.LpMaximize)
    
    men = list(men_valuations.keys())
    women = list(women_valuations.keys())
    
    # Create variables
    x = pulp.LpVariable.dicts("match", ((m, w) for m in men for w in women), lowBound=0, upBound=1)
    
    # Objective function
    prob += pulp.lpSum((men_valuations[m][w] + women_valuations[w][m]) * x[m, w] for m in men for w in women)
    
    # Constraints
    # Each participant is matched exactly once
    for m in men:
        prob += pulp.lpSum(x[m, w] for w in women) == 1
    
    for w in women:
        prob += pulp.lpSum(x[m, w] for m in men) == 1
    
    # Stability constraints
    for m in men:
        for w in women:
            prob += (x[m, w] + 
                     pulp.lpSum(x[m, w2] for w2 in women if men_valuations[m][w2] > men_valuations[m][w]) + 
                     pulp.lpSum(x[m2, w] for m2 in men if women_valuations[w][m2] > women_valuations[w][m])) >= 1
    
    # Solve the problem
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    
    # Extract the solution
    matching = {m: max(women, key=lambda w: x[m, w].value()) for m in men}
    
    return matching

#------------------------------------------------------------------------------------------------------------
##Linear Programming Algorithms without Stability Constraints

##Egalitarian Matching
def egalitarian_matching(men_prefs, women_prefs):
    """
    Calculates the Egalitarian Matching without stability constraint.
    
    Args:
    men_prefs (dict): A dictionary where keys are men and values are lists of women in order of preference.
    women_prefs (dict): A dictionary where keys are women and values are lists of men in order of preference.
    
    Returns:
    dict: A dictionary representing the Egalitarian Stable Matching, where keys are men 
          and values are their matched women.
    """
    
    # Create the LP problem
    prob = pulp.LpProblem("Egalitarian_Stable_Matching", pulp.LpMinimize)
    
    men = list(men_prefs.keys())
    women = list(women_prefs.keys())
    
    # Create variables
    x = pulp.LpVariable.dicts("match", ((m, w) for m in men for w in women), lowBound=0, upBound=1)
    
    # Helper function to get rank
    def get_rank(prefs, a, b):
        return prefs[a].index(b) + 1
    
    # Objective function
    prob += pulp.lpSum((get_rank(men_prefs, m, w) + get_rank(women_prefs, w, m)) * x[m, w] 
                       for m in men for w in women)
    
    # Constraints
    # Each participant is matched exactly once
    for m in men:
        prob += pulp.lpSum(x[m, w] for w in women) == 1
    
    for w in women:
        prob += pulp.lpSum(x[m, w] for m in men) == 1
     
    # Solve the problem
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    
    # Extract the solution
    matching = {m: max(women, key=lambda w: x[m, w].value()) for m in men}
    
    return matching
#------------------------------------------------------------------------------------------------------------

##Nash Matching
def nash_matching(men_valuations, women_valuations):
    """
    Calculates the Nash Matching without stability constraint.
    
    Args:
    men_valuations (dict): A dictionary where keys are men and values are 
                           dictionaries of their valuations for each woman.
    women_valuations (dict): A dictionary where keys are women and values are 
                             dictionaries of their valuations for each man.
    
    Returns:
    dict: A dictionary representing the Nash Matching, where keys are men 
          and values are their matched women.
    """
    
    # Create the LP problem
    prob = pulp.LpProblem("Nash_Stable_Matching", pulp.LpMaximize)
    
    men = list(men_valuations.keys())
    women = list(women_valuations.keys())
    
    # Create variables
    x = pulp.LpVariable.dicts("match", ((m, w) for m in men for w in women), lowBound=0, upBound=1)
    
    # Objective function (logarithmic transformation)
    prob += pulp.lpSum(x[m, w] * (math.log(men_valuations[m][w]) + math.log(women_valuations[w][m])) 
                       for m in men for w in women)
    
    # Constraints
    # Each participant is matched exactly once
    for m in men:
        prob += pulp.lpSum(x[m, w] for w in women) == 1
    
    for w in women:
        prob += pulp.lpSum(x[m, w] for m in men) == 1
    
    # Solve the problem
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    
    # Extract the solution
    matching = {m: max(women, key=lambda w: x[m, w].value()) for m in men}
    
    return matching

#------------------------------------------------------------------------------------------------------------
##Utilitarian Matching
def utilitarian_matching(men_valuations, women_valuations):
    """
    Calculates the Utilitarian Matching without stability constraint.
    
    Args:
    men_valuations (dict): A dictionary where keys are men and values are 
                           dictionaries of their valuations for each woman.
    women_valuations (dict): A dictionary where keys are women and values are 
                             dictionaries of their valuations for each man.
    
    Returns:
    dict: A dictionary representing the Utilitarian Stable Matching, where keys are men 
          and values are their matched women.
    """
    
    # Create the LP problem
    prob = pulp.LpProblem("Utilitarian_Stable_Matching", pulp.LpMaximize)
    
    men = list(men_valuations.keys())
    women = list(women_valuations.keys())
    
    # Create variables
    x = pulp.LpVariable.dicts("match", ((m, w) for m in men for w in women), lowBound=0, upBound=1)
    
    # Objective function
    prob += pulp.lpSum((men_valuations[m][w] + women_valuations[w][m]) * x[m, w] for m in men for w in women)
    
    # Constraints
    # Each participant is matched exactly once
    for m in men:
        prob += pulp.lpSum(x[m, w] for w in women) == 1
    
    for w in women:
        prob += pulp.lpSum(x[m, w] for m in men) == 1
    
    # Solve the problem
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    
    # Extract the solution
    matching = {m: max(women, key=lambda w: x[m, w].value()) for m in men}
    
    return matching

#------------------------------------------------------------------------------------------------------------
##Helper Functions
import random

def generate_instance(num_agents, num_schools=None, is_marriage_market=True, is_cardinal=False):
    """
    Generates random preference lists or valuations for a given number of agents in a matching market.
    For school choice, also generates random capacities and priorities for schools.
    
    Args:
    num_agents (int): Number of agents on each side of the market (or number of students for school choice)
    num_schools (int, optional): Number of schools for school choice. Default is num_agents // 2.
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
        if num_schools is None:
            num_schools = num_agents // 2
        num_schools = max(2, min(num_schools, num_agents))  # Ensure at least 2 schools and not more than num_agents
        side2 = [f'C{i+1}' for i in range(num_schools)]
    
    # Generate preferences or valuations for side1
    side1_preferences = {}
    for agent in side1:
        if is_cardinal:
            side1_preferences[agent] = {partner: random.uniform(1, 100) for partner in side2}
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
        total_capacity = num_agents // 2  # Set total capacity to half of students
        base_capacity = total_capacity // len(side2)  # Distribute capacity evenly
        remaining_capacity = total_capacity % len(side2)  # Any leftover capacity
        
        for school in side2:
            priorities = random.sample(side1, len(side1))
            capacity = base_capacity
            if remaining_capacity > 0:
                capacity += 1
                remaining_capacity -= 1
            side2_data[school] = {
                "priorities": priorities,
                "capacity": capacity
            }
    
    return side1_preferences, side2_data


def is_stable(matching, side1_preferences, side2_preferences, is_cardinal=False):
    """
    Check if a given matching is stable under the given preferences or valuations.
    
    Args:
    matching (dict): A dictionary representing the matching, where keys are side1 agents and values are their matched side2 agents.
    side1_preferences (dict): A dictionary where keys are side1 agents and values are either lists (ordinal) or dicts (cardinal) of side2 agents.
    side2_preferences (dict): A dictionary where keys are side2 agents and values are either lists (ordinal) or dicts (cardinal) of side1 agents.
    is_cardinal (bool): If True, preferences are cardinal valuations. If False, preferences are ordinal.
    
    Returns:
    bool: True if the matching is stable, False otherwise.
    """
    
    def prefers(agent, new_partner, current_partner, preferences):
        """Helper function to check if an agent prefers new_partner over current_partner."""
        if is_cardinal:
            return preferences[agent][new_partner] > preferences[agent][current_partner]
        else:
            return preferences[agent].index(new_partner) < preferences[agent].index(current_partner)
    
    for side1_agent, side2_agent in matching.items():
        if is_cardinal:
            current_value = side1_preferences[side1_agent][side2_agent]
            better_options = [partner for partner, value in side1_preferences[side1_agent].items() if value > current_value]
        else:
            current_rank = side1_preferences[side1_agent].index(side2_agent)
            better_options = side1_preferences[side1_agent][:current_rank]
        
        for preferred_partner in better_options:
            preferred_partner_match = next(s1 for s1, s2 in matching.items() if s2 == preferred_partner)
            
            if prefers(preferred_partner, side1_agent, preferred_partner_match, side2_preferences):
                print(f"Instability found: {side1_agent} and {preferred_partner} prefer each other over their current partners.")
                return False
    
    return True

