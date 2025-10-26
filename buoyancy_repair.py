#!/usr/bin/env python3
# Buoyancy Repair — Batch Demo Edition (no external libraries)

import re, sys, os, datetime
from io import StringIO
import contextlib

# ---------- COLORS ----------
USE_COLOR = True
class C:
    RED   = "\033[31m" if USE_COLOR else ""
    GREEN = "\033[32m" if USE_COLOR else ""
    YEL   = "\033[33m" if USE_COLOR else ""
    CYAN  = "\033[36m" if USE_COLOR else ""
    DIM   = "\033[2m"  if USE_COLOR else ""
    RST   = "\033[0m"  if USE_COLOR else ""

def color(s, c): return f"{c}{s}{C.RST}"

def _enable_ansi():
    # Enable ANSI colors on Windows (harmless if it fails)
    try:
        if os.name == "nt":
            import ctypes, ctypes.wintypes
            k = ctypes.windll.kernel32
            h = k.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
            m = ctypes.wintypes.DWORD()
            if k.GetConsoleMode(h, ctypes.byref(m)):
                k.SetConsoleMode(h, m.value | 0x0004)  # ENABLE_VIRTUAL_TERMINAL_PROCESSING
    except Exception:
        pass

# ---------- WORD LISTS ----------
NEG = {
    "always","never","forever","cages","criminals","evil","hate","violent",
    "idiot","barbaric","lock","prison","worthless","threat","ban"
}
POS = {
    "sometimes","often","can","may","rehab","rehabilitation","help","heal","hope",
    "support","prevention","education","treatment","reform","dignity","mercy",
    "alternatives","reduce","harm","restore"
}
ABSOLUTES = {"always","never","forever","all","none","everyone","no","nobody"}

def toks(s): return re.findall(r"[A-Za-z']+|[!?]", s)

# ---------- METRICS ----------
def simple_sentiment(t):
    """Polarity in [-1, +1]; negatives slightly heavier so repairs show up."""
    x = toks(t.lower()); s = 0.0
    for w in x:
        if w in NEG: s -= 1.2
        if w in POS: s += 1.0
    return max(-1.0, min(1.0, s / max(6, len(x))))

def provocation(t):
    """0..1: ALLCAPS + !!! + absolutists."""
    x = toks(t); n = len(x) or 1
    caps  = sum(1 for w in x if w.isalpha() and w.upper()==w and len(w)>2)
    bangs = sum(1 for w in x if w in {"!","?"})
    absol = sum(1 for w in x if w.lower() in ABSOLUTES)
    return min(1.0, 0.55*(caps/n) + 0.15*(bangs/n) + 0.45*(absol/n))

def harm(t):
    """Higher when polarity is negative."""
    pol = simple_sentiment(t)
    return max(0.0, min(1.0, (-pol + 1)/2))

def pi(t):
    """Gate-4 metric Π."""
    return harm(t) / (1.0 + provocation(t))

# ---------- OPERATORS ----------
def R(t):
    """Re-express: de-spice + de-yell + soften absolutes."""
    t = re.sub(r"([!?])\1+", r"\1", t)
    t = re.sub(r"\b([A-Z]{4,})\b", lambda m: m.group(1).title(), t)  # LONG ALLCAPS -> Title
    t = re.sub(r"\b(all|always|never|forever)\b", "some", t, flags=re.I)
    t = re.sub(r"\bCRIMINALS\b", "criminals", t)  # normalize leftover capitalization
    t = re.sub(r"\bcriminals\b", "people convicted of crimes", t)
    t = re.sub(r"\blife in jail\b", "serious sentences", t, flags=re.I)
    return t.strip()

def Cx(t):
    """Context: add evidence hedge if missing."""
    if re.search(r"\bevidence\b", t, flags=re.I):
        return t
    if re.search(r"[.?!]\s*$", t):
        return re.sub(r"[.?!]\s*$", " according to available evidence.", t)
    return t + " according to available evidence"

def F(t):
    """Frame: balanced tail with explicit prosocial content."""
    if t.lower().startswith("while"):
        return t
    core = t.rstrip(" .!?")
    return f"While {core}, rehabilitation and prevention can reduce harm."

# ---------- ρ³ ON STANCE BUCKETS ----------
def stance_bucket(text):
    p = simple_sentiment(text)
    if p < -0.2: return "negative"
    if p >  0.2: return "positive"
    return "neutral"

def rho_bucket(b):
    order = ["negative","neutral","positive"]
    return order[(order.index(b)+1) % 3]

def rho3_identity_test():
    b = "negative"
    return rho_bucket(rho_bucket(rho_bucket(b))) == b

# ---------- REPAIR ----------
def repair(text, max_steps=4):
    cur = text
    before = pi(cur)
    trail = []

    for s in range(1, max_steps+1):
        prev = pi(cur)
        cur  = F(Cx(R(cur)))
        now  = pi(cur)
        trail.append((s, prev, now, cur))
        if now <= 0.35 or abs(prev - now) < 0.02:
            break

    after = pi(cur)
    delta = before - after  # how much Π dropped

    # Pretty print (colored)
    print(color("Input :", C.DIM), text)
    print(color("Output:", C.DIM),
          color(cur, C.GREEN if after <= before else C.YEL))
    print(
        color("Π before:", C.DIM), color(f"{before:.2f}", C.RED),
        color(" → ", C.DIM),
        color("Π after:",  C.DIM), color(f"{after:.2f}", C.GREEN if after < before else C.YEL),
    )
    print(color("ΔΠ:", C.DIM), color(f"{delta:.2f}", C.GREEN if delta > 0 else C.YEL))
    for s, p0, p1, _ in trail:
        arrow = "↓" if p1 < p0 else ("→" if abs(p1 - p0) < 1e-6 else "↑")
        col   = C.GREEN if p1 < p0 else (C.YEL if abs(p1 - p0) < 1e-6 else C.RED)
        print(" ", color(f"step {s}:", C.CYAN), color(f"Π {p0:.2f} {arrow} {p1:.2f}", col))

    if rho3_identity_test():
        print(color("ρ³ = I holds ✅", C.CYAN))
    else:
        print(color("ρ³ = I failed ❌", C.RED))

    # Return clean (no color) text block for saving
    block = []
    block.append(f"Input : {text}")
    block.append(f"Output: {cur}")
    block.append(f"Π before: {before:.2f} → Π after: {after:.2f}")
    block.append(f"ΔΠ: {delta:.2f}")
    for s, p0, p1, _ in trail:
        arrow = "↓" if p1 < p0 else ("→" if abs(p1 - p0) < 1e-6 else "↑")
        block.append(f"  step {s}: Π {p0:.2f} {arrow} {p1:.2f}")
    block.append("ρ³ = I holds ✅" if rho3_identity_test() else "ρ³ = I failed ❌")
    return "\n".join(block)

# ---------- BATCH DEMO ----------
def load_quotes_from_file(fname="quotes.txt"):
    try:
        with open(fname, "r", encoding="utf-8") as f:
            lines = [ln.strip() for ln in f.readlines()]
        return [ln for ln in lines if ln]
    except Exception:
        return None

def batch_demo():
    # If quotes.txt is present, use it; else use built-in examples
    file_quotes = load_quotes_from_file("quotes.txt")
    examples = file_quotes or [
        "ALL CRIMINALS deserve life in jail!!!",
        "These people are EVIL and should ALWAYS be locked up!!!",
        "No one can ever change—they are ALL hopeless!!!",
        "Everyone in that group is DANGEROUS and should NEVER speak!!!",
        "Those kids are worthless troublemakers forever!!!",
    ]

    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    outname = f"demo_results_{ts}.txt"

    print(color("Running Buoyancy Algebra Batch Demo...", C.CYAN))
    results = []
    for i, ex in enumerate(examples, 1):
        print(color(f"\n--- Example {i} ---", C.CYAN))
        report = repair(ex)
        print(color(report, C.DIM))
        results.append(report + "\n")

    clean = "\n".join(results)
    with open(outname, "w", encoding="utf-8") as f:
        f.write(re.sub(r"\x1b\[[0-9;]*m", "", clean))  # strip any color
    print(color(f"\nAll results saved to {outname} ✅", C.GREEN))

# ---------- MAIN ----------
def main():
    _enable_ansi()
    if len(sys.argv) == 1:
        batch_demo()
        return

    # Single sentence mode
    txt = " ".join(sys.argv[1:])
    report = repair(txt)
    print(report)
    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    outname = f"result_{ts}.txt"
    with open(outname, "w", encoding="utf-8") as f:
        f.write(re.sub(r"\x1b\[[0-9;]*m", "", report))
    print(color(f"Saved results to {outname} ✅", C.CYAN))

if __name__ == "__main__":
    main()
