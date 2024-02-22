#!/usr/local/bin/FreeCADCmd
print("test")

FREECADPATH = '/usr/lib/freecad-python3/lib/' # path to your FreeCAD.so or FreeCAD.pyd file,
# for Windows you must either use \\ or / in the path, using a single \ is problematic
# FREECADPATH = 'C:\\FreeCAD\\bin'
import sys
sys.path.append(FREECADPATH)
sys.path.append("/")

def renderdxf(path, name):
    try:
        import FreeCAD
        import importDXF
        import Draft
        # from FreeCAD import importDXF
    except ValueError:
        print('FreeCAD library not found. Please check the FREECADPATH variable in the import script is correct')
        exit()
    # print('FreeCAD library found')
    filepath = path+name+".FCStd"
    doc = FreeCAD.open(filepath)
    # print('File opened')
    # print(doc.__dict__)
    sv0 = Draft.make_shape2dview(FreeCAD.getDocument(name).Sketch, FreeCAD.Vector(0,-1,0))
    FreeCAD.getDocument(name).recompute()
    # replace fcstd with dxf
    pathOut = filepath.replace(".FCStd", ".dxf")
    __objs__ = []
    __objs__.append(FreeCAD.getDocument(name).getObject("Shape2DView"))

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
    FreeCAD.closeDocument(name)

# def main():
# renderdxf("/mirte-frame/", "layer") 
# renderdxf("/mirte-frame/", "wedge") 
import os
# assign directory
directory = '/tmp/mirte-frame/'
 
# iterate over files in
# that directory
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

# This lets you import the script without running it
# if __name__=='__main__':
# main()