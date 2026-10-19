Theory of Computation – Project 16

**Academic Project: Undecidability and Antivirus Limits**

# Summary of Rice's Theorem: Statement, Proof and Application to Antivirus Limits

## Project Overview

This project explores **Rice's Theorem**, a fundamental result in the Theory of Computation that states that every non-trivial semantic property of recursively enumerable (RE) languages is undecidable.

The project explains the theorem, presents its proof using a reduction from the Acceptance Problem (\(A_{TM}\)), and demonstrates its application to antivirus software. It shows why no algorithm can perfectly classify all arbitrary programs as malicious or safe based solely on their computational behaviour.

## Objectives

- Understand the statement and significance of Rice's Theorem.
- Learn semantic properties, Turing-recognisable languages, and undecidability.
- Study the proof of Rice's Theorem using reduction from \(A_{TM}\).
- Apply the theorem to understand the theoretical limitations of perfect antivirus detection.
- Demonstrate undecidability concepts through Python simulations.

## Key Concepts

- **Rice's Theorem:** Every non-trivial semantic property of recursively enumerable languages is undecidable.
- **Turing Machines:** Mathematical models used to study computation.
- **Acceptance Problem (\(A_{TM}\)):** The undecidable problem of determining whether a Turing Machine accepts a given input.
- **Semantic Properties:** Properties that depend on the language recognised by a machine rather than its implementation.
- **Undecidability:** The impossibility of constructing an algorithm that always produces the correct answer and halts for every input for a given problem.

## Application to Antivirus Limits

The project applies Rice's Theorem to the problem of perfect malware detection. By modelling malicious behaviour as a program accepting at least one input, we show that determining whether every arbitrary program exhibits this behaviour is undecidable.

The project also discusses self-reference using Kleene's Recursion Theorem, demonstrating why a hypothetical perfect antivirus classifier leads to a contradiction.

It further explores practical detection approaches, including signature-based, behaviour-based, and machine-learning-based methods, and explains why these methods cannot guarantee perfect classification for all arbitrary programs.

## Python Implementation

The accompanying Python demonstration illustrates:

- Turing Machine simulation and bounded execution.
- Reduction from the Acceptance Problem.
- The limitations of fixed execution-step budgets.
- A self-referential paradox program.
- Heuristic malware detection using signatures, behaviour, and scoring.

## Key Takeaways

- Non-trivial semantic properties of recursively enumerable languages are undecidable.
- A universal algorithm cannot perfectly classify every arbitrary program based on its semantic behaviour.
- Malware detection tools can be useful in practice, but they cannot guarantee perfect detection in every possible case.
- Restricting the class of programs being analysed can make certain problems decidable.

## Technologies Used

- **Python** – Simulation and demonstration
- **Theory of Computation** – Turing Machines, reductions, and undecidability
- **GitHub** – Project documentation and version control

## References

1. Michael Sipser, *Introduction to the Theory of Computation*, Cengage.
2. A. M. Turing, *On Computable Numbers, with an Application to the Entscheidungsproblem*, 1936.
3. H. G. Rice, *Classes of Recursively Enumerable Sets and Their Decision Problems*, 1953.
4. S. C. Kleene, *On Notation for Ordinal Numbers*, 1938.

---


