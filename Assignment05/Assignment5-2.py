# http://networkx.github.io/documentation/latest/examples/subclass/printgraph.html

import networkx as nx
from networkx import Graph
from math import radians, cos, sin, asin, sqrt
import matplotlib.pyplot as plt
from time import sleep 
import random as r

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def cloneNetwork(G, target):
	for n in target.nodes(data=True):
		
		G.add_node(n[0])
		for att in n[1].keys():
			G.node[n[0]][att] = n[1][att]

	for e in target.edges(data=True):
		G.add_edge(e[0],e[1])
		for att in e[2].keys():
			G[e[0]][e[1]][att] = e[2][att]
	
	return G

def setPosition(G):
	for n in G.nodes(data=True):
		G.node[n[0]]['pos'] = (n[1]['Latitude'],n[1]['Longitude'])

	return G

def setEdgeAttributes(G):
	nx.set_edge_attributes(G,'distance',0)
	nx.set_edge_attributes(G,'capacity',0)
	nx.set_edge_attributes(G,'flow',0)
	for (u,v,d) in G.edges(data=True):
		# print (u,v)
		x1 = G.node[u]['pos'][0]
		y1 = G.node[u]['pos'][1]

		x2 = G.node[v]['pos'][0]
		y2 = G.node[v]['pos'][1]

		G[u][v]['weight'] = G[u][v]['distance'] = haversine(x1,y1,x2,y2)
		if      0 <= G[u][v]['distance'] <= 1000:
			G[u][v]['capacity'] = 100
		elif 1000 <  G[u][v]['distance'] <= 2000:
			G[u][v]['capacity'] = 200
		elif 2000 <  G[u][v]['distance'] <= 3000:
			G[u][v]['capacity'] = 300
		else: # exception, should be check!!!
			G[u][v]['capacity'] = 400
		# print "edge[",u,"][",v,"] \tdist : ",G[u][v]['distance'],"\tcapa : ",G[u][v]['capacity']
	return G

def graphInfo(G):
	print "Nodes"
	print len(G.nodes()),G.nodes()
	for n in G.nodes(data=True):
		print n[1]
	print
	print "Edges"
	print G.edges()
	for i in G.edges(data=True):
		print i

	print "=================================="

def getDemands(path=None):
	demands = {}
	if path is None:
		print "There is no target demands file"
	else:
		f = open(path,"r")
		index = 0
		for line in f:
			if "#" not in line:
				demands[index] = line.replace("\n","")\
						   			 .replace(" ","") \
						   			 .split(",")[1:]
				# print index, demands[index]
				index += 1
		f.close()
	return demands

def setDemand(G, u, v, bw, i):
	path = nx.shortest_path(G,source=int(u),target=int(v))
	print "#",i," (",u,"->",v,") \tBW: ",bw,"\t", path
	for i in range(len(path)-1):
		if G[path[i]][path[i+1]]['flow'] + float(bw) < G[path[i]][path[i+1]]['capacity']:
			G[path[i]][path[i+1]]['flow'] += float(bw)
		else: 
			print "\t\t\toverflow!!"
			return False
		# print G[path[i]][path[i+1]]['flow']
	return True

def statistics(G):
	## flow
	flowSum = 0.
	flowVar = 0.
	flowMin = 9999999990.
	flowMax = 0.
	capaSum = 0.
	unUsedEdgelist = []
	highUsageEdgelist = []

	for (u,v,d) in G.edges(data=True):
		flow = G[u][v]['flow']
		capa = G[u][v]['capacity']
		
		if flowMin > flow:
			flowMin = flow
		if flowMax < flow:
			flowMax = flow
		if flow == 0:
			unUsedEdgelist.append((u,v))
		if flow/capa > 0.7:
			highUsageEdgelist.append((u,v))

		flowSum += flow
		capaSum += capa
	flowAvg = flowSum/len(G.edges())
	usage = flowSum/capaSum
	for (u,v,d) in G.edges(data=True):
		flow = G[u][v]['flow']
		capa = G[u][v]['capacity']
		flowVar += (flowAvg - flow)*(flowAvg - flow)
	flowVar /= len(G.edges())

	print "Flow"
	print "\tmean : ", flowAvg
	print "\tvari : ", flowVar
	print "\tmax. : ", flowMax
	print "\tmin. : ", flowMin
	print "Ratio of network usage : ", usage
	print "unUsedLinks : ",unUsedEdgelist
	print "highUsageEdgelist : ", highUsageEdgelist
	
def drawMST(G,t):
	print "\n\n=========Simulation start========="
	print "Find min. spanning tree"
	plt.ion()
	fig = plt.figure()
	nx.draw(G, pos = nx.get_node_attributes(G,'pos'), with_labels=True)
	fig.canvas.draw()
	fig.clf()
	sleep(t)

	## Find minimum tree
	mst = nx.minimum_spanning_tree(G)

	## drawing graph
	edgelist1 =[]
	for (u,v,d) in G.edges(data=True):
		if (u,v) not in mst.edges():
			edgelist1.append((u,v))
	print mst.edges()
	print edgelist1
	# nx.draw_networkx_nodes(G,pos=nx.get_node_attributes(G,'pos'))
	nx.draw_networkx_labels(G,pos=nx.get_node_attributes(G,'pos'))
	nx.draw_networkx_edges(mst,pos=nx.get_node_attributes(G,'pos'),style="solid")
	nx.draw_networkx_edges(G,edgelist=edgelist1,pos=nx.get_node_attributes(G,'pos'),style="dotted")
	fig.canvas.draw()

	# insert the text about two edge lists
	# fig.savefig("MST.png")
	# fig2 = plt.figure()
	# plt.show(fig2)
	fig.clf()
	# sleep(t)

	sumDist = 0
	for (u,v,d) in G.edges(data=True):
		# print (u,v)
		x1 = G.node[u]['pos'][0]
		y1 = G.node[u]['pos'][1]

		x2 = G.node[v]['pos'][0]
		y2 = G.node[v]['pos'][1]

		sumDist += haversine(x1,y1,x2,y2)
	print "Total distance of graph : ",sumDist

	sumDist = 0
	for (u,v,d) in mst.edges(data=True):
		# print (u,v)
		x1 = G.node[u]['pos'][0]
		y1 = G.node[u]['pos'][1]

		x2 = G.node[v]['pos'][0]
		y2 = G.node[v]['pos'][1]

		sumDist += haversine(x1,y1,x2,y2)
	print "Total distance of MST \t: ",sumDist

	return G

if __name__ == "__main__":
	t = nx.Graph()
	
	# generate random graph with weight
	path = "AttMpls.gml"
	f = open(path)
	if f is not None:
		t = cloneNetwork(t, nx.read_gml(path))
		t = setPosition(t)
		t = setEdgeAttributes(t)
	else:
		print "There is no file : ",path
	# graphInfo(t)

	# load demands
	path = "AttDemands-v2.csv"
	demands = getDemands(path)

	index = 0
	for d in demands:
		if not setDemand(t, demands[d][0],demands[d][1],demands[d][2],index):
			break
		index += 1

	statistics(t)
	
	# simulation
	transTime = 1
	result = drawMST(t,transTime)

	# drawing
	fig = plt.figure()
	nx.draw(result, pos = nx.get_node_attributes(t,'pos'), with_labels=True)
	edgewidth =[]
	for (u,v,d) in t.edges(data=True):
		edgewidth.append(float(d['flow'])/10)
	nx.draw_networkx_edges(t,pos=nx.get_node_attributes(t,'pos'),alpha=0.3,width=edgewidth, edge_color='m')
	edgeLabels = {}
	for (u,v,d) in t.edges(data=True):
		edgeLabels[(u,v)] = str(int(d['flow']))
	nx.draw_networkx_edge_labels(t,pos=nx.get_node_attributes(t,'pos'),edge_labels=edgeLabels)
	plt.show(fig)
