#!/bin/bash

# Conda Packages 
echo "Nvida Enviorment Setup ..."
# conda install -y -c conda-forge nvitop 

# Python Packages 
echo "Python Enviorment Setup ..."
pip install ipyleaflet
pip install cogeo_mosaic
pip install localtileserver
pip install rasterio
pip install matplotlib folium
pip install geopandas pycrs osmnx
pip install leafmap
pip install segment-geospatial
pip install --find-links=https://girder.github.io/large_image_wheels --no-cache GDAL

# Update from GitHub
echo "Optional update of leafmap ..."
pip install git+https://github.com/opengeos/leafmap

# Install from GitHub
echo "Optional update of Geospatial AIML Developer Enviorment Setup ..."
pip install git+https://github.com/opengeos/segment-geospatial

# Conda Packages 
echo "Java Geo-Display Enviorment Setup ..."
# conda install -y jupyter_contrib_nbextensions -c conda-forge
conda install -c conda-forge geoai
# jupyter labextension install @jupyter-widgets/jupyterlab-manager @lumino/widgets jupyter-leaflet
# jupyter nbextension enable widgetsnbextension --py --sys-prefix
# jupyter labextension install js
jupyter labextension list

# Create Kernel for Notebook
ipython kernel install --name "python-geo" --user
