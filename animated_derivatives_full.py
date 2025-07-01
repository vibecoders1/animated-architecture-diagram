from manim import *

class DerivativeVisualization(Scene):
    def construct(self):
        # Initialize t_val at the class level
        self.t_val = 0

        rules = [
            (r"1. \quad \frac{d}{dx} e^x = e^x", lambda x: np.exp(x), "e^x", [-2, 2]),
            (r"2. \quad \frac{d}{dx} \ln x = \frac{1}{x}", lambda x: np.log(x), "ln(x)", [0.1, 4]),
            (r"3. \quad \frac{d}{dx} \sin x = \cos x", lambda x: np.sin(x), "sin(x)", [-PI, PI]),
            (r"4. \quad \frac{d}{dx} \tan x = \sec^2 x", lambda x: np.tan(x), "tan(x)", [-1.2, 1.2]),
            (r"5. \quad \frac{d}{dx} x^2 = 2x", lambda x: x**2, "x^2", [-2, 2]),
        ]

        for latex, func, label, x_range in rules:
            # Add title
            rule_text = MathTex(latex, font_size=50).to_edge(UP)
            self.play(Write(rule_text))

            # Axes setup
            axes = Axes(
                x_range=[x_range[0], x_range[1], 1],
                y_range=[-5, 10, 1],
                tips=False,
                axis_config={"include_numbers": True}
            ).scale(0.8)

            graph = axes.plot(func, color=BLUE)
            func_label = MathTex(label, font_size=36).next_to(axes, UP)

            self.play(Create(axes), Create(graph), FadeIn(func_label))
            self.wait(0.5)

            # Initialize t_val for this iteration
            self.t_val = x_range[0] + 0.3

            # Animate tangent sweeping through x-values
            dot = Dot().set_color(RED)
            dot.add_updater(lambda m: m.move_to(axes.c2p(self.t_val, func(self.t_val))))

            # Use tangent_line method correctly without dx parameter
            tangent_line = always_redraw(
                lambda: axes.get_secant_slope_group(
                    x=self.t_val,
                    graph=graph,
                    dx=0.01,
                    secant_line_color=YELLOW,
                    secant_line_length=4
                ).set_color(YELLOW)
            )

            self.add(dot, tangent_line)

            # Sweep animation
            for x in np.linspace(x_range[0] + 0.3, x_range[1] - 0.3, 25):
                self.t_val = x
                self.wait(0.03)

            self.remove(dot, tangent_line)
            self.wait(1)

            # Fade out before next rule
            self.play(
                FadeOut(axes),
                FadeOut(graph),
                FadeOut(func_label),
                FadeOut(rule_text)
            )
            self.clear()