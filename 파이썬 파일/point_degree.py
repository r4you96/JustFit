import math

class degree_class :
    def __init__(self):
        print("get a make degree!^^*")

    def get_degree(self, point1, point2):
        if point1 == None or point2 == None :
            return None

        width = point2[0] - point1[0]
        height = point2[1] - point1[1]

        if width == 0 :
            if height > 0 :
                return 90
            else :
                return 270

        if height == 0:
            if width > 0:
                return 0
            else:
                return 180

        #print("width : " + str(width) + ", height : " + str(height))

        radian = math.atan2(height, width)
        #print(radian)

        degree = math.degrees(radian)
        if degree < 0:
            degree = 360 + degree

        return degree

    def degree_compare(self, degree1, degree2):
        if degree1 == None or degree2 == None:
            return (0, 255, 255)

        if degree1<degree2:
            tmp = degree1
            degree1 = degree2
            degree2 = tmp

        if degree1 - degree2 > 30 :
            #return (255, 0, 0)
            return (0, 0, 255)
        else :
            return (0, 255, 255)


if __name__ == "__main__":
    dc = degree_class()
    point1 = (0, 0)
    point2 = (-10 * math.sqrt(3), -10)
    dc.get_degree(point1, point2)


