from fractions import Fraction
import numpy as np

def print_matrix_frac(matrix, augmented=True):
    """Print matrix with fractions. If augmented, prints with vertical separator."""
    n = len(matrix)
    mid = n if not augmented else len(matrix[0])//2
    
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

def gauss_jordan_inverse_with_steps(matrix):
    """
    Find the inverse of a 3x3 matrix using Gauss-Jordan elimination.
    Shows each step of the transformation.
    """
    n = len(matrix)
    # Create augmented matrix [A|I]
    augmented = [[Fraction(0) for _ in range(2*n)] for _ in range(n)]
    
    # Fill the augmented matrix
    for i in range(n):
        for j in range(n):
            augmented[i][j] = Fraction(matrix[i][j])
    for i in range(n):
        augmented[i][n+i] = Fraction(1)
    
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
                    print(f"\nStep {step}: Swap row {i+1} with row {j+1}")
                    augmented[i], augmented[j] = augmented[j], augmented[i]
                    print_matrix_frac(augmented)
                    pivot = augmented[i][i]
                    step += 1
                    break
            if pivot == 0:
                return None
        
        # Normalize row
        if pivot != 1:
            print(f"\nStep {step}: Multiply row {i+1} by {Fraction(1, pivot)}")
            for j in range(2*n):
                augmented[i][j] /= pivot
            print_matrix_frac(augmented)
            step += 1
        
        # Eliminate column
        for j in range(n):
            if i != j:
                factor = augmented[j][i]
                if factor != 0:
                    print(f"\nStep {step}: Subtract {factor} times row {i+1} from row {j+1}")
                    for k in range(2*n):
                        augmented[j][k] -= factor * augmented[i][k]
                    print_matrix_frac(augmented)
                    step += 1
    
    # Extract inverse matrix
    inverse = [[augmented[i][j] for j in range(n, 2*n)] for i in range(n)]
    return inverse

def main():
    while True:
        matrix = []
        print("Enter the matrix row by row (enter 'q' to quit):")
        while True:
            row_input = input("Enter row (comma-separated values) or 'q' to quit: ")
            if row_input.lower() == 'q':
                print("Exiting...")
                return
            
            try:
                row = list(map(Fraction, row_input.split(',')))
                matrix.append(row)
            except ValueError:
                print("Invalid input. Please enter numeric values separated by commas.")
                continue
            
            if len(matrix) > 1 and len(matrix[-1]) != len(matrix[0]):
                print("All rows must have the same number of columns. Please re-enter the last row.")
                matrix.pop()
                continue
            
            if len(matrix) > 0 and len(matrix[-1]) == 0:
                print("Empty row detected. Please enter a valid row.")
                matrix.pop()
                continue
            
            if len(matrix) > 0 and len(matrix[-1]) == len(matrix[0]):
                break  # Exit the inner loop if the row is valid and has the correct length

        print("Input matrix:")
        print_matrix_frac(matrix, augmented=False)
        print("Finding inverse using Gauss-Jordan elimination:")
        inverse = gauss_jordan_inverse_with_steps(matrix)
        if inverse:
            print("\nFinal inverse matrix:")
            print_matrix_frac(inverse, augmented=False)
        else:
            print("Matrix is not invertible")

if __name__ == "__main__":
    main()