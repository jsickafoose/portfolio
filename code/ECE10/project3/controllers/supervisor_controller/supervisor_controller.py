"""supervisor_controller controller."""
from controller import Supervisor
from controller import Robot
from controller import Keyboard
from math import cos, sin, acos

def euler_axis(euler):
    c1 = cos(euler[0] / 2)
    c2 = cos(euler[1] / 2)
    c3 = cos(euler[2] / 2)
    s1 = sin(euler[0] / 2)
    s2 = sin(euler[1] / 2)
    s3 = sin(euler[2] / 2)
    
    x = s1 * s2 * c3 + c1 * c2 * s3
    y = s1 * c2 * c3 + c1 * s2 * s3
    z = c1 * s2 * c3 - s1 * c2 * s3
    
    angle = 2*acos(c1 * c2 * c3 - s1 * s2 * s3)
    
    return[x, y, z, angle]
     
def check_keyboard(key):
    global new_value_trans
    global euler_angles
    global translation_field
    global rotation_field
    if key != -1:
        if key == ord('Q') or key == ord('W') or key == ord('A') or key == ord('S') or key == ord('Z') or key == ord('X'): 
            if key == ord('Q'):
                new_value_trans[0] -= 0.01
                translation_field.setSFVec3f(new_value_trans)
            if key == ord('W'):
                new_value_trans[0] += 0.01
                translation_field.setSFVec3f(new_value_trans)
            if key == ord('A'):
                new_value_trans[1] -= 0.01
                translation_field.setSFVec3f(new_value_trans)
            if key == ord('S'):
                new_value_trans[1] += 0.01
                translation_field.setSFVec3f(new_value_trans)
            if key == ord('Z'):
                new_value_trans[2] -= 0.01
                translation_field.setSFVec3f(new_value_trans)
            if key == ord('X'):
                new_value_trans[2] += 0.01
                translation_field.setSFVec3f(new_value_trans)
                
        if key == keyboard.LEFT:
            euler_angles[0] -= 0.04
            rot = euler_axis(euler_angles)
            rotation_field.setSFRotation(rot)
        if key == keyboard.RIGHT:
            euler_angles[0] += 0.04
            rot = euler_axis(euler_angles)
            rotation_field.setSFRotation(rot)
            
        if key == keyboard.DOWN:
            euler_angles[2] += 0.04
            rot = euler_axis(euler_angles)
            rotation_field.setSFRotation(rot)
        if key == keyboard.UP:
            euler_angles[2] -= 0.04
            rot = euler_axis(euler_angles)
            rotation_field.setSFRotation(rot)
            
        if key == ord('.'):
            euler_angles[1] -= 0.04
            rot = euler_axis(euler_angles)
            rotation_field.setSFRotation(rot)
        if key == ord(','):
            euler_angles[1] += 0.04
            rot = euler_axis(euler_angles)
            rotation_field.setSFRotation(rot)


supervisor = Supervisor()  # create Supervisor instance


timestep = int(supervisor.getBasicTimeStep())


keyboard = Keyboard()

keyboard.enable(timestep)

target = supervisor.getFromDef('TARGET')
translation_field = target.getField('translation')
rotation_field = target.getField('rotation')

new_value_trans = [0.0, 0.0, 2.16, 0.0, 0.0, 0.0]

euler_angles = [0, 0, 0]
# print(dir(translation_field))

while supervisor.step(timestep) != -1:
    key = keyboard.getKey()
    check_keyboard(key)