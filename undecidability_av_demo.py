"""
Project 16: Undecidability and Antivirus Limits
Theory concept: Turing Machine + Rice's Theorem + Undecidability

Parts
  1. Turing Machine simulator
  2. Halting problem: why "just run it and see" fails
  3. Reduction: a perfect antivirus would solve the halting problem
  4. The paradox program: defeats ANY candidate perfect_av
  5. Real-world style heuristics (signature / behaviour / score): FP and FN

No real malware is used anywhere. "Malware" is just a harmless marker string.
"""

import sys

# make arrows and dashes print correctly on Windows terminals
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# =====================================================================
# PART 1: Turing Machine simulator
# =====================================================================
class TuringMachine:
    """transitions: {(state, symbol): (new_state, write_symbol, 'L'|'R')}"""

    def __init__(self, transitions, start, accept, reject, blank="_"):
        self.t = transitions
        self.start, self.accept, self.reject, self.blank = start, accept, reject, blank

    def run(self, input_str, max_steps=None):
        """Returns (result, steps). result is ACCEPT / REJECT / UNKNOWN.
        UNKNOWN means the step limit was hit: we cannot tell if it loops
        forever or would halt later. That uncertainty is the whole point."""
        tape = dict(enumerate(input_str))
        state, head, steps = self.start, 0, 0
        while max_steps is None or steps < max_steps:
            if state == self.accept:
                return "ACCEPT", steps
            if state == self.reject:
                return "REJECT", steps
            sym = tape.get(head, self.blank)
            if (state, sym) not in self.t:
                return "REJECT", steps
            state, tape[head], move = self.t[(state, sym)]
            head += 1 if move == "R" else -1
            steps += 1
        return "UNKNOWN", steps


# Machine A: accepts strings of the form 0^n 1^n  (n >= 1)
def machine_0n1n():
    t = {
        ("q0", "0"): ("q1", "X", "R"),
        ("q0", "Y"): ("q3", "Y", "R"),
        ("q1", "0"): ("q1", "0", "R"),
        ("q1", "Y"): ("q1", "Y", "R"),
        ("q1", "1"): ("q2", "Y", "L"),
        ("q2", "0"): ("q2", "0", "L"),
        ("q2", "Y"): ("q2", "Y", "L"),
        ("q2", "X"): ("q0", "X", "R"),
        ("q3", "Y"): ("q3", "Y", "R"),
        ("q3", "_"): ("acc", "_", "R"),
    }
    return TuringMachine(t, "q0", "acc", "rej")


# Machine B: loops forever on every input
def machine_loop():
    return TuringMachine({("q0", "_"): ("q0", "_", "R"),
                          ("q0", "1"): ("q0", "1", "R")}, "q0", "acc", "rej")


# Machine C: scans right over 1s, halts after len(input) steps
def machine_count():
    return TuringMachine({("q0", "1"): ("q0", "1", "R"),
                          ("q0", "_"): ("acc", "_", "R")}, "q0", "acc", "rej")


def part1():
    print("=" * 66)
    print("PART 1: Turing Machine simulator")
    print("=" * 66)
    m = machine_0n1n()
    for w in ["0011", "000111", "0101", "001"]:
        print(f"  0^n1^n machine on {w!r:10} -> {m.run(w, 10_000)[0]}")
    print(f"  looping machine on '111'   -> {machine_loop().run('111', 10_000)[0]}"
          "  (step limit hit, cannot tell if it ever halts)")


# =====================================================================
# PART 2 and 3: Halting problem and the reduction to antivirus
# =====================================================================
def make_program(M, w):
    """Build program P(M, w):
         1. simulate M on w  (this may never finish)
         2. then do the 'malicious' action (harmless marker here)
       P is malware  <=>  M halts on w.
       This is the heart of the reduction from the Halting Problem."""
    def P():
        M.run(w, max_steps=None)          # may loop forever
        return "MALWARE"                  # reached only if M halts
    P.description = f"P(M, w) with |w|={len(w)}"
    return P


def bounded_av(budget):
    """A realistic AV that tries to decide by running P for `budget` steps.
    It must give an answer, so it guesses 'safe' when time runs out."""
    def av(M, w):
        result, _ = M.run(w, max_steps=budget)
        if result == "UNKNOWN":
            return False                  # guess: safe
        return True                       # M halted -> P reaches malware code
    return av


def part2_3():
    print("\n" + "=" * 66)
    print("PART 2/3: Reduction  Halting Problem  ->  perfect antivirus")
    print("=" * 66)
    print("  P(M,w) = simulate M on w; then run malware.")
    print("  perfect_av(P) == True  <=>  M halts on w.")
    print("  So a perfect AV would decide the Halting Problem (impossible).\n")

    cases = [
        ("halts quickly (len 20)", machine_count(), "1" * 20, True),
        ("halts slowly (len 50000)", machine_count(), "1" * 50_000, True),
        ("loops forever", machine_loop(), "1", False),
    ]
    for budget in (100, 1_000, 100_000):
        av = bounded_av(budget)
        print(f"  AV with budget = {budget} steps:")
        for name, M, w, truly_malware in cases:
            verdict = av(M, w)
            status = "correct" if verdict == truly_malware else (
                "WRONG (false negative: missed malware)" if truly_malware
                else "WRONG (false positive)")
            print(f"    {name:26} verdict={'MALWARE' if verdict else 'SAFE':8} {status}")
        print()
    print("  Any budget fails on some input: raising it only moves the failure.")


# =====================================================================
# PART 4: The paradox program (self-reference, exactly as in the brief)
# =====================================================================
def make_paradox(perfect_av):
    def paradox_program():
        if perfect_av(paradox_program) is True:   # AV says: malware
            return "behave_safely"
        else:                                     # AV says: safe
            return "behave_as_malware"
    return paradox_program


def part4():
    print("\n" + "=" * 66)
    print("PART 4: Paradox program vs. candidate perfect_av functions")
    print("=" * 66)
    print("  Assume: perfect_av(program) = True if malware, else False")
    print("  Construct paradox_program:")
    print("     if perfect_av(paradox_program) == True: behave_safely()")
    print("     else: behave_as_malware()\n")

    candidates = {
        "always_true": lambda p: True,
        "always_false": lambda p: False,
        "length_rule": lambda p: len(p.__name__) > 5,
    }
    for name, av in candidates.items():
        p = make_paradox(av)
        verdict = av(p)
        actual = p()
        print(f"  av = {name}")
        print(f"    perfect_av(paradox) = {verdict}")
        if verdict:
            print(f"    paradox behaves: {actual}  -> paradox behaves safely"
                  "  -> AV was WRONG")
        else:
            print(f"    paradox behaves: {actual}  -> paradox is malware"
                  "  -> AV was WRONG")

    # An AV that tries to analyse by running the program never answers:
    print("\n  av = 'run it and watch' (dynamic analysis)")
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(200)
    def watcher(p):
        return p() == "behave_as_malware"
    try:
        make_paradox(watcher)()
    except RecursionError:
        print("    -> never terminates (infinite self-reference), no verdict")
    finally:
        sys.setrecursionlimit(old)

    print("\n  CONCLUSION: No algorithm perfect_av can exist.")
    print("  This is a direct consequence of Rice's Theorem.")
    print("  Real AV tools use heuristics: signature, behavior, ML - all have gaps.")


# =====================================================================
# PART 5: Heuristic AV on simulated test samples (FP / FN)
# =====================================================================
FAKE_SIGNATURE = "FAKE-MALWARE-SIGNATURE-DEMO-123"   # harmless stand-in

SAMPLES = [
    # name, content, behaviours, truly_malware
    ("plain_malware",   f"data {FAKE_SIGNATURE} data", {"encrypt_files", "contact_c2"}, True),
    ("repacked_malware", "ZGF0YSBGQUtFLU1BTFdBUkU=",   {"encrypt_files", "contact_c2"}, True),  # encoded
    ("slow_malware",    "benign looking code",          {"sleep_then_encrypt"},        True),
    ("backup_tool",     "legit backup software",        {"encrypt_files"},             False),
    ("text_editor",     "legit editor",                 set(),                         False),
    ("av_test_docs",    f"docs quoting {FAKE_SIGNATURE}", set(),                       False),
]

def signature_av(content, behaviours):
    return FAKE_SIGNATURE in content

def behaviour_av(content, behaviours):
    return "encrypt_files" in behaviours or "contact_c2" in behaviours

def score_av(content, behaviours):
    score = 0.0
    score += 0.6 if FAKE_SIGNATURE in content else 0.0
    score += 0.35 if "encrypt_files" in behaviours else 0.0
    score += 0.35 if "contact_c2" in behaviours else 0.0
    return score >= 0.5

def part5():
    print("\n" + "=" * 66)
    print("PART 5: Heuristic AV methods on simulated test samples")
    print("=" * 66)
    engines = [("signature", signature_av),
               ("behaviour", behaviour_av),
               ("score/ML-style", score_av)]
    print(f"  {'sample':18} {'truth':8}" + "".join(f"{n:16}" for n, _ in engines))
    totals = {n: {"FP": 0, "FN": 0} for n, _ in engines}
    for name, content, beh, truth in SAMPLES:
        row = f"  {name:18} {'MALWARE' if truth else 'SAFE':8}"
        for en, fn in engines:
            v = fn(content, beh)
            tag = "ok"
            if v and not truth:
                tag = "FALSE POS"; totals[en]["FP"] += 1
            elif not v and truth:
                tag = "FALSE NEG"; totals[en]["FN"] += 1
            row += f"{('MAL' if v else 'safe') + ' ' + tag:16}"
        print(row)
    print()
    for en, c in totals.items():
        print(f"  {en:16} false positives={c['FP']}  false negatives={c['FN']}")
    print("\n  No engine gets 0 FP and 0 FN: consistent with Rice's Theorem.")


# =====================================================================
# INTERACTIVE MODE (default): user enters True / False for perfect_av
# =====================================================================
def paradox_case(assumed):
    """Run the paradox program against an AV that answers `assumed`.
    Returns (output_line, av_was_wrong)."""
    av = lambda program, a=assumed: a
    paradox = make_paradox(av)
    verdict = av(paradox)                    # what the AV claims
    behaviour = paradox()                    # what the program really does
    is_malware = (behaviour == "behave_as_malware")
    wrong = (verdict != is_malware)
    left = f"If perfect_av(paradox) = {verdict}".ljust(31)
    mid = ("paradox behaves safely" if not is_malware else "paradox is malware").ljust(24)
    return f"  {left}\u2192 {mid}\u2192 AV was {'WRONG' if wrong else 'RIGHT'}", wrong


def print_conclusion():
    print("  CONCLUSION: No algorithm perfect_av can exist.")
    print("  This is a direct consequence of Rice's Theorem.")
    print("  Real AV tools use heuristics: signature, behavior, ML \u2014 all have gaps.")


def interactive_paradox():
    print("Input:")
    print("  Assume: perfect_av(program) = True if malware, else False")
    print("  Construct: paradox_program:")
    print("    if perfect_av(paradox_program) == True: behave_safely()")
    print("    else: behave_as_malware()")
    print()
    print("You play the role of perfect_av. Enter its answer for paradox_program.")
    tried = set()
    while True:
        raw = input("\nEnter perfect_av(paradox_program) = True or False (q to quit): ").strip().lower()
        if raw in ("q", "quit", "exit"):
            break
        if raw in ("true", "t", "1", "yes", "y"):
            answer = True
        elif raw in ("false", "f", "0", "no", "n"):
            answer = False
        else:
            print("  Please type True or False.")
            continue
        line, wrong = paradox_case(answer)
        print("\nOutput:")
        print(line)
        if tried == {True, False}:
            continue
        tried.add(answer)
        if tried == {True, False}:
            print_conclusion()
        else:
            print("  (Now try the other value: that one fails too.)")
    if tried != {True, False}:
        print("\nTip: try both True and False to see the full conclusion.")


def sample_io():
    """Static version: both cases, exactly as in the project brief."""
    print("Input:")
    print("  Assume: perfect_av(program) = True if malware, else False")
    print("  Construct: paradox_program:")
    print("    if perfect_av(paradox_program) == True: behave_safely()")
    print("    else: behave_as_malware()")
    print()
    print("Output:")
    for assumed in (True, False):
        print(paradox_case(assumed)[0])
    print_conclusion()


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "interactive"
    if mode == "sample":          # python undecidability_av_demo.py sample
        sample_io()
    elif mode == "all":           # python undecidability_av_demo.py all
        sample_io()
        print()
        part1()
        part2_3()
        part4()
        part5()
    else:                         # python undecidability_av_demo.py
        interactive_paradox()
