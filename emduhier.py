from collections import defaultdict
import networkx as nx

class EMDDAG:
    ## Bottom up approach, extended to hierarchies with multiple inheritence aka multitrees aka DAG
    ## Also accomodating hierarchies that jump levels
    ## two major data structures: graph structure for the topology of the hierarchy
    ## 2. levels - list of defaultdicts: for each level maintain a dict of nodes with how much earth is deposited there
    ## sounds like overhead but not using entire graph for flow of earth in order to be quick on sparse input, i.e. sparse flow bottom
    ## up should only touch as little nodes as necessary, not full graph

    def __init__(self, G, root=None, autoDetermineLevels=True):
        self.G = G   
        assert nx.is_directed_acyclic_graph(G)#, raise Flag
        if root is None: ## determine root/toplevel
            self.toplevel = [k for k, v in G.out_degree(G.nodes()) if v == 0]
            if len(self.toplevel) == 1:
                self.root = self.toplevel[0]
            else:
                print ("Warning, toplevel not unique and no root provided, creating superroot")
                self.makeRoot()
        else:
            self.root = root
        self.maxlevel = 0
        if autoDetermineLevels:
            self.determineLevels()
            self.makeLevelDicts()
    def makeRoot(self):
        ## WordNet now has a 'fake' root
        ## provide umbrella root for all toplevel nodes
        ## TODO: exclude that a toplevel node is called 'root'
        self.G.add_weighted_edges_from( [(topnode, 'root', 1) for topnode in self.toplevel])
        self.root = 'root'
    def determineLevels(self, node=None, level=0):
        if node is None: node=self.root
        ## If level has been set previously (possible in DAGs), use maximum depth
        ## Level differs if edges can skip levels (e.g. from L1->L3)
        self.G.nodes[node]['level'] = max(level, self.G.nodes[node].get('level', 0))
        if level > self.maxlevel: self.maxlevel = level
        for child in self.G.predecessors(node):
            self.determineLevels(child, level+1)
    def addWeights(self, node=None):
        if node is None: node=self.root
        for child in self.G.predecessors(node):
            self.addWeights(child)
        parents = list(self.G.successors(node))
        for parent in parents:
            self.G[node][parent]['weight'] = 1/len(parents) ## equal weights to parents, can be improved
    def depositeEarth(self, valueDict, factor=1):
        for node, value in valueDict.items():
            nodelevel = self.G.nodes[node]['level']
            self.levels[nodelevel][node] += factor*value
    def makeLevelDicts(self):        
        self.levels = [defaultdict(float) for level in range(self.maxlevel+1)]
    def distance(self, dist1, dist2):  ## all-in-one api call for convenience
        self.makeLevelDicts() ## emd consumes them, redo or rewrite emd
        self.depositeEarth(dist1)
        self.depositeEarth(dist2, factor=-1)
        return self.emd()
    def emd(self, eps = 1e-08):
        Z = 0        
        while self.levels:
            currentLevelDict = self.levels.pop()
            for node, value in currentLevelDict.items():
                if abs(value) > eps:
                    parents = self.G.successors(node) ## far more elegant than previously
                    if not parents: break ## reached top
                    for parent in parents:
                        parentlevel = self.G.nodes[parent]['level']
                        movedEarth = self.G[node][parent]['weight'] * value
                        self.levels[parentlevel][parent] += movedEarth
                        Z += self.G[node][parent].get('length', 1) * abs(movedEarth)
        return Z


if __name__ == "__main__":
    # Toy example with multiple inheritance
    #  0                     9
    #                  /          \
    #  1             7             8
    #               / \           /  \
    #  2          3    4        5     6
    #           /  \  /
    #  3       1     2
    #         /
    #  4     0
    G = nx.DiGraph()
    edges =[(0, 1, 1), (1, 3, 1), (2, 3, .7), (3, 7, 1), 
            (4, 7, 1), (5, 8, 1), (6, 8, 1), 
            (8, 9, 1), (7, 9, 1), (2, 4,.3)]
    G.add_weighted_edges_from(edges)
    dag = EMDDAG(G)

    # two probability distributions over arbitrary nodes (not necessarily leaf nodes!)
    # i.e., two relatively similar docs (prob. distributions)
    # earth moving: earth on 4 and 5 cancels each other out, 1/3 from 0 to 1, 1/3 from 1 to 3, 0.2333 from 2 to 3,
    # 0.1 from 2 to 7, 0.1 from 3 to 7
    # total value: 1.1
    distrib1 = {2:1/3.,4:1/3.,5:1/3.}
    distrib2 = {0:1/3.,4:1/3.,5:1/3.}
    print(dag.distance(distrib1, distrib2))

