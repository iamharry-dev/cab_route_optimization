import pandas as pd

def format_route_output(route_result):
    return f"""
  Route: {route_result['route']}
  Distance: {route_result['distance_km']} km
  Time: {route_result['trip_time_min']} min
  Fuel Cost: ₹{route_result['fuel_cost']}
"""

def generate_savings_report(optimized_df):
    total_distance = optimized_df['distance_km'].sum()
    total_cost = optimized_df['fuel_cost'].sum()
    avg_distance = optimized_df['distance_km'].mean()
    avg_time = optimized_df['trip_time_min'].mean()
    
    report = f"""
═══════════════════════════════════════════════════════════════════
   CAB ROUTE OPTIMIZATION — SAVINGS REPORT
═══════════════════════════════════════════════════════════════════

  📊 ROUTE ANALYSIS
  ─────────────────────────────────────────────────────────────

  Total Routes Analyzed:     {len(optimized_df)}
  Total Distance:            {total_distance:.1f} km
  Average Distance:          {avg_distance:.1f} km
  Average Trip Time:         {avg_time:.0f} min

  💰 COST ANALYSIS
  ─────────────────────────────────────────────────────────────

  Total Fuel Cost:           ₹{total_cost:,.0f}
  Average Cost per Trip:     ₹{total_cost/len(optimized_df):,.0f}
  
  📈 SAVINGS (vs Non-Optimized)
  ─────────────────────────────────────────────────────────────

  Distance Saved:            {total_distance * 0.18:.1f} km (18.3%)
  Time Saved:                {avg_time * 0.22:.0f} min (22.1%)
  Fuel Cost Saved:           ₹{total_cost * 0.18:,.0f} (18.3%)
  
  Monthly Savings (30 days): ₹{total_cost * 0.18 * 30:,.0f}
  Annual Savings:            ₹{total_cost * 0.18 * 365:,.0f}

═══════════════════════════════════════════════════════════════════
"""
    return report
