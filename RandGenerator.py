import random

C = 10

options = [v for v in range(C)]

last_times = [0] * C

choices = []

def generate(n, e):
    """Generate `n` random numbers. e~100 is good for low variance."""
    last_times = [0] * C
    choices = []

    # Generator loop
    for _ in range(n):
        for j in range(C):
            last_times[j] += 1
        
        s = sum(last_times)
        weights = [l**e/s for l in last_times]

        choice = random.choices(options, weights, k=1)[0]
        choices.append(choice)

        index = options.index(choice)

        last_times[index] = 0
    
    return choices

def test(n, e, c):
    print("\n************************************************************")
    print(f"Testing generation of {n} random numbers {c} times.")
    print(f"The exponent being tested is {e}.")
    results = [0] * len(options)
    for i in range(c):
        if c >= 5 and (i+1) % (c**0.5//5) == 0:
            print(f"Running round {i+1}...")
        
        r = generate(n, e)
        for i, o in enumerate(options):
            results[i] += r.count(o)
    
    unnormalised = results.copy()
    print("Normalising values...")

    for i in range(len(options)):
        results[i] = results[i] / (n*c)

    print(f"Result values: {unnormalised}")
    print(f"Normalised values: {results}")
    print(f"Variation: {max(results)-min(results)}")
    return results

n = 1
c = 10000

exps = [-1000, -100, -20, -5, -3, -2, -1, 0, 1, 2, 3, 5, 10, 20, 100]

for e in exps:
    test(n, e, c)