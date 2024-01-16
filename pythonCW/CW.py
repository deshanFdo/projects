from graphics import GraphWin, Point, Text, Rectangle, GraphicsError

outcomes_list = []
outcome_counts = {"Progress": 0, "Progress (module trailer)": 0, "Do not progress – module retriever": 0, "Exclude": 0}

# Define the possible outcomes using a dictionary
outcomes_dict = {
    (120, 0, 0): "Progress",
    (100, 20, 0): "Progress (module trailer)",
    (100, 0, 20): "Progress (module trailer)",
    (80, 40, 0): "Do not progress – module retriever",
    (80, 20, 20): "Do not progress – module retriever",
    (80, 0, 40): "Do not progress – module retriever",
    (60, 60, 0): "Do not progress – module retriever",
    (60, 40, 20): "Do not progress – module retriever",
    (60, 20, 40): "Do not progress – module retriever",
    (60, 0, 60): "Do not progress – module retriever",
    (40, 80, 0): "Do not progress – module retriever",
    (40, 60, 20): "Do not progress – module retriever",
    (40, 40, 40): "Do not progress – module retriever",
    (40, 20, 60): "Do not progress – module retriever",
    (40, 0, 80): "Exclude",
    (20, 100, 0): "Do not progress – module retriever",
    (20, 80, 20): "Do not progress – module retriever",
    (20, 60, 40): "Do not progress – module retriever",
    (20, 40, 60): "Do not progress – module retriever",
    (20, 20, 80): "Exclude",
    (20, 0, 100): "Exclude",
    (0, 120, 0): "Do not progress – module retriever",
    (0, 100, 20): "Do not progress – module retriever",
    (0, 80, 40): "Do not progress – module retriever",
    (0, 60, 60): "Do not progress – module retriever",
    (0, 40, 80): "Exclude",
    (0, 20, 100): "Exclude",
    (0, 0, 120): "Exclude",
}

def user_input():
    try:
        pass_credit = int(input("Please enter your credits at pass: "))
        defer_credit = int(input("Please enter your credits at defer: "))
        fail_credit = int(input("Please enter your credits at fail: "))
        return pass_credit, defer_credit, fail_credit
    except ValueError:
        print("Integer required")
        return user_input()

def validate_credits(pass_credit, defer_credit, fail_credit):
    if pass_credit not in [0, 20, 40, 60, 80, 100, 120] or defer_credit not in [0, 20, 40, 60, 80, 100, 120] or fail_credit not in [0, 20, 40, 60, 80, 100, 120]:
        print("Out of range")
        return False
    if pass_credit + defer_credit + fail_credit != 120:
        print("Total incorrect")
        return False
    return True

def predict_progression(pass_credit, defer_credit, fail_credit):
    key = (pass_credit, defer_credit, fail_credit)
    if key in outcomes_dict:
        return outcomes_dict[key]
    else:
        return "Outcome not found"

while True:
    pass_credit, defer_credit, fail_credit = user_input()
    if not validate_credits(pass_credit, defer_credit, fail_credit):
        continue
    outcome = predict_progression(pass_credit, defer_credit, fail_credit)
    outcomes_list.append((pass_credit, defer_credit, fail_credit, outcome))  # Store input data and outcome

    # Update outcome counts
    if outcome == "Progress":
        outcome_counts["Progress"] += 1
    elif outcome == "Progress (module trailer)":
        outcome_counts["Progress (module trailer)"] += 1
    elif outcome == "Do not progress – module retriever":
        outcome_counts["Do not progress – module retriever"] += 1
    elif outcome == "Exclude":
        outcome_counts["Exclude"] += 1

    print(outcome)

    while True:
        final_input = input("Would you like to enter another set of data? Enter 'y' for yes or 'q' to quit: ")
        if final_input.lower() == 'y':
            break
        elif final_input.lower() == 'q':
            break
        else:
            print("Invalid input. Please enter 'y' for yes or 'q' to quit.")

    if final_input.lower() == 'q':
        break

# Display histogram using graphics.py
win = GraphWin("Histogram", 900, 700)
win.setBackground("white")

# Constants for the histogram display
bar_width = 70
bar_gap = 10
max_height = max(1, max(outcome_counts.values()))

# Color mapping for different outcomes
color_map = {
    "Progress": ("#aef8a1", "Progress"),
    "Progress (module trailer)": ("#a0c689", "Trailer"),
    "Do not progress – module retriever": ("#a7bc77", "Retriever"),
    "Exclude": ("#d2b6b5", "Exclude"),
}

def draw_histogram(win, outcome_counts):
    for i, (outcome, count) in enumerate(outcome_counts.items()):
        x1 = 100 + i * (bar_width + bar_gap)
        y1 = 400 - (count / max_height) * 10  # Adjusted scaling factor
        x2 = x1 + bar_width
        y2 = 400  # Set the y2 value to the desired height

        # Display the value above each bar
        Text(Point(x1 + bar_width / 2, y1 - 10), str(count)).draw(win)

        # Display the outcome name under each bar
        outcome_name = Text(Point(x1 + bar_width / 2, y2 + 20), color_map[outcome][1])
        outcome_name.setSize(8)
        outcome_name.draw(win)

        # Draw the histogram bars with different colors
        bar = Rectangle(Point(x1, y1), Point(x2, y2))
        bar.setFill(color_map[outcome][0])
        bar.draw(win)

def draw_title(win, title_text, sub_title_text):
    title = Text(Point(150, 50), title_text)
    title.setSize(20)
    title.setStyle("bold")
    title.setTextColor("#7b8796")
    title.draw(win)

    titleSub = Text(Point(450, 500), sub_title_text)
    titleSub.setSize(20)
    titleSub.setStyle("bold")
    titleSub.setTextColor("#7b8796")
    titleSub.draw(win)

draw_histogram(win, outcome_counts)
draw_title(win, "HISTOGRAM Results", f"{sum(outcome_counts.values())} outcomes in total.")

# Print stored data in the specified format
print("Part 2:")
for data in outcomes_list:
    print(f"{data[3]} - {data[0]}, {data[1]}, {data[2]}")

# Wait for a mouse click before closing the window
try:
    win.getMouse()
except GraphicsError:
    pass
win.close()

# Open a file in write mode
with open("outcomes_details.txt", "w") as file:
    # Write header
    file.write("Outcome - Pass Credits, Defer Credits, Fail Credits\n")
    
    # Write stored data in the specified format
    for data in outcomes_list:
        file.write(f"{data[3]} - {data[0]}, {data[1]}, {data[2]}\n")

print("Details written to 'outcomes_details.txt'")

