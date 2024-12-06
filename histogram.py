import matplotlib.pyplot as plt

def get_grouped_data():
    print("Enter the grouped data (class intervals and frequencies):")
    intervals = []
    frequencies = []

    # Accept intervals
    print("Enter class intervals (e.g., 0-5, 5-10, etc.). Type 'done' when finished:")
    while True:
        interval = input("Class interval: ").strip()
        if interval.lower() == 'done':
            break
        try:
            lower, upper = map(float, interval.split('-'))
            intervals.append((lower, upper))
        except ValueError:
            print("Invalid format. Use 'lower-upper', e.g., 0-5.")

    # Accept frequencies
    print("Now, enter the frequencies for each interval in order:")
    for i, (lower, upper) in enumerate(intervals, 1):
        while True:
            try:
                freq = float(input(f"Frequency for {lower}-{upper}: "))
                frequencies.append(freq)
                break
            except ValueError:
                print("Please enter a numeric value for frequency.")

    return intervals, frequencies

def plot_histogram(intervals, frequencies):
    # Prepare bins and weights for matplotlib
    bins = [interval[0] for interval in intervals] + [intervals[-1][1]]
    plt.hist(
        bins[:-1],
        bins=bins,
        weights=frequencies,
        edgecolor='black'
    )
    # Add labels and title
    plt.xlabel("Class Intervals")
    plt.ylabel("Frequency")
    plt.title("Histogram for Grouped Data")
    plt.show()

# Main program
if __name__ == "__main__":
    intervals, frequencies = get_grouped_data()
    plot_histogram(intervals, frequencies)
