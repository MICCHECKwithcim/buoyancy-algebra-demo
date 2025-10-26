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

Created by: Michael Dixon
