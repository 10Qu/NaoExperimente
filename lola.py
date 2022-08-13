import socket
import msgpack
import time
import math

class Robot :
  def __init__ (self):
    self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    self.socket.connect( "/tmp/robocup" )
    self.joints = [
      "HeadYaw" ,
      "HeadPitch" ,
      "LShoulderPitch" ,
      "LShoulderRoll" ,
      "LElbowYaw" ,
      "LElbowRoll" ,
      "LWristYaw" ,
      "LHipYawPitch" ,
      "LHipRoll" ,
      "LHipPitch" ,
      "LKneePitch" ,
      "LAnklePitch" ,
      "LAnkleRoll" ,
      "RHipRoll" ,
      "RHipPitch" ,
      "RKneePitch" ,
      "RAnklePitch" ,
      "RAnkleRoll" ,
      "RShoulderPitch" ,
      "RShoulderRoll" ,
      "RElbowYaw" ,
      "RElbowRoll" ,
      "RWristYaw" ,
      "LHand" ,
      "RHand"
    ]
    self.sonars = [
      "Left" ,
      "Right" ,
    ]
    self.touch = [
      "ChestBoard/Button" ,
      "Head/Touch/Front" ,
      "Head/Touch/Middle" ,
      "Head/Touch/Rear" ,
      "LFoot/Bumper/Left" ,
      "LFoot/Bumper/Right" ,
      "LHand/Touch/Back" ,
      "LHand/Touch/Left" ,
      "LHand/Touch/Right" ,
      "RFoot/Bumper/Left" ,
      "RFoot/Bumper/Right" ,
      "RHand/Touch/Back" ,
      "RHand/Touch/Left" ,
      "RHand/Touch/Right" ,
    ]
    self.LEar = [
      "0" ,
      "36" ,
      "72" ,
      "108" ,
      "144" ,
      "180" ,
      "216" ,
      "252" ,
      "288" ,
      "324"
    ]

    self.REar = [
      "324" ,
      "288" ,
      "252" ,
      "216" ,
      "180" ,
      "144" ,
      "108" ,
      "72" ,
      "36" ,
      "0"
    ]

    self.actuators = {
      'Position' : self.joints,
      'Stiffness' : self.joints,
      'Chest' : [ 'Red' , 'Green' , 'Blue' ],
      'Sonar' : self.sonars,
      'LEar' : self.LEar,
      'REar' : self.REar,
      'LEye' : [ 0.0 ] * 24,
      'REye' : [ 0.0 ] * 24
    }
    

    self.commands = {
      'Position' : [ 0.0 ] * 25 ,
      'Stiffness' : [ 0.0 ] * 25 ,
      'Chest' : [ 0.0 ] * 3 ,
      'LEye' : [ 0.0 ] * 24 ,
      'REye' : [ 0.0 ] * 24 ,
      'Sonar' : [ True , True ] ,
      'LEar' : [ 0.0 ] * 10 ,
      'REar' : [ 0.0 ] * 10
    }
    
  def read (self):
    stream = self.socket.recv( 896 )
    upacker = msgpack.unpackb(stream, raw=False)
    return upacker
    
  def command (self, category, device, value):
    self.commands[category][self.actuators[category].index(device)] = value

  def send (self):
    stream = msgpack.packb(self.commands)
    self.socket.send(stream)
    
  def close (self):
    self.socket.close()
    
def set_red_eyes():
  eye_data = [ 0.0 ] * 24
  for i in range(0, 8):
    eye_data[i] = 1.0

  return eye_data

def set_green_eyes():
  eye_data = [ 0.0 ] * 24
  for i in range(8, 16):
    eye_data[i] = 1.0

  return eye_data

def set_blue_eyes():
  eye_data = [ 0.0 ] * 24
  for i in range(16, 24):
    eye_data[i] = 1.0

  return eye_data

def set_green_red_eyes():
  eye_data = [0.0] * 24
  for i in range(3, 16):
    eye_data[i] = 1.0
  
  return eye_data

def blink():
  current_time = int(time.time() / 10)
  if current_time % 3 == 0:
    return set_blue_eyes()
  if current_time % 3 == 1:
    return set_green_eyes()
  if current_time % 3 == 2:
    return set_red_eyes()

def set_rainbow_eyes():
  # TODO rotating does not seem to work really well because its not symmetric
  eye_data = [ 0.0 ] * 24
  eye_data[0] = 1.0
  eye_data[3] = 1.0
  eye_data[6] = 1.0
  eye_data[9] = 1.0
  eye_data[12] = 1.0
  eye_data[15] = 1.0
  eye_data[18] = 1.0
  eye_data[21] = 1.0

  current_time = int(time.time()* 10)
  if current_time % 3 == 0:
    return eye_data[-1:] + eye_data[:-1]

  return eye_data

def test_rotation_eyes():
  current_time = int(time.time()* 10)
  rotation_offset = current_time % 8
  arr1=[0.0] *24
  # red
  arr1[(0 + rotation_offset) % 8] = 1.0
  arr1[(3 + rotation_offset) % 8] = 1.0
  #arr1[(6 + rotation_offset) % 8] = 1.0
  # blue
  #arr1[8 + (2 + rotation_offset) % 8] = 1.0
  #arr1[8 + (5 + rotation_offset) % 8] = 1.0
  #arr1[8 + (7 + rotation_offset) % 8] = 1.0
  # green
  #arr1[16 + (1 + rotation_offset) % 8] = 1.0
  #arr1[16 + (4 + rotation_offset) % 8] = 1.0

  return arr1

def set_blue_ears():
  ear_data = [ 0.0 ] * 10
  for i in range(0, 9):
    ear_data[i] = 1.0

  return ear_data

def half_blue_ears():
  ear_data = [ 0.0 ] * 10
  for i in range(0, 5):
    ear_data[i] = 1.0

  return ear_data

def rotate_ears():
  ear_data = [ 0.0 ] * 10
  ear_data[1] = 1.0

  current_time = int(time.time())
  if current_time % 10 == 0:
    return ear_data[-1:] + ear_data[:-1]

  return ear_data

def main ():
  robot = Robot()
  try :
    #robot.command( "Position" , "HeadYaw" , 0.0 )
    #robot.command( "Position" , "HeadPitch" , 0.0 )
    #robot.command( "Stiffness" , "HeadYaw" , 1.00 )
    #robot.command( "Stiffness" , "HeadPitch" , 1.00 )
    ear_completion = 0
    head_pitch = 0.0

    while True :
      data = robot.read()
      positions_value = data[ "Position" ]
      positions = {}
      for index,name in enumerate (robot.joints):
        positions[name] = positions_value[index]
      sonars_value = data[ "Sonar" ]
      distances = {}
      for index,name in enumerate (robot.sonars):
        distances[name] = sonars_value[index]
      #print(distances)
      touch_value = data[ "Touch" ]
      touch = {}
      for index,name in enumerate (robot.touch):
        touch[name] = touch_value[index]
      if touch[ 'Head/Touch/Front' ] == True :
        if ear_completion <= 9.0 :
          ear_completion += 0.1
        if head_pitch <= 1.0 :
          head_pitch += 0.01
      elif touch[ 'Head/Touch/Rear' ] == True :
        if ear_completion > 0.0 :
          ear_completion -= 0.1
        if head_pitch >= -1.0 :
          head_pitch -= 0.01
          
      #robot.commands[ 'LEar' ] = [ 1.0 if n <= int (ear_completion) else 0.0 for n in range ( 0 , 10 )]
      #robot.commands[ 'LEar' ][ int (ear_completion)] = float (ear_completion - int (ear_completion))
      #robot.commands[ 'REar' ] = [ 1.0 if n <= int (ear_completion) else 0.0 for n in range ( 0 , 10 )]
      #robot.commands[ 'REar' ][ int (ear_completion)] = float (ear_completion - int (ear_completion))
      #robot.command( "Chest" , "Red" , abs (math.sin( 2 *time.time())))
      #robot.command( "Chest" , "Blue" , abs (math.sin( 2 *time.time())))
      #robot.command( "Position" , "HeadPitch" , head_pitch)


      robot.commands[ 'LEye' ] = (set_rainbow_eyes)
      robot.commands[ 'REye' ] = (set_green_eyes) 
      robot.commands[ 'REar' ] = (half_blue_ears)

      robot.send()
  except KeyboardInterrupt :
    print("Exit")
  finally :
    robot.close()
  
if __name__ == "__main__" :
  main()
