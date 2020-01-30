# Created by Margot Vore, Jan 2020 (Written in QGIS 3.10)
#
# This code performs resampling of a DEM, fills the sinks in the DEM, and 
# creates a stream channel and flow direction rasters. These are the first three
# steps to delineating a watershed .
# Note: this code only works in the QGIS python console. 

#-------------------------------------------------------------------------------
# Packages needed 
from qgis.analysis import QgsRasterCalculatorEntry, QgsRasterCalculator
import osgeo
import numpy as np


# change this for each trial you do. Ensures that you are not reading in an old DEM
Num=11

#----------------------------------------------------------------------------------
#Path to original DEM
DEM='C:/Users/margo/Desktop/Nechako database/GIS/clipped_DEM_NEW.tif'

#Path to save resampled DEM
RS='C:/Users/margo/Desktop/Nechako database/GIS/Outputs/RS%s.tif'%Num


Res=0.0002777777777777780486 #original DEM resolution
Inc=5 # How much increase Resolution by 

#Resampling DEM using wrap project tool 
processing.run("gdal:warpreproject", 
{'INPUT':DEM,
'SOURCE_CRS':None,'TARGET_CRS':None,'RESAMPLING':0,'NODATA':None,'TARGET_RESOLUTION':Res*Inc,
'OPTIONS':'','DATA_TYPE':0,'TARGET_EXTENT':None,'TARGET_EXTENT_CRS':None,'MULTITHREADING':False,
'EXTRA':'','OUTPUT':RS})

#------------------------------------------------------------------------------------
#Path to save filled DEM 
Fill='C:/Users/margo/Desktop/Nechako database/GIS/Outputs/DEM_Fill.sdat'

# threshold slope for filling sinks 
slope= 0.001


# Running fill sink tool
processing.run("saga:fillsinkswangliu", 
{'ELEV':RS,'MINSLOPE':slope,'FILLED':Fill,'FDIR':'TEMPORARY_OUTPUT','WSHED':'TEMPORARY_OUTPUT'})

#----------------------------------------------------------------------------------
# Path to save stream channel raster
Stream='C:/Users/margo/Desktop/Nechako database/GIS/Outputs/Stream_channels.tif'

#Path to save flow direction raster
Dir='C:/Users/margo/Desktop/Nechako database/GIS/Outputs/Flow_Direction.tif'

threshold=10

# running stream extract tool
processing.run("grass7:r.stream.extract", 
{'elevation':Fill,'accumulation':None,'depression':None,'threshold':threshold,'mexp':0,
'stream_length':0,'d8cut':None,'memory':300,'stream_raster':Stream,'stream_vector':'TEMPORARY_OUTPUT',
'direction':Dir,'GRASS_REGION_PARAMETER':None,'GRASS_REGION_CELLSIZE_PARAMETER':0,
'GRASS_RASTER_FORMAT_OPT':'','GRASS_RASTER_FORMAT_META':'','GRASS_OUTPUT_TYPE_PARAMETER':0,
'GRASS_VECTOR_DSCO':'','GRASS_VECTOR_LCO':'','GRASS_VECTOR_EXPORT_NOCAT':False})

            
        















