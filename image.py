import turtle
import math

screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Color Spiral")

t = turtle.Turtle()
t.speed(0)
t.pensize(2)

colors = ["red", "orange", "yellow", "green", "cyan", "blue", "purple"]

for i in range(360):
    t.color(colors[i % len(colors)])

    angle = math.radians(i)
    radius = i * 2

    x = radius * math.cos(angle)
    y = radius * math.sin(angle)

    t.goto(x, y)
    t.forward(1)

turtle.done()