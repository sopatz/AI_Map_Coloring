import csv
import random

def load_county_data(filepath="county_adjacency2025.txt"):
    county_borders = []
    states = set()
    with open(filepath, newline='', encoding='utf-8') as f:
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

    return county_borders, states


def color_state_counties(state, county_borders, user_colors):
    # Create subset of county border list where both the counties are in the user's desired state
    state_county_borders = [
        row for row in county_borders
        if row["County State"] == state and row["Neighbor State"] == state
    ]
    #print(f"Number of county borders in {state}:", len(state_county_borders))
    #print(state_county_borders[:5])   # preview

    colors = user_colors


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


    # Create dictionary where keys are the county IDs and the values are the color set
    county_colors = {countyID: set(colors) for countyID in counties_in_state}


    # Count how many borders (neighbors) each county has
    border_counts = {}
    for row in state_county_borders:
        id = row["County GEOID"]

        # for every county ID in a border, add 1
        border_counts[id] = border_counts.get(id, 0) + 1 #if id does not exist in border_counts yet, give it default value of 0

    # Add counties with no borders to list with value of zero
    for id in counties_in_state:
        border_counts[id] = border_counts.get(id, 0)

    # Model county borders as graph-style adjacency list for easier usage
    adj_list = {county: set() for county in counties_in_state}

    for row in state_county_borders:
        county1 = row["County GEOID"]
        county2 = row["Neighbor GEOID"]
        adj_list[county1].add(county2)
        adj_list[county2].add(county1)
    #print(adj_list)


    # Keep track of final assigned colors
    final_colors = {}

    # Check if assigning a color to a county is valid given the county's neighbors
    def is_valid_color(county, color):
        # Loop over every neighbor of the input county
        for neighbor in adj_list[county]:
            # Check if neighboring county has been assigned the color we are testing
            if final_colors.get(neighbor) == color:
                return False
        return True

    # Choose the next county to color using Most Restrained Variable, then Most Restraining Variable
    def select_next_county():
        # Creates list of tuples containing: county, number of color options, and border count
        uncolored = [
            (county, len(county_colors[county]), border_counts[county])
            for county in counties_in_state if county not in final_colors
        ]
        # Signal to recursion that every county is colored (uncolored is empty)
        if not uncolored:
            return None  #signal that all counties are colored
        # Sort by number of options (ascending), then number of borders (descending)
        uncolored.sort(key=lambda x: (x[1], -x[2], x[0]))
        # Return first county in sorted uncolored county list, as this is the one we now choose to color
        return uncolored[0][0]

    # Recursive function that performs map coloring with backtracking
    # Returns True if all counties were successfully colored
    # Returns False if current county color assignment doesn't meet constraints --> backtrack to last assignment
    def color_counties():
        # Base case: all counties have been colored
        if len(final_colors) == len(counties_in_state):
            return True

        # Select county to try coloring using the heuristic outlined in "select_next_county()" function
        county = select_next_county()
        # Check if county == None
        if not county:
            return True  # no uncolored counties left

        # Iterate through available colors for the selected county (in random order)
        for color in random.sample(list(county_colors[county]), len(county_colors[county])):
            # Confirm color is conflict-free with currently assigned neighbors
            if is_valid_color(county, color):
                final_colors[county] = color # assign color to selected county


                # Temporarily reduce neighbor color options for pruning:

                # dict to hold the neighbors which have had the chosen color removed, so it can be restored on backtrack
                removed = {} 

                # Loop through all of the current county's neighbors
                for neighbor in adj_list[county]:
                    # Check if neighbor is uncolored and the chosen color is in their available set
                    if neighbor not in final_colors and color in county_colors[neighbor]:
                        # Remove chosen color from neighbor's available set of colors
                        county_colors[neighbor].remove(color)

                        # Record the removal in "removed" so that it can be restored on backtrack
                        removed[neighbor] = color

                # Recursive call
                if color_counties():
                    return True  # stop iteration if full solution was found

                # If recursive call fails:

                # Undo assignment
                del final_colors[county]
                # Restore neighbors' color options that got removed
                for neighbor in removed:
                    county_colors[neighbor].add(color)

        # No color worked --> backtrack to undo last assignment and try alternatives
        return False


    print("\nColoring counties...")
    success = color_counties()  # Call backtracking county-coloring function

    return final_colors, success
