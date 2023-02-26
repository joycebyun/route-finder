# route-finder

Given a maximum run distance and a starting location, `route-finder` generates a running route that aims to maximize the number of new locations visited.

## Description

`route-finder` uses map data from [OpenStreetMap](https://www.openstreetmap.org) (OSM), which is retrieved and analyzed using the Python package [`osmnx`](https://github.com/gboeing/osmnx/). 
Using `osmnx`, the map data is represented as a graph data structure, consisting of nodes (points on the map) that are connected by edges (roads, streets, paths, etc).

Given a maximum run distance and a starting location, `route-finder` generates a running route that aims to maximize the number of new nodes visited. The generated route starts and ends at the same location, and its total distance is less than the input maximum distance.

(In graph terminology, `route-finder` works on a weighted undirected graph, and generates a closed walk that aims to maximizes the number of new nodes visited, while keeping the total weight less than the input maximum.)

I don't know of an existing algorithm for generating a route under these constraints, so I created an [algorithm](#algorithm) described below. 
*It does **not** guarantee that the generated route visits the largest possible number of new nodes!* 
But it should give a reasonably good answer.

## Algorithm

:construction_worker: *Under construction* :construction:

## License

This project is licensed under the terms of the MIT license.
