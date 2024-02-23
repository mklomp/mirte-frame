#!/usr/local/bin/FreeCADCmd
print("test")
docker=False
FREECADPATH = '/usr/lib/freecad-python3/lib/' # path to your FreeCAD.so or FreeCAD.pyd file,
# for Windows you must either use \\ or / in the path, using a single \ is problematic
# FREECADPATH = 'C:\\FreeCAD\\bin'
import sys
sys.path.append(FREECADPATH)
sys.path.append("/")
try:
    import FreeCAD
    import importDXF
    import Draft
    import Mesh
    # from FreeCAD import importDXF
except ValueError:
    print('FreeCAD library not found. Please check the FREECADPATH variable in the import script is correct')
    exit()
def renderdxf(path, name):
    
    # print('FreeCAD library found')
    filepath = path+name+".FCStd"
    doc = FreeCAD.open(filepath)
    bodies = list()
    for obj in doc.Objects:
        # Fix for motor clamp lock, the chamfer one is the final one
        if obj.isDerivedFrom("PartDesign::Body") or obj.isDerivedFrom("Part::Chamfer"):
                bodies.append(obj)
    print(bodies)
    for body in bodies:
        renderbody(path, name, body, doc, filepath)
        renderstl(path, name, body, doc, filepath)
    FreeCAD.closeDocument(name)

    # print('File opened')
    # print(doc.__dict__)
def renderbody(path, name, body, doc, filepath):
    sv0 = Draft.make_shape2dview(body, FreeCAD.Vector(0,-1,0))
    FreeCAD.getDocument(name).recompute()
    # replace fcstd with dxf
    pathOut = filepath.replace(".FCStd", f"_{body.Label}.dxf")
    __objs__ = []
    __objs__.append(FreeCAD.getDocument(name).getObject(sv0.Name))

    # exit()
    if hasattr(importDXF, "exportOptions"):
        # print('exportOptions')
        options = importDXF.exportOptions(pathOut)
        importDXF.export(__objs__, pathOut, options)
    else:
        # print('exportOptions2')
        d = importDXF.export(__objs__, pathOut)
        # print(d)

    del __objs__
    # FreeCAD.getDocument(name).getObject("Shape2DView").removeObject()

def renderstl(path, name, body, doc, filepath):
    __objs__ = []
    __objs__.append(body)
    pathOut = filepath.replace(".FCStd", f"_{body.Label}.stl")

    if hasattr(Mesh, "exportOptions"):
        options = Mesh.exportOptions(pathOut)
        Mesh.export(__objs__, pathOut, options)
    else:
        Mesh.export(__objs__, pathOut)
	
    del __objs__


# def main():
# renderdxf("/mirte-frame/", "layer") 
# renderdxf("/mirte-frame/", "wedge") 
import os
# assign directory
directory = '/tmp/mirte-frame/'
if docker:
    directory = '/mirte-frame/'
# iterate over files in
# that directory
if not docker:
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            print(f)
            if f.endswith(".FCStd"):
                print(f)
                name = f.split("/")[-1].split(".")[0]
                print(name)
                renderdxf(directory, name)
else:
    renderdxf(directory, "attachments")
# This lets you import the script without running it
# if __name__=='__main__':
# main()