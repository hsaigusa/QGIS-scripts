mc = iface.mapCanvas()
lyr = mc.currentLayer()
flds = lyr.fields()
pr = lyr.dataProvider()
lyr.selectByExpression("\"NAME\" = 'Donald Trampstan'")
if lyr.selectedFeatureCount()>0:
    fids = lyr.selectedFeatureIds()
    fid = fids[0]
    print(fid)
    attrs = {flds.indexOf("NAME"):'United States of America'}
    pr.changeAttributeValues({fid:attrs})