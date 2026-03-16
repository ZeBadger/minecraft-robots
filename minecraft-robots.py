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
    """Represents the player in the Minecraft world."""


    def __init__(self, mc):
        """Initialize player position and alive status."""
        ppos = mc.player.getPos()
        self.alive = True
        self.x = ppos.x
        self.y = ppos.y
        self.z = ppos.z

    def wherePlayer(self, mc):
        """Update player position and print it."""
        ppos = mc.player.getPos()
        self.x = int(ppos.x)
        self.y = int(ppos.y)
        self.z = int(ppos.z)
        print(f"p: x = {self.x} z = {self.z} y = {self.y}")

#robot class 

class Robot:
    """Represents a robot enemy in the Minecraft world."""
    robotCount = 0
    numDeadRobots = 0

    def __init__(self, mc):
        """Initialize robot at a random position."""
        self.mc = mc
        self.alive = True
        self.x = random.randrange(-186, 68)
        self.y = 0
        self.y2 = 1
        self.z = random.randrange(-63, 191)
        Robot.robotCount += 1

    def displayCount(self):
        """Print the total number of robots."""
        print(f"Number of robots = {Robot.robotCount}")

    def whereRobot(self):
        """Print the robot's current position and status."""
        print(f"r: x = {self.x} z = {self.z} y = {self.y} y2 = {self.y2} alive = {self.alive}")

    def kill(self):
        """Kill the robot and replace its blocks with stone."""
        if self.alive:
            Robot.numDeadRobots += 1
            self.alive = False
        self.mc.setBlock(self.x, self.y, self.z, block.STONE)
        self.mc.setBlock(self.x, self.y2, self.z, block.STONE)
        

    def moveRobot(self, player):
        """Move the robot towards the player and update its position in the world."""
        if not self.alive:
            return

        # Remove robot's previous blocks
        self.mc.setBlock(self.x, self.y, self.z, block.AIR)
        self.mc.setBlock(self.x, self.y2, self.z, block.AIR)

        # Move towards player
        if player.x > self.x:
            self.x += 1
        if player.x < self.x:
            self.x -= 1

        if player.y > self.y:
            self.y += 1
            self.y2 += 1
        if player.y < self.y:
            self.y -= 1
            self.y2 -= 1

        if player.z > self.z:
            self.z += 1
        if player.z < self.z:
            self.z -= 1

        # Check if robot caught the player
        if (player.x == self.x) and ((player.y == self.y) or (player.y == self.y2)) and (player.z == self.z):
            player.alive = False

        # Place robot's new blocks
        self.mc.setBlock(self.x, self.y, self.z, block.IRON_BLOCK)
        self.mc.setBlock(self.x, self.y2, self.z, block.NETHER_REACTOR_CORE)


# Main program
if __name__ == "__main__":
    mc = minecraft.Minecraft.create()
    player = Player(mc)

    num_robots = 10
    robots = []
    for _ in range(num_robots):
        robots.append(Robot(mc))

    robots[0].displayCount()

    # Game intro
    mc.postToChat("MCPI Robots! by ZeBadger (www.zebadger.com)")
    mc.postToChat("")
    mc.postToChat(f"I spy {num_robots} robots coming to get you!")
    mc.postToChat("They are unstoppable, except when they crash into")
    mc.postToChat("each other.  Can you survive?")
    time.sleep(5)
    mc.postToChat("3...")
    time.sleep(1)
    mc.postToChat("...2...")
    time.sleep(1)
    mc.postToChat("...1...")
    time.sleep(1)
    mc.postToChat("...Go!")
    time.sleep(1)

    # Main game loop
    while True:
        player.wherePlayer(mc)
        for r in range(num_robots):
            robots[r].moveRobot(player)
            robots[r].whereRobot()
            # Check for robot collisions
            for c in range(num_robots):
                if c != r:
                    if (
                        robots[r].x == robots[c].x and
                        (robots[r].y == robots[c].y or robots[r].y == robots[c].y2) and
                        robots[r].z == robots[c].z
                    ):
                        robots[r].kill()
                        robots[c].kill()

        time.sleep(0.3)

        if not player.alive:
            mc.postToChat("The robots got you!")
            break

        if Robot.numDeadRobots == num_robots:
            mc.postToChat("You win!")
            break

    # Clean up all robots
    for r in range(num_robots):
        robots[r].kill()

    mc.postToChat("Game Over")
