# Middle Square Algorithm with user input

def middle_square(seed, iterations):
    n = len(str(seed))   # Number of digits in the seed
    current = seed

    print("\nGenerated Random Numbers:\n")

    for i in range(iterations):
        # Square the current number
        square = current ** 2

        # Convert to string and add leading zeros if needed
        square_str = str(square).zfill(2 * n)

        # Extract the middle digits
        start = (len(square_str) - n) // 2
        middle = square_str[start:start + n]

        # Update current value
        current = int(middle)

        print(f"Iteration {i + 1}: {current}")


# User inputs
seed = int(input("Enter seed value: "))
iterations = int(input("Enter number of iterations: "))

# Call the function
middle_square(seed, iterations)