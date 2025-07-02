from manim import *

class CareerGrowthScene(MovingCameraScene):
    def construct(self):
        # Titles
        title_good = Text("Supportive IT Environment", font_size=28).to_edge(UP + LEFT)
        title_bad = Text("Unsupportive IT Environment", font_size=28).to_edge(UP + RIGHT)

        # Axes for both plots
        axes_good = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 120, 20],
            x_length=5,
            y_length=3,
            axis_config={"include_tip": True},
        ).to_edge(LEFT, buff=1.2)

        axes_bad = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 120, 20],
            x_length=5,
            y_length=3,
            axis_config={"include_tip": True},
        ).to_edge(RIGHT, buff=1.2)

        labels_good = axes_good.get_axis_labels(x_label="Time", y_label="Level")
        labels_bad = axes_bad.get_axis_labels(x_label="Time", y_label="Level")

        # Generate values manually (simplified model)
        t_vals = [x * 0.05 for x in range(180)]
        growth_good = [8*t for t in t_vals]
        motivation_good = [7*t for t in t_vals]
        growth_bad = [11*t - 0.8*t**2 for t in t_vals]
        motivation_bad = [5*t - 0.5*t**2 for t in t_vals]

        # Create plot lines
        graph_growth_good = axes_good.plot_line_graph(
            x_values=t_vals,
            y_values=growth_good,
            line_color=GREEN,
            add_vertex_dots=False
        )

        graph_motivation_good = axes_good.plot_line_graph(
            x_values=t_vals,
            y_values=motivation_good,
            line_color=BLUE,
            add_vertex_dots=False
        )

        graph_growth_bad = axes_bad.plot_line_graph(
            x_values=t_vals,
            y_values=growth_bad,
            line_color=RED,
            add_vertex_dots=False
        )

        graph_motivation_bad = axes_bad.plot_line_graph(
            x_values=t_vals,
            y_values=motivation_bad,
            line_color=ORANGE,
            add_vertex_dots=False
        )

        # Legends
        legend_good = VGroup(
            Dot(color=GREEN), Text("Growth", font_size=24),
            Dot(color=BLUE), Text("Motivation", font_size=24)
        ).arrange(RIGHT).next_to(axes_good, DOWN)

        legend_bad = VGroup(
            Dot(color=RED), Text("Growth", font_size=24),
            Dot(color=ORANGE), Text("Motivation", font_size=24)
        ).arrange(RIGHT).next_to(axes_bad, DOWN)

        # Animate
        self.play(Write(title_good), Write(title_bad))
        self.play(Create(axes_good), Create(labels_good))
        self.play(Create(axes_bad), Create(labels_bad))

        self.play(FadeIn(legend_good), FadeIn(legend_bad))
        self.play(
            Create(graph_growth_good),
            Create(graph_motivation_good),
            Create(graph_growth_bad),
            Create(graph_motivation_bad),
            run_time=10
        )

        
        self.wait(2)