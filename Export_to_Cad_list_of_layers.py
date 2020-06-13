# coding: utf-8
"""
Tool Name:  Export to Cad list of layers
Source Name: Export_to_Cad_list_of_layers.py
Version: 1.0
Author: lotan souid

This script will export list of layers to selected folder.
each layer will export with the same name of layer in the gis.
each layer will export as "dwg 2000" file format.

"""
# import necessary modules
import arcpy
import os

# arcpy.env.workspace = 'CURRENT'
arcpy.env.workspace = r"in_memory"
arcpy.env.overwriteOutput = True

# collect the parameters form the gui
input_layers = arcpy.GetParameterAsText(0)
output_folder = arcpy.GetParameterAsText(1)


# split the input string to list (the input layers enter as string)
input_layers = input_layers.split(";")

print(arcpy.AddMessage(input_layers[0]))
print(arcpy.AddMessage(type(input_layers[0])))

# set the counter for giving different color for each output cad layer
counter = 0

# loop throw the list of input layers and export each one
try:
    for i in input_layers:
        counter += 1
        in_memory = r"in_memory\\"
        arcpy.CopyFeatures_management(i, in_memory + i)
        arcpy.AddField_management(in_memory + i, 'Layer', 'text')
        arcpy.CalculateField_management(in_memory + i, 'Layer', i)
        arcpy.AddField_management(in_memory + i, 'LyrColor', 'short')
        arcpy.CalculateField_management(in_memory + i, 'LyrColor', counter)
        output_type = "DWG_R2000"
        output_file = output_folder + "\\" + i + '.dwg'
        print(arcpy.AddMessage(output_file))
        arcpy.ExportCAD_conversion(in_memory + i, output_type, output_file)
        arcpy.Delete_management(r"in_memory")
    print(arcpy.AddMessage("all layers was expoerted!"))
except arcpy.ExecuteError:
    print(arcpy.AddMessage("All layers must not be in group!!!"))
    raise