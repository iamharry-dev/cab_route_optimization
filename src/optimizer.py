import pandas as pd
import numpy as np
from src.graph_builder import CityGraph

class CabRouteOptimizer:
    def __init__(self):
        self.city_graph = CityGraph()
        self.G = self.city_graph.build_chennai_graph()
        
    def calculate_fuel_cost(self, distance_km, fuel_price=95, mileage=15):
        fuel_liters = distance_km / mileage
        return round(fuel_liters * fuel_price, 0)
    
    def calculate_trip_time(self, distance_km, avg_speed_kmh=25):
        return round((distance_km / avg_speed_kmh) * 60, 0)
    
    def optimize_route(self, pickup, dropoff):
        path, distance = self.city_graph.find_shortest_path(pickup, dropoff)
        
        if path is None:
            return None
        
        fuel_cost = self.calculate_fuel_cost(distance)
        trip_time = self.calculate_trip_time(distance)
        
        return {
            'pickup': pickup,
            'dropoff': dropoff,
            'route': ' → '.join(path),
            'distance_km': round(distance, 2),
            'trip_time_min': int(trip_time),
            'fuel_cost': int(fuel_cost),
            'path_length': len(path)
        }
    
    def batch_optimize(self, routes_df):
        results = []
        for _, row in routes_df.iterrows():
            result = self.optimize_route(row['pickup'], row['dropoff'])
            if result:
                results.append(result)
        return pd.DataFrame(results)
    
    def get_demand_heatmap_data(self):
        locations = list(self.G.nodes())
        np.random.seed(42)
        
        demand_data = []
        for loc in locations:
            for hour in range(24):
                base_demand = np.random.poisson(5)
                if 7 <= hour <= 10 or 17 <= hour <= 20:
                    base_demand *= 2
                demand_data.append({
                    'location': loc,
                    'hour': hour,
                    'demand': base_demand,
                    'lat': self.city_graph.positions[loc][0],
                    'lon': self.city_graph.positions[loc][1]
                })
        
        return pd.DataFrame(demand_data)
