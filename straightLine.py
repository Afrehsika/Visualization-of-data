import matplotlib.pyplot as plt
import numpy as np

def plot_multiple_lines():
    n = int(input("How many lines would you like to plot? "))

    # Loop to get the slope and y-intercept for each line
    for i in range(1, n + 1):
        print(f"Enter details for Line {i}:")
        m = float(input(f"  Slope (m) of Line {i}: "))
        c = float(input(f"  Y-intercept (c) of Line {i}: "))

        # Generate x values
        x = np.linspace(-10, 10, 100)  # Generate 100 points between -10 and 10

        # Compute y values for this line
        y = m * x + c

        # Plot the line
        plt.plot(x, y, label=f"y = {m}x + {c}")

    # Add labels and title
    plt.xlabel("x-axis")
    plt.ylabel("y-axis")
    plt.title("Graph of Multiple Lines y = mx + c")

    # Add grid, legend, and axes
    plt.axhline(0, color="black", linewidth=0.5, linestyle="--")  # x-axis
    plt.axvline(0, color="black", linewidth=0.5, linestyle="--")  # y-axis
    plt.grid(color="gray", linestyle="--", linewidth=0.5)
    plt.legend()

    # Show the plot
    plt.show()

# Main Program
if __name__ == "__main__":
    plot_multiple_lines()
