from fractions import Fraction
import numpy as np
import os
from io import StringIO
import sys
import csv

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

def ensure_output_directory():
    """Create outputs directory if it doesn't exist."""
    output_dir = os.path.join(os.path.dirname(__file__), 'outputs')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def capture_output(func):
    """Capture stdout output from a function."""
    old_stdout = sys.stdout
    string_io = StringIO()
    sys.stdout = string_io
    try:
        result = func()
        output = string_io.getvalue()
        return output, result
    finally:
        sys.stdout = old_stdout

def save_matrix_output(matrix_num, matrix, inverse):
    """Save matrix and its inverse to a file."""
    output_dir = ensure_output_directory()
    output_file = os.path.join(output_dir, f'output{matrix_num}.txt')
    
    def process_matrix():
        print(f"Matrix {matrix_num}:")
        print_matrix_frac(matrix, augmented=False)
        print("\nSteps to find inverse using Gauss-Jordan elimination:")
        inverse_result = gauss_jordan_inverse_with_steps(matrix)
        if inverse_result:
            print("\nFinal inverse matrix:")
            print_matrix_frac(inverse_result, augmented=False)
        else:
            print("Matrix is not invertible")
    
    output, _ = capture_output(process_matrix)
    
    with open(output_file, 'w') as f:
        f.write(output)
    
    print(f"Results saved to {output_file}")

def parse_matrix_string(matrix_str):
    """Parse a string representation of a matrix into a numpy array."""
    try:
        # Split the string into rows
        rows = [row.strip() for row in matrix_str.strip().split('\n')]
        # Parse each row into numbers
        matrix = []
        for row in rows:
            # Handle both space and comma-separated values
            numbers = row.replace(',', ' ').split()
            row_values = [float(num) for num in numbers]
            matrix.append(row_values)
        
        # Validate matrix dimensions
        if not matrix or not all(len(row) == len(matrix[0]) for row in matrix):
            raise ValueError("Invalid matrix dimensions. All rows must have the same length.")
        
        return np.array(matrix)
    except ValueError as e:
        print(f"Error parsing matrix: {e}")
        return None

def read_matrix_from_file(file_path):
    """Read matrix from a file (supports txt and csv formats)."""
    try:
        with open(file_path, 'r') as f:
            if file_path.endswith('.csv'):
                reader = csv.reader(f)
                matrix = [[float(num) for num in row] for row in reader if row]
            else:
                content = f.read()
                return parse_matrix_string(content)
        
        if not matrix:
            raise ValueError("Empty matrix file")
        
        return np.array(matrix)
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def get_matrix_input():
    """Interactive function to get matrix input from user."""
    print("\nEnter matrix data in one of the following ways:")
    print("1. Enter predefined matrix number (1-7)")
    print("2. Enter path to a file containing the matrix")
    print("3. Enter matrix rows manually")
    print("4. Show example input formats")
    print("q. Quit")
    
    choice = input("\nYour choice: ").strip().lower()
    
    if choice == 'q':
        return None, True
    
    if choice == '4':
        print("\nExample input formats:")
        print("\n1. Space-separated values:")
        print("1 2 3\n4 5 6\n7 8 9")
        print("\n2. Comma-separated values (CSV):")
        print("1,2,3\n4,5,6\n7,8,9")
        print("\n3. File format: Same as above, saved in .txt or .csv")
        return get_matrix_input()
    
    if choice == '1':
        try:
            matrix_num = int(input("Enter matrix number (1-7): "))
            if 1 <= matrix_num <= 7:
                return get_predefined_matrix(matrix_num), False
            print("Invalid matrix number. Please enter a number between 1 and 7.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        return get_matrix_input()
    
    if choice == '2':
        file_path = input("Enter the path to your matrix file: ").strip()
        if not os.path.isabs(file_path):
            # Make path relative to script directory
            file_path = os.path.join(os.path.dirname(__file__), file_path)
        matrix = read_matrix_from_file(file_path)
        if matrix is not None:
            return matrix, False
        return get_matrix_input()
    
    if choice == '3':
        print("\nEnter matrix rows (one row per line, numbers separated by spaces)")
        print("Press Enter twice when done:")
        rows = []
        while True:
            line = input()
            if not line and rows:  # Empty line and we have some rows
                break
            if line:  # Non-empty line
                rows.append(line)
        
        if rows:
            matrix = parse_matrix_string('\n'.join(rows))
            if matrix is not None:
                return matrix, False
        
        return get_matrix_input()
    
    print("Invalid choice. Please try again.")
    return get_matrix_input()

def main():
    print("Welcome to Matrix Inverse Calculator using Gauss-Jordan Elimination")
    print("===============================================================")
    
    while True:
        matrix, should_quit = get_matrix_input()
        
        if should_quit:
            print("\nGoodbye!")
            break
            
        if matrix is not None:
            print("\nInput matrix:")
            print_matrix_frac(matrix, augmented=False)
            
            if matrix.shape[0] != matrix.shape[1]:
                print("Error: Matrix must be square to have an inverse.")
                continue
                
            inverse = gauss_jordan_inverse_with_steps(matrix)
            
            if inverse is None:
                print("This matrix is not invertible.")
            else:
                print("\nInverse found successfully!")
                
            # Ask if user wants to save the results
            save = input("\nDo you want to save the results? (y/n): ").lower().strip()
            if save == 'y':
                output_num = 1
                while os.path.exists(os.path.join(ensure_output_directory(), f'output{output_num}.txt')):
                    output_num += 1
                save_matrix_output(output_num, matrix, inverse)

if __name__ == "__main__":
    main()