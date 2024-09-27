# Matching Algorithms

This project implements a variety of matching algorithms, including the Deferred Acceptance algorithm, the Boston Mechanism, the Top Trading Cycles (TTC) mechanism, and several linear programming approaches. These algorithms are widely applicable in various domains such as school admissions, organ allocation, job assignments, and resource allocation problems. Their effectiveness in creating stable and efficient matchings makes them valuable tools in economics, operations research, and decision-making processes.


## Table of Contents

- [Installation](#installation)
- [Algorithms Implemented](#algorithms-implemented)
  - [Deferred Acceptance](#deferred-acceptance)
    - [Marriage Market Deferred Acceptance](#marriage-market-deferred-acceptance)
    - [School Choice Deferred Acceptance](#school-choice-deferred-acceptance)
  - [Boston Mechanism](#boston-mechanism)
  - [Top Trading Cycles (TTC)](#top-trading-cycles-ttc)
  - [Serial Dictatorship](#serial-dictatorship)
  - [Random Serial Dictatorship](#random-serial-dictatorship)
  - [Linear Programming Algorithms with Stability Constraint](#linear-programming-algorithms-with-stability-constraint)
    - [Stable Matching via Linear Programming](#stable-matching-via-linear-programming)
    - [Egalitarian Stable Matching](#egalitarian-stable-matching)
    - [Nash Stable Matching](#nash-welfare-stable-matching)
    - [Utilitarian Stable Matching](#utilitarian-stable-matching)
  - [Linear Programming Algorithms without Stability Constraint](#linear-programming-algorithms-without-stability-constraint)
    - [Egalitarian Matching](#egalitarian-matching)
    - [Nash Matching](#nash-welfare-matching)
    - [Utilitarian Matching](#utilitarian-matching)
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

## Deferred Acceptance

# Marriage Market Deferred Acceptance

## Overview

The Deferred Acceptance algorithm for the Marriage Market is a two-sided matching algorithm that pairs participants from two groups (e.g., men and women) based on their preferences. The algorithm ensures that no pair of participants would rather be matched with each other than with their current match, leading to a stable matching. In this setup, one group (typically men) proposes to the other group, and participants from the second group (women) accept or reject proposals based on their preferences.

## Algorithm Steps

The algorithm proceeds in rounds:

1. Each participant in the proposing group proposes to their most-preferred partner who has not yet rejected them.
2. Participants in the receiving group tentatively accept the most-preferred proposal they have received so far and reject the others.
3. Rejected participants propose to their next most-preferred partner in the next round.
4. The process continues until no more proposals are made, and the tentative matches become final.

## Implementation

The algorithm is implemented in Python, using dictionaries to represent preferences and matches.

## Usage

To use the Marriage Market Deferred Acceptance algorithm, follow these steps:

1. Import the function:

```python
from marriage_market import deferred_acceptance

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

matches = deferred_acceptance(men_preferences, women_preferences)

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

## Mathematical Formulation

Let $S$ be the set of students and $C$ be the set of schools. For each student $s \in S$, let $P_s$ be their preference list over schools. For each school $c \in C$, let $\succ_c$ be its priority ordering over students, and $q_c$ its capacity.

The algorithm proceeds in rounds:

1. In each round $t$:
   - Each unassigned student $s$ proposes to their most preferred school $c$ that hasn't rejected them yet.
   - Each school $c$ considers all proposals received, including students tentatively assigned from previous rounds.
   - School $c$ tentatively accepts the top $q_c$ students according to $\succ_c$ and rejects the rest.

2. The algorithm terminates when no student is rejected in a round.

## Implementation

Here's a Python implementation of the School Choice Deferred Acceptance algorithm:

```python
# Example usage
students = {
    'Alice': ['School1', 'School2', 'School3'],
    'Bob': ['School2', 'School1', 'School3'],
    'Charlie': ['School1', 'School3', 'School2']
}

schools = {
    'School1': {'capacity': 1, 'priorities': ['Alice', 'Bob', 'Charlie']},
    'School2': {'capacity': 1, 'priorities': ['Bob', 'Alice', 'Charlie']},
    'School3': {'capacity': 1, 'priorities': ['Charlie', 'Alice', 'Bob']}
}

matching = school_choice_da(students, schools)
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

## Implementation

```python
# Example usage:
students = {
    'Alice': ['School1', 'School2', 'School3'],
    'Bob': ['School2', 'School1', 'School3'],
    'Charlie': ['School1', 'School3', 'School2'],
    'David': ['School3', 'School2', 'School1']
}

schools = {
    'School1': {
        'capacity': 1,
        'priorities': ['Alice', 'Bob', 'Charlie', 'David']
    },
    'School2': {
        'capacity': 2,
        'priorities': ['Bob', 'Alice', 'David', 'Charlie']
    },
    'School3': {
        'capacity': 1,
        'priorities': ['Charlie', 'David', 'Alice', 'Bob']
    }
}

matching = boston_mechanism(students, schools)
print("Boston Mechanism Matching:")
for student, school in matching.items():
    print(f"{student} -> {school}")
```
# Top Trading Cycles (TTC) for School Choice

## Overview

The Top Trading Cycles (TTC) algorithm is an efficient and strategy-proof mechanism for school choice. It aims to produce a Pareto efficient matching where no student can be made better off without making another student worse off. The algorithm is particularly useful in scenarios where students have initial priority at certain schools (e.g., based on their current school or neighborhood).

## Algorithm Description

1. Each student points to their favorite school among those with remaining seats.
2. Each school points to the student with the highest priority among those pointing to it.
3. This forms at least one cycle. Every student in a cycle is assigned to the school they are pointing to.
4. Remove these students and reduce the capacity of the schools by the number of students assigned to them.
5. Repeat steps 1-4 until all students are assigned or no more cycles can be formed.

## Mathematical Formulation

While TTC is typically described as an algorithmic process rather than an optimization problem, we can represent its outcome using binary variables:

Let $x_{i,j}$ be 1 if student $i$ is assigned to school $j$, and 0 otherwise.

The TTC outcome satisfies:

$$
\sum_{j \in S} x_{i,j} = 1 \quad \forall i \in N
$$


$$
\sum_{i \in N} x_{i,j} \leq q_j \quad \forall j \in S
$$


Where $N$ is the set of students, $S$ is the set of schools, and $q_j$ is the capacity of school $j$.

The TTC algorithm ensures these constraints are met while achieving Pareto efficiency.

## Implementation

Here's a basic implementation of TTC for school choice:

```python
# Example usage:
students = {
    'Alice': ['School1', 'School2', 'School3'],
    'Bob': ['School2', 'School1', 'School3'],
    'Charlie': ['School1', 'School3', 'School2']
}
schools = ['School1', 'School2', 'School3']
capacities = {'School1': 1, 'School2': 1, 'School3': 1}
priorities = {
    'School1': ['Alice', 'Bob', 'Charlie'],
    'School2': ['Bob', 'Charlie', 'Alice'],
    'School3': ['Charlie', 'Alice', 'Bob']
}

assignment = top_trading_cycles(students, schools, capacities, priorities)
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

```python
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

# Random Serial Dictatorship (RSD)

## Overview

The Random Serial Dictatorship (RSD) mechanism is a variation of the Serial Dictatorship mechanism that introduces an element of randomness in determining the order in which participants make their selections. This method is particularly useful in situations where there is no pre-existing priority order among participants.

## How it Works

1. **Random Ordering:** A random order of participants is generated, typically using a fair randomization process.

2. **Sequential Selection:** Following this random order, each participant selects their most preferred available option from the remaining choices.

3. **Allocation:** The process continues until all participants have made their selections or all options have been allocated.

## Key Properties

- **Strategy-proof:** Participants have no incentive to misrepresent their preferences.
- **Ex-post Pareto efficient:** The resulting allocation is always Pareto efficient.
- **Fair ex-ante:** Due to the random ordering, all participants have an equal chance of being in any position in the selection order.

#### How It Works:

1. **Random Order Generation:** At the beginning of the allocation process, a random order is generated for all participants. This order dictates the sequence in which participants will choose their preferred options.

2. **Choice Process:** Similar to the Serial Dictatorship mechanism, each participant selects their most preferred available option in the order determined by the random draw. The participant with the highest priority (based on the random order) chooses first, followed by the next participant, and so on.

3. **Subsequent Choices:** As each participant makes their selection, options become unavailable to those who choose later. The process continues until all participants have selected their options or all available options have been allocated.

4. **Fairness:** The Random Serial Dictatorship mechanism aims to create a fairer allocation process by giving each participant an equal chance of being chosen first, thereby reducing the potential inequalities that might arise from a fixed priority order. 

5. **Strategy-Proofness:** Like its predecessor, RSD is strategy-proof, meaning participants have no incentive to misrepresent their preferences, as their best outcomes are achieved by honestly selecting their most preferred options available at their turn.

The RSD mechanism is particularly effective in educational contexts, such as school assignments, where fairness and transparency in the selection process are essential.

## Usage
```python
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

# Stable Matching via Linear Programming

## Overview

This approach uses linear programming to find a stable matching in the classic stable marriage problem. It formulates the stability constraints and matching requirements as a set of linear inequalities, allowing us to find a stable matching efficiently using standard linear programming solvers.

## Mathematical Formulation

Let $x_{ij}$ be a binary variable indicating whether man $i$ is matched with woman $j$. The linear program can be formulated as follows:

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
x_{ij} + \sum_{k: w_j \text{ prefers } m_k \text{ to } m_i} x_{kj} + \sum_{l: m_i \text{ prefers } w_l \text{ to } w_j} x_{il} \geq 1 \quad \forall i,j \in \{1, \ldots, n\}
$$


$$
x_{ij} \in \{0, 1\} \quad \forall i,j \in \{1, \ldots, n\}
$$


Where:
- $n$ is the number of men (equal to the number of women)
- $x_{ij}$ is 1 if man $i$ is matched with woman $j$, and 0 otherwise
- The first two constraints ensure that each person is matched exactly once
- The third constraint ensures stability: for each potential pair $(i,j)$, either they are matched, or at least one of them is matched to someone they prefer

## Implementation

The algorithm is implemented in Python using the PuLP library for linear programming. It sets up the linear program based on the preference lists of men and women, solves it, and extracts the stable matching from the solution.

## Usage

To use the algorithm, provide dictionaries representing the preferences of men and women. The output will be a dictionary indicating the matched pairs.

```python
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
- $$\mu_{\ell,r}$$ is a binary variable indicating whether participant $$\ell$$ and participant $$r$$ are matched.
- $$s \succ_\ell r$$ means that participant $$\ell$$ prefers participant $$s$$ to participant $$r$$.

This formulation minimizes the sum of ranks while ensuring that each participant is matched exactly once and that the matching is stable. The algorithm produces a matching that is Pareto efficient with respect to the participants' preferences.

## Implementation

The algorithm has been implemented in Python using the PuLP library for linear programming. You can use this implementation to find egalitarian stable matchings based on given preferences.

## Usage

To use the algorithm, provide dictionaries representing the preferences of men and women. The output will be a dictionary indicating the matched pairs.

```python
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
print("Egalitarian Matching:")
for man, woman in matching.items():
    print(f"{man} - {woman}")
```


# Nash Stable Matching

## Overview

The **Nash Stable Matching** algorithm finds a stable matching that maximizes the product of utilities (Nash social welfare) across all participants, while maintaining stability. This approach aims to produce a "fair" and efficient matching by balancing individual utilities in a multiplicative way. The algorithm is implemented using linear programming with a logarithmic transformation.

## Mathematical Formulation

The objective function for the Nash Stable Matching problem can be formulated as follows:

$$
\text{maximize} \quad \prod_{(\ell,r) \in L \times R} v(\ell,r)^{\mu_{\ell,r}}
$$


which is equivalent to maximizing:

$$
\text{maximize} \quad \sum_{(\ell,r) \in L \times R} \mu_{\ell,r} \log v(\ell,r)
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
- $$\mu_{\ell,r}$$ is a binary variable indicating whether participant $$\ell$$ and participant $$r$$ are matched.

This formulation maximizes the product of valuations (Nash social welfare) while ensuring that each participant is matched exactly once and that the matching is stable. The logarithmic transformation allows us to solve this as a linear programming problem.

## Implementation

The algorithm is implemented in Python using the PuLP library for linear programming. The logarithmic transformation is used to convert the product maximization into a sum maximization, which can be solved using standard linear programming techniques.

## Usage

To use the algorithm, provide dictionaries representing the valuations of participants for each other. The output will be a dictionary indicating the matched pairs.

```python
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
\text{maximize} \quad \sum_{(\ell,r) \in L \times R} v(\ell,r) \cdot \mu_{\ell,r}
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
- $$\mu_{\ell,r}$$ is a binary variable indicating whether participant $$\ell$$ and participant $$r$$ are matched.

This formulation maximizes the sum of valuations while ensuring that each participant is matched exactly once and that the matching is stable. The algorithm produces a matching that is both stable and Pareto efficient.

## Implementation

The algorithm has been implemented in Python using the PuLP library for linear programming. You can use this implementation to find utilitarian stable matchings based on given valuations.

## Usage

To use the algorithm, provide dictionaries representing the valuations of men and women for each other. The output will be a dictionary indicating the matched pairs.

```python
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

# Egalitarian Matching (Without Stability Constraint)

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
- $$\mu_{\ell,r}$$ is a binary variable indicating whether participant $$\ell$$ and participant $$r$$ are matched.

This formulation minimizes the sum of ranks for all matched pairs, ensuring that each participant is matched exactly once. Unlike the stable matching variants, this formulation does not include stability constraints.

## Implementation

The algorithm is implemented in Python using the PuLP library for linear programming. It directly minimizes the sum of ranks without considering stability constraints.

## Usage

To use the algorithm, provide dictionaries representing the preferences of participants. The output will be a dictionary indicating the matched pairs.

```python
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
# Nash Matching (Without Stability Constraint)

## Overview

The **Nash Matching** algorithm without stability constraints finds a matching that maximizes the product of utilities (or satisfaction) of all participants. This approach aims to balance equity and efficiency in matching outcomes without enforcing stability. The algorithm is implemented using linear programming with a logarithmic transformation.

## Mathematical Formulation

The objective function for the Nash Matching problem can be formulated as follows:

$$
\text{maximize} \quad \prod_{(\ell,r) \in L \times R} (v(\ell,r) + v(r,\ell))^{\mu_{\ell,r}}
$$


which is equivalent to maximizing:

$$
\text{maximize} \quad \sum_{(\ell,r) \in L \times R} \mu_{\ell,r} \log(v(\ell,r) + v(r,\ell))
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
- $$\mu_{\ell,r}$$ is a binary variable indicating whether participant $$\ell$$ and participant $$r$$ are matched.

## Implementation

The algorithm is implemented in Python using the PuLP library for linear programming. The logarithmic transformation allows us to solve this as a linear programming problem. The key features of the implementation include:

- Use of binary variables for matching and continuous variables for log utilities.
- Logarithmic utility constraints to handle the product maximization.
- No stability constraints, focusing solely on maximizing the Nash social welfare.

## Usage

To use the algorithm, provide dictionaries representing the valuations of participants for each other. The output will be a dictionary indicating the matched pairs.

```python

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
# Utilitarian Matching (Without Stability Constraint)

## Overview

The **Utilitarian Matching** algorithm without stability constraints finds a matching that maximizes the total sum of utilities (or valuations) across all participants. This approach aims to produce an "efficient" matching by maximizing overall welfare, without the requirement of stability. The algorithm is implemented using linear programming.

## Mathematical Formulation

The objective function for the Utilitarian Matching problem can be formulated as follows:

$$
\text{maximize} \quad \sum_{(\ell,r) \in L \times R} v(\ell,r) \cdot \mu_{\ell,r}
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
- $$v(\ell,r)$$ is the utility (or valuation) that participant $$\ell$$ assigns to being matched with participant $$r$$.
- $$\mu_{\ell,r}$$ is a binary variable indicating whether participant $$\ell$$ and participant $$r$$ are matched.

This formulation maximizes the sum of utilities for all matched pairs, ensuring that each participant is matched exactly once. Unlike the stable matching variants, this formulation does not include stability constraints.

## Implementation

The algorithm is implemented in Python using the PuLP library for linear programming. It directly maximizes the sum of utilities without considering stability constraints.

## Usage

To use the algorithm, provide dictionaries representing the valuations of participants for each other. The output will be a dictionary indicating the matched pairs.

```python
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

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
