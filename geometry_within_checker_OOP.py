"""This script is to check a layer geometries are within another geometry using QGIS geometry commands """

# Import necessary packages
from qgis.core import *
from qgis.utils import iface
from PyQt5.QtWidgets import *
import time

# for pop-up window
parent = iface.mainWindow()

# Create combobox to select countries
# Layers - from Natural Earth website (https://www.naturalearthdata.com/)
def layerSetter(layer):
    return QgsProject.instance().mapLayersByName(layer)

def validityChecker(layers):
    # Check the validity of the data
    if len(layers) > 0:
        countries = layers[0]
        if countries.isValid():
            print("Layer is valid.")
        else:
            print("It is not a valid layer.")
    else:
        ("Layer was not found.")

def assignFilter(field):
    # Assign filters - arrange the order ascending manner
    request = QgsFeatureRequest()
    clause = QgsFeatureRequest.OrderByClause(field)
    orderby = QgsFeatureRequest.OrderBy([nmClause])
    return request.setOrderBy(orderby)

def withInGeometry(filter1, filter2, layer, checkLayer, field1, field2):
    #Prepare a list to chuck filtered result to
    filteredField = []

    for lyr in layer.getFeatures(filter1):
        filteredField.append(lyr[field1])

    # Select the AOI and extract geometries from the layer
    selectedLayer, bOk = QInputDialog.getItem(parent, "City Names", "Select the containing boundary: ", filteredField)
    if bOk:
        for lyr in layer.getFeatures():
            if lyr[field1] == selectedLayer:
                lyrGeom = lyr.geometry()
        # Checked result text container
        sStr = ""
        for clyr in checkLayer.getFeatures(filter2):
            if clyr.geometry().within(lyrGeom):
                sStr += "{0:15} {1:10}\n".format(clyr[field1], clyr[field2])

    else:
        QMessageBox.warning(parent, "Input", "User Cancelled")

    # Generate result with the excution run time info
    tmEnd = time.time()
    sStr = f"Run time = {round((tmEnd - tmStart), 3)} seconds\n\n" + sStr
    QMessageBox.information(parent, f"Checked Layer in {selectedLayer}", sStr)

# Assign time to check run time
tmStart = time.time()
validityChecker("Countries","ne_10m_populated_places")
countryLayer = layerSetter("Countries")
cityLayer = layerSetter("ne_10m_populated_places")
cntryFilter = assignFilter("Countries")
cityFilter = assignFilter("ne_10m_populated_places")
withInGeometry(cntryFilter, cityFilter, countryLayer, cityLayer, "NAME", "POP_MAX")
