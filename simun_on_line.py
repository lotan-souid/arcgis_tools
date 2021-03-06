# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# simun_on_line.py
# Created on: 2020-06-09 08:27:54.00000
#   (generated by ArcGIS/ModelBuilder)
# Usage: simun_on_line <Parcel_input> <Hafkaa_input>
# Description:
# ---------------------------------------------------------------------------

# Set the necessary product code
# import arcinfo


# Import arcpy module
import arcpy
import os

# Script arguments
Parcel_input = arcpy.GetParameterAsText(0)
Hafkaa_input = arcpy.GetParameterAsText(1)
interval = arcpy.GetParameterAsText(2)

# Setting the Script Workspace
arcpy.env.workspace = arcpy.GetParameterAsText(3)
arcpy.env.overwriteOutput = True

Simun_line = 'Simun_line'
Simun_line_generalize = Simun_line
Line_vertices = 'Line_vertices'
Line_vertices_Layer = 'Line_vertices_Layer'
Selected_simun_points = 'Selected_simun_points'
Simon_Points_Layer = 'Simon_Points_Layer'

# Process: Feature To Line
in_feature = Hafkaa_input + ';' + Parcel_input
arcpy.FeatureToLine_management(in_feature, Simun_line, "", "NO_ATTRIBUTES")

# Process: Generalize
arcpy.Generalize_edit(Simun_line, "0.001 Meters")

# Process: Densify
arcpy.Densify_edit(Simun_line_generalize, "DISTANCE", interval+" Meters", "", "")

# Process: Feature Vertices To Points
arcpy.FeatureVerticesToPoints_management(Simun_line_generalize, Line_vertices, "ALL")

# Process: Make Feature Layer
arcpy.MakeFeatureLayer_management(Line_vertices, Line_vertices_Layer, "", "", "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;ORIG_FID ORIG_FID VISIBLE NONE")

# Process: Select Layer By Location
arcpy.SelectLayerByLocation_management(Line_vertices_Layer, "BOUNDARY_TOUCHES", Hafkaa_input, "", "NEW_SELECTION", "NOT_INVERT")

# Process: Copy Features
arcpy.CopyFeatures_management(Line_vertices_Layer, Selected_simun_points, "", "0", "0", "0")

# Process: Delete Identical
arcpy.DeleteIdentical_management(Selected_simun_points, "SHAPE", "", "0")

# Process: Add Field
arcpy.AddField_management(Selected_simun_points, "parcel_intersect", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Make Feature Layer
arcpy.MakeFeatureLayer_management(Selected_simun_points, Simon_Points_Layer, "", "", "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;ORIG_FID ORIG_FID VISIBLE NONE;parcel_intersect parcel_intersect VISIBLE NONE")

# Process: Select Layer By Location
arcpy.SelectLayerByLocation_management(Simon_Points_Layer, "BOUNDARY_TOUCHES", Parcel_input, "", "NEW_SELECTION", "NOT_INVERT")

# Process: Calculate Field
expression = "'"+"p"+"'"
arcpy.CalculateField_management(Simon_Points_Layer, "parcel_intersect", expression, "PYTHON_9.3", "")

# Process: Select Layer By Attribute
arcpy.SelectLayerByAttribute_management(Simon_Points_Layer, "CLEAR_SELECTION", "")

# Process: Add Field
arcpy.AddField_management(Simon_Points_Layer, "Label", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.AddField_management(Simon_Points_Layer, "Number", "short", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
path_to_shp_out = os.path.dirname(arcpy.env.workspace) + r"\line_shp.shp"
arcpy.FeatureToLine_management(Hafkaa_input, path_to_shp_out)

arcpy.Near_analysis(Simon_Points_Layer, path_to_shp_out)
print(arcpy.AddMessage("path: " + path_to_shp_out))
code_block="""
import os
g = arcpy.Geometry()
geom_list = arcpy.CopyFeatures_management(os.path.dirname(arcpy.env.workspace) + "\line_shp.shp", g)
def chainage(id,shp):
    geom = geom_list[id]
    l = geom.measureOnLine(shp.firstPoint)
    return l
"""
arcpy.CalculateField_management(Simon_Points_Layer, "Number", "chainage(!NEAR_FID!, !Shape!)", "PYTHON_9.3", code_block)

counter = 1
rows = arcpy.UpdateCursor(Simon_Points_Layer, "", "", "Number; NEAR_FID", "Number")
for row in rows:
    row.Number = counter
    counter = counter + 1
    rows.updateRow(row)

arcpy.CalculateField_management(Simon_Points_Layer, "Label", "[Number] & [parcel_intersect]", "VB")
arcpy.AddXY_management(Simon_Points_Layer)
arcpy.Delete_management(path_to_shp_out)

# Adding the result layer to the map
mxd = arcpy.mapping.MapDocument('CURRENT')
data_frame = arcpy.mapping.ListDataFrames(mxd)[0]
add_layer = arcpy.mapping.Layer(Simon_Points_Layer)
arcpy.mapping.AddLayer(data_frame, add_layer)

