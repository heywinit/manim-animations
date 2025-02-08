from manim import *
import numpy as np

class GaussJordanElimination(Scene):
    def construct(self):
        # Configure the scene
        self.camera.background_color = "#1f1f1f"
        
        # Title and introduction
        title = Text("Understanding Gauss-Jordan Elimination", font_size=40)
        title.to_edge(UP, buff=0.5)
        subtitle = Text("Geometric Interpretation of Row Operations", font_size=28, color=BLUE_C)
        subtitle.next_to(title, DOWN, buff=0.3)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.wait()
        
        # Clear introduction
        self.play(
            title.animate.scale(0.8).to_corner(UP + LEFT),
            FadeOut(subtitle)
        )

        # Create coordinate system
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=8,
            y_length=8,
            axis_config={
                "include_tip": True,
                "numbers_to_include": list(range(-4, 5, 1))
            },
        )
        
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
        
        # Add grid for better visualization
        grid = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=8,
            y_length=8,
            background_line_style={
                "stroke_opacity": 0.2
            }
        )
        
        # Group coordinate system elements
        coord_system = VGroup(grid, axes, axes_labels)
        coord_system.shift(RIGHT * 2 + DOWN * 0.5)
        
        # Initial matrix and explanation
        matrix = np.array([[2, 1],
                         [1, 2]])
        
        initial_system = MathTex(
            r"\begin{cases} 2x + y = 0 \\ x + 2y = 0 \end{cases}"
        ).scale(0.8)
        
        matrix_tex = MathTex(
            r"A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}"
        ).scale(0.8)
        
        # Position equations on the left
        eq_group = VGroup(matrix_tex, initial_system).arrange(DOWN, buff=0.5)
        eq_group.to_edge(LEFT, buff=1)
        
        # Add explanation text
        explanation = Text(
            "This system represents two lines in the plane.\nEach row of the matrix defines a vector.",
            font_size=24,
            line_spacing=1.5
        ).next_to(eq_group, DOWN, buff=0.5)
        
        # Show coordinate system and equations
        self.play(Create(coord_system, run_time=2))
        self.play(
            Write(matrix_tex),
            Write(initial_system)
        )
        self.play(Write(explanation))
        self.wait()

        # Draw initial vectors with proper scaling
        def get_vector(start, end, color):
            return Arrow(
                start=axes.c2p(*start),
                end=axes.c2p(*end),
                buff=0,
                color=color,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.15
            )

        vector1 = get_vector([0, 0], [2, 1], BLUE)
        vector2 = get_vector([0, 0], [1, 2], RED)
        
        v1_label = MathTex(r"\vec{v_1} = \begin{bmatrix} 2 \\ 1 \end{bmatrix}", color=BLUE).scale(0.7)
        v2_label = MathTex(r"\vec{v_2} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}", color=RED).scale(0.7)
        
        v1_label.next_to(vector1.get_end(), RIGHT)
        v2_label.next_to(vector2.get_end(), RIGHT)
        
        # Show vectors
        self.play(
            GrowArrow(vector1),
            GrowArrow(vector2)
        )
        self.play(
            Write(v1_label),
            Write(v2_label)
        )
        self.wait()

        # Step 1: Explain first row operation
        step1_text = Text(
            "Step 1: Multiply first row by 2 and subtract second row",
            font_size=24
        ).next_to(title, DOWN, buff=0.5)
        
        step1_math = MathTex(
            r"2\vec{v_1} - \vec{v_2} = \begin{bmatrix} 3 \\ 0 \end{bmatrix}"
        ).scale(0.8).next_to(step1_text, DOWN, buff=0.3)
        
        self.play(
            Write(step1_text),
            Write(step1_math)
        )
        
        # Show intermediate vector for 2v1
        vector1_scaled = get_vector([0, 0], [4, 2], YELLOW)
        self.play(GrowArrow(vector1_scaled))
        
        # Add explanation for this step
        step1_explanation = Text(
            "First, we scale v₁ by 2 (yellow vector)\nThen subtract v₂ to eliminate y-component",
            font_size=24,
            line_spacing=1.5
        ).next_to(step1_math, DOWN, buff=0.3)
        
        self.play(Write(step1_explanation))
        self.wait()

        # Show the subtraction result
        vector1_new = get_vector([0, 0], [3, 0], BLUE)
        
        self.play(
            Transform(vector1, vector1_new),
            FadeOut(vector1_scaled),
            v1_label.animate.next_to(vector1_new.get_end(), RIGHT)
        )
        
        # Update matrix
        matrix_step1 = MathTex(
            r"A = \begin{bmatrix} 3 & 0 \\ 1 & 2 \end{bmatrix}"
        ).scale(0.8).move_to(matrix_tex)
        
        self.play(Transform(matrix_tex, matrix_step1))
        self.wait()

        # Step 2: Scale second row
        step2_text = Text(
            "Step 2: Scale second row by 1/2",
            font_size=24
        ).next_to(title, DOWN, buff=0.5)
        
        step2_math = MathTex(
            r"\frac{1}{2}\vec{v_2} = \begin{bmatrix} \frac{1}{2} \\ 1 \end{bmatrix}"
        ).scale(0.8).next_to(step2_text, DOWN, buff=0.3)
        
        self.play(
            ReplacementTransform(step1_text, step2_text),
            ReplacementTransform(step1_math, step2_math),
            FadeOut(step1_explanation)
        )
        
        # Show the scaling of vector2
        vector2_new = get_vector([0, 0], [0.5, 1], RED)
        
        self.play(
            Transform(vector2, vector2_new),
            v2_label.animate.next_to(vector2_new.get_end(), RIGHT)
        )
        
        # Final matrix
        matrix_final = MathTex(
            r"A = \begin{bmatrix} 3 & 0 \\ \frac{1}{2} & 1 \end{bmatrix}"
        ).scale(0.8).move_to(matrix_tex)
        
        self.play(Transform(matrix_tex, matrix_final))
        
        # Final explanation
        final_explanation = Text(
            "The matrix is now in row echelon form!\nNotice how the vectors are now more aligned with the axes.",
            font_size=24,
            line_spacing=1.5,
            color=GREEN
        ).next_to(step2_math, DOWN, buff=0.5)
        
        self.play(Write(final_explanation))
        self.wait(2)
