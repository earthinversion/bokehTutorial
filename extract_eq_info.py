from obspy.clients.fdsn import Client
from obspy import UTCDateTime
import numpy as np
from merc_proj import merc, LongLat_to_EN


minmagnitude=6
def extract_eq_info(starttime,endtime,minmagnitude=minmagnitude):
    client = Client("IRIS")
    starttime = UTCDateTime(starttime)
    endtime = UTCDateTime(endtime)
    cat = client.get_events(starttime=starttime, endtime=endtime, minmagnitude=minmagnitude, catalog="ISC")
    years,juldays,latitudes,longitudes,depths,magnitudes,magnitude_type,event_text,eq_time=[],[],[],[],[],[],[],[],[]

    for i in range(len(cat.events)):
        try:
            yr = cat.events[i].origins[0].time.year
            jd = cat.events[i].origins[0].time.julday
            lat = cat.events[i].origins[0].latitude
            lon = cat.events[i].origins[0].longitude
            dp = cat.events[i].origins[0].depth/1000
            mg = cat.events[i].magnitudes[0].mag
            mg_type = cat.events[i].magnitudes[0].magnitude_type
            e_text = cat.events[i].event_descriptions[0].text
            e_time=str(cat.events[i].origins[0].time)
            x,y = merc(lon,lat)
            years.append(yr)
            juldays.append(jd)
            latitudes.append(lat)
            longitudes.append(lon)
            depths.append(dp)
            magnitudes.append(mg)
            magnitude_type.append(mg_type)
            event_text.append(e_text)
            eq_time.append(e_time)
        except:
            pass

    return (years,juldays,latitudes,longitudes,depths,magnitudes,magnitude_type,event_text,eq_time)