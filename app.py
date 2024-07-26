import streamlit as st
import searoute as sr
import geopandas as gpd
from shapely.geometry import LineString
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Function to calculate and plot the sea route
def plot_sea_route(origin, destination):
    routeMiles = sr.searoute(origin, destination, units="km")
    distance = "{:.1f} {}".format(routeMiles.properties['length'], routeMiles.properties['units'])
    coordinates = routeMiles["geometry"]["coordinates"]
    route_line = LineString(coordinates)
    gdf = gpd.GeoDataFrame({'geometry': [route_line]})

    fig, ax = plt.subplots(figsize=(15, 10), subplot_kw={'projection': ccrs.PlateCarree()})
    ax.set_global()
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAKES, alpha=0.5)
    ax.add_feature(cfeature.RIVERS)

    # Plot the route
    gdf.plot(ax=ax, color='blue', linewidth=2)

    # Set plot titles and labels
    ax.set_title('Sea Route on World Map')
    st.pyplot(fig)

    return distance

# Streamlit app
st.title("Sea Route Plotter")

st.write("Enter the coordinates of the origin and destination:")

origin_lat = st.number_input("Origin Latitude", value=11.28399)
origin_lon = st.number_input("Origin Longitude", value=59.13765)
destination_lat = st.number_input("Destination Latitude", value=-79.927361)
destination_lon = st.number_input("Destination Longitude", value=32.992062)

origin = [origin_lat, origin_lon]
destination = [destination_lat, destination_lon]

if st.button("Plot Route"):
    distance = plot_sea_route(origin, destination)
    st.write(f"Distance: {distance}")
