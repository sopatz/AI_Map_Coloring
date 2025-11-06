import csv

points = []
with open("points.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        points.append((float(row["x"]), float(row["y"])))

# print(points)

x_values = [x for x,y in points]
y_values = [y for x,y in points]

x_bar = sum(x_values) / len(points)
y_bar = sum(y_values) / len(points)

x_variance = sum((x - x_bar) ** 2 for x in x_values) / (len(points) - 1)
# y_variance = sum((y - y_bar) ** 2 for y in y_values) / (len(points) - 1)

covariance = sum((point[0] - x_bar) * (point[1] - y_bar) for point in points) / (len(points) - 1)

std_x = x_variance ** 0.5
# std_y = y_variance ** 0.5

beta = covariance / (std_x ** 2)

alpha = y_bar - beta * x_bar

if (alpha >= 0):
    print(f"The equation of the linear regression line from the input data is: y = {beta}x + {alpha}")

if (alpha < 0):
    print(f"The equation of the linear regression line from the input data is: y = {beta}x - {abs(alpha)}")

new_iv = float(input("New independent variable value: "))
pred_dv = beta * new_iv + alpha
print(f"The predicted dependent variable value for x = {new_iv} is: y = {pred_dv}")
