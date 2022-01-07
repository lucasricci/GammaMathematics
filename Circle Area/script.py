from manim import *
import math
import numpy as np

class CircleArea(Scene):
    def construct(self):

        radius = 1.875
        v = ValueTracker(value=6)
        sectors = VGroup(*self.get_sectors(radius, v.get_value()))
        theta = TAU / 6

        messageGroup = VGroup(Tex(r"The circumference is equal to $2 \cdot \pi \cdot r$", color=BLUE, font_size=40),
                              Tex(r"We divide the circle in 4 sectors, for now!", color=BLUE, font_size=40),
                              Tex(r"Now, we align them in this way", color=BLUE, font_size=40)
                              ).shift(UP * 2.5)
        
        messageGroup2 = VGroup(Tex(r"If we continue subdiving in smaller pieces,", color=BLUE, font_size=40),
                               Tex(r"we will form a rectangle as you see will see.", color=BLUE, font_size=40)).arrange(DOWN).shift(UP * 3)
        
        message1 = Tex(r"\\Have you ever stoped to think")
        
        message2 = Tex(r"\\why $\pi \cdot r^2$ is the area of the circle?")
        
        messages = VGroup(message1, message2).arrange(DOWN)
        
        count = 0
        
        lines = VGroup()
        circle = Circle(radius=1.875, color=WHITE)
        rectangle = Rectangle(height=1.875, width=(1.875)*PI)
        arc = Arc(radius=1.875, angle = TAU, stroke_color=YELLOW)
        point = Dot(color=YELLOW)
        point.add_updater(lambda x: x.move_to(arc.get_end()))
        label = Tex("$2 \\pi r$", color=YELLOW).move_to(circle.get_right()*1.2).rotate(-TAU/4)

        self.play(Write(messages.move_to(ORIGIN)), run_time=5)

        def LineCreator(start=0,stop=360,step=90):
            for x in range(start, stop, step):
                p = circle.point_at_angle(x * DEGREES)
                line = Line(start=ORIGIN, end=p, color=YELLOW, stroke_width=circle.get_stroke_width())
                lines.add(line)

        LineCreator()

        self.play(Unwrite(messages))
        self.wait()
        self.play(GrowFromCenter(circle))
        self.wait()
        self.play(Write(messageGroup[0]), run_time = 1)
        self.play(FadeIn(point), Create(arc), run_time=4, rate_func=linear)

        self.wait()
        self.play(Write(label))
        self.wait()

        self.play(Unwrite(messageGroup[0]))
        self.play(Uncreate(point), GrowFromCenter(lines), Write(messageGroup[1]))

        # Create the name labels
        nameTexs = VGroup()
        for y in range(1, 5, 1):
            n = f'P{y}'
            texEl = Tex(n)
            if n == 'P1':
                texEl.move_to(UL*0.75)
            elif n == 'P2':
                texEl.move_to(UR*0.75)
            elif n in 'P3':
                texEl.move_to(DL*0.75)
            else:
                texEl.move_to(DR*0.75)
            nameTexs.add(texEl)

        self.play(Write(nameTexs), run_time=4)


        ans = AnnularSector(inner_radius=0, outer_radius=1.875, fill_opacity=.25, color=YELLOW)
        self.play(FadeIn(ans), run_time=3)

        while count < 3:
            self.play(ans.animate.rotate_about_origin(TAU/4))
            self.wait(1.125)
            count += 1

        self.play(FadeOut(ans))

        self.play(Uncreate(arc), Uncreate(lines), Unwrite(label), Uncreate(circle),
                  Unwrite(nameTexs), Unwrite(messageGroup[1]))

        self.wait()

        def update_sectors(mob, dt):
            new_sectors = VGroup(*self.get_sectors(radius, v.get_value()))
            new_sectors.move_to(ORIGIN)
            mob.become(new_sectors)
            return mob
        
        def update_right_brace(mob: Brace):
            pieces = math.floor(v.get_value())
            direction = math.cos(PI/pieces)*RIGHT + math.sin(PI/pieces)*UP
            if pieces%2 == 1:
                direction -= 2* math.sin(PI/pieces)*UP
            brace = Brace(sectors[-1], direction=direction)
            brace.match_style(mob)
            brace.add(brace.get_tex("r", buff=0.1))
            mob.become(brace)
            return mob
        
        def update_down_brace(mob: Brace):
            new_mob = Brace(sectors)
            new_mob.match_style(mob)
            new_mob.add(new_mob.get_tex("\\pi \\cdot r"))
            mob.become(new_mob)
            return mob

        sectors.add_updater(update_sectors)
        sectors.update()

        self.play(Create(sectors.move_to(ORIGIN)), Write(messageGroup[2]), run_time=2)

        self.wait()

        bracket1 = Brace(sectors)
        bracket2 = Brace(sectors[-1], direction = [np.cos(theta/2), np.sin(theta/2), 0])

        self.play(
            GrowFromCenter(bracket1),
            GrowFromCenter(bracket2)
        )

        bracket1.add_updater(update_down_brace)
        bracket2.add_updater(update_right_brace)

        bracket1.update()
        bracket2.update()

        self.play(Unwrite(messageGroup[2]), run_time=2)

        self.wait()

        self.play(Write(messageGroup2), run_time=2)

        self.play(v.animate.set_value(96), run_time=10, rate_func=linear)

        self.wait(1)

        self.play(
            ReplacementTransform(sectors, rectangle),
            run_time = 3
        )

        bracket1.suspend_updating()
        bracket2.suspend_updating()
        sectors.suspend_updating()

        self.wait(3)

        self.play(Uncreate(rectangle), Uncreate(bracket1), Uncreate(bracket2), Unwrite(messageGroup2))

        eq1 = Tex(r"$\pi \cdot r \cdot r$").move_to(ORIGIN).scale(2)
        eq2 = Tex(r"$\pi \cdot r^2$").move_to(ORIGIN).scale(2)

        self.wait()

        self.play(Write(eq1))

        tex4 = Tex("We know that we have a rectangle with base $\pi \cdot r$", color=BLUE, font_size=40)
        tex5 = Tex("and height $r$, so we multiplie these two", color=BLUE, font_size=40)
        texs = VGroup(tex4, tex5).arrange(DOWN).shift(UP * 3)

        self.play(Create(texs))

        self.play(ReplacementTransform(eq1, eq2))

        self.wait()

        self.play(FadeOut(eq2), FadeOut(texs), run_time=3)

        self.wait(1)

        finaltex = VGroup(Tex(r"\\Wherever there is number, there is beauty."), Tex(r"\\— Proclus, Greek philosopher")).arrange(DOWN)
        self.play(FadeIn(finaltex), run_time=4.5)

        self.wait(5)

    def get_sectors(self, radius, v):
        slices = int(v)
        theta = TAU/slices
        for d in range(slices):
            start_angle = (PI-theta)/2
            arc_center=RIGHT*radius*math.sin(theta/2)*d
            if d%2==1:
                start_angle += PI
                arc_center += UP*radius*math.cos(theta/2)
            sector = Sector(
                outer_radius=radius,
                angle=theta,
                start_angle=start_angle,
                stroke_width=0.5,
                stroke_opacity=1,
                fill_opacity=0,
                stroke_color=BLUE_A,
                arc_center=arc_center
            )
            yield sector