from decentralizepy.graphs.FullyConnected import FullyConnected


graphs_nodes = [2, 4, 8, 16, 32, 64, 96, 128, 256, 512]
path_to_topo = 'topo/'
for nodes in graphs_nodes:
    s = FullyConnected(nodes)
    s.write_graph_to_file(path_to_topo +str(nodes)+'_fully_connected' + '.edges')


