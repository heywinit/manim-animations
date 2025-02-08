import numpy as np

def gauss_jordan_elimination(A, b=None):
    """
    Performs Gauss-Jordan elimination to solve a system of linear equations Ax = b.
    
    Parameters:
    - A (list of lists or np.ndarray): Coefficient matrix (n x n).
    - b (list or np.ndarray, optional): Right-hand side vector (n x 1). If None, the function will compute the inverse of A.

    Returns:
    - If b is provided: Solution vector x or a message indicating inconsistency.
    - If b is None: Inverse of matrix A if it exists.
    """
    
    A = np.array(A, dtype=float)  # Convert input to NumPy array for stability
    n = len(A)
    
    if b is not None:
        b = np.array(b, dtype=float).reshape(n, 1)  # Convert b to a column vector
        augmented_matrix = np.hstack([A, b])  # Create augmented matrix
    else:
        augmented_matrix = np.hstack([A, np.eye(n)])  # Augment with identity matrix to find inverse

    # Perform Gauss-Jordan elimination
    for i in range(n):
        # Pivoting: Find the maximum element in the current column for numerical stability
        max_row = np.argmax(np.abs(augmented_matrix[i:, i])) + i
        augmented_matrix[[i, max_row]] = augmented_matrix[[max_row, i]]  # Swap rows

        # Check if the matrix is singular (zero pivot means no unique solution or no inverse)
        if np.isclose(augmented_matrix[i, i], 0):
            if b is not None:
                return "No unique solution exists (dependent or inconsistent system)."
            else:
                return "Matrix is singular and non-invertible."

        # Normalize the pivot row (make leading coefficient 1)
        augmented_matrix[i] = augmented_matrix[i] / augmented_matrix[i, i]

        # Eliminate other entries in the current column
        for j in range(n):
            if i != j:
                augmented_matrix[j] -= augmented_matrix[j, i] * augmented_matrix[i]

    # Extract results
    if b is not None:
        return augmented_matrix[:, -1]  # Return solution vector
    else:
        return augmented_matrix[:, n:]  # Return inverse matrix


# Example Usage
if __name__ == "__main__":
    # Example 1: Solving a system of equations
    A = [[0, -1, -5], 
         [3, 8, -2], 
         [10, -3, 4]]

    # b = [3, 3, 4]

    # solution = gauss_jordan_elimination(A, b)
    # print("Solution to Ax = b:", solution)

    # Example 2: Finding the inverse of a matrix
    A_inv = gauss_jordan_elimination(A)
    print("Inverse of A:\n", A_inv)
