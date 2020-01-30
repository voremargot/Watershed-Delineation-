# Created by Margot Vore, Jan 2020 (Written in QGIS 3.10)
#
# This code performs the delineation of a watershed for multiple locations, and 
# transforms the drainage basin into a shapefile. 
# Note: The user should run QGIS_WS_part1 prior to running this code

#-----------------------------------------------------------------------------
#Location of flow direction raster
Dir='C:/Users/margo/Desktop/Nechako database/GIS/Outputs/Flow_Direction.tif'

#List of stations to delineate watersheds for 
Stations=['A029','B008','B003','B002','C001','C002','E001']

# Lat and Long coordinates for the outlet of the basin:
#NOTE: These locations are found by hand by looking for a stream that is in closest
#      proximity to the hyrdometric station of interest.  The coordinates MUST BE
#      within a grid cell that contains a stream channel (look at stream channel raster).
# Lat and Long must be in same order at the station array above

Lat=[53.662696,53.90223,54.08624,54.00984,54.01528,53.96003,54.41522]
Long=[-126.989306,-126.95420,-124.60084,-125.00662,-124.00658,-123.23641,-124.27277]

# for each stations creates a drainage basin 
for id in range(len(Stations)):
    #choosing the station name and lat long coordiantes
    S=Stations[id]
    Lt=Lat[id]
    Lo=Long[id]
    
    # Path to save basin raster to
    Ot='C:/Users/margo/Desktop/Nechako database/GIS/Outputs/%s.tif'%S

    # Running water outlet tool 
    processing.run("grass7:r.water.outlet", 
    {'input':Dir,'coordinates':'%s,%s [EPSG:4326]'%(Lo,Lt),
    'output':Ot,'GRASS_REGION_PARAMETER':None,
    'GRASS_REGION_CELLSIZE_PARAMETER':0,'GRASS_RASTER_FORMAT_OPT':'',
    'GRASS_RASTER_FORMAT_META':''})
 
# For each station,vectorize the drainage basin 
for S in Stations:
    # where to save the shapefiles to
    R= 'C:/Users/margo/Desktop/Nechako database/GIS/Outputs/%s_shapefile.shp'%S
    
    # path to where the drainage basin rasters are located 
    Ot='C:/Users/margo/Desktop/Nechako database/GIS/Outputs/%s.tif'%S
    
    # running the polygoize tool 
    processing.run("gdal:polygonize", 
    {'INPUT':Ot,'BAND':1,'FIELD':'DN',
    'EIGHT_CONNECTEDNESS':False,'EXTRA':'',
    'OUTPUT':R})
        