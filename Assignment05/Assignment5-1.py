# -*- coding:utf-8 -*-
import networkx as nx, matplotlib.pyplot as plt, csv, statistics
from networkx import Graph
from math import radians, cos, sin, asin, sqrt


class GraphForMST(Graph):

    def __init__(self, gmlFilePath):
        Graph.__init__(self, nx.read_gml(gmlFilePath))
        self.hidden_edges = []
        self.initializeEdges()

    def getDistance(self, source, destination):
        lat1, lng1 = source
        lat2, lng2 = destination

        AVG_EARTH_RADIUS = 6371
        # convert all latitudes/longitudes from decimal degrees to radians
        lat1, lng1, lat2, lng2 = list(map(radians, [lat1, lng1, lat2, lng2]))

        # calculate haversine
        lat = lat2 - lat1
        lng = lng2 - lng1
        d = sin(lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(lng / 2) ** 2
        h = 2 * AVG_EARTH_RADIUS * asin(sqrt(d))
        return h  # in kilometersreturn haversine(source, destination)

    def initializeEdges(self):
        for u, v, d in self.edges(data=True):
            source = self.node[u]['Latitude'], self.node[u]['Longitude']
            destination = self.node[v]['Latitude'], self.node[v]['Longitude']
            distance = self.getDistance(source, destination)
            d['distance'] = distance
            d['capacity'] = self.getCapacityFromDistance(distance)
            d['flow'] = 0.0

    def getCapacityFromDistance(self, distance):
        if distance <= 1000:
            return 100
        elif distance <= 2000:
            return 200
        elif distance <= 3000:
            return 300

    def hide_edge(self, u, v):
        self.hidden_edges.append( (u, v, self[u][v]) )
        self.remove_edge(u, v)

    def show_all_edges(self):
        for u, v, d in self.hidden_edges:
            self.add_edge( u, v, attr_dict=d )
        self.hidden_edges = []

    def show_edge(self, u, v):
        for u_, v_, d in self.hidden_edges:
            if u == u_ and v == v_:
                self.add_edge( u, v, attr_dict=d )
                self.hidden_edges.remove( (u, v, d) )
                break

class Tester():

    def __init__(self, gmlFilePath, csvFilePath):
        """
        This class is for testing our assignment 5.
        :param gmlFilePath: the location of gml file
        :param csvFilePath: the location of csv file
        :return: none
        """
        self.g = GraphForMST(gmlFilePath)
        self.demands = []
        self.initializeDemands(csvFilePath)

    def initializeDemands(self, csvFilePath):
        """
        This method is for initialization of demands from csv file.
        The results is a list of set like edge element (' 1', ' 18', {'bandwidth': ' 3.0'})
        :param csvFilePath:
        :return: [(' 24', ' 22', {'bandwidth': ' 9.0'}), (' 1', ' 18', {'bandwidth': ' 3.0'})]
        """
        with open(csvFilePath, 'rb') as csvfile:
            demands = csv.reader(csvfile, delimiter=',')
            try:
                for demand in demands:
                    self.demands.append((int(demand[1]), int(demand[2]), {'bandwidth' : float(demand[3])}))
            except Exception:
                pass

    def findShortestPathOfDemand(self):

        index = 0
        MaxN = 0
        while len(self.demands) > 0:
            demand = self.demands.pop(0)
            bandwidth = demand[2]["bandwidth"]
            hiddenEdges = []

            #Hiding all the nodes that have residual capacity smaller than demanding bandwidth
            for u, v, d in self.g.edges(data=True):
                if d["capacity"] < (d["flow"] + bandwidth):
                    self.g.hide_edge(u, v)
                    hiddenEdges.append((u, v))

            #Using shortest_path function to find the shortest path from source node to target node
            if nx.has_path(self.g, source=demand[0], target=demand[1]):
                #If the path is found, mark it in the result list
                shortestPathList = nx.shortest_path(self.g, source=demand[0], target=demand[1], weight="distance")
                print "No.", index, ", ShortestPath:", shortestPathList
                MaxN = 200
                #Reset the value of MaxN
                for i in range(0, len(shortestPathList)-1):
                    source, destination = shortestPathList[i], shortestPathList[i+1]
                    edge = self.g[source][destination]
                    #Update the value of flow
                    edge["flow"] += bandwidth
                    if edge["capacity"] == edge["flow"]:
                        #If an edge's flow is same with capacity, then hide it
                        self.g.hide_edge(source, destination)
            else:
                print "First MaxN : ", index
                MaxN = index
                #If shortest path is not found, let MaxN is the sequence of the demand

            for source, destination in hiddenEdges:
                #Show the hidden nodes, except the nodes having residual capacity = 0
                self.g.show_edge(source, destination)

            if MaxN is not 200:
                print self.g.number_of_edges()
                break

            #break
            #Move to the next demand
            index += 1

        print self.g.number_of_edges()
        print MaxN

        tester.plotResultingGraphAfterFindingMaximumN()

        #Print all results
        self.g.show_all_edges()
        flows = []
        initializedCapacities = []
        edgesAt70 = []
        unusedEdges = []
        for u, v, d in self.g.edges(data=True):
            flows.append(d['flow'])
            initializedCapacities.append(d['capacity'])
            percentage = d['flow']/d['capacity']
            if percentage < 0.7:
                edgesAt70.append((u,v,d))
            if d['flow'] == 0.0:
                unusedEdges.append((u,v,d))
        print "Edges At 70"
        print len(edgesAt70), edgesAt70
        print "Unused Edges"
        print len(unusedEdges), unusedEdges
        print "Mean"
        print statistics.mean(flows)
        print "Variance"
        print statistics.variance(flows)
        print "Min"
        print min(flows)
        print "Max"
        print max(flows)
        print "Percentage of the total capacity"
        print ( sum(flows)/sum(initializedCapacities) ) * 100
        print "Total Capacity"
        print sum(initializedCapacities)


    def getEdgesMinimumSpanningTreeWithTotalDistance(self):
        """
        This method is for returning the edges of minimum spanning tree and total distance of MST
        :return: the edges of MST and total distance
        """
        mst = nx.minimum_spanning_edges(self.g, weight='distance')
        edgesOfMST = []
        totalDistance = 0
        for u, v, d in mst:
            edgesOfMST.append((u,v))
            totalDistance += d['distance']
        return edgesOfMST, totalDistance

    def plotGraphWithMinimumSpanningTreeEdgesAndOtherEdges(self):
        """
        This method is for plotting of our graph.
        :return: none
        """

        positions = {}

        for node in self.g.nodes():
            positions[node] = (self.g.node[node]['Longitude'], self.g.node[node]['Latitude'])

        edgesOfMST, totalDistance = self.getEdgesMinimumSpanningTreeWithTotalDistance()
        edgesOFNotMST = list(set(self.g.edges()) - set(edgesOfMST))

        # The total distance of the tree
        print "The total distance of the tree :", totalDistance

        # Nodes
        nx.draw_networkx_nodes(self.g, positions, node_color='w', node_size = 800)

        # Labels
        nodeLabels = {}
        for index in range(0, self.g.number_of_nodes()):
            nodeLabels[index]= index

        nx.draw_networkx_labels(self.g, positions,nodeLabels,font_size=15)


        # Edges
        nx.draw_networkx_edges(self.g, positions,edgelist=edgesOfMST, width=2)
        nx.draw_networkx_edges(self.g, positions,edgelist=edgesOFNotMST, width=2, alpha=0.5, style='dashed')

        plt.axis('off')
        plt.show()


    def plotResultingGraphAfterFindingMaximumN(self):
        """
        This method is for plotting of our graph.
        :return: none
        """

        positions = {}

        for node in self.g.nodes():
            positions[node] = (self.g.node[node]['Longitude'], self.g.node[node]['Latitude'])

        edges = self.g.edges()

        # Nodes
        nx.draw_networkx_nodes(self.g, positions, node_color='w', node_size = 800)

        # Labels
        nodeLabels = {}
        for index in range(0, self.g.number_of_nodes()):
            nodeLabels[index]= index

        nx.draw_networkx_labels(self.g, positions,nodeLabels,font_size=15)

        # Edges
        nx.draw_networkx_edges(self.g, positions,edgelist=edges, width=2)

        edgeLabels = {}
        for u, v, d in self.g.edges(data=True):
            #edgeLabels[(u, v)] = "AF:" + str(d["flow"]) + " " + "C:" + str(d["capacity"])
            edgeLabels[(u, v)] = str(d["flow"])

        nx.draw_networkx_edge_labels(self.g, positions, edge_labels=edgeLabels,font_size=10)

        plt.axis('off')
        plt.show()

if __name__ == "__main__":
    tester = Tester("./AttMpls.gml", "./AttDemands-v2.csv")
    tester.plotGraphWithMinimumSpanningTreeEdgesAndOtherEdges()
    tester.findShortestPathOfDemand()

