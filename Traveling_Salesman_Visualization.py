# Traveling Salesman Visualization
# Calvin Giroud, 2015

###############################################################################
# Packages

from mpl_toolkits.basemap import Basemap
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import matplotlib.pyplot as plt
import numpy as np
import itertools

###############################################################################
# Client Interface
# Modify the 'cities.txt' file in the containing folder to generate the list
# of waypoints with new lines delimiting each location. The first location in
# this file will used as the starting and ending point.

# run(exact, blueearth)
# Parameters:
# 'exact' : Whether the traveling salesman algorithm used provides an exact
# solution. If used, it will be slower than using the algorithm that
# generates an approximate solution.
# 'blueearth' : Whether the background image used in the plot uses the NASA
# "Blue Earth" satellite image.

###############################################################################
# Implementation

#Populate data
def populate_data():
    data = []
    totDist = 0
    geoloc = Nominatim()
    try: 
        f = open('Cities.txt','r')
        dataList = f.read().splitlines()
    except IOError: 
        print "Error: Make sure 'Cities.txt' is in the same directory as \
'Traveling_Salesman_Visualization.py' \n"
        raise
    for i in xrange(len(dataList)):
        coord = geoloc.geocode(dataList[i])
        data.append((coord.latitude,coord.longitude,dataList[i]))
    return data

#Traveling Salesman Optimization: Nearest Neighbor variant
def calc_tot_dist(cities):
    totDist = 0
    for i in xrange(1,len(cities)):
        start = (cities[i][0],cities[i][1])
        end = (cities[i-1][0],cities[i-1][1])
        totDist += great_circle(start,end).miles
    return totDist

def nn_tsp(cities):
    start = cities[0]
    tour = [start]
    unvisited = set(cities[1:])
    while (len(unvisited) != 0):
        C = find_nearest(tour[-1], unvisited)
        tour.append(C)
        unvisited.remove(C)
    tour += [start]
    return tour

def find_nearest(A, cities):
    minDist = 1000000
    minElem = None
    for elem in cities:
        start = (A[0],A[1])
        end = (elem[0],elem[1])
        curDist = great_circle(start,end).miles
        if curDist < minDist:
            minDist = curDist
            minElem = elem
    return minElem

def parse_reversed_segments(tour, i, j):
    A, B, C, D = tour[i-1], tour[i], tour[j-1], tour[j % len(tour)]
    if great_circle((A[0],A[1]),(B[0],B[1])).miles + \
       great_circle((C[0],C[1]),(D[0],D[1])).miles > \
       great_circle((A[0],A[1]),(C[0],C[1])).miles + \
       great_circle((B[0],B[1]),(D[0]),D[1]).miles:
       tour[i:j] = reversed(tour[i:j])

def alter_tour(tour):
    orig_dist = calc_tot_dist(tour)
    for (start, end) in all_segments(len(tour)):
        parse_reversed_segments(tour, start, end)
    if calc_tot_dist(tour) < orig_dist:
        alter_tour(tour)
    return tour

def all_segments(N):
    return [(start, start + length)
            for length in xrange(N, 1, -1)
            for start in xrange(N - length + 1)]

def nn_tsp_optimized(cities):
    return alter_tour(nn_tsp(cities))

# Traveling Salesman: All Tours variant
def all_tsp(cities):
    all_tours = list(itertools.permutations(cities[1:]))
    for i in xrange(len(all_tours)):
        all_tours[i] = (cities[0],) + all_tours[i] + (cities[0],)
    minDist = 100000
    bestTour = None
    for tour in all_tours:
        currDist = calc_tot_dist(tour)
        if currDist < minDist:
            minDist = currDist
            bestTour = tour
    return list(bestTour)

def solve_tsp(data, exact=True):
    if (exact): return all_tsp(data)
    else: return nn_tsp_optimized(data)

def get_map_bounds(data):
    llcrnrlon = 10000
    llcrnrlat = 10000
    urcrnrlon = -10000
    urcrnrlat = -10000
    for i in xrange(len(data)):
        currLon = data[i][1]
        currLat = data[i][0]
        if currLon < llcrnrlon: llcrnrlon = currLon
        if currLon > urcrnrlon: urcrnrlon = currLon
        if currLat < llcrnrlat: llcrnrlat = currLat
        if currLat > urcrnrlat: urcrnrlat = currLat
    return (llcrnrlon,llcrnrlat,urcrnrlon,urcrnrlat) 

#Plot Map
def draw_map(data,totDist,blueearth=False):
    m_bounds = get_map_bounds(data)
    m = Basemap(resolution='l',\
                llcrnrlon=max(m_bounds[0]-10,-180),\
                llcrnrlat=max(m_bounds[1]-10,-90),\
                urcrnrlon=min(m_bounds[2]+10,180),\
                urcrnrlat=min(m_bounds[3]+10,90),\
                projection='merc')
    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()
    m.bluemarble() if blueearth else m.fillcontinents()
    
    #Plot data
    for i in xrange(len(data)):
        x,y = m(data[i][1],data[i][0])
        typeColor = 'ro' if i == 0 or i == len(data)-1 else 'bo' 
        lat1, lon1 = data[i][0], data[i][1]
        lat2, lon2 = data[i-1][0], data[i-1][1]
        m.drawgreatcircle(lon1, lat1, lon2, lat2, lw=2, color='b')
        textColor = "w" if blueearth else "k"
        plt.text(x+40000,y-200000,data[i][2],weight="bold",color=textColor)
        m.plot(x,y,typeColor,markersize=10)
    plt.title("Starting from %s via %d waypoints | \
Total Distance: %d miles" % (data[0][2], len(data)-2, totDist))

    #Show Plot
    plt.show()

def run(exact, blueearth):
    data = populate_data()
    data = solve_tsp(data, exact)
    totDist = calc_tot_dist(data)
    draw_map(data,totDist,blueearth)

###############################################################################

run(True, True)