from fractions import Fraction
import numpy as np

def print_matrix_frac(matrix, augmented=True):
    """Print matrix with fractions. If augmented, prints with vertical separator."""
    n = len(matrix)
    mid = n if not augmented else len(matrix[0]) // 2

    for row in matrix:
        print('[', end=' ')
        for j, elem in enumerate(row):
            if j == mid and augmented:
                print('|', end=' ')
            frac = Fraction(elem).limit_denominator()
            if frac.denominator == 1:
                print(f"{frac.numerator:3}", end=' ')
            else:
                print(f"{frac!s:8}", end=' ')
        print(']')
    print()

def get_predefined_matrix(number):
    """Returns one of the predefined matrices from the image."""
    matrices = {
        1: np.array([
            [-2, -3, -4],
            [5, -10, 8],
            [1, -3, -8]
        ]),
        2: np.array([
            [-3, -1, 4],
            [-8, 13, 11],
            [-5, -13, 11]
        ]),
        3: np.array([
            [-13, -5, -20],
            [4, -15, -8],
            [13, -12, 8]
        ]),
        4: np.array([
            [-7, 3, 12],
            [-8, -2, -10],
            [10, 12, 54]
        ]),
        5: np.array([
            [-3, -13, 1],
            [-10, 5, -2],
            [7, -18, 3]
        ]),
        6: np.array([
            [-2, 4, 6],
            [-6, 12, 18],
            [-2, 4, 6]
        ]),
        7: np.array([
            [2, 1, -4],
            [-8, -4, 16],
            [2, 1, -4]
        ])
    }

    return matrices.get(number)

def gauss_jordan_inverse_with_steps(matrix):
    """
    Find the inverse of a square matrix using Gauss-Jordan elimination.
    Shows each step of the transformation.
    """
    n = len(matrix)
    # Create augmented matrix [A|I]
    augmented = [[Fraction(0) for _ in range(2 * n)] for _ in range(n)]

    # Fill the augmented matrix
    for i in range(n):
        for j in range(n):
            augmented[i][j] = Fraction(matrix[i][j])
    for i in range(n):
        augmented[i][n + i] = Fraction(1)

    print("Initial augmented matrix:")
    print_matrix_frac(augmented)

    step = 1
    # Gauss-Jordan elimination
    for i in range(n):
        # Find pivot
        pivot = augmented[i][i]
        if pivot == 0:
            # Look for non-zero pivot in rows below
            for j in range(i + 1, n):
                if augmented[j][i] != 0:
                    print(f"\nStep {step}: Swap row {i + 1} with row {j + 1}")
                    augmented[i], augmented[j] = augmented[j], augmented[i]
                    print_matrix_frac(augmented)
                    pivot = augmented[i][i]
                    step += 1
                    break
            if pivot == 0:
                return None

        # Normalize row
        if pivot != 1:
            print(f"\nStep {step}: Divide row {i + 1} by {pivot}")
            for j in range(2 * n):
                augmented[i][j] /= pivot
            print_matrix_frac(augmented)
            step += 1

        # Eliminate column
        for j in range(n):
            if i != j:
                factor = augmented[j][i]
                if factor != 0:
                    print(f"\nStep {step}: Subtract {factor} times row {i + 1} from row {j + 1}")
                    for k in range(2 * n):
                        augmented[j][k] -= factor * augmented[i][k]
                    print_matrix_frac(augmented)
                    step += 1

    # Extract inverse matrix
    inverse = [[augmented[i][j] for j in range(n, 2 * n)] for i in range(n)]
    return inverse

def main():
    while True:
        print("\nAvailable matrices (1-7) or 'q' to quit:")
        choice = input("Enter matrix number or 'q': ")
        
        if choice.lower() == 'q':
            break
            
        try:
            matrix_num = int(choice)
            if 1 <= matrix_num <= 7:
                matrix = get_predefined_matrix(matrix_num)
                print(f"\nMatrix {matrix_num}:")
                print_matrix_frac(matrix, augmented=False)
                print("Finding inverse using Gauss-Jordan elimination:")
                inverse = gauss_jordan_inverse_with_steps(matrix)
                if inverse:
                    print("\nFinal inverse matrix:")
                    print_matrix_frac(inverse, augmented=False)
                else:
                    print("Matrix is not invertible")
            else:
                print("Please enter a number between 1 and 7")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 7 or 'q' to quit")

if __name__ == "__main__":
    main()