# Ori Karni - 316499607
# Yael Muchtar - 208606079
#import pip
#pip.main(['install', 'networkx'])
import networkx as nx
import time

# this is a recursion with the purpose of creating all the connected motifs
# of n vertices. each recursive call is decides whether the edge (i,j)
# will be added to G. the stopping condition is when the i,j = n (the final edge is (n,n) )
# the assumption is that there are no self edges.
def build_graphs_recursion(i, j, G, motifs, n):
    if i == j == n:
        # go over the motifs and add G to be a motif, if no motif is isomorphic to G.
        exists = False
        for k in range(0, len(motifs)):
            if nx.is_isomorphic(G, motifs[k]):
                exists = True
                break
        # if no motif is isomorphic and G is connected add it
        if (not exists) and nx.is_connected(G.to_undirected()):
            motifs.append(G.copy())
        return
    # calculate the next edge to consider
    nextJ = (j % n) + 1
    nextI = i + (nextJ == 1)
    # if (i,j) != (n,n) split to to options (adding it and not adding it)
    # case 1 - the edge doesnt exist
    build_graphs_recursion(nextI, nextJ, G, motifs, n)
    # case 2 - the edge exists
    # this case is only when i!=j because there are no self edges
    if i != j:
        G.add_edge(i, j)
        build_graphs_recursion(nextI, nextJ, G, motifs, n)
        G.remove_edge(i, j)
    return


# this is a function that utilizes the recursion and provides it with the starting parameters
def build_graphs(n):
    G = nx.DiGraph()
    G.add_nodes_from(range(1, n + 1))
    motifs = []
    build_graphs_recursion(1, 1, G, motifs, n)
    return motifs


def print_motifs_to_file(motifs, n, question, motifs_count):
    file = open(f"solution_{question}.txt", 'w')
    file.write(f"n={n}\n")
    file.write(f"count={len(motifs)}\n")
    for k in range(0, len(motifs)):
        file.write(f"#{k + 1}\n")
        if motifs_count is not None:
            file.write(f"count={motifs_count[k]}\n")
        for edge in motifs[k].edges:
            file.write(f"{edge[0]} {edge[1]}\n")
    file.close()


# function that prints the motifs array according to the requirements
def print_motifs(motifs, n):
    print(f"n={n}")
    print(f"count={len(motifs)}")
    for k in range(0, len(motifs)):
        print(f"#{k+1}")
        for edge in motifs[k].edges:
            print(edge[0], edge[1])


# Ex1 , Question 1
# Question 1, a
print("Ex1 , Question 1:")
n = int(input("please enter n:"))
motifs = build_graphs(n)
print_motifs_to_file(motifs, n, "Question_1_a", None)

# Question 1, b
# prints the motifs of n = 1, 2, 3, 4
if input("Would you like to see Q1.b? (y/n):") == 'y':
    n = 1
    while n <= 4:
        motifs = build_graphs(n)
        print_motifs(motifs, n)
        n += 1

# Question 1, c
# calculates the motifs of each n until the running time is more than an hour
if input("Would you like to see Q1.c? (y/n):") == 'y':
    n = 1
    exec_time = 0
    while exec_time < 3600:
        start = time.time()
        motifs = build_graphs(n)
        end = time.time()
        exec_time = end - start
        print(f"execution time for n = {n} is : {exec_time} s")
        n += 1


# Ex1 , Question 2
# get n and a graph
print("Ex1, Question 2:")
G2 = nx.DiGraph()
n = int(input("please enter n:"))
file = open(input("please enter a text file with the graphs representation:"), "r")
# read the text file and create a graph out of it
for line in file.read().splitlines():
    edge = line.split(" ")
    G2.add_edge(int(edge[0]), int(edge[1]))
file.close()
# create the motifs to compare to
motifs = build_graphs(n)
motifs_count = [0]*len(motifs)


# this recursive function goes over all the subgraphs of size n and for every such subgraph
# it checks for which motif it is isomorphic to
def go_over_subgraphs(i, nodes, G2_size):
    # stopping condition - when the size of nodes is n, we check the restriction of G2 to 'nodes'
    if len(nodes) == n:
        subgraph = G2.subgraph(nodes)
        if nx.is_connected(subgraph.to_undirected()):
            # go over all the motifs
            for k in range(0, len(motifs)):
                # when finding the isomorphic one, mark +1
                if nx.is_isomorphic(subgraph, motifs[k]):
                    motifs_count[k] += 1
                    return
        return
    # if i exceeds the last node, there is no more vertices to add
    if i == G2_size+1:
        return

    # case 1 - the vertex doesn't exist
    go_over_subgraphs(i+1, nodes, G2_size)
    # case 2 - the vertex exist
    nodes.append(i)
    go_over_subgraphs(i+1, nodes, G2_size)
    nodes.remove(i)


# run the function starting with an empty array, and
go_over_subgraphs(1, [], len(G2.nodes))
print_motifs_to_file(motifs, n, "Question_2", motifs_count)
# for i in range(0, len(motifs_count)):
#     if motifs_count[i] > 0:
#         print(f"no. {i+1} = {motifs_count[i]}")
