from manim import *


class Scene1(Scene):
    def construct(self):
        theorem = Tex(r'$\sin$', r'$^{2}$', r"$\theta$", '+', r'$\cos$', r'$^{2}$', r"$\theta$", '=1').scale(2)

        # Part 1:
        self.play(Write(theorem), run_time=1)
        self.wait()

        # Part 2:
        highlightsin = Indicate(mobject=theorem[0],color=BLUE)
        self.play(highlightsin, run_time=1)
        self.wait(0.1)
        highlightcos = Indicate(mobject=theorem[4],color=BLUE)
        self.play(highlightcos, run_time=1)
        self.wait(0.2)

        # Part 3:
        highlighttheta1 = Indicate(mobject=theorem[2])
        highlighttheta2 = Indicate(mobject=theorem[6])
        self.play(highlighttheta1, highlighttheta2, run_time=1)
        self.wait()
        self.play(FadeOut(theorem))
        self.wait()


class Scene2(Scene):
    def construct(self):
        e = ValueTracker(0.01)

        def param_get_vertical_line_to_graph(axes, x, function1, function2, width, color):
            result = VGroup()
            line = DashedLine(
                start=axes.c2p(function1.underlying_function(x), 0),
                end=axes.c2p(function1.underlying_function(x), function2.underlying_function(x)),
                stroke_width=width,
                stroke_color=color,
            )
            dot = Dot().set_color(color).move_to(
                axes.c2p(function1.underlying_function(x), function2.underlying_function(x)))
            result.add(line, dot)
            return result

        def get_horizontal_line_to_graph(axes, function, x, width, color):
            line = DashedLine(
                start=axes.c2p(0, 0),
                end=axes.c2p(function.underlying_function(x), 0),
                stroke_width=width,
                stroke_color=color,
            )
            return line

        def param_get_diagonal_line_to_graph(axes, x, function1, function2, width, color):
            line = Line(
                start=axes.c2p(0, 0),
                end=axes.c2p(function1.underlying_function(x), function2.underlying_function(x)),
                stroke_width=width,
                stroke_color=color,
            )
            return line

        def get_angle_to_line(line1, line2, radius):
            angle = Angle(line1, line2, radius=radius)
            return angle

        axes = Axes(x_range=[-2, 2, 2], y_range=[-2, 2, 2], x_length=4, y_length=4,
                    axis_config={"include_tip": False, "numbers_to_exclude": [0]})
        circle = Circle(radius=2, color=BLUE)

        circle_opposite = axes.plot(lambda x: 2 * np.sin(x), x_range=[0, 2 * np.pi], color=BLUE)
        circle_adjacent = axes.plot(lambda x: 2 * np.cos(x), x_range=[0, 2 * np.pi], color=BLUE)

        moving_v_line = always_redraw(
            lambda: param_get_vertical_line_to_graph(
                axes=axes, x=e.get_value(),
                function1=circle_adjacent,
                function2=circle_opposite,
                width=4,
                color=YELLOW
            )
        )

        moving_h_line = always_redraw(
            lambda: get_horizontal_line_to_graph(
                axes=axes,
                function=circle_adjacent,
                x=e.get_value(), 
                width=4,
                color=YELLOW
            )
        )

        moving_d_line = always_redraw(
            lambda: param_get_diagonal_line_to_graph(
                axes=axes, x=e.get_value(),
                function1=circle_adjacent,
                function2=circle_opposite,
                width=4,
                color=BLUE
            )
        )

        moving_angle = always_redraw(
            lambda: get_angle_to_line(Line(start=axes.c2p(0, 0), end=axes.c2p(1, 0)), moving_d_line,
                                      radius=0.2)
        )

        moving_value = always_redraw(
            lambda: Tex(r"$\theta$").shift(
                0.5 * np.cos(0.5 * e.get_value()) * RIGHT + 0.5 * np.sin(0.5 * e.get_value()) * UP)
        )
        # Part 1:
        self.play(LaggedStart(
            Write(axes), Create(circle), run_time=3, lag_ratio=0.5)
        )
        self.wait()

        # Part 2:
        self.add(moving_d_line, moving_angle, moving_value)
        self.play(e.animate.set_value(0.25 * PI), run_time=0.8, rate_func=linear)

        self.wait()

        # Part 3:
        self.add(moving_h_line, moving_v_line)
        vbrace = always_redraw(
            lambda: BraceBetweenPoints(axes.c2p(2 * np.cos(e.get_value()), 0),
                                       axes.c2p(2 * np.cos(e.get_value()), 2 * np.sin(e.get_value())))
        )
        vtextbrace = vbrace.get_tex('\\sin', '\\theta')
        self.play(Create(vbrace), FadeIn(vtextbrace))
        self.wait()
        # Part 4:
        hbrace = always_redraw(
            lambda: Brace(moving_h_line)
        )
        htextbrace = hbrace.get_tex('\\cos', '\\theta')
        self.play(Create(hbrace), FadeIn(htextbrace))
        self.wait()

        # Part 5:
        self.play(
            FadeOut(hbrace, vbrace, htextbrace, vtextbrace, moving_h_line, moving_v_line, moving_d_line, moving_value,
                    moving_angle))
        self.wait()
        e = ValueTracker(0.01)
        moving_value1 = always_redraw(
            lambda: Tex(r"$\theta=$").shift(
                0.5 * np.cos(0.5 * e.get_value()) * RIGHT + 0.5 * np.sin(0.5 * e.get_value()) * UP)
        )
        decimal = DecimalNumber(
            0,
            show_ellipsis=True,
            num_decimal_places=3,
            include_sign=False,
        )

        decimal.add_updater(lambda d: d.next_to(moving_value1))
        decimal.add_updater(lambda d: d.set_value(e.get_value()))

        self.add(moving_d_line, moving_angle, moving_value1, moving_v_line, moving_h_line, decimal)
        self.play(e.animate.set_value(2 * PI), run_time=5, rate_func=linear)
        self.wait()

        self.play(FadeOut(circle, axes, moving_h_line, moving_v_line, moving_d_line, moving_angle, decimal, moving_value1))
        self.wait()


class Scene3(Scene):
    def construct(self):
        # my_plane = NumberPlane(background_line_style={"stroke_color": TEAL, "stroke_width": 1, "stroke_opacity": 0.3})
        # self.play(DrawBorderThenFill(my_plane))

        def get_horizontal_line_to_graph(axes, function, x, width, color):
            result = VGroup()
            line = DashedLine(
                start=axes.c2p(0, function.underlying_function(x)),
                end=axes.c2p(x, function.underlying_function(x)),
                stroke_width=width,
                stroke_color=color,
            )
            dot = Dot().set_color(color).move_to(axes.c2p(x, function.underlying_function(x)))
            result.add(line, dot)
            return result

        def get_vertical_line_to_graph(axes, function, x, width, color):
            result = VGroup()
            line = DashedLine(
                start=axes.c2p(x, 0),
                end=axes.c2p(x, function.underlying_function(x)),
                stroke_width=width,
                stroke_color=color,
            )
            dot = Dot().set_color(color).move_to(axes.c2p(x, function.underlying_function(x)))
            result.add(line, dot)
            return result

        def param_get_horizontal_line_to_graph(axes, x, function1, function2, width, color):
            line = DashedLine(
                start=axes.c2p(0, function2.underlying_function(x)),
                end=axes.c2p(function1.underlying_function(x), function2.underlying_function(x)),
                stroke_width=width,
                stroke_color=color,
            )
            return line

        # the following definition was made purely for this example to deal with the technicality, the previous one
        # is the more general one.
        def param_get_horizontal_line_to_graph2(axes, x, function1, function2, width, color):
            line = DashedLine(
                start=axes.c2p(0, function2.underlying_function(x)),
                end=axes.c2p(function1.underlying_function(x) - PI, function2.underlying_function(x)),
                stroke_width=width,
                stroke_color=color,
            )
            return line

        def param_get_vertical_line_to_graph(axes, x, function1, function2, width, color):
            line = DashedLine(
                start=axes.c2p(function1.underlying_function(x), 0),
                end=axes.c2p(function1.underlying_function(x), function2.underlying_function(x)),
                stroke_width=width,
                stroke_color=color,
            )
            return line

        e = ValueTracker(0.01)

        axes1 = Axes(x_range=[0, 2 * np.pi, 1 * np.pi], y_range=[-2, 2, 2], x_length=2 * np.pi, y_length=4,
                     axis_config={"include_tip": False, "numbers_to_exclude": [0]}).shift(RIGHT * np.pi)
        axes2 = Axes(x_range=[-2, 2, 2], y_range=[-2, 2, 2], x_length=4, y_length=4,
                     axis_config={"include_tip": False, "numbers_to_exclude": [0]}).shift(LEFT * 1 * np.pi)
        axes3 = Axes(x_range=[0, 2 * np.pi, 1 * np.pi], y_range=[-2, 2, 2], x_length=2 * np.pi, y_length=4,
                     axis_config={"include_tip": False, "numbers_to_exclude": [0]}).shift(RIGHT * np.pi)
        
        graph1 = always_redraw(lambda: axes1.plot(lambda x: 2 * np.sin(x), x_range=[0, e.get_value()], color=BLUE))
        graph2 = always_redraw(lambda: ParametricFunction(lambda t: axes2.c2p(2 * np.cos(t), 2 * np.sin(t)),
                                                          t_range=[0, e.get_value()], color=BLUE))
        graph3 = axes1.plot(lambda x: 2 * np.sin(x), x_range=[0, 2 * np.pi], color=BLUE)
        graph4 = axes1.plot(lambda x: 2 * np.cos(x), x_range=[0, 2 * np.pi], color=BLUE)
        graph5 = always_redraw(lambda: axes1.plot(lambda x: 2 * np.cos(x), x_range=[0, e.get_value()], color=BLUE))

        dot1 = always_redraw(lambda: Dot(fill_color=YELLOW, fill_opacity=0.8).scale(1).move_to(graph1.get_end()))
        dot2 = always_redraw(lambda: Dot(fill_color=YELLOW, fill_opacity=0.8).scale(1).move_to(graph2.get_end()))
        dot3 = always_redraw(lambda: Dot(fill_color=YELLOW, fill_opacity=0.8).scale(1).move_to(graph5.get_end()))      

        circle = Circle(2, color=BLUE).shift(LEFT * np.pi)

        moving_h_line = always_redraw(
            lambda: get_horizontal_line_to_graph(
                axes=axes1, function=graph1, x=e.get_value(), width=1, color=RED
            )
        )

        moving_h_line3 = always_redraw(
            lambda: param_get_horizontal_line_to_graph2(
                axes=axes1, x=e.get_value(), function1=graph4, function2=graph3, width=1, color=RED
            )
        )

        moving_v_line = always_redraw(
            lambda: get_vertical_line_to_graph(
                axes=axes1, function=graph1, x=e.get_value(), width=4, color=YELLOW
            )
        )

        moving_v_line2 = always_redraw(
            lambda: param_get_vertical_line_to_graph(
                axes=axes2, x=e.get_value(), function1=graph4, function2=graph3, width=4, color=YELLOW
            )
        )

        moving_h_line2 = always_redraw(
            lambda: param_get_horizontal_line_to_graph(axes2, x=e.get_value(), function1=graph4, function2=graph3,
                                                       width=4, color=YELLOW)
        )

        moving_v_line3 = always_redraw(
            lambda: get_vertical_line_to_graph(axes3, function=graph4, x=e.get_value(), width=4, color=YELLOW)
        )

        self.play(LaggedStart(
            Write(axes2), Write(axes1),  run_time=3, lag_ratio=0.1)
        )
        self.add(graph1, graph2, moving_h_line, moving_h_line3, moving_v_line, moving_v_line2, dot1, dot2)
        self.play(e.animate.set_value(2 * PI), run_time=10, rate_func=linear)
        self.wait()
        self.play(FadeOut(axes2,graph1,axes1,graph2,moving_h_line, moving_h_line3, moving_v_line, moving_v_line2, dot1, dot2))
        self.wait()

        e = ValueTracker(0.01)

        self.play(LaggedStart(
            Write(axes2),Write(axes3), run_time=3, lag_ratio=0.1)
        )
        self.add(graph2,graph5, dot3, dot2, moving_h_line2, moving_v_line3)
        self.play(e.animate.set_value(2 * PI), run_time=10, rate_func=linear)
        self.wait()

        leaving_group = VGroup(graph2,axes2,axes3, graph5, dot3, dot2, moving_h_line2, moving_v_line3)
        self.play(FadeOut(leaving_group))
        self.wait()


class Scene4(Scene):
    def construct(self):
        line1 = Line(start=np.array([- 1., 0., 0.]), end=np.array([1., 0., 0.]))
        line2 = Line(start=np.array([1., 0., 0.]), end=np.array([1., 1., 0.]))
        line3 = Line(start=np.array([1., 1., 0.]), end=np.array([-1., 0., 0.]))
        rightangle = RightAngle(line1, line2, quadrant=(-1, 1), length=0.2)
        rtri = VGroup(line1, line2, line3, rightangle).scale(2)

        side_lengths = VGroup(
            Tex("b", color=RED).move_to(line1.get_center() + DOWN * 0.3),
            Tex("a", color=BLUE).move_to(line2.get_center() + RIGHT * 0.3),
            Tex("c", color=GREEN).move_to(line3.get_center() + UP * 0.3),
        )

        self.play(LaggedStart(
            Create(rtri), Write(side_lengths), run_time=3, lag_ratio=0.5)
        )
        self.wait()

        group1 = VGroup(rtri, rightangle, side_lengths)
        self.play(group1.animate.shift(UP * 1))
        pyth = Tex('$a$', '$^2$', '$+$', '$b$', '$^2$', '$=$', '$c$', '$^2$', ).shift(DOWN * 1)
        pyth.set_color_by_tex("b", color=RED)
        pyth.set_color_by_tex("a", color=BLUE)
        pyth.set_color_by_tex("c", color=GREEN)
        self.play(Write(pyth))
        self.wait()
        group2 = VGroup(rtri, rightangle, side_lengths, pyth)
        self.play(group2.animate.shift(RIGHT * 3))
        self.wait()

        e = ValueTracker(0.01)

        def param_get_vertical_line_to_graph(axes, x, function1, function2, width, color):
            result = VGroup()
            line = Line(
                start=axes.c2p(function1.underlying_function(x), 0),
                end=axes.c2p(function1.underlying_function(x), function2.underlying_function(x)),
                stroke_width=width,
                stroke_color=color,
            )
            dot = Dot().set_color(color).move_to(
                axes.c2p(function1.underlying_function(x), function2.underlying_function(x)))
            result.add(line, dot)
            return result

        def get_horizontal_line_to_graph(axes, function, x, width, color):
            line = Line(
                start=axes.c2p(0, 0),
                end=axes.c2p(function.underlying_function(x), 0),
                stroke_width=width,
                stroke_color=color,
            )
            return line

        def param_get_diagonal_line_to_graph(axes, x, function1, function2, width, color):
            line = Line(
                start=axes.c2p(0, 0),
                end=axes.c2p(function1.underlying_function(x), function2.underlying_function(x)),
                stroke_width=width,
                stroke_color=color,
            )
            return line

        def get_angle_to_line(line1, line2, radius):
            angle = Angle(line1, line2, radius=radius)
            return angle

        axes = Axes(x_range=[-2, 2, 2], y_range=[-2, 2, 2], x_length=4, y_length=4,
                    axis_config={"include_tip": False, "numbers_to_exclude": [0]})
        circle = Circle(radius=2, color=BLUE)

        circle_opposite = axes.plot(lambda x: 2 * np.sin(x), x_range=[0, 2 * np.pi], color=BLUE)
        circle_adjacent = axes.plot(lambda x: 2 * np.cos(x), x_range=[0, 2 * np.pi], color=BLUE)

        moving_v_line = always_redraw(
            lambda: param_get_vertical_line_to_graph(
                axes=axes, x=e.get_value(), function1=circle_adjacent, function2=circle_opposite, width=4, color=BLUE
            )
        )

        moving_h_line = always_redraw(
            lambda: get_horizontal_line_to_graph(
                axes=axes, 
                function=circle_adjacent, 
                x=e.get_value(), 
                width=4, 
                color=BLUE
            )
        )

        moving_d_line = always_redraw(
            lambda: param_get_diagonal_line_to_graph(
                axes=axes, x=e.get_value(), 
                function1=circle_adjacent, 
                function2=circle_opposite, 
                width=4, 
                color=BLUE
            )
        )

        moving_angle = always_redraw(
            lambda: get_angle_to_line(Line(start=axes.c2p(0, 0), end=axes.c2p(1, 0)), moving_d_line,
                                      radius=0.2)
        )

        moving_value = always_redraw(
            lambda: Tex(r"$\theta$").shift(
                0.5 * np.cos(0.5 * e.get_value()) * RIGHT + 0.5 * np.sin(0.5 * e.get_value()) * UP).shift(LEFT * 3)
        )

        axes.shift(LEFT * 3)
        circle.shift(LEFT * 3)
        moving_d_line.shift(LEFT * 3)
        moving_v_line.shift(LEFT * 3)
        moving_h_line.shift(LEFT * 3)

        # Part 1:
        self.play(LaggedStart(
            Write(axes), Create(circle), run_time=3, lag_ratio=0.5)
        )
        self.wait()

        # Part 2:
        self.add(moving_d_line, moving_angle, moving_value)
        self.play(e.animate.set_value(0.25 * PI), run_time=0.8, rate_func=linear)

        self.wait()

        # Part 3:
        self.add(moving_h_line, moving_v_line)
        vbrace = always_redraw(
            lambda: BraceBetweenPoints(axes.c2p(2 * np.cos(e.get_value()), 0),
                                       axes.c2p(2 * np.cos(e.get_value()), 2 * np.sin(e.get_value())))
        )
        vtextbrace = vbrace.get_tex('\\sin', '\\theta')
        self.play(Create(vbrace), FadeIn(vtextbrace))
        self.wait()
        # Part 4:
        hbrace = always_redraw(
            lambda: Brace(moving_h_line)
        )
        htextbrace = hbrace.get_tex('\\cos', '\\theta')
        self.play(Create(hbrace), FadeIn(htextbrace))
        self.wait()

        dbrace = always_redraw(
            lambda: BraceBetweenPoints(axes.c2p(0, 0),
                                       axes.c2p(2 * np.cos(e.get_value()), 2 * np.sin(e.get_value())),
                                       direction=np.array([-1., 1., 0.]))
        )
        dtextbrace = dbrace.get_tex('1').shift(RIGHT * 0.2)
        self.play(Create(dbrace), FadeIn(dtextbrace))
        self.wait()

        theorem = Tex(r'$(\sin\theta)$', r'$^{2}$', '+', r'$(\cos\theta)$', r'$^{2}$', '=1')
        #theorem.set_color_by_tex("\sin\\theta", color=BLUE)
        #theorem.set_color_by_tex("\cos\\theta", color=RED)
        #theorem.set_color_by_tex("1", color=GREEN)

        theorem.shift(RIGHT*3+DOWN*1)


        new_side_lengths  = VGroup(
            Tex('$\\cos\\theta$', color=RED).move_to(line1.get_center() + DOWN * 0.3),
            Tex('$\\sin\\theta$', color=BLUE).move_to(line2.get_center() + RIGHT * 0.6),
            Tex("1", color=GREEN).move_to(line3.get_center() + UP * 0.3),
        )


        self.play(ReplacementTransform(side_lengths, new_side_lengths),
        ReplacementTransform(vtextbrace, side_lengths[1]),
        ReplacementTransform(htextbrace, side_lengths[0]),
        ReplacementTransform(dtextbrace, side_lengths[2]))
        self.wait(0.01)
        self.play(FadeOut(side_lengths))
        self.wait()

        self.play(ReplacementTransform(pyth,theorem))
        self.wait()


class Scene(Scene):
    def construct(self):
        Scene1.construct(self)
        Scene2.construct(self)
        Scene3.construct(self)
        Scene4.construct(self)

