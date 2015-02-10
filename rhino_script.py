#!/usr/bin/env python

import rhinoscriptsyntax as rs
import json

data = json.load(open('/Users/dtasse/src/city_blocks/rhino_data.json'))
for nghd in data:
    if nghd['name'] != 'Central Oakland':
        continue
    # print nghd['name']
    border_points = nghd['border']
    curve = rs.AddPolyline(border_points)
    surface = rs.AddPlanarSrf(curve)
    extrusion_line = rs.AddLine((0,0,0), (0,0,3))
    solid = rs.ExtrudeSurface(surface, extrusion_line)
    rs.DeleteObjects([curve, surface, extrusion_line])

    for pipe in nghd['pipes']:
        p0 = pipe[0]
        p1 = pipe[1]
        pipe_line = rs.AddLine((p0[0], p0[1], -.5), (p1[0], p1[1], 3.5))
        # pipes.append(rs.AddPipe(pipe_line, 0, 0.5, cap=2))
        pipe = rs.AddPipe(pipe_line, 0, 0.5, cap=2)
        rs.DeleteObject(pipe_line)
        new_solid = None
        try:
            new_solid = rs.BooleanDifference([solid], [pipe])
        except:
            print "a boolean difference failed in " + nghd['name']
            rs.DeleteObject(pipe)
            continue

        if new_solid == None:
            rs.DeleteObject(pipe)
            continue # boolean difference failed, just skip one pipe
        else:
            solid = new_solid

