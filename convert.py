import rasterio
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np
import shutil

def show_and_save_geotiff(filename, output_filename):
    # Read the GeoTIFF file
    with rasterio.open(filename) as src:
        # Get the raster data
        band = src.read(1)

        # Convert the raster data to a NumPy array
        data = np.array(band)

        # Create a figure and axes
        fig, ax = plt.subplots()

        # Display the raster data
        ax.imshow(data, cmap='viridis')

        # Set the extent of the plot
        #ax.set_extent(src.bounds)

        # Add a colorbar
        fig.colorbar(ax.imshow(data, cmap='viridis'))

        # Create a PNG buffer
        buffer = BytesIO()
        plt.savefig(buffer, format='png')

        # Save the PNG buffer to a file
        buffer.seek(0)
        with open(output_filename, 'wb') as f:
            shutil.copyfileobj(buffer, f)
show_and_save_geotiff("/Users/laptop/Downloads/wc2.1_30s_tavg/wc2.1_30s_tavg_01.tif", 'test')   
