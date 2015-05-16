# Traveling Salesman Visualization
# Calvin Giroud, 2015

###############################################################################
# Packages

from mpl_toolkits.basemap import Basemap
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import matplotlib.pyplot as plt
import numpy as np
import sys
import itertools as it
from Graph_Interface import *

###############################################################################
# Client Interface
# Modify the 'cities.txt' file in the containing folder to generate the list
# of waypoints with new lines delimiting each location. The first location in
# this file will used as the starting and ending point.

###############################################################################
# Implementation

#Populate data
def populate_data():

    geoloc = Nominatim()

    #Read from file
    try:
        f = open('Cities.txt','r')
        cityList = f.read().splitlines()
    except IOError:
        IOErrMsg = "Make sure 'Cities.txt' is in the same directory as \
'Traveling_Salesman_Visualization.py.' \n"
        raise Exception(IOErrMsg)

    graphSize = len(cityList)
    graphData = graph_new(graphSize)

    locList = dict()
    for k in xrange(len(cityList)):
        cityName = cityList[k]
        locList[cityName] = geoloc.geocode(cityName)

        if locList[cityName] == None:
            errMsg = "'%s' is an invalid location name." % cityName
            raise Exception(errMsg)

    for i in xrange(graphSize):
        for j in xrange(i, graphSize):

            if (i == j): continue
            v1 = locList[cityList[i]]
            v2 = locList[cityList[j]]
            v1Loc = (v1.latitude, v1.longitude)
            v2Loc = (v2.latitude, v2.longitude)
            dist = round(great_circle(v1Loc, v2Loc).miles)

            add_edge(graphData, i, j, dist)

    return (cityList, graphData, locList)

#TSP Algorithm, using dynamic programming
def tsp_dynamic(graphData):
    m = len(graphData)

    A = {}
    A[frozenset([0])] = {}
    for n in xrange(1, m):
        A[(frozenset([0, n]), n)] = (graphData[0][n], [0, n])

    for i in xrange(2, m):
        B = {}
        S = [frozenset(C).union({0}) for C in it.combinations(range(1, m), i)]
        for s in S:
            for j in s:

                if (j == 0): continue

                minDist = sys.maxsize
                minPath = []
                for k in s:
                    if (k == 0 or k == j): continue
                    currDist = A[(s - {j}, k)][0] + graphData[k][j]
                    currPath = A[(s - {j}, k)][1] + [j]
                    if currDist < minDist:
                        minDist = currDist
                        minPath = currPath
                B[(s, j)] = (minDist, minPath)
        A = B

    minLen, minTour = (sys.maxsize, [])
    for l in A:
        currLen = A[l][0] + graphData[0][l[1]]
        currTour = A[l][1]
        if currLen < minLen:
            minLen = currLen
            minTour = currTour
    return (minTour + [0], minLen)

###############################################################################
#Graphing

def get_long(data, i):
    return data[i][2]

def get_lat(data, i):
    return data[i][1]

def get_loc(data, i):
    return data[i][0]

def get_map_bounds(data):
    llcrnrlon =  10000
    llcrnrlat =  10000
    urcrnrlon = -10000
    urcrnrlat = -10000
    for i in xrange(len(data)):
        currLon = get_long(data, i)
        currLat = get_lat(data, i)
        if currLon < llcrnrlon: llcrnrlon = currLon
        if currLon > urcrnrlon: urcrnrlon = currLon
        if currLat < llcrnrlat: llcrnrlat = currLat
        if currLat > urcrnrlat: urcrnrlat = currLat
    return (llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat)

#Plot Map
def draw_map(data,tourDist):
    m_bounds = get_map_bounds(data)
    m = Basemap(resolution = 'l',                         \
                llcrnrlon  = max(m_bounds[0] - 10, -180), \
                llcrnrlat  = max(m_bounds[1] - 10,  -90), \
                urcrnrlon  = min(m_bounds[2] + 10,  180), \
                urcrnrlat  = min(m_bounds[3] + 10,   90), \
                projection = 'merc')
    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()
    m.bluemarble()

    start, end = 0, len(data) - 1

    #Plot data
    for i in xrange(len(data)):
        x,y = m(get_long(data, i), get_lat(data, i))
        typeColor = 'ro' if i == start or i == end else 'bo'

        lat1, lon1 = get_lat(data, i)    , get_long(data, i)
        lat2, lon2 = get_lat(data, i - 1), get_long(data, i -  1)
        m.drawgreatcircle(lon1, lat1, lon2, lat2, lw=2, color='b')

        textColor = "w"
        name = get_loc(data, i)
        plt.text(x + 40000, y - 200000, name, weight= "bold", color= textColor)
        m.plot(x , y, typeColor, markersize= 10)

    plt.title("Starting from %s via %d waypoints | \
Total Distance: %d miles" % (get_loc(data, start), end - 1, tourDist))

    #Show Plot
    plt.show()

def run():
    cityList, graphData, locList = populate_data()
    tour, tourDist = tsp_dynamic(graphData)

    tourData = [0]*len(tour)
    for i in xrange(len(tour)):
        j = tour[i]
        city = cityList[j]
        cityLoc = locList[city]
        tourData[i] = (city, cityLoc.latitude, cityLoc.longitude)

    print tourData
    draw_map(tourData,tourDist)

###############################################################################

run()
