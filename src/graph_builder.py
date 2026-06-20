import networkx as nx
import numpy as np
import pandas as pd

class CityGraph:
    def __init__(self):
        self.G = nx.Graph()
        self.positions = {}
        
    def build_chennai_graph(self):
        locations = {
            'T. Nagar': (13.0418, 80.2341),
            'Adyar': (13.0063, 80.2574),
            'Anna Nagar': (13.0850, 80.2101),
            'Velachery': (12.9815, 80.2180),
            'Guindy': (13.0067, 80.2206),
            'Airport': (12.9941, 80.1709),
            'Tambaram': (12.9249, 80.1000),
            'OMR': (12.9170, 80.2280),
            'ECR': (12.8964, 80.2481),
            'Sholinganallur': (12.9010, 80.2279),
            'Mylapore': (13.0339, 80.2676),
            'Nungambakkam': (13.0604, 80.2439),
            'Kodambakkam': (13.0520, 80.2276),
            'Ashok Nagar': (13.0374, 80.2121),
            'K.K. Nagar': (13.0300, 80.2000),
            'Saidapet': (13.0220, 80.2230),
            'T. Nagar Bus Depot': (13.0400, 80.2350),
            'Chetpet': (13.0700, 80.2400),
            'Vadapalani': (13.0500, 80.2180),
            'Kodungaiyur': (13.1100, 80.2300),
            'Tondiarpet': (13.1000, 80.2700),
            'Royapuram': (13.0950, 80.2850),
            'Mint': (13.0900, 80.2750),
            'Washermanpet': (13.1050, 80.2650),
            'Parry': (13.0890, 80.2880)
        }
        
        self.positions = locations
        edges = [
            ('T. Nagar', 'Adyar', 3.2), ('T. Nagar', 'Mylapore', 2.1),
            ('T. Nagar', 'Nungambakkam', 2.8), ('T. Nagar', 'Kodambakkam', 2.5),
            ('Adyar', 'Velachery', 4.5), ('Adyar', 'OMR', 5.2),
            ('Adyar', 'Guindy', 3.8), ('Anna Nagar', 'Kodambakkam', 4.1),
            ('Anna Nagar', 'Vadapalani', 3.5), ('Anna Nagar', 'Chetpet', 3.2),
            ('Velachery', 'Sholinganallur', 6.8), ('Velachery', 'OMR', 4.2),
            ('Guindy', 'Airport', 8.5), ('Guindy', 'Saidapet', 2.1),
            ('Airport', 'Tambaram', 9.2), ('Tambaram', 'Sholinganallur', 12.5),
            ('OMR', 'Sholinganallur', 3.8), ('ECR', 'Sholinganallur', 5.5),
            ('ECR', 'Adyar', 7.2), ('Nungambakkam', 'Chetpet', 2.5),
            ('Vadapalani', 'Kodambakkam', 1.8), ('Saidapet', 'K.K. Nagar', 3.2),
            ('Ashok Nagar', 'K.K. Nagar', 2.1), ('Ashok Nagar', 'Vadapalani', 2.8),
            ('Kodambakkam', 'Ashok Nagar', 2.2), ('T. Nagar', 'Saidapet', 3.5),
            ('Chetpet', 'Nungambakkam', 2.5), ('Mylapore', 'Adyar', 3.8),
            ('Kodungaiyur', 'Tondiarpet', 3.2), ('Tondiarpet', 'Royapuram', 2.8),
            ('Royapuram', 'Mint', 1.5), ('Mint', 'Washermanpet', 2.1),
            ('Washermanpet', 'Parry', 2.5), ('Parry', 'Royapuram', 3.1),
            ('T. Nagar Bus Depot', 'T. Nagar', 0.8), ('T. Nagar Bus Depot', 'Saidapet', 2.8)
        ]
        
        for node, pos in locations.items():
            self.G.add_node(node, pos=pos)
            
        for loc1, loc2, dist in edges:
            self.G.add_edge(loc1, loc2, weight=dist)
            
        return self.G
    
    def find_shortest_path(self, source, target):
        try:
            path = nx.dijkstra_path(self.G, source, target, weight='weight')
            length = nx.dijkstra_path_length(self.G, source, target, weight='weight')
            return path, length
        except nx.NetworkXNoPath:
            return None, float('inf')
    
    def get_all_shortest_paths(self, source):
        paths = {}
        for target in self.G.nodes():
            if source != target:
                path, length = self.find_shortest_path(source, target)
                paths[target] = {'path': path, 'distance': length}
        return paths
