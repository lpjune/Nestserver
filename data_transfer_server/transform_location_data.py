from pyproj import Proj, transform


def xy_to_latlong(x,y):
    
    inProj = Proj(init='epsg:3857')
    outProj = Proj(init='epsg:4326')
    #x1,y1 = -11705274.6374,4826473.6922
    
    x2,y2 = transform(inProj,outProj,x1,y1)
    return x2,y2



def latlong_to_xy(latitude, longitude):

    inProj = Proj(init = 'epsg:4326')
    outProj = Proj(init = 'epsg:3857')

    x,y = transform(inProj,outProj,latitude,longitude)
    return x,y

