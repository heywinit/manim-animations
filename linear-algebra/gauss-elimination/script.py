import numpy as np

def print_matrix(matrix, precision=3):
    """Print matrix with specified precision."""
    for row in matrix:
        print('[', end=' ')
        for elem in row:
            if abs(elem) < 1e-10:  # Handle near-zero values
                print(f"{0:8.{precision}f}", end=' ')
            else:
                print(f"{elem:8.{precision}f}", end=' ')
        print(']')
    print()

def gauss_jordan_inverse(matrix):
    """
    Find the inverse of a 3x3 matrix using Gauss-Jordan elimination.
    Returns None if matrix is not invertible.
    """
    n = len(matrix)
    # Create augmented matrix [A|I]
    augmented = np.zeros((n, 2*n))
    augmented[:n, :n] = matrix
    augmented[:n, n:] = np.eye(n)
    
    # Convert to float for division operations
    augmented = augmented.astype(float)
    
    # Gauss-Jordan elimination
    for i in range(n):
        # Find pivot
        pivot = augmented[i][i]
        if abs(pivot) < 1e-10:  # Check if matrix is singular
            # Look for non-zero pivot in rows below
            found_pivot = False
            for j in range(i + 1, n):
                if abs(augmented[j][i]) > 1e-10:
                    # Swap rows
                    augmented[[i, j]] = augmented[[j, i]]
                    pivot = augmented[i][i]
                    found_pivot = True
                    break
            if not found_pivot:
                return None  # Matrix is not invertible
        
        # Divide row by pivot
        augmented[i] = augmented[i] / pivot
        
        # Eliminate column
        for j in range(n):
            if i != j:
                factor = augmented[j][i]
                augmented[j] = augmented[j] - factor * augmented[i]
    
    # Extract inverse matrix
    inverse = augmented[:, n:]
    return inverse

def main():
    matrix1 = np.array([
        [0, -1, -5],
        [3, 8, -2],
        [10, -3, 4]
    ])
    
    # Test both matrices
    print("Matrix 1:")
    print_matrix(matrix1)
    print("Inverse of Matrix 1:")
    inverse1 = gauss_jordan_inverse(matrix1)
    if inverse1 is not None:
        print_matrix(inverse1)
        # Verify result
        print("Verification (should be identity matrix):")
        print_matrix(np.dot(matrix1, inverse1))
    else:
        print("Matrix is not invertible")
    

if __name__ == "__main__":
    main()