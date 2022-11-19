import matplotlib.pyplot as plt
import networkx as nx
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
G = nx.DiGraph()
G.add_node('公司1')
G.add_node('公司2')

nx.draw(G, with_labels=True)
plt.show()
