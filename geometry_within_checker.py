"""This script is to check a layer geometries are within another geometry using QGIS geometry commands """

# Import necessary packages
from qgis.core import *
from qgis.utils import iface
from PyQt5.QtWidgets import *
import time

# Assign time to check run time
tmStart = time.time()

# for pop-up window
parent = iface.mainWindow()

# Layers - from Natural Earth website (
layers = QgsProject.instance().mapLayersByName("Countries")
if len(layers) > 0:
    countries = layers[0]
    if countries.isValid():
        lCntry_names = []
        request = QgsFeatureRequest()
        nmClause = QgsFeatureRequest.OrderByClause("NAME")
        orderby = QgsFeatureRequest.OrderBy([nmClause])
        request.setOrderBy(orderby)
        for cntry in countries.getFeatures(request):
            lCntry_names.append(cntry['NAME'])

        sCntry, bOk = QInputDialog.getItem(parent, "City Names", "Select country: ", lCntry_names)
        if bOk:
            for cntry in countries.getFeatures():
                if cntry['NAME'] == sCntry:
                    geomCntry = cntry.geometry()

            layers = QgsProject.instance().mapLayersByName("ne_10m_populated_places")
            if len(layers) > 0:
                cities = layers[0]
                if cities.isValid():
                    sStr = ""
                    request = QgsFeatureRequest()
                    popClause = QgsFeatureRequest.OrderByClause("POP_MAX", ascending=False)
                    orderby = QgsFeatureRequest.OrderBy([popClause])
                    request.setOrderBy(orderby)
                    for city in cities.getFeatures(request):
                        if city.geometry().within(geomCntry):
                            sStr += "{0:15} {1:10}\n".format(city['NAME'], city['POP_MAX'])
                else:
                    print("'Cities' is not a valid layer")
            else:
                ("Cities was not found")
        else:
            QMessageBox.warning(parent, "Cities", "User Cancelled")
    else:
        print("'Countries is not a valid layer")
else:
    print("Countries was not found")

if bOk:
    tmEnd = time.time()
    sStr = f"Run time = {round((tmEnd - tmStart), 3)} seconds\n\n" + sStr
    QMessageBox.information(parent, f"Cities in {sCntry}", sStr)