from math import sqrt

def detect_collision(rect_1, rect_2):

    for r1, r2 in [(rect_1, rect_2), (rect_2, rect_1)]:
       
        return point_in_rectangle(r1.topleft, r2) or point_in_rectangle(r1.topright, r2) or \
        point_in_rectangle(r1.bottomright, r2) or point_in_rectangle(r1.bottomleft, r2)
            




def point_in_rectangle(punto, rect):
    x, y = punto
    return x >= rect.left and x <= rect.right and y >= rect.top and y <= rect.bottom
 
    
 
def detect_collision_circ(rect_1, rect_2):

    distance =  distance_centers_rectangles(rect_1, rect_2) 
    r1 = calculate_radio_rectangle(rect_1)
    r2 = calculate_radio_rectangle(rect_2)

    return distance <= (r1 + r2)

def distance_between_points(point_1, point_2):

    x1, y1 = point_1
    x2, y2 = point_2
    return sqrt( (y1 -y2) ** 2 + (x1-x2) ** 2) 

def calculate_radio_rectangle(rect):
    return rect.width // 2 

def distance_centers_rectangles(rect_1, rect_2):
    return distance_between_points(rect_1.center, rect_2.center)