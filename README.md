# Matching Algorithms

This project implements a variety of matching algorithms, including the Deferred Acceptance algorithm, the Boston Mechanism, the Top Trading Cycles (TTC) mechanism, and several linear programming approaches. These algorithms are widely applicable in various domains such as school admissions, job assignments, and resource allocation problems. Their effectiveness in creating stable and efficient matchings makes them valuable tools in economics, computer science and operations research.


## Table of Contents

- [Installation](#installation)
- [Algorithms Implemented](#algorithms-implemented)
  - [Marriage Market Deferred Acceptance](#marriage-market-deferred-acceptance)
  - [School Choice Deferred Acceptance](#school-choice-deferred-acceptance)
  - [Boston Mechanism](#boston-mechanism)
  - [Top Trading Cycles for School Choice](#top-trading-cycles-for-school-choice)
  - [Serial Dictatorship](#serial-dictatorship)
  - [Random Serial Dictatorship](#random-serial-dictatorship)
  - [Linear Programming Algorithms with Stability Constraint](#linear-programming-algorithms-with-stability-constraint)
    - [Stable Matching via Linear Programming](#stable-matching-via-linear-programming)
    - [Egalitarian Stable Matching](#egalitarian-stable-matching)
    - [Nash Stable Matching](#nash-stable-matching)
    - [Utilitarian Stable Matching](#utilitarian-stable-matching)
  - [Linear Programming Algorithms without Stability Constraint](#linear-programming-algorithms-without-stability-constraint)
    - [Egalitarian Matching](#egalitarian-matching)
    - [Nash Matching](#nash-matching)
    - [Utilitarian Matching](#utilitarian-matching)
- [Helper Functions](#helper-functions)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install the package, use pip:

```bash
pip install matching_algorithms
```

Alternatively, you can clone the repository and install it manually:

```bash
git clone https://github.com/Tekdirfan/Matching-Algorithms.git
cd matching_algorithms
pip install .

```


# Algorithms Implemented

# Marriage Market Deferred Acceptance

## Overview

The Deferred Acceptance algorithm for the Marriage Market is a two-sided matching algorithm that pairs participants from two groups (e.g., men and women) based on their preferences. The algorithm ensures that no pair of participants would rather be matched with each other than with their current match, leading to a stable matching. In this setup, one group (typically men) proposes to the other group, and participants from the second group (women) accept or reject proposals based on their preferences.

## Algorithm Steps

The algorithm proceeds in rounds:

1. Each participant in the proposing group proposes to their most-preferred partner who has not yet rejected them.
2. Participants in the receiving group tentatively accept the most-preferred proposal they have received so far and reject the others.
3. Rejected participants propose to their next most-preferred partner in the next round.
4. The process continues until no more proposals are made, and the tentative matches become final.

## Characteristics
- Stability: The algorithm always produces a stable matching, where no two participants would prefer each other over their assigned partners.
- Optimality: The resulting matching is optimal for the proposing side. For example, if men propose, the outcome is the best possible stable matching for all men.
- Truthfulness: It's a dominant strategy for the proposing side to reveal their true preferences. However, the receiving side may have incentives to misrepresent their preferences.
- Efficiency: The algorithm terminates in at most n^2 rounds, where n is the number of participants on each side

## Parameters

- `men_preferences` (dict): A dictionary where keys are men and values are lists of women in order of preference.
- `women_preferences` (dict): A dictionary where keys are women and values are lists of men in order of preference.
- `men_propose` (bool, optional): If True, men propose to women. If False, women propose to men. Default is True.

## Returns

- `dict`: A dictionary representing the stable matching, where keys are proposers and values are their matched partners.

## Runtime Table:
| Number of Agents per Side | Average Runtime (seconds) |
|---------------------------|---------------------------|
| 10                        | 0.000132                  |
| 50                        | 0.001144                  |
| 90                        | 0.003932                  |
| 130                       | 0.007014                  |
| 170                       | 0.013835                  |
| 210                       | 0.020685                  |

![Deferred Acceptance Algorithm Runtime](images/da_runtime.png)

## Usage
```python
from matching_algorithms import deferred_acceptance

men_preferences = {
    'M1': ['W1', 'W2', 'W3'],
    'M2': ['W2', 'W1', 'W3'],
    'M3': ['W3', 'W1', 'W2']
}

women_preferences = {
    'W1': ['M2', 'M3', 'M1'],
    'W2': ['M1', 'M2', 'M3'],
    'W3': ['M3', 'M1', 'M2']
}

matches = deferred_acceptance(men_preferences, women_preferences,men_propose=True)

print("Final Matches:")
for man, woman in matches.items():
    print(f"{man} is matched with {woman}")
```

# School Choice Deferred Acceptance

## Overview

The **School Choice Deferred Acceptance** algorithm adapts the classic Deferred Acceptance algorithm to the context of assigning students to schools. It creates a stable matching between students and schools based on student preferences and school priorities, ensuring no student-school pair would prefer each other over their current assignment.

## Algorithm Description

1. Students submit ranked preferences for schools.
2. Schools rank students based on their priorities (e.g., entrance exams, sibling attendance).
3. Students propose to their most-preferred school.
4. Schools tentatively accept the highest-ranked students up to their capacity and reject others.
5. Rejected students propose to their next most-preferred school in subsequent rounds.
6. The process continues until no more students are proposing, and tentative assignments become final.

## Characteristics

- Strategy-proof: Students have no incentive to misrepresent their true preferences.
- Produces stable matchings: No student-school pair would prefer each other over their assigned matches.
- Eliminates "justified envy" - no student can claim they should have a spot at a school over someone with lower priority.
- Student-optimal: When students propose, it produces the best stable matching for students.
## Parameters
- `students` : dict
  - A dictionary where keys are student names and values are lists of school names in order of preference
- `schools` : dict
  - A dictionary where keys are school names and values are dictionaries containing:
    - `'preferences'` : list
      - List of student names in order of preference
    - `'capacity'` : int
      - Integer representing the school's capacity

- `student_proposing` : bool, optional
  - If True, students propose to schools. If False, schools propose to students.
  - Default is True.

## Returns

- dict
  - A dictionary representing the matching, where keys are school names and values are lists of assigned students

## Usage
```python
from matching_algorithms import school_choice_da

students = {
    'Alice': ['School1', 'School2', 'School3'],
    'Bob': ['School2', 'School1', 'School3'],
    'Charlie': ['School1', 'School3', 'School2'],
    'David': ['School3', 'School1', 'School2']
}

schools = {
    'School1': {
        'priorities': ['Alice', 'Bob', 'Charlie', 'David'],
        'capacity': 1,
    },
    'School2': {
        'priorities': ['Bob', 'Alice', 'David', 'Charlie'],
        'capacity': 2,
    },
    'School3': {
        'priorities': ['Charlie', 'David', 'Alice', 'Bob'],
        'capacity': 1,
    }
}

matching = school_choice_da(schools,students,student_proposing=True)
print("School Choice Deferred Acceptance Matching:")
for school, assigned_students in matching.items():
    print(f"{school}: {', '.join(assigned_students)}")
```
# Boston Mechanism

## Overview

The Boston Mechanism is a direct, priority-based algorithm for matching students to schools. It is widely used in school admission processes where students have preferences over schools, and schools have priorities over students.

## Algorithm

The mechanism works as follows:

1. **First Round:** Students submit their ranked preferences for schools. Schools first allocate spots to students who ranked them as their first choice, based on the schools' priorities and capacities.

2. **Subsequent Rounds:** Any students who didn't get placed in their first-choice schools (due to capacity limits) participate in the next round. In this round, the schools consider students who listed them as their second choice. This process continues until all students are matched to a school, or there are no more options left.

3. **Final Assignment:** The algorithm ends when all remaining students are assigned based on their next available preference, or no further assignments are possible.

## Characteristics

- Not strategy-proof: Students may have incentives to misrepresent their true preferences.
- Favors students who rank popular schools highly.
- Simple to understand and implement.
- May lead to unstable matchings.

## Parameters

- `students` : dict
  - A dictionary where keys are student names and values are lists of school preferences.
  - Example: `{'Alice': ['School1', 'School2'], 'Bob': ['School2', 'School1']}`

- `schools` : dict
  - A dictionary where keys are school names and values are dictionaries containing:
    - `priorities` : list
      - List of student names in order of priority
    - `capacity` : int
      - Integer representing the school's capacity
  - Example: `{'School1': {'priorities': ['Bob', 'Alice'], 'capacity': 2}, 'School2': {'priorities': ['Alice', 'Bob'], 'capacity': 1}}`

- `student_proposing` : bool, optional
  - If True, students propose to schools. If False, schools propose to students.
  - Default is True.

## Returns

- `dict`
  - A dictionary representing the matching, where keys are school names and values are lists of assigned students.
  - Example: `{'School1': ['Alice'], 'School2': ['Bob']}`

## Usage

```python

from matching_algorithms import boston_mechanism
students = {
    'Alice': ['School1', 'School2', 'School3'],
    'Bob': ['School2', 'School1', 'School3'],
    'Charlie': ['School1', 'School3', 'School2'],
    'David': ['School3', 'School2', 'School1']
}

schools = {
    'School1': {
        'priorities': ['Alice', 'Bob', 'Charlie', 'David'],
        'capacity': 1,
    },
    'School2': {
        'priorities': ['Bob', 'Alice', 'David', 'Charlie'],
        'capacity': 2,
    },
    'School3': {
        'priorities': ['Charlie', 'David', 'Alice', 'Bob'],
        'capacity': 1,
    }
}

matching = boston_mechanism(students, schools)
print("Boston Mechanism Matching:")
for student, school in matching.items():
    print(f"{student} -> {school}")
```
# Top Trading Cycles for School Choice

## Overview

The Top Trading Cycles (TTC) algorithm is an efficient and strategy-proof mechanism for school choice. It aims to produce a Pareto efficient matching where no student can be made better off without making another student worse off. The algorithm is particularly useful in scenarios where students have initial priority at certain schools (e.g., based on their current school or neighborhood).

## Algorithm Description

### Initialization
- Set of unassigned students S
- Set of schools C with capacities {qc}
- Student preferences ≻s for each student s
- School priorities ≻c for each school c

### Main Loop
While there are unassigned students and schools with available seats:

1. Each school c with qc > 0 points to its highest-priority unassigned student.
2. Each unassigned student s points to their most preferred school with available seats.
3. Identify cycles in the resulting graph.
4. For each identified cycle:
   - Assign each student to their pointed school
   - Remove assigned students from S
   - Decrease school capacities
   - Remove schools with no capacity
5. If no cycles are found, break the loop

### Output
Return the final assignment

## Characteristics

- Strategy-proof: Agents have no incentive to misrepresent their preferences.
- Pareto efficient: Always produces a Pareto-optimal matching.
- Individually rational: When agents have initial endowments, no agent is made worse off than their initial allocation.
- Core selecting: The resulting allocation is always in the core of the housing market.
- Respects improvement: If an agent's priority improves at a school, they are guaranteed to be no worse off.
- May not always produce a stable matching in the two-sided sense.

## Parameters

- `students` : dict
  - A dictionary where keys are student names and values are lists of school preferences.
  - Example: `{'Alice': ['School1', 'School2'], 'Bob': ['School2', 'School1']}`

- `schools` : dict
  - A dictionary where keys are school names and values are dictionaries containing:
    - `priorities` : list
      - A list of student names in order of preference.
    - `capacity` : int
      - An integer representing the school's capacity.
  - Example: 
    ```python
    {
      'School1': {
        'priorities': ['Bob', 'Alice'],
        'capacity': 1
      },
      'School2': {
        'priorities': ['Alice', 'Bob'],
        'capacity': 1
      }
    }
    ```

## Returns

- dict
  - A dictionary representing the matching, where keys are student names and values are assigned schools.
  - Example: `{'Alice': 'School1', 'Bob': 'School2'}`

## Usage

```python

from matching_algorithms import top_trading_cycles
students = {
    'Alice': ['School1', 'School2', 'School3'],
    'Bob': ['School2', 'School1', 'School3'],
    'Charlie': ['School1', 'School3', 'School2']
}
schools = {
    'School1': {
        'priorities': ['Alice', 'Bob', 'Charlie', 'David'],
        'capacity': 1,
    },
    'School2': {
        'priorities': ['Bob', 'Alice', 'David', 'Charlie'],
        'capacity': 2,
    },
    'School3': {
        'priorities': ['Charlie', 'David', 'Alice', 'Bob'],
        'capacity': 1,
    }
}

assignment = top_trading_cycles(students, schools)
print("TTC Assignment:")
for student, school in assignment.items():
    print(f"{student} -> {school}")
```

# Serial Dictatorship

## Overview

The Serial Dictatorship mechanism is a priority-based allocation method where participants select their preferred options sequentially based on a predetermined priority order. This mechanism is commonly applied in contexts such as school choice and housing allocation.

## How it Works

1. **Priority Order:** Each participant is assigned a rank or priority based on a predetermined criterion (e.g., random lottery, academic performance, etc.).

2. **Choice Process:** Starting with the highest priority participant, each individual selects their most preferred available option.

3. **Subsequent Choices:** The next participant in the priority order selects from the remaining available choices.

4. **Final Allocation:** The process continues until all participants have made their selections or all options have been allocated.

## Characteristics

- Strategy-proof: Agents have no incentive to misrepresent their preferences.
- Pareto efficient: Always produces a Pareto-optimal matching.
- Deterministic: Given a fixed priority order, the outcome is always the same for the same preferences[1].
- May lead to unfair outcomes if the priority order is not carefully chosen or justified.

## Parameters

- `students` : dict
  - A dictionary where keys are student names and values are lists of school preferences.
- `schools` : dict
  - A dictionary where keys are school names and values are their capacities.
- `student_order` : list
  - List of student names in the order they should choose schools.

## Returns

- dict
  - A dictionary representing the matching, where keys are student names and values are assigned schools.

## Usage
```python
from matching_algorithms import serial_dictatorship

# Define student preferences
students = {
    'Alice': ['School1', 'School2', 'School3'],
    'Bob': ['School2', 'School1', 'School3'],
    'Charlie': ['School1', 'School3', 'School2']
}

# Define school capacities
schools = {
    'School1': 1,
    'School2': 1,
    'School3': 1
}

# Define student order (priority)
student_order = ['Alice', 'Bob', 'Charlie']

# Run the algorithm
matching = serial_dictatorship(students, schools, student_order)

# Print the results
print("\nFinal Matching:")
for student, school in matching.items():
    print(f"{student} -> {school if school else 'Unassigned'}")
```

# Random Serial Dictatorship 

## Overview

The Random Serial Dictatorship (RSD) mechanism is a variation of the Serial Dictatorship mechanism that introduces an element of randomness in determining the order in which participants make their selections. This method is particularly useful in situations where there is no pre-existing priority order among participants.

## How it Works

1. **Random Ordering:** A random order of participants is generated, typically using a fair randomization process.

2. **Sequential Selection:** Following this random order, each participant selects their most preferred available option from the remaining choices.

3. **Allocation:** The process continues until all participants have made their selections or all options have been allocated.

## Characteristics 

- Strategy-proof: Agents have no incentive to misrepresent their preferences
- Ex-post Pareto efficient: The final allocation is always Pareto optimal.
- Fair ex-ante: All agents have an equal chance of being in any position in the selection order.
- Widely used in practice: Common in house allocation problems, such as allocating dormitory rooms to students.

## Parameters

- `students` : dict
  - A dictionary where keys are student names and values are lists of school preferences.
- `schools` : dict
  - A dictionary where keys are school names and values are their capacities.

## Returns

- dict
  - A dictionary representing the matching, where keys are student names and values are assigned schools.

## Usage
```python
from matching_algorithms import random_serial_dictatorship
# Define student preferences
students = {
    'Alice': ['School1', 'School2', 'School3'],
    'Bob': ['School2', 'School1', 'School3'],
    'Charlie': ['School1', 'School3', 'School2'],
    'David': ['School3', 'School2', 'School1']
}

# Define school capacities
schools = {
    'School1': 2,
    'School2': 1,
    'School3': 1
}

# Run the algorithm
matching = random_serial_dictatorship(students, schools)

# Print the results
print("\nFinal Matching:")
for student, school in matching.items():
    print(f"{student} -> {school if school else 'Unassigned'}")
```

## Linear Programming Algorithms with Stability Constraint

# Stable Matching via Linear Programming

## Overview

This approach uses linear programming to find a stable matching in the classic stable marriage problem. It formulates the stability constraints and matching requirements as a set of linear inequalities, allowing us to find a stable matching efficiently using standard linear programming solvers.

## Mathematical Formulation

Let x_ij be a continuous variable indicating the extent to which man i is matched with woman j. The linear program can be formulated as follows:

$$
\text{maximize} \quad \sum_{i=1}^n \sum_{j=1}^n x_{ij}
$$


subject to:

$$
\sum_{j=1}^n x_{ij} = 1 \quad \forall i \in \{1, \ldots, n\}
$$


$$
\sum_{i=1}^n x_{ij} = 1 \quad \forall j \in \{1, \ldots, n\}
$$


$$
x_{ij} + \sum_{k: m_k \succ_j m_i} x_{kj} + \sum_{k: w_k \succ_i w_j} x_{ik} \geq 1 \quad \forall i,j \in \{1, \ldots, n\}
$$


$$
0 \leq x_{ij} \leq 1 \quad \forall i,j \in \{1, \ldots, n\}
$$


Where:
- n is the number of men (equal to the number of women)
- x_ij represents the extent to which man i is matched with woman j (0 ≤ x_ij ≤ 1)
- The first two constraints ensure that each person is fully matched (potentially fractionally to multiple partners)
- The third constraint ensures stability: for each potential pair (i,j), either they are matched to some extent, or at least one of them is matched to a preferable partner to some extent
- ≻_j denotes woman j's preference order over men
- ≻_i denotes man i's preference order over women

Note: This formulation allows for fractional matchings. However, it can be shown that for the stable marriage problem, there always exists an optimal solution where all x_ij are either 0 or 1. This is due to the structure of the constraint matrix, which is totally unimodular. Therefore, solving this linear program will yield an integer solution, corresponding to a stable matching.

## Implementation

The algorithm is implemented in Python using the PuLP library for linear programming. It sets up the linear program based on the preference lists of men and women, solves it, and extracts the stable matching from the solution.

## Parameters

- `men_prefs` (dict): A dictionary where keys are men and values are lists of women in order of preference.
- `women_prefs` (dict): A dictionary where keys are women and values are lists of men in order of preference.

## Returns

- `dict`: A dictionary representing the stable matching, where keys are men and values are their matched women.

## Runtime Table:

| Number of Agents per Side | Average Runtime (seconds) |
|---------------------------|---------------------------|
| 10                        | 0.037072                  |
| 40                        | 0.493957                  |
| 70                        | 2.998246                  |
| 100                       | 10.351443                 |

![Runtime of Stable Matching LP Algorithm](images/stable_matching_lp.png)

## Usage

```python
from matching_algorithms import stable_matching_lp
men_prefs = {
    'M1': ['W1', 'W2', 'W3'],
    'M2': ['W2', 'W1', 'W3'],
    'M3': ['W3', 'W1', 'W2']
}

women_prefs = {
    'W1': ['M2', 'M1', 'M3'],
    'W2': ['M1', 'M2', 'M3'],
    'W3': ['M3', 'M2', 'M1']
}

matching = stable_matching_lp(men_prefs, women_prefs)
print("Stable Matching:")
for man, woman in matching.items():
    print(f"{man} - {woman}")
```


# Egalitarian Stable Matching

## Overview

The **Egalitarian Stable Matching** algorithm finds a stable matching that minimizes the total dissatisfaction (or rank) across all participants. It seeks to produce the most "fair" matching by minimizing the sum of preference ranks for all matched pairs. This algorithm is implemented using linear programming.

## Mathematical Formulation

The objective function for the Egalitarian Stable Matching problem can be formulated as follows:

$$
\text{minimize} \quad \sum_{(\ell,r) \in L \times R} \big( h(\ell,r) + h(r,\ell) \big) \cdot \mu_{\ell,r}
$$


subject to:

$$
\sum_{r \in R} \mu_{\ell,r} = 1 \quad \forall \, \ell \in L
$$


$$
\sum_{\ell \in L} \mu_{\ell,r} = 1 \quad \forall \, r \in R
$$


$$
\mu_{\ell,r} + \sum_{s \in R: \, s \, \succ_\ell \, r} \mu_{\ell,s} + \sum_{k \in L: \, k \, \succ_r \, \ell} \mu_{k,r} \geq 1 \quad \forall \, (\ell,r) \in L \times R
$$


$$
\mu_{\ell,r} \geq 0 \quad \forall \, (\ell,r) \in L \times R
$$


Where:
- $$L$$ and $$R$$ are the two sets of participants to be matched.
- $$h(\ell,r)$$ is the rank of $$r$$ in $$\ell$$'s preference list.
- $$\mu_{\ell,r}$$ is the extent to which $$\ell$$ and $$r$$ are matched.
- $$s \succ_\ell r$$ means that participant $$\ell$$ prefers participant $$s$$ to participant $$r$$.

This formulation minimizes the sum of ranks while ensuring that each participant is matched exactly once and that the matching is stable. The algorithm produces a matching that is Pareto efficient with respect to the participants' preferences.

## Implementation

The algorithm has been implemented in Python using the PuLP library for linear programming. You can use this implementation to find egalitarian stable matchings based on given preferences.

## Parameters

- `men_prefs` : dict
  - A dictionary where keys are men and values are lists of women in order of preference.

- `women_prefs` : dict
  - A dictionary where keys are women and values are lists of men in order of preference.

## Returns

- dict
  - A dictionary representing the Egalitarian stable matching, where keys are men and values are their matched women.

## Runtime Table :

| Number of Agents per Side | Average Runtime (seconds) |
|---------------------------|---------------------------|
| 10                        | 0.037443                  |
| 40                        | 0.469973                  |
| 70                        | 2.617627                  |
| 100                       | 8.258007                  |

![Runtime of Egalitarian Stable Matching Algorithm](images/egalitarian_stable_matching.png)


## Usage

```python
from matching_algorithms import egalitarian_stable_matching
men_prefs = {
    'M1': ['W1', 'W2', 'W3'],
    'M2': ['W2', 'W1', 'W3'],
    'M3': ['W3', 'W1', 'W2']
}

women_prefs = {
    'W1': ['M2', 'M1', 'M3'],
    'W2': ['M1', 'M2', 'M3'],
    'W3': ['M3', 'M2', 'M1']
}

matching = egalitarian_stable_matching(men_prefs, women_prefs)
print("Egalitarian Stable Matching:")
for man, woman in matching.items():
    print(f"{man} - {woman}")
```


# Nash Stable Matching

## Overview

The **Nash Stable Matching** algorithm finds a stable matching that maximizes the product of utilities (Nash social welfare) across all participants, while maintaining stability. This approach aims to produce a "fair" and efficient matching by balancing individual utilities in a multiplicative way. The algorithm is implemented using linear programming with a logarithmic transformation.

## Mathematical Formulation

The objective function for the Nash Stable Matching problem can be formulated as follows:

$$
\text{maximize} \quad \prod_{(\ell,r) \in L \times R} (v(\ell,r) \times v(r,\ell))^{\mu_{\ell,r}}
$$


which is equivalent to maximizing:

$$
\text{maximize} \quad \sum_{(\ell,r) \in L \times R} \mu_{\ell,r} (\log v(\ell,r)+\log v(r,\ell))
$$


subject to:

$$
\sum_{r \in R} \mu_{\ell,r} = 1 \quad \forall \, \ell \in L
$$


$$
\sum_{\ell \in L} \mu_{\ell,r} = 1 \quad \forall \, r \in R
$$


$$
\mu_{\ell,r} + \sum_{s \in R: \, v(\ell,s) > v(\ell,r)} \mu_{\ell,s} + \sum_{k \in L: \, v(k,r) > v(\ell,r)} \mu_{k,r} \geq 1 \quad \forall \, (\ell,r) \in L \times R
$$


$$
\mu_{\ell,r} \geq 0 \quad \forall \, (\ell,r) \in L \times R
$$


Where:
- $$L$$ and $$R$$ are the two sets of participants to be matched.
- $$v(\ell,r)$$ is the valuation that participant $$\ell$$ assigns to being matched with participant $$r$$.
- $$v(r,\ell)$$ is the valuation that participant $$r$$ assigns to being matched with participant $$\ell$$.
- $$\mu_{\ell,r}$$ is the extent to which $$\ell$$ and $$r$$ are matched.

This formulation maximizes the product of valuations (Nash social welfare) while ensuring that each participant is matched exactly once and that the matching is stable. The logarithmic transformation allows us to solve this as a linear programming problem.

## Implementation

The algorithm is implemented in Python using the PuLP library for linear programming. The logarithmic transformation is used to convert the product maximization into a sum maximization, which can be solved using standard linear programming techniques.

## Parameters

- `men_valuations` (dict): A dictionary where keys are men and values are dictionaries of their valuations for each woman.
- `women_valuations` (dict): A dictionary where keys are women and values are dictionaries of their valuations for each man.

## Returns

- `dict`: A dictionary representing the Nash stable matching, where keys are men and values are their matched women.

## Runtime Table:


| Number of Agents per Side | Average Runtime (seconds) |
|---------------------------|---------------------------|
| 10                        | 0.034171                  |
| 40                        | 0.416633                  |
| 70                        | 1.799205                  |
| 100                       | 5.155402                  |

![Runtime of Nash Stable Matching Algorithm](images/nash_stable_matching.png)

## Usage
```python
from matching_algorithms import nash_stable_matching

men_valuations = {
    'M1': {'W1': 10, 'W2': 5, 'W3': 3},
    'M2': {'W1': 4, 'W2': 8, 'W3': 6},
    'M3': {'W1': 7, 'W2': 6, 'W3': 9}
}

women_valuations = {
    'W1': {'M1': 8, 'M2': 6, 'M3': 4},
    'W2': {'M1': 5, 'M2': 9, 'M3': 7},
    'W3': {'M1': 3, 'M2': 5, 'M3': 10}
}

matching = nash_stable_matching(men_valuations, women_valuations)
print("Nash Stable Matching:")
for man, woman in matching.items():
    print(f"{man} - {woman}")
```

# Utilitarian Stable Matching

## Overview

The **Utilitarian Stable Matching** algorithm finds a stable matching that maximizes the total utility (or valuation) across all participants. It aims to produce the most "efficient" matching by maximizing the sum of valuations for all matched pairs, while still maintaining stability. This algorithm is implemented using linear programming.

## Mathematical Formulation

The objective function for the Utilitarian Stable Matching problem can be formulated as follows:

$$
\text{maximize} \quad \sum_{(\ell,r) \in L \times R} (v(\ell,r)+v(r,\ell)) \cdot \mu_{\ell,r}
$$


subject to:

$$
\sum_{r \in R} \mu_{\ell,r} = 1 \quad \forall \, \ell \in L
$$


$$
\sum_{\ell \in L} \mu_{\ell,r} = 1 \quad \forall \, r \in R
$$


$$
\mu_{\ell,r} + \sum_{s \in R: \, v(\ell,s) > v(\ell,r)} \mu_{\ell,s} + \sum_{k \in L: \, v(k,r) > v(\ell,r)} \mu_{k,r} \geq 1 \quad \forall \, (\ell,r) \in L \times R
$$


$$
\mu_{\ell,r} \geq 0 \quad \forall \, (\ell,r) \in L \times R
$$


Where:
- $$L$$ and $$R$$ are the two sets of participants to be matched.
- $$v(\ell,r)$$ is the valuation that participant $$\ell$$ assigns to being matched with participant $$r$$.
- $$v(r,\ell)$$ is the valuation that participant $$r$$ assigns to being matched with participant $$\ell$$.
- $$\mu_{\ell,r}$$ is the extent to which $$\ell$$ and $$r$$ are matched.

This formulation maximizes the sum of valuations while ensuring that each participant is matched exactly once and that the matching is stable. The algorithm produces a matching that is both stable and Pareto efficient.

## Implementation

The algorithm has been implemented in Python using the PuLP library for linear programming. You can use this implementation to find utilitarian stable matchings based on given valuations.

## Parameters

- `men_valuations` : dict
  - A dictionary where keys are men and values are dictionaries of their valuations for each woman.
  - Example: `{'M1': {'W1': 10, 'W2': 5}, 'M2': {'W1': 7, 'W2': 8}}`

- `women_valuations` : dict
  - A dictionary where keys are women and values are dictionaries of their valuations for each man.
  - Example: `{'W1': {'M1': 8, 'M2': 6}, 'W2': {'M1': 5, 'M2': 9}}`

## Returns

- dict
  - A dictionary representing the utilitarian stable matching, where keys are men and values are their matched women.
  - Example: `{'M1': 'W1', 'M2': 'W2'}`

## Runtime Table:

| Number of Agents per Side | Average Runtime (seconds) |
|---------------------------|---------------------------|
| 10                        | 0.034295                  |
| 40                        | 0.371985                  |
| 70                        | 1.791714                  |
| 100                       | 5.238294                  |

![Runtime of Utilitarian Stable Matching Algorithm](images/utilitarian_stable_matching.png)

## Usage
```python
from matching_algorithms import utilitarian_stable_matching

men_valuations = {
    'M1': {'W1': 10, 'W2': 5, 'W3': 3},
    'M2': {'W1': 4, 'W2': 8, 'W3': 6},
    'M3': {'W1': 7, 'W2': 6, 'W3': 9}
}

women_valuations = {
    'W1': {'M1': 8, 'M2': 6, 'M3': 4},
    'W2': {'M1': 5, 'M2': 9, 'M3': 7},
    'W3': {'M1': 3, 'M2': 5, 'M3': 10}
}

matching = utilitarian_stable_matching(men_valuations, women_valuations)
print("Utilitarian Stable Matching:")
for man, woman in matching.items():
    print(f"{man} - {woman}")
```

## Linear Programming Algorithms without Stability Constraint

# Egalitarian Matching 

## Overview

The **Egalitarian Matching** algorithm without stability constraints finds a matching that minimizes the total sum of preference ranks across all participants. This approach aims to produce a "fair" matching by balancing the satisfaction of all participants, without the requirement of stability. The algorithm is implemented using linear programming.

## Mathematical Formulation

The objective function for the Egalitarian Matching problem can be formulated as follows:

$$
\text{minimize} \quad \sum_{(\ell,r) \in L \times R} (h(\ell,r) + h(r,\ell)) \cdot \mu_{\ell,r}
$$


subject to:

$$
\sum_{r \in R} \mu_{\ell,r} = 1 \quad \forall \, \ell \in L
$$


$$
\sum_{\ell \in L} \mu_{\ell,r} = 1 \quad \forall \, r \in R
$$


$$
\mu_{\ell,r} \geq 0 \quad \forall \, (\ell,r) \in L \times R
$$


Where:
- $$L$$ and $$R$$ are the two sets of participants to be matched.
- $$h(\ell,r)$$ is the rank of $$r$$ in $$\ell$$'s preference list.
- $$\mu_{\ell,r}$$ is the extent to which $$\ell$$ and $$r$$ are matched.

This formulation minimizes the sum of ranks for all matched pairs, ensuring that each participant is matched exactly once. Unlike the stable matching variants, this formulation does not include stability constraints.

## Implementation

The algorithm is implemented in Python using the PuLP library for linear programming. It directly minimizes the sum of ranks without considering stability constraints.

## Parameters

- `men_prefs` : dict
  - A dictionary where keys are men and values are lists of women in order of preference.
- `women_prefs` : dict
  - A dictionary where keys are women and values are lists of men in order of preference.

## Returns

- dict
  - A dictionary representing the egalitarian matching, where keys are men and values are their matched women.

## Usage

```python
from matching_algorithms import egalitarian_matching

men_prefs = {
    'M1': ['W1', 'W2', 'W3'],
    'M2': ['W2', 'W1', 'W3'],
    'M3': ['W3', 'W1', 'W2']
}

women_prefs = {
    'W1': ['M2', 'M1', 'M3'],
    'W2': ['M1', 'M2', 'M3'],
    'W3': ['M3', 'M2', 'M1']
}

matching = egalitarian_matching(men_prefs, women_prefs)
print("Egalitarian Matching:")
for man, woman in matching.items():
    print(f"{man} - {woman}")
```
# Nash Matching 

## Overview

The **Nash Matching** algorithm without stability constraints finds a matching that maximizes the product of utilities (or satisfaction) of all participants. This approach aims to balance equity and efficiency in matching outcomes without enforcing stability. The algorithm is implemented using linear programming with a logarithmic transformation.

## Mathematical Formulation

The objective function for the Nash Matching problem can be formulated as follows:

$$
\text{maximize} \quad \prod_{(\ell,r) \in L \times R} (v_{\ell}(\ell,r) \times v_{r}(r,\ell))^{\mu_{\ell,r}}
$$


which is equivalent to maximizing:

$$
\text{maximize} \quad \sum_{(\ell,r) \in L \times R} \mu_{\ell,r} (\log(v(\ell,r)) + \log(v(r,\ell)))
$$


subject to:

$$
\sum_{r \in R} \mu_{\ell,r} = 1 \quad \forall \, \ell \in L
$$


$$
\sum_{\ell \in L} \mu_{\ell,r} = 1 \quad \forall \, r \in R
$$


$$
\mu_{\ell,r} \geq 0 \quad \forall \, (\ell,r) \in L \times R
$$


Where:
- $$L$$ and $$R$$ are the two sets of participants to be matched.
- $$v(\ell,r)$$ is the valuation that participant $$\ell$$ assigns to being matched with participant $$r$$.
- $$v(r,\ell)$$ is the valuation that participant $$r$$ assigns to being matched with participant $$\ell$$.
- $$\mu_{\ell,r}$$ is the extent to which $$\ell$$ and $$r$$ are matched.

## Implementation

The algorithm is implemented in Python using the PuLP library for linear programming. The logarithmic transformation allows us to solve this as a linear programming problem. The key features of the implementation include:

- Logarithmic utility constraints to handle the product maximization.
- No stability constraints, focusing solely on maximizing the Nash social welfare.

## Parameters

- `men_valuations` : dict
  - A dictionary where keys are men and values are dictionaries of their valuations for each woman.
- `women_valuations` : dict
  - A dictionary where keys are women and values are dictionaries of their valuations for each man.

## Returns

- dict
  - A dictionary representing the Nash matching, where keys are men and values are their matched women.

## Usage

```python
from matching_algorithms import nash_matching

men_valuations = {
    'M1': {'W1': 10, 'W2': 5, 'W3': 3},
    'M2': {'W1': 4, 'W2': 8, 'W3': 6},
    'M3': {'W1': 7, 'W2': 6, 'W3': 9}
}

women_valuations = {
    'W1': {'M1': 8, 'M2': 6, 'M3': 4},
    'W2': {'M1': 5, 'M2': 9, 'M3': 7},
    'W3': {'M1': 3, 'M2': 5, 'M3': 10}
}

matching = nash_matching(men_valuations, women_valuations)
print("Nash Matching:")
for man, woman in matching.items():
    print(f"{man} - {woman}")
```
# Utilitarian Matching

## Overview

The **Utilitarian Matching** algorithm without stability constraints finds a matching that maximizes the total sum of utilities (or valuations) across all participants. This approach aims to produce an "efficient" matching by maximizing overall welfare, without the requirement of stability. The algorithm is implemented using linear programming.

## Mathematical Formulation

The objective function for the Utilitarian Matching problem can be formulated as follows:

$$
\text{maximize} \quad \sum_{(\ell,r) \in L \times R} (v(\ell,r)+v(\ell,r))\cdot \mu_{\ell,r}
$$


subject to:

$$
\sum_{r \in R} \mu_{\ell,r} = 1 \quad \forall \, \ell \in L
$$


$$
\sum_{\ell \in L} \mu_{\ell,r} = 1 \quad \forall \, r \in R
$$


$$
\mu_{\ell,r} \geq 0 \quad \forall \, (\ell,r) \in L \times R
$$


Where:
- $$L$$ and $$R$$ are the two sets of participants to be matched.
- $$v(\ell,r)$$ is the valuation that participant $$\ell$$ assigns to being matched with participant $$r$$.
- $$v(r,\ell)$$ is the valuation that participant $$r$$ assigns to being matched with participant $$\ell$$.
- $$\mu_{\ell,r}$$ is the extent to which $$\ell$$ and $$r$$ are matched.

This formulation maximizes the sum of utilities for all matched pairs, ensuring that each participant is matched exactly once. Unlike the stable matching variants, this formulation does not include stability constraints.

## Implementation

The algorithm is implemented in Python using the PuLP library for linear programming. It directly maximizes the sum of utilities without considering stability constraints.

## Parameters

- `men_valuations` (dict): A dictionary where keys are men and values are dictionaries of their valuations for each woman.
- `women_valuations` (dict): A dictionary where keys are women and values are dictionaries of their valuations for each man.

## Returns

- `dict`: A dictionary representing the utilitarian matching, where keys are men and values are their matched women.

## Usage

```python
from matching_algorithms import utilitarian_matching
men_valuations = {
    'M1': {'W1': 10, 'W2': 5, 'W3': 3},
    'M2': {'W1': 4, 'W2': 8, 'W3': 6},
    'M3': {'W1': 7, 'W2': 6, 'W3': 9}
}

women_valuations = {
    'W1': {'M1': 8, 'M2': 6, 'M3': 4},
    'W2': {'M1': 5, 'M2': 9, 'M3': 7},
    'W3': {'M1': 3, 'M2': 5, 'M3': 10}
}

matching = utilitarian_matching(men_valuations, women_valuations)
print("Utilitarian Matching:")
for man, woman in matching.items():
    print(f"{man} - {woman}")everyone's satisfaction is maximized without stability constraint.
```

## Helper Functions
# Generate Instance

This helper function generates instances of matching markets. The function `generate_instance` can create preferences or valuations for both marriage markets and school choice problems, with options for cardinal or ordinal preferences.

## Parameters

- `num_agents` (int): Number of agents on each side of the market (or number of students for school choice).
- `num_schools` (int, optional): Number of schools for school choice. Default is `num_agents // 2`. Cannot be less than 2 or greater than `num_agents`.
- `is_marriage_market` (bool): If True, generates for marriage market. If False, generates for school choice.
- `is_cardinal` (bool): If True, generates cardinal valuations. If False, generates ordinal preferences.

## Returns

- For marriage market: A tuple of two dictionaries (men_preferences, women_preferences).
- For school choice: A tuple of two dictionaries (student_preferences, school_data).
  - `school_data` contains both priorities and capacities for each school.

## Usage

1. Generate preferences for a marriage market with ordinal preferences:
    ```python
    from matching_algorithms import generate_instance

    men_prefs, women_prefs = generate_instance(10, is_marriage_market=True, is_cardinal=False)
    ```

2. Generate cardinal valuations for a marriage market:
    ```python
    from matching_algorithms import generate_instance

    men_vals, women_vals = generate_instance(10, is_marriage_market=True, is_cardinal=True)
    ```

3. Generate preferences and data for a school choice problem:
    ```python
    from matching_algorithms import generate_instance

    student_prefs, school_data = generate_instance(100, is_marriage_market=False, is_cardinal=False)

    # Accessing school priorities and capacities
    for school, data in school_data.items():
        print(f"School {school}:")
        print(f"  Priorities: {data['priorities']}")
        print(f"  Capacity: {data['capacity']}")
    ```

4. Generate cardinal valuations for a school choice problem:
    ```python
    from matching_algorithms import generate_instance

    student_vals, school_data = generate_instance(100, is_marriage_market=False, is_cardinal=True)

    # Accessing school valuations and capacities
    for school, data in school_data.items():
        print(f"School {school}:")
        print(f"  Valuations: {data['priorities']}")  # In this case, 'priorities' contains valuations
        print(f"  Capacity: {data['capacity']}")
    ```

5. Generate preferences and data for a school choice problem with a specific number of schools:
    ```python
    from matching_algorithms import generate_instance

    student_prefs, school_data = generate_instance(100, num_schools=5, is_marriage_market=False, is_cardinal=False)

    print(f"Number of schools: {len(school_data)}")
    ```

**Note:** For school choice problems, the total capacity of all schools is set to half the number of students, distributed as evenly as possible among the schools.

# Is Stable

The `is_stable` function checks whether a given matching is stable under the provided preferences or valuations. It supports both ordinal preferences and cardinal valuations for both sides of the market.

## Parameters

- `matching` (dict): A dictionary representing the matching, where keys are side1 agents and values are their matched side2 agents.
- `side1_preferences` (dict): A dictionary where keys are side1 agents and values are either lists (ordinal) or dicts (cardinal) of side2 agents.
- `side2_preferences` (dict): A dictionary where keys are side2 agents and values are either lists (ordinal) or dicts (cardinal) of side1 agents.
- `is_cardinal` (bool): If True, preferences are treated as cardinal valuations. If False, preferences are treated as ordinal.

## Returns

- `bool`: True if the matching is stable, False otherwise.

## Usage

1. Check stability with ordinal preferences:

    ```python
    from matching_algorithms import is_stable, generate_instance

    # Generate an instance
    men_prefs, women_prefs = generate_instance(10, is_marriage_market=True, is_cardinal=False)

    # Assume we have a matching
    matching = {'M1': 'W1', 'M2': 'W2', ...}  # Complete this with your matching

    # Check stability
    is_stable_result = is_stable(matching, men_prefs, women_prefs, is_cardinal=False)
    print(f"Is the matching stable? {is_stable_result}")
    ```

2. Check stability with cardinal valuations:

    ```python
    from matching_algorithms import is_stable, generate_instance

    # Generate an instance with cardinal valuations
    men_vals, women_vals = generate_instance(10, is_marriage_market=True, is_cardinal=True)

    # Assume we have a matching
    matching = {'M1': 'W1', 'M2': 'W2', ...}  # Complete this with your matching

    # Check stability
    is_stable_result = is_stable(matching, men_vals, women_vals, is_cardinal=True)
    print(f"Is the matching stable? {is_stable_result}")
    ```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements. 

If you have any questions or would like to discuss potential contributions, you can reach me at [here](mailto:irfan.tekdir@gmail.com).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
