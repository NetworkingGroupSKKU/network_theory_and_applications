#---------------------------------------------------------------------#
#---import the library for solve Assignmetn4---#
#---------------------------------------------------------------------#
import networkx as nx
import matplotlib.pyplot as plt
import copy
graph = nx.Graph                

#---------------------------------------------------------------------#
#-----------class for solve Assignment 4 -------------#
#---------------------------------------------------------------------#

class Ass4(graph):          
    Stack_nodes = []
    Stack_edges = []
    Node_cnt = 0
    Edge_cnt = 0
    Data = []


#Hide the node function#
    def hide_node(self, u):
        
        #Save the edge remove soon
        for k in range(0, len(self.Data.edges())):
                       if self.Data.edges(data=True)[k][0] == str(u) or self.Data.edges(data=True)[k][1] == str(u):
                           self.Stack_edges.append(self.Data.edges(data=True)[k])
                           
        #Save the node remove soon
        for k in range(0, len(self.Data.nodes())):
            if self.Data.nodes(data= True)[k][0] == str(u):
                self.Stack_nodes.append(self.Data.nodes(data=True)[k])
                
        #Remove the node u
        self.Data.remove_node(str(u))
        
                  
#Show the node function#                                    
    def show_node(self, u):
        tmp = copy.deepcopy(self.Stack_nodes)
        l=[]
        
        #Show the node u
        for k in range(0, len(tmp)):
            if self.Stack_nodes[k][0] == str(u):
                self.Data.add_node(str(u), self.Stack_nodes[k][1])
                l.append(k)
                
        #Remove the node on ths stack
        for k in l:
                del self.Stack_nodes[k]

#Show the all nodes function#
    def show_all_nodes(self):
        tmp = copy.deepcopy(self.Stack_nodes)
        l=[]
        
        #Show the all node
        for k in range(0, len(tmp)):
            self.Data.add_node(self.Stack_nodes[k][0], self.Stack_nodes[k][1])
            l.append(k)
            
        #Remove all data on the Stack_nodes
        for k in l:
            del self.Stack_nodes[0]
            
#Hide the edge function#
    def hide_edge(self, u, v):
        tmp = copy.deepcopy(self.Data.edges())
        
        #Remove the edge (u,v)
        for k in range(0, len(tmp)):
            if (self.Data.edges(data=True)[k][0] == str(u) and self.Data.edges(data=True)[k][1] == str(v)) \
               or(self.Data.edges(data=True)[k][0] == str(v) and self. Data.edges(data=True)[k][1] == str(u)):
                self.Stack_edges.append(self.Data.edges(data=True)[k])
                u1 = copy.deepcopy(u)
                v1 = copy.deepcopy(v)
                self.Data.remove_edge(str(u1),str(v1))
                break

#Show the edge function#		
    def show_edge(self, u, v):
        tmp = copy.deepcopy(self.Stack_edges())
        l = []
        
        #Show the edge(u,v)
        for k in range(0, len(tmp)):
            if (self.Stack_edges[k][0] == str(u) and self.Stack_edges[k][1] == str(v)) or\
               (self.Stack_edges[k][0] == str(v) and self.Stack_edges[k][1] == str(u)):
                self.Data.add_edge(u,v,self.Stack_edges[k][2])
                l.append(k)
        #Remove the edge(u,v) on the stack        
        for k in l:
                del self.Stack_edges[k]
#Show the all edges function# 
    def show_all_edges(self):
        tmp = copy.deepcopy(self.Stack_edges)
        l = []
        
        #Show the all edges
        for k in range(0, len(tmp)):
                for i in range(0, len(self.Data.nodes())):
                        if(self.Stack_edges[k][0]==self.Data.nodes(data=True)[i][0]):
                                for j in range(0, len(self.Data.nodes())):
                                        if(self.Stack_edges[k][1]==self.Data.nodes(data=True)[j][0]):
                                                self.Data.add_edge(self.Stack_edges[k][0],self.Stack_edges[k][1],self.Stack_edges[k][2])
                                                l.append(k)
                                                
        #Remove all data on the Stack_edges                                        
        for k in l:
                del self.Stack_edges[0]
                       

FileName = 'D:\python\PythonAss\SN001.gexf'
InputData = nx.read_gexf(FileName)


SN = Ass4()
SN.Data =  copy.deepcopy(InputData)
NL = copy.deepcopy(len(SN.Data.nodes()))
EL = copy.deepcopy(len(SN.Data.edges()))

lat = 'latitude'
lon = 'longitude'
count = 0

#---------------------------------------------------------------------------------#
#-----------------------------Problem 1   ---------------------------------#
#---------------------------------------------------------------------------------#
#longitude
tmp = copy.deepcopy(SN.Data.edges())
m = []
n = []

for k in range(0,len(tmp)):
	if((SN.Data.node[SN.Data.edges(data=True)[k][0]][lon]<=150 and \
	    SN.Data.node[SN.Data.edges(data=True)[k][1]][lon]>=150) or \
	   (SN.Data.node[SN.Data.edges(data=True)[k][0]][lon]>=150 and \
	    SN.Data.node[SN.Data.edges(data=True)[k][1]][lon]<=150)):
		m.append(int(SN.Data.edges(data=True)[k][0]))
		n.append(int(SN.Data.edges(data=True)[k][1]))

for k in range(0,len(m)):
        SN.hide_edge(m[k],n[k])
        
#calculate mean degree
print('Longitude(150) cut mean degree is %f'%(float(len(SN.Data.edges()))*2/float(len(SN.Data.nodes()))))

#draw the graph on the absolute coordinate(longitude cut)
SN_lon = copy.deepcopy(SN.Data)
pos = nx.spring_layout(SN_lon)
pos_node = sorted(pos)
data_node = sorted(SN_lon.nodes(data=True))

for k in range(0,len(pos_node)):
	pos[pos_node[k]] = (data_node[k][1][lat],data_node[k][1][lon])

nx.draw(SN_lon,pos)
#plt.show()	
plt.savefig("lon_cut_graph.png")

#---------------------------------------------------------------------------------#
#-----------------------------Problem 2   ---------------------------------#
#---------------------------------------------------------------------------------#
#show all nodes and edges
SN.show_all_nodes();
SN.show_all_edges();

#---------------------------------------------------------------------------------#
#-----------------------------Problem 3   ---------------------------------#
#---------------------------------------------------------------------------------#
#latitude
m = []
n = []

for k in range(0,len(tmp)):
	if((SN.Data.node[SN.Data.edges(data=True)[k][0]][lat]<=150 and \
	    SN.Data.node[SN.Data.edges(data=True)[k][1]][lat]>=150) or \
	   (SN.Data.node[SN.Data.edges(data=True)[k][0]][lat]>=150 and \
	    SN.Data.node[SN.Data.edges(data=True)[k][1]][lat]<=150)):
		m.append(int(SN.Data.edges(data=True)[k][0]))
		n.append(int(SN.Data.edges(data=True)[k][1]))

for k in range(0,len(m)):
        SN.hide_edge(m[k],n[k])
        
#calculate mean degree
print('Latitude(150) cut mean degree is %f'%(float(len(SN.Data.edges()))*2/float(len(SN.Data.nodes()))))

#draw the graph on the absolute cooridnate(latitude cut)
SN_lat = copy.deepcopy(SN.Data)
pos = nx.spring_layout(SN_lat)
pos_node = sorted(pos)
data_node = sorted(SN_lat.nodes(data=True))

for k in range(0,len(pos_node)):
	pos[pos_node[k]] = (data_node[k][1][lat],data_node[k][1][lon])

nx.draw(SN_lat,pos)
#plt.show()	
plt.savefig("lat_cut_graph.png")


