# Budget-Google-Maps
a* pathfinding on any city 

# Packages
- osmnx
- matplotlib
- scikit-learn

# How to create new graphs

import osmnx as ox

G_nyc = ox.graph_from_place("New York City, New York, USA", network_type="drive") # see all network types at https://osmnx.readthedocs.io/en/stable/user-reference.html#module-osmnx.graph

# Save to file
ox.save_graphml(G_nyc, "nyc_drive.graphml")

# How to use

you will be prompted to give an address for your destination and starting point. eg. Empire State Building, DCA, LAX, National Mall
if it throws and error saying that it cant geocache that address, either be more or less specific in your input (20 W 34th St., New York, NY 10001 -> empire state building)

# Example

Friendship Heights -> DCA

<img width="529" height="611" alt="image" src="https://github.com/user-attachments/assets/2230b8e5-3ddf-4deb-85f4-8a8251f0073d" />
<img width="373" height="513" alt="image" src="https://github.com/user-attachments/assets/69c5a8ec-94cf-435b-93ca-8acd34529d9f" />
