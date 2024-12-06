import matplotlib.pyplot as plt
import numpy as np

# Define the slope (m) and y-intercept (c)
m = float(input("Enter the slope (m): "))
c = float(input("Enter the y-intercept (c): "))

# Generate x values (e.g., from -10 to 10)
x = np.linspace(-10, 10, 100)  # 100 evenly spaced points between -10 and 10

# Compute y values using the line equation y = mx + c
y = m * x + c

# Plot the line
plt.plot(x, y, label=f"y = {m}x + {c}", color="blue")

# Add labels and a title
plt.xlabel("x-axis")
plt.ylabel("y-axis")
plt.title(f"Graph of y = {m}x + {c}")

# Add grid and legend
plt.axhline(0, color="black", linewidth=0.5, linestyle="--")  # x-axis
plt.axvline(0, color="black", linewidth=0.5, linestyle="--")  # y-axis
plt.grid(color="gray", linestyle="--", linewidth=0.5)
plt.legend()

# Show the plot
plt.show()
