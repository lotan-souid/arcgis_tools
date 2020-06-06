# coding: utf-8
"""
Tool Name:  bookmarks to polygons
Source Name: bookmarks_to_polygons.py
Version: 1.0
Author: lotan souid

This script create polygon feature class from your bookmarks in the mxd(active dataframe)
"""
# import necessary modules
import arcpy

# set the enviroment settings
arcpy.env.overwriteOutput = True
workspace = arcpy.env.workspace
mxd = arcpy.mapping.MapDocument('CURRENT')
bookmarks = arcpy.mapping.ListBookmarks(mxd) # collect the bookmarks
data_frame = mxd.activeDataFrame
crs = mxd.activeDataFrame.spatialReference.PCSCode # get the corrent crs from the dataframe

# create a polygon feature class
arcpy.CreateFeatureclass_management(workspace, 'bookmarks','polygon', "", "", "", crs)
path_to_layer = workspace + r'\\' + 'bookmarks'
# add field for the name of the bookmark in the feature class
arcpy.AddField_management(path_to_layer, 'bookmark_name','text')

# insert the collected data to the feature class
my_cursor = arcpy.da.InsertCursor(path_to_layer, ["bookmark_name", "SHAPE@"])
for mark in bookmarks:
    my_cursor.insertRow([mark.name, mark.extent.polygon])

# add the created feature class to the corrent dataframe
add_layer = arcpy.mapping.Layer(path_to_layer)
arcpy.mapping.AddLayer(data_frame, add_layer, "TOP")



