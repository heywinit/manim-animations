from manim import *

class MatrixInversionAndTransformation(Scene):
    def construct(self):
        # Step 1: Display Initial Matrix
        matrix = Matrix(
            [
                [2, 3],
                [1, 4]
            ]
        ).scale(0.8)

        matrix_label = Tex("Initial Matrix").next_to(matrix, UP)
        self.play(Write(matrix_label), Write(matrix))
        self.wait(1)

        # Step 2: Show the Inverse of a Matrix
        inverse_matrix_label = Tex("Inverse of a Matrix").next_to(matrix, DOWN)
        self.play(Write(inverse_matrix_label))

        inverse_matrix = Matrix(
            [
                [4, -3],
                [-1, 2]
            ]
        ).scale(0.8).next_to(inverse_matrix_label, DOWN)
        
        self.play(Write(inverse_matrix))
        self.wait(1)

        # Step 3: Apply Transformations on Matrix (show a new matrix)
        new_matrix_label = Tex("Transformed Matrix").next_to(inverse_matrix, DOWN)
        self.play(Write(new_matrix_label))

        new_matrix = Matrix(
            [
                [1, 2],
                [3, 4]
            ]
        ).scale(0.8).next_to(new_matrix_label, DOWN)

        self.play(Transform(matrix, new_matrix))
        self.wait(1)

        # Step 4: Explain the transformation (Scaling and Rotation)
        transform_label = Tex("Applying Transformation (Scaling and Rotation)").next_to(new_matrix, DOWN)
        self.play(Write(transform_label))
        self.wait(1)

        # Show how a scaling transformation works (scale matrix)
        scale_matrix = Matrix(
            [
                [2, 0],
                [0, 2]
            ]
        ).scale(0.8).next_to(transform_label, DOWN)

        self.play(Write(scale_matrix))
        self.wait(1)

        # Apply the scaling transformation (show scaled matrix)
        scaled_matrix = Matrix(
            [
                [2, 4],
                [6, 8]
            ]
        ).scale(0.8).next_to(scale_matrix, DOWN)

        self.play(Transform(new_matrix, scaled_matrix))
        self.wait(1)

        # Step 5: Apply rotation (rotation matrix)
        rotation_label = Tex("Applying Rotation").next_to(scaled_matrix, DOWN)
        self.play(Write(rotation_label))
        self.wait(1)

        rotation_matrix = Matrix(
            [
                [0, -1],
                [1, 0]
            ]
        ).scale(0.8).next_to(rotation_label, DOWN)

        self.play(Write(rotation_matrix))
        self.wait(1)

        # Apply the rotation transformation
        rotated_matrix = Matrix(
            [
                [-4, -3],
                [2, 1]
            ]
        ).scale(0.8).next_to(rotation_matrix, DOWN)

        self.play(Transform(new_matrix, rotated_matrix))
        self.wait(1)

        # Step 6: Show Inverse After Transformation
        inverse_after_transformation_label = Tex("Inverse After Transformation").next_to(rotated_matrix, DOWN)
        self.play(Write(inverse_after_transformation_label))

        inverse_after_transformation = Matrix(
            [
                [0.25, 0.375],
                [0.125, 0.5]
            ]
        ).scale(0.8).next_to(inverse_after_transformation_label, DOWN)

        self.play(Write(inverse_after_transformation))
        self.wait(2)

        # Step 7: Compare original inverse and transformed inverse
        comparison_label = Tex("Comparing Inverse and Transformed Inverse").next_to(inverse_after_transformation, DOWN)
        self.play(Write(comparison_label))

        original_inverse_label = Tex("Original Inverse").next_to(inverse_matrix, RIGHT)
        transformed_inverse_label = Tex("Transformed Inverse").next_to(inverse_after_transformation, RIGHT)

        self.play(Write(original_inverse_label), Write(transformed_inverse_label))
        self.wait(2)

        # Highlight the differences between the inverses
        self.play(
            inverse_matrix[0][0].animate.set_color(BLUE),
            inverse_after_transformation[0][0].animate.set_color(BLUE),
            inverse_matrix[0][1].animate.set_color(BLUE),
            inverse_after_transformation[0][1].animate.set_color(BLUE),
        )
        self.wait(2)
