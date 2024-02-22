#!/usr/local/bin/FreeCADCmd
print("test")

FREECADPATH = '/usr/lib/freecad-python3/lib/' # path to your FreeCAD.so or FreeCAD.pyd file,
# for Windows you must either use \\ or / in the path, using a single \ is problematic
# FREECADPATH = 'C:\\FreeCAD\\bin'
import sys
sys.path.append(FREECADPATH)
sys.path.append("/")

def renderdxf():
    try:
        import FreeCAD
        import importDXF
        import Draft
        # from FreeCAD import importDXF
    except ValueError:
        print('FreeCAD library not found. Please check the FREECADPATH variable in the import script is correct')
        exit()
    print('FreeCAD library found')
    path = "/mirte-frame/wedge.FCStd"
    doc = FreeCAD.open(path)
    print('File opened')
    print(doc.__dict__)
    sv0 = Draft.make_shape2dview(FreeCAD.getDocument("wedge").Sketch, FreeCAD.Vector(0,-1,0))
    FreeCAD.getDocument("wedge").recompute()
    # replace fcstd with dxf
    pathOut = path.replace(".FCStd", ".dxf")
    __objs__ = []
    __objs__.append(FreeCAD.getDocument("wedge").getObject("Shape2DView"))

    # exit()
    if hasattr(importDXF, "exportOptions"):
        print('exportOptions')
        options = importDXF.exportOptions(pathOut)
        importDXF.export(__objs__, pathOut, options)
    else:
        print('exportOptions2')
        d = importDXF.export(__objs__, pathOut)
        print(d)

    del __objs__
    exit()

# def main():
renderdxf() 
# This lets you import the script without running it
# if __name__=='__main__':
# main()
