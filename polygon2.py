import itertools as IT

def area_of_polygon(x, y):
    """Calculates the signed area of an arbitrary polygon given its verticies
    http://stackoverflow.com/a/4682656/190597 (Joe Kington)
    http://softsurfer.com/Archive/algorithm_0101/algorithm_0101.htm#2D%20Polygons
    """
    print('x:',x,'\ny:',y)
    area = 0.0
    for i in range(-1, len(x) - 1):
        area += x[i] * (y[i + 1] - y[i - 1])
        print('i:%s x[i]:%s y[i+1]:%s y[i-1]:%s alan:%s'%(i, x[i], y[i+1],y[i-1],area))
    print('alan:',area/2)
    return area / 2.0

def centroid_of_polygon(points):
    """
    http://stackoverflow.com/a/14115494/190597 (mgamba)
    """
    area = area_of_polygon(*zip(*points))
    result_x = 0
    result_y = 0
    N = len(points)
    points = IT.cycle(points)
    x1, y1 = next(points)
    for i in range(N):
        x0, y0 = x1, y1
        x1, y1 = next(points)
        cross = (x0 * y1) - (x1 * y0)
        result_x += (x0 + x1) * cross
        result_y += (y0 + y1) * cross
    result_x /= (area * 6.0)
    result_y /= (area * 6.0)
    return (result_x, result_y)

def demo_centroid():
    points = [
        (30,50),
        (200,10),
        (250,50),
        (350,100),
        (200,180),
        (100,140),
        (10,200)
        ]
    cent = centroid_of_polygon(points)
    print(cent)
    # (159.2903828197946, 98.88888888888889)

def demo_centroid2():
    points = [
        (10,10),
        (110,10),
        (110,60)
        ]
    cent = centroid_of_polygon(points)
    print(cent)

demo_centroid()
