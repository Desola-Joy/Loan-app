# M/M/1/N Queueing Model

# Inputs
lam = float(input("Enter arrival rate (lambda): "))
mu = float(input("Enter service rate (mu): "))
N = int(input("Enter maximum number of customers in system (N): "))

# Traffic intensity
rho = lam / mu

# Calculate P0
if rho != 1:
    P0 = (1 - rho) / (1 - rho**(N + 1))
else:
    P0 = 1 / (N + 1)

print("\n--- Results ---")
print(f"Traffic Intensity (rho) = {rho:.4f}")
print(f"P0 (Probability system is empty) = {P0:.4f}")

# Probabilities Pn
print("\nProbabilities Pn:")
for n in range(N + 1):
    Pn = (rho**n) * P0
    print(f"P{n} = {Pn:.4f}")

# Probability system is full
PN = (rho**N) * P0
print(f"\nProbability system is full (PN) = {PN:.4f}")

# Effective arrival rate
lambda_eff = lam * (1 - PN)
print(f"Effective arrival rate = {lambda_eff:.4f}")

# Average number in system (Ls)
if rho != 1:
    Ls = (rho * (1 - (N + 1)*(rho**N) + N*(rho**(N + 1)))) / \
         ((1 - rho) * (1 - rho**(N + 1)))
else:
    Ls = N / 2

# Average number in queue (Lq)
Lq = Ls - (lambda_eff / mu)

print(f"Average number in system (Ls) = {Ls:.4f}")
print(f"Average number in queue (Lq) = {Lq:.4f}")