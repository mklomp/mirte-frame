from freecad_build_instruction_generator import instruction_generator as gen
from pathlib import Path
import time
import importlib
importlib.reload(gen)

#TODO: 
# - fix freecad warning
# - can we create smaller step files?
# - use new PCB
# - step names when exporting
# - account for 3/4 mm differences
# - combine with: https://osh-autodoc.org/#_installation

# Our own STEP files do not have color yet
def colorFix(item):
   item.ViewObject.ShapeColor = (184, 147, 103)
   return item

mirte = "lite" # lite, basic, pioneer
type = "breadboard" # breadboard, pcb
battery = "aa" # aa, powerbank
modules = ["ir_left", "ir_right"] # ir_left_, ir_right, line_center

mirte_version = "mirte_" + mirte +\
               (("_" + type) if ((mirte == "pioneer" and type == "breadboard") or (mirte == "basic" and type == "breadboard")) else "") +\
               (("_" + battery) if (mirte == "basic" and battery == "powerbank") else "")

# set the path where we are running the sources
dir_path = os.path.dirname(os.path.realpath(__file__))
gen.setCwdPath(dir_path)
gen.addSourcesPath('mirte', str(     (Path(dir_path) / '../../build/step').resolve()     ))
gen.addSourcesPath('external', str(     (Path(dir_path) / '../../external_parts').resolve()     ))
gen.setWarningPath( str(     (Path(dir_path) / './warnings').resolve()     ))
gen.setMIRTEVersion(mirte_version)


############################
####    FIRST LAYER HARDWARE
############################

### Create MIRTE assembly
mirte_assembly = gen.AssemblyProject("MIRTE", False)
base_lower = colorFix(mirte_assembly.import_object("mirte", "layer_bottom-minimal.step", App.Vector(0, -3, 0), App.Rotation(0,0,180)))

if mirte == "pioneer":

  ## Insert SD card into Orange Pi
  opi_assembly = gen.AssemblyProject("OPI", False)
  opi = opi_assembly.import_object("external", "OrangePi_Zero2.step", App.Vector(-27,7,0), App.Rotation(0,90,0))
  sd = opi_assembly.import_object("external", "Micro SD Card.STEP", App.Vector(-14.3,6.7,39.6), App.Rotation(0,180,90))
  #mirte_assembly.addWarning("sd")
  opi_assembly.addStep(gen.Step(sd, App.Vector(0,0,10)))
  opi_assembly.save_image_new_parts()
  opi_assembly.close(True)

  opi_step = mirte_assembly.import_object("build", "OPI.step", App.Vector(0, -5,0), App.Rotation(0,0,0))
  mirte_assembly.addWarning("orangepi")
  mirte_assembly.addStep(gen.Step(opi_step, App.Vector(0,50,0)))
  mirte_assembly.save_image_new_parts()

  ### Add Orange Pi Bolts and Nuts
  opi_bolt1 = mirte_assembly.import_object("external", "CHC M3 L14.step", App.Vector(-54.5,6,24), App.Rotation(0,90,180))
  opi_bolt2 = mirte_assembly.import_object("external", "CHC M3 L14.step", App.Vector(.5,6,24), App.Rotation(0,90,180))
  opi_bolt3 = mirte_assembly.import_object("external", "CHC M3 L14.step", App.Vector(-54.5,6,-24), App.Rotation(0,90,180))
  opi_bolt4 = mirte_assembly.import_object("external", "CHC M3 L14.step", App.Vector(.5,6,-24), App.Rotation(0,90,180))
  mirte_assembly.addStep(gen.ParallelSequence([gen.Sequence([gen.Step(opi_bolt1, App.Vector(0,50,0))]), gen.Sequence([gen.Step(opi_bolt2, App.Vector(0,50,0)) ]), gen.Sequence([gen.Step(opi_bolt3, App.Vector(0,50,0)) ]), gen.Sequence([gen.Step(opi_bolt4, App.Vector(0,50,0)) ])]))
  opi_nut1 = mirte_assembly.import_object("external", "M3 Nut.step", App.Vector(-54.5,-3,24), App.Rotation(0,90,180))
  opi_nut2 = mirte_assembly.import_object("external", "M3 Nut.step", App.Vector(.5,-3,24), App.Rotation(0,90,180))
  opi_nut3 = mirte_assembly.import_object("external", "M3 Nut.step", App.Vector(-54.5,-3,-24), App.Rotation(0,90,180))
  opi_nut4 = mirte_assembly.import_object("external", "M3 Nut.step", App.Vector(.5,-3,-24), App.Rotation(0,90,180))
  mirte_assembly.addStep(gen.ParallelSequence([gen.Sequence([gen.Step(opi_nut1, App.Vector(0,-60,0))]), gen.Sequence([gen.Step(opi_nut2, App.Vector(0,-60,0)) ]), gen.Sequence([gen.Step(opi_nut3, App.Vector(0,-60,0)) ]), gen.Sequence([gen.Step(opi_nut4, App.Vector(0,-60,0)) ])]))
  mirte_assembly.save_image_new_parts()


##################################
####    FIRST LAYER INNER SENSORS
##################################

if "line_center" in modules:
  line_center = mirte_assembly.import_object("external", "TCRT5000mod.STEP", App.Vector(56.3,1.8,5.8), App.Rotation(-122,0,180))
  mirte_assembly.addStep(gen.Step(line_center, App.Vector(0,50,0)))
  line_center_bolt1 = mirte_assembly.import_object("external", "CHC M3 L14.step", App.Vector(57.9,5.6,0), App.Rotation(0,90,180))
  mirte_assembly.addStep(gen.Step(line_center_bolt1, App.Vector(0,50,0)))
  line_center_nut1 = mirte_assembly.import_object("external", "M3 Nut.step", App.Vector(57.9,-3.2,0), App.Rotation(0,90,180))
  mirte_assembly.addStep(gen.Step(line_center_nut1, App.Vector(0,-50,0)))


##################################
####    FIRST LAYER WHEEL SUPPORTS
##################################

##### Add Motor Frames
motor_frame_front = colorFix(mirte_assembly.import_object("mirte", "motor_clamp_plate.step", App.Vector(-2.7,-9.1,47), App.Rotation(0,90,-90)))
motor_frame_back = colorFix(mirte_assembly.import_object("mirte", "motor_clamp_plate.step", App.Vector(-2.7 + 25,-9.1,47), App.Rotation(0,90,-90)))
###TODO: this should be: ParallelSequence([Step(motor_frame_front, App.Vector(0,100,0)), Step(motor_frame_back, App.Vector(0,100,0))]).execute()
mirte_assembly.addStep(gen.ParallelSequence([gen.Sequence([gen.Step(motor_frame_front, App.Vector(0,100,0))]), gen.Sequence([gen.Step(motor_frame_back, App.Vector(0,100,0))])]))
mirte_assembly.save_image_new_parts()

if mirte != "pioneer":
  ##### Add motor spacer
  motor_spacer_left = colorFix(mirte_assembly.import_object("mirte", "spacer_motor-clamp.step", App.Vector(28 ,40, 28), App.Rotation(-90,0,90)))
  motor_spacer_right = colorFix(mirte_assembly.import_object("mirte", "spacer_motor-clamp.step", App.Vector(28 ,40,-25), App.Rotation(-90,0,90)))
  mirte_assembly.addStep(gen.ParallelSequence([gen.Sequence([gen.Step(motor_spacer_left, App.Vector(0,100,0))]), gen.Sequence([gen.Step(motor_spacer_right, App.Vector(0,100,0))])]))

#### Add Holders
mirte_assembly.setView("bottom")
motor_frame_holder_left = colorFix(mirte_assembly.import_object("mirte", "motor_clamp_wedge.step", App.Vector(-3 ,-3,-44.4), App.Rotation(0,0,0)))
motor_frame_holder_right = colorFix(mirte_assembly.import_object("mirte", "motor_clamp_wedge.step", App.Vector(-3 ,-3,36.2), App.Rotation(0,0,0)))
mirte_assembly.addStep(gen.ParallelSequence([gen.Sequence([gen.Step(motor_frame_holder_left, App.Vector(-100,0,0))]), gen.Sequence([gen.Step(motor_frame_holder_right, App.Vector(-100,0,0))])]))
mirte_assembly.save_image_new_parts()

### Add caster wheel
caster_wheel = mirte_assembly.import_object("external", "Low ball caster plastic.step", App.Vector(-87,-3,0), App.Rotation(0,90,180))
mirte_assembly.addStep(gen.Step(caster_wheel,  App.Vector(0,-50,0)))
mirte_assembly.save_image_new_parts()

### Add caster wheel Bolts and Nuts
caster_bolt1 = mirte_assembly.import_object("external", "CHC M3 L14.step", App.Vector(-87,3,20), App.Rotation(0,90,180))
caster_bolt2 = mirte_assembly.import_object("external", "CHC M3 L14.step", App.Vector(-87,3,-20), App.Rotation(0,90,180))
mirte_assembly.addStep(gen.ParallelSequence([gen.Sequence([gen.Step(caster_bolt1, App.Vector(0,50,0))]), gen.Sequence([gen.Step(caster_bolt2, App.Vector(0,50,0)) ])]))
caster_nut1 = mirte_assembly.import_object("external", "M3 Nut.step", App.Vector(-87,-6,20), App.Rotation(0,90,180))
caster_nut2 = mirte_assembly.import_object("external", "M3 Nut.step", App.Vector(-87,-6,-20), App.Rotation(0,90,180))
mirte_assembly.addStep(gen.ParallelSequence([gen.Sequence([gen.Step(caster_nut1, App.Vector(0,-50,0))]), gen.Sequence([gen.Step(caster_nut2, App.Vector(0,-50,0)) ])]))
mirte_assembly.save_image_new_parts()
mirte_assembly.setView("top")


#####################################
####    ADD UPPER BASE (PIONEER ONLY)
#####################################
if mirte == "pioneer":
   #### Add Upper Base
   base_upper = colorFix(mirte_assembly.import_object("mirte", "layer_top.step", App.Vector(-.5, 40.15, 0), App.Rotation(0,0,0)))
   mirte_assembly.addStep(gen.Step(base_upper, App.Vector(0,100,0)))
   mirte_assembly.save_image_new_parts()

   #### Pen hole lock
   pen_hole_lock = colorFix(mirte_assembly.import_object("mirte", "motor_clamp_lock.step", App.Vector(-3.5, 43.9, -12.4), App.Rotation(0,0,0)))
   mirte_assembly.addStep(gen.Step(pen_hole_lock, App.Vector(100,0,0)))
   wig = colorFix(mirte_assembly.import_object("mirte", "wedge.step", App.Vector(25, 27, 1.5), App.Rotation(0,180,-90)))
   mirte_assembly.addStep(gen.Step(wig, App.Vector(0,100,0)))
   mirte_assembly.save_image_new_parts()

   ##### Spacers
   spacer1 = colorFix(mirte_assembly.import_object("mirte", "spacer_layer.step", App.Vector(57.8, 45.3, 64), App.Rotation(0,180,90)))
   spacer2 = colorFix(mirte_assembly.import_object("mirte", "spacer_layer.step", App.Vector(57.8, 45.3, -64), App.Rotation(0,180,90)))
   spacer3 = colorFix(mirte_assembly.import_object("mirte", "spacer_layer.step", App.Vector(-67, 44, 67), App.Rotation(0,45,90)))
   spacer4 = colorFix(mirte_assembly.import_object("mirte", "spacer_layer.step", App.Vector(-70, 43, -64.5), App.Rotation(0,-45,90)))
   mirte_assembly.addStep(gen.ParallelSequence([gen.Sequence([gen.Step(spacer1, App.Vector(0,50,0))]), gen.Sequence([gen.Step(spacer2, App.Vector(0,50,0)) ]), gen.Sequence([gen.Step(spacer3, App.Vector(0,50,0)) ]), gen.Sequence([gen.Step(spacer4, App.Vector(0,50,0)) ])]))
   mirte_assembly.save_image_new_parts()


#####################################
####    ADD MOTORS AND WHEELS
#####################################

motor_left = mirte_assembly.import_object("external", "Mini Gear DC Motor 6 V Yellow.step", App.Vector(-1.7, 70.3,12.4), App.Rotation(0,0,90))
motor_right = mirte_assembly.import_object("external", "Mini Gear DC Motor 6 V Yellow.step", App.Vector(24.5, 70.3, -12.4), App.Rotation(0,180,90))
mirte_assembly.addStep(gen.ParallelSequence([gen.Sequence([gen.Step(motor_left, App.Vector(0,0,37), App.Vector(1,0,0), 30), gen.Step(motor_left, App.Vector(0,0,37+50))]), gen.Sequence([gen.Step(motor_right, App.Vector(0,0,-37), App.Vector(1,0,0), 30), gen.Step(motor_right, App.Vector(0,0, -37-50))])]))
mirte_assembly.save_image_new_parts()

wheel_left = mirte_assembly.import_object("external", "Wheel D65x25.STEP", App.Vector(11.5, 15.5, 77), App.Rotation(0,0,0))
wheel_right = mirte_assembly.import_object("external", "Wheel D65x25.STEP", App.Vector(11.5, 15.5, -77), App.Rotation(0,0,180))
mirte_assembly.addStep(gen.ParallelSequence([gen.Sequence([gen.Step(wheel_left, App.Vector(0,0,50))]), gen.Sequence([gen.Step(wheel_right, App.Vector(0,0,-50))])]))
mirte_assembly.save_image_new_parts()

##################################
####    FIRST LAYER OUTER SENSORS
##################################

if mirte != "pioneer":

  if "ir_left" in modules and "ir_right" in modules:
    ir_left = mirte_assembly.import_object("external", "IRsensors.step", App.Vector(93, 0, 39.5), App.Rotation(180,0,180))
    ir_right = mirte_assembly.import_object("external", "IRsensors.step", App.Vector(93, 0, -39.5), App.Rotation(180,0,180))
    mirte_assembly.addStep(gen.ParallelSequence([gen.Sequence([gen.Step(ir_left, App.Vector(0,50,0))]), gen.Sequence([gen.Step(ir_right, App.Vector(0,50,0)) ])]))
    ir_left_bolt1 = mirte_assembly.import_object("external", "CHC M3 L14.step", App.Vector(84.5,4.6,39.5), App.Rotation(0,90,180))
    ir_right_bolt1 = mirte_assembly.import_object("external", "CHC M3 L14.step", App.Vector(84.5,4.6,-39.5), App.Rotation(0,90,180))
    mirte_assembly.addStep(gen.ParallelSequence([gen.Sequence([gen.Step(ir_left_bolt1, App.Vector(0,50,0))]), gen.Sequence([gen.Step(ir_right_bolt1, App.Vector(0,50,0)) ])]))
    ir_left_nut1 = mirte_assembly.import_object("external", "M3 Nut.step", App.Vector(84.5,-3.2,39.5), App.Rotation(0,90,180))
    ir_right_nut1 = mirte_assembly.import_object("external", "M3 Nut.step", App.Vector(84.5,-3.2,-39.5), App.Rotation(0,90,180))
    mirte_assembly.addStep(gen.ParallelSequence([gen.Sequence([gen.Step(ir_left_nut1, App.Vector(0,-50,0))]), gen.Sequence([gen.Step(ir_right_nut1, App.Vector(0,-50,0)) ])]))

  elif "ir_left" in modules: 
    ir_left = mirte_assembly.import_object("external", "IRsensors.step", App.Vector(93, 0, 39.5), App.Rotation(180,0,180))
    mirte_assembly.addStep(gen.Step(ir_left, App.Vector(0,50,0)))
    ir_left_bolt1 = mirte_assembly.import_object("external", "CHC M3 L14.step", App.Vector(84.5,4.6,39.5), App.Rotation(0,90,180))
    mirte_assembly.addStep(gen.Step(ir_left_bolt1, App.Vector(0,50,0)))
    ir_left_nut1 = mirte_assembly.import_object("external", "M3 Nut.step", App.Vector(84.5,-3.2,39.5), App.Rotation(0,90,180))
    mirte_assembly.addStep(gen.Step(ir_left_nut1, App.Vector(0,-50,0)))

  elif "ir_right" in modules:
    ir_right = mirte_assembly.import_object("external", "IRsensors.step", App.Vector(93, 0, -39.5), App.Rotation(180,0,180))
    mirte_assembly.addStep(gen.Step(ir_right, App.Vector(0,50,0)))
    ir_right_bolt1 = mirte_assembly.import_object("external", "CHC M3 L14.step", App.Vector(84.5,4.6,39.5), App.Rotation(0,90,180))
    mirte_assembly.addStep(gen.Step(ir_right_bolt1, App.Vector(0,50,0)))
    ir_right_nut1 = mirte_assembly.import_object("external", "M3 Nut.step", App.Vector(84.5,-3.2,39.5), App.Rotation(0,90,180))
    mirte_assembly.addStep(gen.Step(ir_right_nut1, App.Vector(0,-50,0)))


#######################################
####    ADD AA BATTERIES (LITE & BASIC)
#######################################

if battery == "aa":
  #### Insert batteries in holder
  battery_assembly = gen.AssemblyProject("BatteryHolder", False)
  battery_holder = battery_assembly.import_object("external", "battery_holder.step", App.Vector(0, 0, 0), App.Rotation(0, 0,0))
  battery1 = battery_assembly.import_object("external", "AA Battery.step", App.Vector(-4.2, -10.7, -19.3), App.Rotation(0,-90,0))
  battery2 = battery_assembly.import_object("external", "AA Battery.step", App.Vector(-10.7, -10.7, 28.3), App.Rotation(0, 90,0))
  battery3 = battery_assembly.import_object("external", "AA Battery.step", App.Vector(25.8, -10.7, -19.3), App.Rotation(0,-90,0))
  battery_assembly.addStep(gen.ParallelSequence([gen.Sequence([gen.Step(battery1, App.Vector(0,25,0))]), gen.Sequence([gen.Step(battery2, App.Vector(0,25,0)) ]), gen.Sequence([gen.Step(battery3, App.Vector(0,25,0)) ])]))

  #### Insert lid
  battery_holder_lid = battery_assembly.import_object("external", "battery_lid.step", App.Vector(0, 0, -34), App.Rotation(0, 0, 90))
  battery_assembly.addStep(gen.Step(battery_holder_lid, App.Vector(0,25,0)))  
  battery_assembly.save_image_new_parts()
  battery_assembly.close(True)

  ###### Add Battery holder lockers
  mirte_assembly.setView("rear")
  spacer1 = colorFix(mirte_assembly.import_object("mirte", "spacer_layer.step", App.Vector(-21.7, 42.9, 24.1), App.Rotation(0,90,90)))
  spacer2 = colorFix(mirte_assembly.import_object("mirte", "spacer_layer.step", App.Vector(-24.8, 42.9, -24.8), App.Rotation(0,-90,90)))
  mirte_assembly.addStep(gen.ParallelSequence([gen.Sequence([gen.Step(spacer1, App.Vector(0,50,0))]), gen.Sequence([gen.Step(spacer2, App.Vector(0,50,0)) ]) ]))

  ##### Add battery holder (the closed one, not our generated one)
  battery_pack = mirte_assembly.import_object("external", "battery_pack_assembly.step", App.Vector(7.7, 5.9, 32.3), App.Rotation(90,0,0))
  mirte_assembly.addStep(gen.Step(battery_pack, App.Vector(0,50,0)))


#####################################
####    ADD PCB OR BREADBOARD
#####################################

if type == "pcb":
  ### Assemble PCB with pico
  pcb_assembly = gen.AssemblyProject("PCB", False)
  pcb = pcb_assembly.import_object("external", "mirte_pcb.step", App.Vector(91, 46, 91.5), App.Rotation(0,180,-90)) # + name
  pipico = pcb_assembly.import_object("external", "PICO_PinsDown.STEP", App.Vector(-16.5, 58, -31.5), App.Rotation(0,180,0))
  mirte_assembly.addWarning("pipico")
  pcb_assembly.addStep(gen.Step(pipico, App.Vector(0,40,0)))
  pcb_assembly.save_image_new_parts()

  ### Assemble PCB with motor controller
  motordriver = pcb_assembly.import_object("external", "I9110 motor driver.STEP", App.Vector(-38.5, 55, 41), App.Rotation(0,90,0))
  mirte_assembly.addWarning("pins")
  pcb_assembly.addStep(gen.Step(motordriver, App.Vector(0,40,0)))
  pcb_assembly.save_image_new_parts()
  pcb_assembly.close(True)
  
  ### Add PCB to OPi
  if mirte == "pioneer":
    pcb_step = mirte_assembly.import_object("build", "PCB.step", App.Vector(-104, 2,0), App.Rotation(-90,0,0))
    mirte_assembly.addWarning("pins")
  else:
    pcb_step = mirte_assembly.import_object("build", "PCB.step", App.Vector(-17.1, -42.8,0), App.Rotation(0,0,0))
  mirte_assembly.addStep(gen.Step(pcb_step, App.Vector(0,50,0)))
  mirte_assembly.save_image_new_parts()

else:
  breadboard_assembly = gen.AssemblyProject("Breadboard", False)
  breadboard = breadboard_assembly.import_object("external", "BreadBoard.STEP", App.Vector(0, 0, 0), App.Rotation(0, 0, 0))
  motordriver = breadboard_assembly.import_object("external", "I9110 motor driver.STEP", App.Vector(7.8, 13.9, 38), App.Rotation(0,90,0))
  breadboard_assembly.addStep(gen.Step(motordriver, App.Vector(0,50,0)))
  breadboard_assembly.save_image_new_parts()
  breadboard_assembly.close(True)

  breadboard_step = mirte_assembly.import_object("build", "BreadBoard.step", App.Vector(-53.2, 0,0), App.Rotation(0,-90,0))

#####################################
####    ADD POWERBANK
#####################################

if battery == "aa":
  mirte_assembly.setView("top")
else:
  ###### Powerbank
  powerbank = mirte_assembly.import_object("external", "dummy_powerbank.step", App.Vector(-76, 36, 0), App.Rotation(0,90,0))
  mirte_assembly.addStep(gen.Step(powerbank, App.Vector(0,100,0)))
  mirte_assembly.save_image_new_parts()


#####################################
####    EXPORT STEP
#####################################
gen.save_image()
mirte_assembly.close(True)

