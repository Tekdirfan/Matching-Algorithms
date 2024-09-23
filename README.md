# Matching Algorithms

This project implements various matching algorithms, including the Deferred Acceptance algorithm, the Boston Mechanism, and the Top Trading Cycles (TTC) mechanism. These algorithms are commonly used in applications such as school admissions, organ donation, and job assignments.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Algorithms Implemented](#algorithms-implemented)
  - [Deferred Acceptance](#deferred-acceptance)
  - [Boston Mechanism](#boston-mechanism)
  - [Top Trading Cycles (TTC)](#top-trading-cycles-ttc)
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

```

## Algorithms Implemented

### Deferred Acceptance

The Deferred Acceptance algorithm is a two-sided matching algorithm that pairs participants from two different groups based on their preferences. This algorithm ensures stability in the matches.

### Boston Mechanism

The Boston Mechanism is a direct mechanism for matching students to schools, where students submit their preferences, and schools accept students based on their preferences and capacities.

### Top Trading Cycles (TTC)

The Top Trading Cycles (TTC) mechanism is an efficient and strategy-proof algorithm for allocating resources. It works by allowing participants to express their preferences and trade until a stable allocation is achieved.


## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
