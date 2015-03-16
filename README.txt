README.txt

The following program is a quick way to visualize the Traveling Salesman
problem and gives some real-word context and possible uses cases to the 
solutions to this problem. The one use case that this program explores in 
particular is planning vacation destinations. Given a starting (home) point and
a set if desired destinations to visit, what is the optimal flight path 
(using great-circle distance) as to visit each of these locations while 
minimizing distance traveled?

Client Interface:

Modify the 'Cities.txt' file in the containing folder to generate the list
of waypoints with new lines delimiting each location. The first location in
this file will used as the starting and ending point.

run(exact, blueearth)
Parameters:
'exact' : Whether the traveling salesman algorithm used provides an exact
solution. If used, it will be slower than using the algorithm that
generates an approximate solution.
'blueearth' : Whether the background image used in the plot uses the NASA
"Blue Earth" satellite image.

Using (Python Libraries):
Matplotlib
Basemap
Geopy
Numpy
Itertools

POSSIBLE TO DO:
1) Implement Held-Karp Algorithm. Provides an exact solution in O(2^n * n^2),
   compared to the naive approach (O(n!)).
2) Integrate with some flight-data API to provides solution based on lowest 
   cost, rather than shortest distance.
3) Integrate with Google Maps API to to to provide solution based on car travel,
   rather than air travel.
4) Optimize the flight data to use flight time rather than distance, which, 
   as a metric, may miss out on other factors.


