# Middle Square Algorithm using seed value 1234

def middle_square(seed, iterations):
    n = len(str(seed))  # Number of digits in the seed
    current = seed

    print("Middle Square Random Numbers:\n")

    for i in range(iterations):
        # Square the current number
        square = current ** 2

        # Convert to string and pad with zeros if necessary
        square_str = str(square).zfill(2 * n)

        # Find the middle digits
        start = (len(square_str) - n) // 2
        middle = square_str[start:start + n]

        # Convert middle digits back to integer
        current = int(middle)

        print(f"Iteration {i + 1}: {current}")


# Seed value
seed = 1234

# Number of random numbers to generate
iterations = 10

middle_square(seed, iterations)