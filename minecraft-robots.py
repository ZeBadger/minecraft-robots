# Raspberry Pi Minecraft 3d Robots
#
# Cobbled together in a few hours by ZeBadger (www.zebadger.com)
# with the help of Emzie, Chloe, Daniel and Sarah
#
# Credits to www.stuffaboutcode.com

#import the minecraft.py module from the minecraft directory
import minecraft.minecraft as minecraft
#import minecraft block module
import minecraft.block as block
#import time, so delays can be used
import time
#import random module to create random number
import random

#player class
class Player:

    def __init__(self, mc):
        ppos=mc.player.getPos()
        self.alive = True
        self.x=ppos.x
        self.y=ppos.x
        self.z=ppos.z

    def wherePlayer(self,mc):
        ppos=mc.player.getPos()
        self.x=int(ppos.x)
        self.y=int(ppos.y)
        self.z=int(ppos.z)
        print "p: x = " , self.x , " z = " , self.z , " y = " , self.y 

#robot class 
class Robot:
    robotCount=0
    numDeadRobots=0

    def __init__(self, mc):
        self.mc = mc
        self.alive = True
        self.x = random.randrange(-186,68)
        self.y = 0
        self.y2 = 1
        self.z = random.randrange(-63,191)
        Robot.robotCount += 1

    def displayCount(self):
        print "Number of robots = %d" % Robot.robotCount

    def whereRobot(self):
        print "r: x = " , self.x , " z = " , self.z , " y = " , self.y , " y2 = " , self.y2 , " alive = ", self.alive

    def kill(self):
        if (self.alive == True):
            Robot.numDeadRobots += 1
            self.alive = False
        self.mc.setBlock(self.x,self.y,self.z,block.STONE)
        self.mc.setBlock(self.x,self.y2,self.z,block.STONE)
        

    def moveRobot(self,player):
        if (self.alive == False):
            return

        self.mc.setBlock(self.x,self.y,self.z,block.AIR)
        self.mc.setBlock(self.x,self.y2,self.z,block.AIR)

        if (player.x > self.x):
            self.x += 1
        if (player.x < self.x):
            self.x -= 1

        if (player.y > self.y):
            self.y += 1
            self.y2 += 1

        if (player.y < self.y):
            self.y -= 1
            self.y2 -= 1

        if (player.z > self.z):
            self.z += 1
        if (player.z < self.z):
            self.z -= 1

        if (player.x == self.x) and ( (player.y == self.y) or (player.y == self.y2) ) and (player.z == self.z):
            player.alive = False

        self.mc.setBlock(self.x,self.y,self.z,block.IRON_BLOCK)
        self.mc.setBlock(self.x,self.y2,self.z,block.NETHER_REACTOR_CORE)


#main program
if __name__ == "__main__":

    mc = minecraft.Minecraft.create()
    #constants
    player = Player(mc)

    numRobots=10
    robot = []
    for r in range (0, numRobots):
        robot.append(Robot(mc))

    robot[0].displayCount()
    
    mc.postToChat("MCPI Robots! by ZeBadger (www.zebadger.com)")
    mc.postToChat((""))
    mc.postToChat(("I spy " + str(numRobots) + " robots coming to get you!"))
    mc.postToChat(("They are unstoppable, except when they crash into"))
    mc.postToChat(("each other.  Can you survive?"))
    time.sleep(5)
    mc.postToChat(("3..."))
    time.sleep(1)
    mc.postToChat(("...2..."))
    time.sleep(1)
    mc.postToChat(("...1..."))
    time.sleep(1)
    mc.postToChat(("...Go!"))
    time.sleep(1)
    while True :
        player.wherePlayer(mc)
        for r in range (0, numRobots):
            robot[r].moveRobot(player)
            robot[r].whereRobot()
            # Now check collisions
            for c in range (0, numRobots):
                if (c != r):
                    if (robot[r].x == robot[c].x) and ( (robot[r].y == robot[c].y) or (robot[r].y == robot[c].y2) ) and (robot[r].z == robot[c].z):
                        robot[r].kill()
                        robot[c].kill()

        time.sleep(.3)

        if (player.alive != True):
            mc.postToChat("The robots got you!")
            break

        if (Robot.numDeadRobots == numRobots):
            mc.postToChat("You win!")
            break

    for r in range (0, numRobots):
        robot[r].kill()

    mc.postToChat("Game Over")
