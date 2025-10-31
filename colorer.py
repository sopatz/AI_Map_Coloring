import csv

county_borders = []
states = set()
with open("county_adjacency2025.txt", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter="|")
    for row in reader:
        # Extract state abbreviations for easy state comparisons
        county_state = row["County Name"].split(", ")[-1] # [-1] = last element
        neighbor_state = row["Neighbor Name"].split(", ")[-1]

        # Save state abbv to new row
        row["County State"] = county_state
        row["Neighbor State"] = neighbor_state

        # Strip ", XX" from the county names, since they're separate now
        row["County Name"] = row["County Name"].split(", ")[0]
        row["Neighbor Name"] = row["Neighbor Name"].split(", ")[0]

        county_borders.append(row)

        # track unique states
        states.add(county_state)

# print(county_borders[0]) # list of dictionaries
# print(type(county_borders))
# print(type(county_borders[0]))
# print(states)
# print(len(states))

state = input("What state would you like to color? ").strip().upper() #wont be case-sensitive
while (state not in states):
    print(f"{state} is NOT a valid state abbreviation in the dataset.\n")
    state = input("What state would you like to color? ").strip().upper()

print(f"{state} is a valid state to color")

# Create subset of county border list where both the counties are in the user's desired state
subset = [
    row for row in county_borders
    if row["County State"] == state and row["Neighbor State"] == state
]

print(f"Number of county borders in {state}:", len(subset))
print(subset[:5])   # preview

color_number = int(input("How many colors would you like to use? (4-5) "))
while (color_number != 4 and color_number != 5):
    print("Please select either '4' or '5'.")
    color_number = input("How many colors would you like to use? (4-5) ")

colors = set(range(color_number)) # just using numbers for each color for now
print(colors)
