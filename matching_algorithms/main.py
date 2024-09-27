import random
import pulp
import numpy as np

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
                    'capacity': integer representing the school's capacity
                    'preferences': list of student names in order of preference
    
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
            for student in schools[school]['preferences']:
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

##Random Stable Matching

def random_stable_matching(men_preferences, women_preferences):
    # Create the LP problem
    prob = pulp.LpProblem("Stable_Matching", pulp.LpMinimize)
    
    men = list(men_preferences.keys())
    women = list(women_preferences.keys())
    
    # Create binary variables for each possible pairing
    x = pulp.LpVariable.dicts("match", ((m, w) for m in men for w in women), cat='Binary')
    
    # Objective function (can be arbitrary for finding any stable matching)
    prob += pulp.lpSum(x)
    
    # Constraint: Each person is matched to exactly one partner
    for m in men:
        prob += pulp.lpSum(x[m, w] for w in women) == 1
    
    for w in women:
        prob += pulp.lpSum(x[m, w] for m in men) == 1
    
    # Stability constraints
    for m in men:
        for w in women:
            # Find indices of current pair in preference lists
            m_pref_index = men_preferences[m].index(w)
            w_pref_index = women_preferences[w].index(m)
            
            # Sum of matches with more preferred partners
            m_preferred = pulp.lpSum(x[m, w2] for w2 in women if men_preferences[m].index(w2) < m_pref_index)
            w_preferred = pulp.lpSum(x[m2, w] for m2 in men if women_preferences[w].index(m2) < w_pref_index)
            
            # Stability constraint
            prob += x[m, w] + m_preferred + w_preferred >= 1
    
    # Solve the problem
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    
    # Extract the solution
    matching = {m: next(w for w in women if x[m, w].value() == 1) for m in men}
    
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


#------------------------------------------------------------------------------------------------------------
##Sex-Equal Stable Matching



#------------------------------------------------------------------------------------------------------------
##Utilitarian Stable Matching


#------------------------------------------------------------------------------------------------------------
##Linear Programming Algorithms without Stability Constraints

##Egalitarian Matching


#------------------------------------------------------------------------------------------------------------

##Nash Matching


#------------------------------------------------------------------------------------------------------------

##Sex-Equal Matching

#------------------------------------------------------------------------------------------------------------
##Utilitarian Matching


#------------------------------------------------------------------------------------------------------------
##Helper Functions

def populate_preferences(num_men):
    """
    Generates random preference lists for a given number of men and women assuming
    that the number of men and the number of women are equal.
    
    Args:
    num_men(int): Number of men/women
    
    
    Returns:
    tuple: Two dictionaries (men_preferences, women_preferences)
    """
    
    # Generate lists of men and women
    men = [f'M{i+1}' for i in range(num_men)]
    women = [f'W{i+1}' for i in range(num_men)]
    
    # Generate preferences for men
    men_preferences = {}
    for man in men:
        men_preferences[man] = random.sample(women, len(women))
    
    # Generate preferences for women
    women_preferences = {}
    for woman in women:
        women_preferences[woman] = random.sample(men, len(men))
    
    return men_preferences, women_preferences

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






