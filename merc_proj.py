import math
from pyproj import Proj, transform

def merc(lon,lat):
    lat = float(lat)
    lon = float(lon)
    
    r_major = 6378137.000
    # r_major = 6378140.000
    x = r_major * math.radians(lon)
    scale = x/lon
    y = 180.0/math.pi * math.log(math.tan(math.pi/4.0 + 
        lat * (math.pi/180.0)/2.0)) * scale
    return (x, y)

def LongLat_to_EN(long, lat):
    easting, northing = transform(Proj(init='epsg:4326'), Proj(init='epsg:3857'), long, lat)
    return easting, northing