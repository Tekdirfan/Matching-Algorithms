# Matching Algorithms

This project implements a variety of matching algorithms, including the Deferred Acceptance algorithm, the Boston Mechanism, the Top Trading Cycles (TTC) mechanism, and several linear programming approaches. These algorithms are widely applicable in various domains such as school admissions, organ allocation, job assignments, and resource allocation problems. Their effectiveness in creating stable and efficient matchings makes them valuable tools in economics, operations research, and decision-making processes.


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
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

## Usage

Here’s a quick example of how to use the matching algorithms in your Python code:

```python
from matching_algorithms import deferred_acceptance, boston_mechanism, ttc

# Example data
students = [...]
schools = [...]

# Using the Deferred Acceptance algorithm
matches = deferred_acceptance(students, schools)

# Using the Boston Mechanism
boston_matches = boston_mechanism(students, schools)

# Using the Top Trading Cycles (TTC) mechanism
ttc_matches = ttc(students, schools)

# Using linear programming for stable matching
lp_matches = stable_matching_lp(students, schools)

```

## Algorithms Implemented

### Deferred Acceptance

#### Marriage Market Deferred Acceptance

The Deferred Acceptance algorithm for the Marriage Market is a two-sided matching algorithm that pairs participants from two groups (e.g., men and women) based on their preferences. The algorithm ensures that no pair of participants would rather be matched with each other than with their current match, leading to a stable matching. In this setup, one group (typically men) proposes to the other group, and participants from the second group (women) accept or reject proposals based on their preferences.

The algorithm proceeds in rounds:

1. Each participant in the proposing group proposes to their most-preferred partner who has not yet rejected them.
2. Participants in the receiving group tentatively accept the most-preferred proposal they have received so far and reject the others.
3. Rejected participants propose to their next most-preferred partner in the next round.
4. The process continues until no more proposals are made, and the tentative matches become final.

#### School Choice Deferred Acceptance

The Deferred Acceptance algorithm in the School Choice setup adapts the same basic framework but focuses on assigning students to schools based on their preferences and the schools' priorities (e.g., entrance exams or other criteria).

In this version:

1. Students submit their ranked preferences for schools.
2. Schools rank students based on their priorities.
3. Students propose to their most-preferred school.
4. Schools tentatively accept the highest-ranked students based on their capacity and reject others.
5. Rejected students propose to their next most-preferred school in subsequent rounds.
6. The process continues until no more students are proposing, and the tentative assignments become final.

This algorithm is commonly used for matching students to schools in centralized systems, ensuring that no student-school pair would rather be matched with each other than with their current assignment, resulting in a stable match.


### Boston Mechanism

The Boston Mechanism is a direct, priority-based algorithm for matching students to schools. It is widely used in school admission processes where students have preferences over schools, and schools have priorities over students.

The mechanism works as follows:

1. **First Round:** Students submit their ranked preferences for schools. Schools first allocate spots to students who ranked them as their first choice, based on the schools' priorities and capacities.
   
2. **Subsequent Rounds:** Any students who didn't get placed in their first-choice schools (due to capacity limits) participate in the next round. In this round, the schools consider students who listed them as their second choice. This process continues until all students are matched to a school, or there are no more options left.

3. **Final Assignment:** The algorithm ends when all remaining students are assigned based on their next available preference, or no further assignments are possible.

The Boston Mechanism has some potential downsides, as students may not always have an incentive to rank schools truthfully. Since priority is given to students who rank a school as their top choice, students might strategically misrepresent their preferences to increase their chances of getting into a higher-priority school. This characteristic distinguishes the Boston Mechanism from strategy-proof algorithms like Deferred Acceptance.

Despite these issues, the Boston Mechanism is still used in various school systems because of its simplicity and the fact that it gives students a higher chance of getting into their top-choice schools compared to some other mechanisms.

### Top Trading Cycles (TTC)

The Top Trading Cycles (TTC) mechanism is an efficient and strategy-proof algorithm used for allocating resources, particularly in situations where participants have preferences over the available resources. It is most famously used in housing markets and school choice problems.

The TTC mechanism works as follows:

1. **Initial Preferences:** Each participant expresses their ranked preferences over the resources (e.g., houses, schools). Similarly, each resource may also have a priority ranking of participants.

2. **Cycle Formation:** Each participant points to their most preferred available resource, and each resource points to its highest-priority participant (if applicable). These "pointing" relationships form directed graphs, which naturally create cycles.

3. **Trading in Cycles:** Once a cycle is formed (even if the cycle only consists of one participant and one resource), the participants in the cycle are immediately matched to the resources they are pointing to. After the match, these participants and resources are removed from further consideration.

4. **Reiteration:** The process is repeated with the remaining participants and resources until no participants are left unmatched.

5. **Final Allocation:** The mechanism ensures that all participants are matched to a resource that they consider to be as good as or better than any other option they could receive through any other stable mechanism. 

TTC is **strategy-proof**, meaning that participants cannot improve their outcomes by misrepresenting their preferences. It also ensures **Pareto efficiency**, meaning no other matching arrangement would make any participant better off without making someone else worse off.


### Serial Dictatorship

The Serial Dictatorship mechanism is a priority-based allocation method where participants select their preferred options sequentially based on a predetermined priority order. This mechanism is commonly applied in contexts such as school choice and housing allocation.

The mechanism operates as follows:

1. **Priority Order:** Each participant is assigned a rank or priority based on a predetermined criterion (e.g., random lottery, academic performance, etc.). This rank determines the order in which participants will choose their preferred options.

2. **Choice Process:** Starting with the participant with the highest priority, each participant selects their most preferred available option from the set of options (e.g., schools, houses). Once a participant selects an option, it becomes unavailable for others.

3. **Subsequent Choices:** The next participant in the priority order then selects their preferred option from the remaining available choices. This process continues until all participants have made their selections or until all options have been allocated.

4. **Final Allocation:** The outcome of the Serial Dictatorship mechanism results in a matching where each participant receives an option they have chosen, based on their preferences and the availability of options at the time of their turn.

The Serial Dictatorship mechanism is **strategy-proof**, meaning that participants have no incentive to misrepresent their preferences, as their best outcome is achieved by honestly selecting their most preferred available option. However, the mechanism can lead to inequalities based on the predetermined priority order, which may not always reflect the participants' actual needs or circumstances.


### Random Serial Dictatorship

The Random Serial Dictatorship (RSD) mechanism is a variation of the Serial Dictatorship mechanism that introduces an element of randomness in determining the order in which participants make their selections. This method is particularly useful in situations where there is no pre-existing priority order among participants.

#### How It Works:

1. **Random Order Generation:** At the beginning of the allocation process, a random order is generated for all participants. This order dictates the sequence in which participants will choose their preferred options.

2. **Choice Process:** Similar to the Serial Dictatorship mechanism, each participant selects their most preferred available option in the order determined by the random draw. The participant with the highest priority (based on the random order) chooses first, followed by the next participant, and so on.

3. **Subsequent Choices:** As each participant makes their selection, options become unavailable to those who choose later. The process continues until all participants have selected their options or all available options have been allocated.

4. **Fairness:** The Random Serial Dictatorship mechanism aims to create a fairer allocation process by giving each participant an equal chance of being chosen first, thereby reducing the potential inequalities that might arise from a fixed priority order. 

5. **Strategy-Proofness:** Like its predecessor, RSD is strategy-proof, meaning participants have no incentive to misrepresent their preferences, as their best outcomes are achieved by honestly selecting their most preferred options available at their turn.

The RSD mechanism is particularly effective in educational contexts, such as school assignments, where fairness and transparency in the selection process are essential.


### Linear Programming Algorithms with Stability Constraint

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

matching = egalitarian_matching(men_prefs, women_prefs)
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

### Linear Programming Algorithms without Stability Constraint

#### Egalitarian  Matching

The Egalitarian Matching algorithm, implemented using linear programming, finds a matching that minimizes the total dissatisfaction (or rank) across all participants. It seeks to produce the most "fair" matching without stability constraint.

#### Nash Matching

The Nash Matching algorithm aims to maximize the product of the utilities (or satisfaction) of all participants in the matching. It is a fairness criterion that balances equity and efficiency in matching outcomes without stability constraint.


#### Utilitarian Stable Matching

The Utilitarian Matching algorithm focuses on maximizing the total utility (or satisfaction) of all participants. It seeks to produce a socially optimal matching where the sum of everyone's satisfaction is maximized without stability constraint.


## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
