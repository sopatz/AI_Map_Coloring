import csv
import math

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
state_county_borders = [
    row for row in county_borders
    if row["County State"] == state and row["Neighbor State"] == state
]

print(f"Number of county borders in {state}:", len(state_county_borders))
print(state_county_borders[:5])   # preview

# Let user choose whether they want their map with 4 colors or 5
color_number = int(input("How many colors would you like to use? (4-5) "))
while (color_number != 4 and color_number != 5):
    print("Please select either '4' or '5'.")
    color_number = input("How many colors would you like to use? (4-5) ")

colors = set(range(color_number)) # just using numbers for each color for now
print(colors)


# Get all unique counties in the selected state
counties_in_state = {
    row["County GEOID"]
    for row in county_borders
    if row["County State"] == state
}.union({
    row["Neighbor GEOID"]
    for row in county_borders
    if row["Neighbor State"] == state
})

print(f"\nNumber of counties in {state}: {len(counties_in_state)}")
print(sorted(counties_in_state))


# Create dictionary where keys are the county IDs and the values are the color set
county_colors = {countyID: set(colors) for countyID in counties_in_state}
#print(county_colors)


# Count how many borders (neighbors) each county has
border_counts = {}

for row in state_county_borders:
    id = row["County GEOID"]

    # for every county ID in a border, add 1
    border_counts[id] = border_counts.get(id, 0) + 1 #if id does not exist in border_counts yet, give it default value of 0

# Add counties with no borders to list with value of zero
for id in counties_in_state:
    border_counts[id] = border_counts.get(id, 0)

# Sort by border count (descending)
ranked_counties = sorted(border_counts.items(), key=lambda x: x[1], reverse=True)

print("\nCounties ranked by number of borders:")
for county_id, count in ranked_counties:
    print(f"{county_id}: {count} borders")
