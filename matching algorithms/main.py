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

------------------------------------------------------------------------------------------------------------
##School Choice Deferred Acceptance



------------------------------------------------------------------------------------------------------------
##Boston Mechanism





------------------------------------------------------------------------------------------------------------
##Top Trading Cycle(TTC)





------------------------------------------------------------------------------------------------------------
##Serial Dictatorship






------------------------------------------------------------------------------------------------------------
##Random Serial Dictatorship





------------------------------------------------------------------------------------------------------------
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



------------------------------------------------------------------------------------------------------------
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

------------------------------------------------------------------------------------------------------------
##Nash Stable Matching


------------------------------------------------------------------------------------------------------------
##Sex-Equal Stable Matching



------------------------------------------------------------------------------------------------------------
##Utilitarian Stable Matching


------------------------------------------------------------------------------------------------------------
##Linear Programming Algorithms without Stability Constraints

##Egalitarian Matching


------------------------------------------------------------------------------------------------------------

##Nash Matching


------------------------------------------------------------------------------------------------------------

##Sex-Equal Matching

------------------------------------------------------------------------------------------------------------
##Utilitarian Matching


------------------------------------------------------------------------------------------------------------
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






