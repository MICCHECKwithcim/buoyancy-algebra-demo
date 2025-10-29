Buoyancy Algebra Demo
---------------------
This folder contains a minimal prototype of the "Buoyancy Repair" algorithm.

Run:
  python buoyancy_repair.py "Your sentence here"

Example:
  python buoyancy_repair.py "ALL CRIMINALS deserve life in jail!!!"

What it does:
  - Measures the harshness of a sentence (Π = harm / (1 + provocation))
  - Applies R→C→F operators:
        R (Re-express): soften language, remove shouting
        C (Contextualize): add evidence/hedges
        F (Frame): balance with “while X, also Y”
  - Prints before/after Π, showing convergence in finite steps
  - Saves a clean timestamped text file with the results

Purpose:
  Demonstrates a symbolic, finite-step approach to linguistic alignment — turning harsh or extreme statements into measured, evidence-based ones.

## Data
- `data/Ethicist_claims.csv` — 18 segments from “Should I Retire…”
- `data/Readers_claims.csv` — 33 segments from “Facebook Enables Extremist Views… (Readers Respond)”

One Ω pass yields:
- Ethicist: mean ΔΠ = 0.079 (≈16% relative drop), n = 18
- Readers: mean ΔΠ = 0.083, n = 33

Created by: Michael Dixon

