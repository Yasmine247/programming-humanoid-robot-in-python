'''In this exercise you need to implement an angle interploation function which makes NAO executes keyframe motion

* Tasks:
    1. complete the code in `AngleInterpolationAgent.angle_interpolation`,
       you are free to use splines interploation or Bezier interploation,
       but the keyframes provided are for Bezier curves, you can simply ignore some data for splines interploation,
       please refer data format below for details.
    2. try different keyframes from `keyframes` folder

* Keyframe data format:
    keyframe := (names, times, keys)
    names := [str, ...]  # list of joint names
    times := [[float, float, ...], [float, float, ...], ...]
    # times is a matrix of floats: Each line corresponding to a joint, and column element to a key.
    keys := [[float, [int, float, float], [int, float, float]], ...]
    # keys is a list of angles in radians or an array of arrays each containing [float angle, Handle1, Handle2],
    # where Handle is [int InterpolationType, float dTime, float dAngle] describing the handle offsets relative
    # to the angle and time of the point. The first Bezier param describes the handle that controls the curve
    # preceding the point, the second describes the curve following the point.
'''


from turtle import delay
from pid import PIDAgent
from keyframes import hello


class AngleInterpolationAgent(PIDAgent):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(AngleInterpolationAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)
        self.keyframes = ([], [], [])

    def think(self, perception):
        target_joints = self.angle_interpolation(self.keyframes, perception)
        self.target_joints.update(target_joints)
        return super(AngleInterpolationAgent, self).think(perception)

    def angle_interpolation(self, keyframes, perception):
        target_joints = {}
        # YOUR CODE HERE
        
        # check if the Keyframe is empty => ERROR
        if (self.keyframes == ([],[],[])):
            return target_joints

        names, times, keys = keyframes
        self.start_time = -1
        #First case
        if(self.start_time == -1):
            self.start_time = perception.time
        
        delay = perception.time - self.start_time
        
        skipped_joints =0
        
        # Iteration over joint names
        for(i, name) in enumerate(names):
            skipped_kf =0
            min_time =0
            max_time=0
            joint_time= times[i]
            
            # skip joint if it's out of time 
            if (joint_time[-1] < delay):
                skipped_joints +=1
                # if we reach the end of the list
                if (skipped_joints == len (name)):
                    # then reset parameters
                    self.start_time = -1
                    self.keyframes =([],[],[])
                    continue

            # Iteration over time list to find the corresponding timeslot    
            for j in range (len(joint_time)):
                max_time = joint_time[j]
                
                if ((min_time <= delay and delay <= max_time)):
                    skipped_kf = j
                    break
                min_time = max_time

            #Points definition for Bezier
            if(skipped_kf == 0):
                p0 =0
                p1 =0
                p3= keys[i][0][0]
                p2 = p3+ keys[i][0][1][2]

            else:
                p0 = keys[i][skipped_kf -1][0]
                p3 = keys[i][skipped_kf][0]
                p1 = p0 + keys[i][skipped_kf -1][1][2]
                p2=  p3 + keys[i][skipped_kf][1][2]
            
            # Bezier formal
            t = (delay- min_time) / (max_time - min_time)
            if t > 1 : t =1
            elif t <0 : t=0
            
            angle = ((1-t)**3)*p0 + 3*t*((1-t)**2)*p1 + 3*(t**2)*(1-t)*p2 + (t**3)*p3
        

            # Error correction caused by the simulation
            if(name == "LHipYawPitch"):
                target_joints["RHipYawPitch"] = angle

            target_joints[name] = angle

        return target_joints

if __name__ == '__main__':
    agent = AngleInterpolationAgent()
    agent.keyframes = hello()  # CHANGE DIFFERENT KEYFRAMES
    agent.run()
