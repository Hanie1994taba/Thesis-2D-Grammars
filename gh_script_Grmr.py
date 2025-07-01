"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: The a output variable"""

__author__ = "Hanie"
__version__ = "2023.06.27"

import rhinoscriptsyntax as rs
import ghpythonlib.components as gh 
import ghpythonlib.treehelpers as gt


#function definitions 

def normalize_list(arr):
    flatten_list = lambda y:[x for a in y for x in flatten_list(a)] if type(y) is list else [y]
    return flatten_list(arr)


# class 

class Subdivision2D:

# init method or constructor 

    def __init__(self, crv, mode_1, mode_2, mode_3):
        self.curve = crv
        #self.loop = loop
        self.mode_1 = mode_1
        self.mode_2 = mode_2
        self.mode_3 = mode_3

# rule method 
    def get_centeral_point(self, crv):
        area, center_point = gh.Area(crv)
        return(center_point)

    def get_exploded_points(self, crv):
        segments, vertices = gh.Explode(crv, 1)
        del vertices[-1]
        #print(vertices)
        return(vertices)

    def get_exploded_segments(self, crv):
        segments, vertices = gh.Explode(crv, 1)
        return(segments)

    def set_scaled_curve(self, crv):
        center_point = self.get_centeral_point(crv)
        scaled_geometry = gh.Scale(crv, center_point, 0.4)[0]
        return(scaled_geometry)

    def set_mid_lines(self, crv):
        mid_point = self.get_centeral_point(crv)
        segments = self.get_exploded_segments(crv)
        segment_mid_point = [gh.CurveMiddle(segments[i]) for i in range(len(segments))]
        mid_lines = [gh.Line(mid_point, segment_mid_point[i]) for i in range(len(segments))]
        return(mid_lines)

    def set_first_loop(self, crv, mode_1):
        new_curve = []
        mode_list = [1, 2, 3, 4]
        #if loop ==1:
            #for i in mode_list:
        if mode_1 == 1:
            for i in range(len(crv)):
                vertices = self.get_exploded_points(crv[i])
                center_point = self.get_centeral_point(crv[i])
                segments = self.get_exploded_segments(crv[i])
                mid_segments = gh.CurveMiddle(segments)
                for j in range(len(vertices)):
                    new_curve.append(gh.PolyLine([vertices[j],mid_segments[j],center_point], 1))
                    new_curve.append(gh.PolyLine([vertices[j],mid_segments[j-1],center_point], 1))
        if mode_1 == 2:
            for i in range(len(crv)):
                vertices = self.get_exploded_points(crv[i])
                center_point = self.get_centeral_point(crv[i])
                for j in range(len(vertices)):
                    new_curve.append(gh.PolyLine([vertices[j-1],vertices[j],center_point], 1))
        if mode_1 == 3:
            for i in range(len(crv)):
                curve_vertices = gh.Explode(crv[i], 1)[1]
                del curve_vertices[-1]
                mid_curve = self.set_scaled_curve(crv[i])
                mid_vertices = gh.Explode(mid_curve, 1)[1]
                del mid_vertices[-1]
                for j in range(len(curve_vertices)):
                    new_curve.append(gh.PolyLine([curve_vertices[j], curve_vertices[j-1], mid_vertices[j-1], mid_vertices[j]],1))
                new_curve.append(mid_curve)
        if mode_1 == 4:
            for i in range(len(crv)):
                vertices = self.get_exploded_points(crv[i])
                        #del vertices[-1]
                mid_point = self.get_centeral_point(crv[i])
                mid_lines = self.set_mid_lines(crv[i])
                mid_lines_points = gh.CurveMiddle(mid_lines)
                for j in range(len(vertices)):
                    new_curve.append(gh.PolyLine([mid_point, mid_lines_points[j], vertices[j], mid_lines_points[j-1]], 1))
                    new_curve.append(gh.PolyLine([vertices[j], vertices[j-1], mid_lines_points[j-1]], 1))
        if mode_1 == 5:
            for i in range(len(crv)):
                center_point = gh.Area(crv[i])[1]
                polygon_vertices = gh.Explode(crv[i], 1)[1]
                del polygon_vertices[-1]
                polygon_segments = gh.Explode(crv[i], 1)[0]
                mid_segments = [gh.CurveMiddle(polygon_segments[i]) for i in range(len(polygon_segments))]
                lines = [gh.Line(mid_segments[i], center_point) for i in range(len(mid_segments))]
                mid_lines = [gh.CurveMiddle(lines[i]) for i in range(len(lines))]
                #polylines = []
                for j in range(len(polygon_vertices)):
                    new_curve.append(gh.PolyLine([polygon_vertices[j], mid_lines[j], center_point], 1))
                    new_curve.append(gh.PolyLine([polygon_vertices[j], mid_lines[j-1], center_point], 1))
        return(new_curve)



    def set_second_loop(self, crv, mode_2):
        crv_loop_1 = self.set_first_loop(crv, mode_1)
        new_curve = []
        mode_list = [1, 2, 3, 4]
        #if loop ==1:
            #for i in mode_list:
        if mode_2 == 1:
            for i in range(len(crv_loop_1)):
                vertices = self.get_exploded_points(crv_loop_1[i])
                center_point = self.get_centeral_point(crv_loop_1[i])
                segments = self.get_exploded_segments(crv_loop_1[i])
                mid_segments = gh.CurveMiddle(segments)
                for j in range(len(vertices)):
                    new_curve.append(gh.PolyLine([vertices[j],mid_segments[j],center_point], 1))
                    new_curve.append(gh.PolyLine([vertices[j],mid_segments[j-1],center_point], 1))
        if mode_2 == 2:
            for i in range(len(crv_loop_1)):
                vertices = self.get_exploded_points(crv_loop_1[i])
                center_point = self.get_centeral_point(crv_loop_1[i])
                for j in range(len(vertices)):
                    new_curve.append(gh.PolyLine([vertices[j-1],vertices[j],center_point], 1))
        if mode_2 == 3:
            for i in range(len(crv_loop_1)):
                curve_vertices = gh.Explode(crv_loop_1[i], 1)[1]
                del curve_vertices[-1]
                mid_curve = self.set_scaled_curve(crv_loop_1[i])
                mid_vertices = gh.Explode(mid_curve, 1)[1]
                del mid_vertices[-1]
                for j in range(len(curve_vertices)):
                    new_curve.append(gh.PolyLine([curve_vertices[j], curve_vertices[j-1], mid_vertices[j-1], mid_vertices[j]],1))
                new_curve.append(mid_curve)
        if mode_2 == 4:
            for i in range(len(crv_loop_1)):
                vertices = self.get_exploded_points(crv_loop_1[i])
                        #del vertices[-1]
                mid_point = self.get_centeral_point(crv_loop_1[i])
                mid_lines = self.set_mid_lines(crv_loop_1[i])
                mid_lines_points = gh.CurveMiddle(mid_lines)
                for j in range(len(vertices)):
                    new_curve.append(gh.PolyLine([mid_point, mid_lines_points[j], vertices[j], mid_lines_points[j-1]], 1))
                    new_curve.append(gh.PolyLine([vertices[j], vertices[j-1], mid_lines_points[j-1]], 1))
        return(new_curve)


    def set_third_loop(self, crv, mode_3):
        crv_loop_2 = self.set_second_loop(crv, mode_2)
        new_curve = []
        mode_list = [1, 2, 3, 4]
        #if loop ==1:
            #for i in mode_list:
        if mode_3 == 1:
            for i in range(len(crv_loop_2)):
                vertices = self.get_exploded_points(crv_loop_2[i])
                center_point = self.get_centeral_point(crv_loop_2[i])
                segments = self.get_exploded_segments(crv_loop_2[i])
                mid_segments = gh.CurveMiddle(segments)
                for j in range(len(vertices)):
                    new_curve.append(gh.PolyLine([vertices[j],mid_segments[j],center_point], 1))
                    new_curve.append(gh.PolyLine([vertices[j],mid_segments[j-1],center_point], 1))
        if mode_3 == 2:
            for i in range(len(crv_loop_2)):
                vertices = self.get_exploded_points(crv_loop_2[i])
                center_point = self.get_centeral_point(crv_loop_2[i])
                for j in range(len(vertices)):
                    new_curve.append(gh.PolyLine([vertices[j-1],vertices[j],center_point], 1))
        if mode_3 == 3:
            for i in range(len(crv_loop_2)):
                curve_vertices = gh.Explode(crv_loop_2[i], 1)[1]
                del curve_vertices[-1]
                mid_curve = self.set_scaled_curve(crv_loop_2[i])
                mid_vertices = gh.Explode(mid_curve, 2)[1]
                del mid_vertices[-1]
                for j in range(len(curve_vertices)):
                    new_curve.append(gh.PolyLine([curve_vertices[j], curve_vertices[j-1], mid_vertices[j-1], mid_vertices[j]],1))
                new_curve.append(mid_curve)
        if mode_3 == 4:
            for i in range(len(crv_loop_2)):
                vertices = self.get_exploded_points(crv_loop_2[i])
                        #del vertices[-1]
                mid_point = self.get_centeral_point(crv_loop_2[i])
                mid_lines = self.set_mid_lines(crv_loop_2[i])
                mid_lines_points = gh.CurveMiddle(mid_lines)
                for j in range(len(vertices)):
                    new_curve.append(gh.PolyLine([mid_point, mid_lines_points[j], vertices[j], mid_lines_points[j-1]], 1))
                    new_curve.append(gh.PolyLine([vertices[j], vertices[j-1], mid_lines_points[j-1]], 1))
        return(new_curve)



#main 

def run(loop):
    sub = Subdivision2D(curve, mode_1, mode_2, mode_3)
    if loop == 0:
        return(curve)
    if loop == 1:
        rule = sub.set_first_loop(curve, mode_1)
        return(rule)
    if loop == 2:
        rule = sub.set_second_loop(curve, mode_2)
        return(rule)
    if loop == 3:
        rule = sub.set_third_loop(curve, mode_3)
        return(rule)


output = run(loop)
#print(output)