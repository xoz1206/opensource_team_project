from ev3dev.ev3 import*

mB = LargeMotor('outB') # left
mC = LargeMotor('outC') # right

x = 0
r = 0

# need image size
Center_x = 0
#Center_y = 0
Config_r = 50

try:
    while True:
        #file read
        f = open("red_ball_info.txt",'r')
        line = f.readline() # location x
        if(line != ''): x = int(line)
        else: x = 0
        line = f.readline() # radius r
        if(line != ''): r = int(line)
        else: r = 0
        line = f.readline() # image width
        if(line != ''): Center_x = int(line) / 2
        else: Center_x = 0

        f.close()
        # no receive information
        if (x == 0 and r == 0 and Center_x == 0): 
            mB.run_to_rel_pos(position_sp=360, speed_sp = 0)
            mC.run_to_rel_pos(position_sp=360, speed_sp = 0)
        
        # ball location is right
        if (x - Center_x) > 5:
            # ball is far
            if Config_r > r:
                # move to right go
                mB.run_to_rel_pos(position_sp=360, speed_sp = 30)
                mC.run_to_rel_pos(position_sp=360, speed_sp = 15)
            # ball is near
            elif Config_r < r:
                # move to left back
                mB.run_to_rel_pos(position_sp=-360, speed_sp = 15)
                mC.run_to_rel_pos(position_sp=-360, speed_sp = 30)
            else:
                mB.stop(stop_action='brake')
                mC.stop(stop_action='brake')

        # ball location is left
        elif x-Center_x < -5:
            # ball is far
            if Config_r > r:
                # move to left go
                mB.run_to_rel_pos(position_sp=360, speed_sp = 15)
                mC.run_to_rel_pos(position_sp=360, speed_sp = 30)
            # ball is near
            elif Config_r < r:
                mB.run_to_rel_pos(position_sp=-360, speed_sp = 30)
                mC.run_to_rel_pos(position_sp=-360, speed_sp = 15)
            else:
                mB.stop(stop_action='brake')
                mC.stop(stop_action='brake')

        # ball location is center
        else:
            # ball is far
            if Config_r < r:
                mB.run_to_rel_pos(position_sp=360, speed_sp = 15)
                mC.run_to_rel_pos(position_sp=360, speed_sp = 15)
            # ball is near
            elif Config_r > r:
                mB.run_to_rel_pos(position_sp=-360, speed_sp = 15)
                mC.run_to_rel_pos(position_sp=-360, speed_sp = 15)
            else:
                mB.stop(stop_action='brake')
                mC.stop(stop_action='brake')
except KeyboardInterrupt:
    pass



