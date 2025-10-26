# 🧮 Buoyancy Algebra Demo

**Author:** Michael Dixon  
**Version:** 1.0  

This repository demonstrates a symbolic, finite-step method for repairing harsh or absolute language into balanced, evidence-based statements.

---

## 🚀 Quick Start

```bash
python buoyancy_repair.py "ALL CRIMINALS deserve life in jail!!!"

Input : ALL CRIMINALS deserve life in jail!!!
Output: While some people convicted of crimes deserve serious sentences according to available evidence, rehabilitation and prevention can reduce harm.
Π before: 0.52 → Π after: 0.37  (ΔΠ = 0.15)
ρ³ = I holds ✅

| Metric                      | Value                  |
| --------------------------- | ---------------------- |
| **n (examples)**            | 91                     |
| **Improved / Same / Worse** | 91 / 0 / 0             |
| **Mean Π (before → after)** | 0.496 → 0.358          |
| **Relative drop**           | 27.8%                  |
| **Mean ΔΠ (median)**        | 0.138 (0.150)          |
| **t(90)**                   | 25.5 (p = 5.8 × 10⁻⁴³) |

| Operator              | Function
| --------------------- | ----------------------------------------------------------------- |
| **R (Re-express)**    | soften absolutes, remove shouting
| --------------------- | ----------------------------------------------------------------- |
| **C (Contextualize)** | add evidence/hedge
| --------------------- | ----------------------------------------------------------------- |
| **F (Frame)**   | add balance (“While X, rehabilitation and prevention can reduce harm.”) |

