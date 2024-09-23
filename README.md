# Matching Algorithms

This project implements various matching algorithms, including the Deferred Acceptance algorithm, the Boston Mechanism, and the Top Trading Cycles (TTC) mechanism. These algorithms are commonly used in applications such as school admissions, organ donation, and job assignments.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Algorithms Implemented](#algorithms-implemented)
  - [Deferred Acceptance](#deferred-acceptance)
  - [Boston Mechanism](#boston-mechanism)
  - [Top Trading Cycles (TTC)](#top-trading-cycles-ttc)
  - [Serial Dictatorship](#serial-dictatorship)
  - [Random Serial Dictatorship](#random-serial-dictatorship)
  - [Linear Programming Algorithms](#linear-programming-algorithms)
    - [Stable Matching LP](#stable-matching-lp)
    - [Egalitarian Stable Matching](#egalitarian-stable-matching)
    - [Nash Welfare Stable Matching](#nash-welfare-stable-matching)
    - [Sex-Equal Stable Matching](#sex-equal-stable-matching)
    - [Utilitarian Stable Matching](#utilitarian-stable-matching)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install the package, use pip:

```bash
pip install matching_algorithms
```

Alternatively, you can clone the repository and install it manually:

```bash
git clone https://github.com/yourusername/matching_algorithms.git
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

The Deferred Acceptance algorithm is a two-sided matching algorithm that pairs participants from two different groups based on their preferences. This algorithm ensures stability in the matches.

### Boston Mechanism

The Boston Mechanism is a direct mechanism for matching students to schools, where students submit their preferences, and schools accept students based on their preferences and capacities.

### Top Trading Cycles (TTC)

The Top Trading Cycles (TTC) mechanism is an efficient and strategy-proof algorithm for allocating resources. It works by allowing participants to express their preferences and trade until a stable allocation is achieved.

### Serial Dictatorship

The Serial Dictatorship mechanism is a priority-based mechanism where participants choose their preferred options one after another based on a predetermined priority order. It is often used in school choice and housing allocation problems.

### Random Serial Dictatorship

The Random Serial Dictatorship (RSD) is a variation of the Serial Dictatorship mechanism where the order of participants is determined randomly. It is used to ensure fairness in assigning preferences, often in situations where no pre-existing priority is available.

### Linear Programming Algorithms

#### Stable Matching LP

The Stable Matching algorithm based on linear programming finds a solution where no pair of participants prefer each other over their assigned matches. It is often used for problems such as marriage matching and student-school assignment.

To find a stable matching using linear programming, we solve the following LP formulation:

$$
\text{Maximize} \sum_{i,j} x_{ij} u_{ij}
$$

subject to the constraints:

1. Each participant is assigned to at most one match:

$$
\sum_{j} x_{ij} \leq 1 \quad \forall i
$$

2. Each match is stable, meaning that there is no blocking pair $(i,j)$ such that both would prefer to be matched with each other over their current assignments:

$$
x_{ij} + x_{ji} \leq 1 \quad \forall (i,j)
$$

3. All assignment variables are binary:

$$
x_{ij} \in \{0, 1\}
$$

Here, $x_{ij}$ is a binary variable indicating whether participant $i$ is matched to participant $j$, and $u_{ij}$ represents the utility or preference of participant $i$ for participant $j$.

#### Egalitarian Stable Matching

The Egalitarian Stable Matching algorithm, implemented using linear programming, finds a stable matching that minimizes the total dissatisfaction (or rank) across all participants. It seeks to produce the most "fair" matching.

#### Nash Welfare Stable Matching

The Nash Welfare Stable Matching algorithm aims to maximize the product of the utilities (or satisfaction) of all participants in the matching. It is a fairness criterion that balances equity and efficiency in matching outcomes.

#### Sex-Equal Stable Matching

The Sex-Equal Stable Matching algorithm seeks to balance the satisfaction between two groups (e.g., men and women) in the matching process. It ensures that both sides have similar outcomes in terms of ranks and preferences.

#### Utilitarian Stable Matching

The Utilitarian Stable Matching algorithm focuses on maximizing the total utility (or satisfaction) of all participants. It seeks to produce a socially optimal matching where the sum of everyone's satisfaction is maximized.


## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
