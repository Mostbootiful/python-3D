######################################
#        Omar                        #
#        2/17/2024                   #
#        3D Engine v2                #
######################################
import math
import time
import keyboard
from turtle import *

# Setup Canvas
screen_width, screen_height = 1280, 720

canvas = Screen()
canvas.setup(screen_width, screen_height)
#screensize(screen_width, screen_height)
#canvas.setworldcoordinates(-screen_width, -screen_height, screen_width, screen_height)

# Set Turtle commands to Turtle version
onclick = canvas.onscreenclick
turtle_speed = speed
hide_turtle = hideturtle
clear_canvas = clear
pen_up = penup
pen_down = pendown
begin__fill = begin_fill
end__fill = end_fill
set_position = setposition
write_text = write
set_color = color
bg_color = bgcolor
pen_size = pensize
turtle_tracer = tracer
turtle_update = update
turtle_mainloop = mainloop

######################################## Main Program ########################################
class Game:
    # Initialization
    def __init__(self):
        global world, findObject
        world, findObject = engine.World, engine.World.findObject

        world.Dampining = vec3(.86, .98, .86)
        world.Gravity = world.Gravity / 8

        engine.Renderer.Wireframe = False
        engine.Renderer.fastRender = True
        engine.Renderer.lineSize = 1

        # Setup Controls
        self.baseCameraControls = self.BaseCameraControls()
        self.baseCameraControls.JumpHeight = 40

        # Camera settings
        engine.Camera.Anchored = True
        engine.Camera.Position = vec3(-0, 2.1, -20)  # vec3(12.0, 15, -12.0)
        engine.Camera.Rotation = vec3(-rot(30), 0, 0)  # vec3(-rot(15), rot(-45.11), rot(0))
        engine.Camera.lookVelocity = vec3(.0315, 0, rot(0))
        engine.Camera.Origin = vec3(0, .75, 0)
        engine.Camera.nearPlane = 1
        engine.Camera.farPlane = 600
        engine.Camera.Speed = .04
        engine.Camera.lookDampining = .88
        engine.Camera.Sensitivity = .4

        # Crosshair
        crosshairSize = 4
        Crosshair = engine.Objects.Object2D("Crosshair").addToWorld()
        Crosshair.Verticies = [
            vector(vec2(0, crosshairSize), vec2(0, -crosshairSize)),
            vector(vec2(crosshairSize, 0), vec2(-crosshairSize, 0))
        ]

        # Create Objects
        self.TestLevel()

    ##############################################################################################
    # Update
    def update(self, delta, clock):
        world.Sun = vec3(sine(rot(clock * 75)), cosine(rot(clock)) * 1, cosine(rot(clock * 75)))#.normalize()

        Cube = findObject("Cube")
        Cube2 = findObject("Cube2")

        # Animate Objects
        Cube2.Rotation = vec3(rot(clock * 0), rot(clock * -45), rot(clock * 0))
        # Cube.Position = vec3(sine(rot(clock * 25)) * 15, 2, cosine(rot(clock * 25)) * 15)
        # Cube2.Rotation = vec3(-rot(clock * 50), -rot(clock * 50), -rot(clock * 50))
        self.baseCameraControls.listen()
    # Level
    def TestLevel(self):
        plane = engine.Objects.Shapes.Plane().addToWorld()  # .hide()
        plane.Triangles = []
        plane.Position = vec3(0, -10, 0)
        plane.Origin = vec3(0, -0, 1)
        plane.Rotation = vec3(rot(90), 0, 0)
        plane.Size = vec3(4, 4, 5)
        plane.Color = vec3(65, 152, 10)

        a = 2
        for i in range(-a, a):
            for j in range(-a, a):
                quad = [
                    triangle(vec3(-1, -1, 0), vec3(-1, 1, 0), vec3(1, 1, 0)),
                    triangle(vec3(-1, -1, 0), vec3(1, 1, 0), vec3(1, -1, 0)),
                ]
                offset = ((vec3(i, j, 0) + vec3(.5, .5, 0)) * 2)

                quad[0].p1 += offset
                quad[0].p2 += offset
                quad[0].p3 += offset

                quad[1].p1 += offset
                quad[1].p2 += offset
                quad[1].p3 += offset

                plane.Triangles.append(quad[0])
                plane.Triangles.append(quad[1])

        def f(z):
            a = (math.log(z + 2) ** .9) * 3; return a - (a / 2)  # (abs(z)**1.1)/2

        for tri in plane.Triangles:
            tri.p1.z = f(sqrt(tri.p1.x ** 2 + tri.p1.y ** 2))
            tri.p2.z = f(sqrt(tri.p2.x ** 2 + tri.p2.y ** 2))
            tri.p3.z = f(sqrt(tri.p3.x ** 2 + tri.p3.y ** 2))

        Cube = engine.Objects.Shapes.Cube().addToWorld()#.hide()
        Cube.Position = vec3(10, 0, -5)
        Cube.Origin = vec3(0, 0, 0)
        Cube.Color = vec3(150, 150, 255)
        Cube.Size = vec3(2, 2, 2)

        # Cube.Anchored = False

        Cube2 = engine.Objects.Shapes.Cube().addToWorld()#.hide()
        Cube2.Name = "Cube2"
        Cube2.Position = vec3(-10, 1, -5)
        Cube2.Origin = vec3(0, 0, 0)
        Cube2.Color = vec3(255, 100, 20)
        Cube2.Size = vec3(2, 3, 2)

        cone = engine.Objects.Shapes.Cone().addToWorld()#.hide()
        cone.Size = vec3(2, 2, 2)

    # Controls
    class BaseCameraControls:
        def __init__(self):
            self.Camera = engine.Camera
            self.Camera.Sensitivity = .85

            self.JumpHeight = 30

            onclick(self.processMouseInput)

            onkeypress(self.toggleInfo, "h")
            onkeypress(self.changeMode, "b")
            onkeypress(self.toggleWireframe, "v")
            onkeypress(self.toggleNormals, "n")
            onkeypress(self.toggleLighting, "l")
            onkeypress(self.chooseFov, "f")

            # Display Controls
            print("WASD to move around")
            print("Arrow Keys/Click on Canvas to look around")
            print("b to change Camera Mode")
            print("f to change FOV")
            print("l to toggle Lighting")
            print("v to toggle Wireframe")
            print("n to toggle Normals")
            print("h to toggle Info")

        def listen(self):
            key(self.lookup, "Up")
            key(self.lookdown, "Down")
            key(self.lookright, "Right")
            key(self.lookleft, "Left")

            key(self.forward, "w")
            key(self.backward, "s")

            key(self.right, "d")
            key(self.left, "a")

            if self.Camera.Anchored:
                key(self.up, "e")
                key(self.down, "q")
            else:
                key(self.jump, "space")
        def processMouseInput(self, x, y):
            lvel = self.Camera.lookVelocity
            sens = self.Camera.Sensitivity
            fov = self.Camera.fov
            rotx = rot((pi / 180) * (x * sens))
            roty = -rot((pi / 180) * (y * sens))
            if fov > 201:
                rotx = (rotx * 201) / fov
                roty = (roty * 201) / fov
            self.Camera.lookVelocity = vec3(lvel.x + roty, lvel.y + rotx, lvel.z)

        def lookup(self, a=-1):
            lvel = self.Camera.lookVelocity
            sens = self.Camera.Sensitivity
            if self.Camera.fov > 201:
                sens = (sens * 201) / self.Camera.fov
            self.Camera.lookVelocity = vec3(lvel.x + rot(sens * a), lvel.y, lvel.z)

        def lookdown(self):
            self.lookup(1)

        def lookright(self, a=1):
            lvel = self.Camera.lookVelocity
            sens = self.Camera.Sensitivity
            if self.Camera.fov > 201:
                sens = (sens * 201) / self.Camera.fov
            self.Camera.lookVelocity = vec3(lvel.x, lvel.y + rot(sens * a), lvel.z)

        def lookleft(self):
            self.lookright(-1)

        def tiltright(self, a=1):
            lvel = self.Camera.lookVelocity
            sens = self.Camera.Sensitivity
            self.Camera.lookVelocity = vec3(lvel.x, lvel.y, lvel.z + rot(((sens * 201) / self.Camera.fov) * -a))

        def tiltleft(self):
            self.tiltright(-1)

        def forward(self, a=1, b=-1, c=None, s=None):
            if not (c or s): c = cosine; s = sine
            vel = self.Camera.Velocity
            crot = self.Camera.Rotation
            speed = self.Camera.Speed
            z = (c(crot.y) * speed) * -1
            x = (s(crot.y) * speed) * b
            self.Camera.Velocity = vec3(vel.x - (x * a), vel.y, vel.z - (z * a))

        def backward(self):
            self.forward(-1)

        def right(self, a=-1, b=1):
            self.forward(a, 1, sine, cosine)

        def left(self):
            self.right(1)

        def jump(self):
            if engine.Camera.Anchored: return
            vel = self.Camera.Velocity
            if abs(vel.y) > 0.5: return
            self.Camera.Velocity = vec3(vel.x, vel.y + self.JumpHeight, vel.z)

        def up(self, a=1):
            vel = self.Camera.Velocity
            speed = self.Camera.Speed
            self.Camera.Velocity = vec3(vel.x, vel.y + (speed * a), vel.z)

        def down(self):
            self.up(a=-1)

        def jump(self):
            if engine.Camera.Anchored: return
            vel = self.Camera.Velocity
            if abs(vel.y) > 0.5: return
            self.Camera.Velocity = vec3(vel.x, vel.y + self.JumpHeight, vel.z)

        def up(self, a=1):
            vel = self.Camera.Velocity
            speed = self.Camera.Speed
            self.Camera.Velocity = vec3(vel.x, vel.y + (speed * a), vel.z)

        def down(self):
            self.up(a=-1)

        def chooseFov(self):
            newfov = float(numinput("Input", "Input a Field of View: \n"))
            canvas.listen()
            if not newfov: return
            newfov = 240 / (math.tan(rot(newfov / 2)))
            self.Camera.fov = newfov

        def toggleInfo(self):
            engine.Renderer.drawInfoEnabled = not engine.Renderer.drawInfoEnabled

        def changeMode(self):
            engine.Camera.Anchored = not engine.Camera.Anchored
            self.Camera.Velocity = vec3(0, 0, 0)
            if engine.Camera.Anchored:
                engine.Camera.Speed *= .03
            else:
                engine.Camera.Speed = engine.Camera.Speed / .03

        def toggleLighting(self):
            engine.Renderer.Lighting = not engine.Renderer.Lighting

        def toggleWireframe(self):
            engine.Renderer.Wireframe = not engine.Renderer.Wireframe

        def toggleNormals(self):
            engine.Renderer.drawNormals = not engine.Renderer.drawNormals

# I Recommend Collapsing the Engine Class for better readability
########################################### Engine ###########################################
class Engine:
    def __init__(self):
        # Set Turtle Settings
        turtle_speed(0)
        hide_turtle()

        # Globals
        self._createGlobals()

        # Create time trackers
        self.clock = float(0)
        self.delta = float(0.016)

        # Create Classes
        self.World = engine.WorldClass()
        self.Camera = engine.CameraClass(vec3(0, 0, -3.0), 201)
        self.Renderer = engine.RenderClass()

    def run(self, gameClass):
        # Run Game Initialization
        game = gameClass()

        # Listen for events
        canvas.listen()

        # Reset per_counter
        startingClock = time.perf_counter()

        # Start Game loop and call update
        while True:
            # Begin time tracking
            currentClock = time.perf_counter()

            # Update World
            self.World.update(self.delta)

            # Update will call before Rendering
            game.update(self.delta, self.clock)

            # Update Camera
            self.Camera.Update()

            # Render Scene
            self.Renderer.renderScene()

            # Track Time
            self.delta = time.perf_counter() - currentClock
            self.clock = time.perf_counter() - startingClock

            # Prevent Exhaustion
            if self.delta < 0.002:
                time.sleep(0.002)

    def _createGlobals(self):
        global engine
        engine = self

        global sine, cosine, sqrt, pi
        sine, cosine, sqrt, pi = math.sin, math.cos, math.sqrt, math.pi

        # Convert Degrees to radians
        def rad(theta):
            return (pi / 180) * theta

        global rot;
        rot = rad

        def Rgb2hex(color):
            color = color * vec3(255, 255, 255)
            if color.x < 20:
                color.x = 20
            elif color.x > 250:
                color.x = 250
            if color.y < 20:
                color.y = 20
            elif color.y > 250:
                color.y = 250
            if color.z < 20:
                color.z = 20
            elif color.z > 250:
                color.z = 250
            # print(color)
            hexid = "#{:02x}{:02x}{:02x}".format(int(color.x), int(color.y), int(color.z))
            # print(hexid)
            return hexid  #

        global rgb2hex;
        rgb2hex = Rgb2hex

        def Key(fun, key):
            if keyboard.is_pressed(key):
                fun()

        global key; key = Key

        global vec2, vec3, vector, triangle
        vec2, vec3, vector, triangle = engine.vec2, engine.vec3, engine.vector, engine.triangle

    ##############################################################################################
    # Vector Classes
    class vec2:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def __str__(self):
            x_y = "x:% s y:% s" % (self.x, self.y)
            if hasattr(self, "z"):
                x_y = x_y + " z:% s " % (self.z)
            return x_y

        def distanceFrom(self, vec):
            x = self.x - vec.x
            y = self.y - vec.y
            return sqrt(x ** 2 + y ** 2)

    class vec3(vec2):
        def __init__(self, x, y, z):
            vec2.__init__(self, x, y)
            self.z = z

        def __add__(self, vec):
            if type(vec) == float or type(vec) == int:
                return vec3(self.x + vec, self.y + vec, self.z + vec)
            return vec3(self.x + vec.x, self.y + vec.y, self.z + vec.z)

        def __iadd__(self, vec):
            return self.__add__(vec)

        def __sub__(self, vec):
            if type(vec) == float or type(vec) == int:
                return vec3(self.x - vec, self.y - vec, self.z - vec)
            return vec3(self.x - vec.x, self.y - vec.y, self.z - vec.z)

        def __mul__(self, vec):
            if type(vec) == float or type(vec) == int:
                return vec3(self.x * vec, self.y * vec, self.z * vec)
            return vec3(self.x * vec.x, self.y * vec.y, self.z * vec.z)

        def __truediv__(self, vec):
            if type(vec) == float or type(vec) == int:
                return vec3(self.x / vec, self.y / vec, self.z / vec)
            return vec3(self.x / vec.x, self.y / vec.y, self.z / vec.z)

        def __neg__(self):
            return self * vec3(-1, -1, -1)

        def distanceFrom(self, vec):
            x = self.x - vec.x
            y = self.y - vec.y
            z = self.z - vec.z
            return sqrt(x ** 2 + y ** 2 + z ** 2)

        def dot(self, vec):
            return (self.x * vec.x) + (self.y * vec.y) + (self.z * vec.z)

        def normalize(self):
            l = self * self
            l = sqrt(l.x + l.y + l.z)
            return self / l

        def lerp(self, vec, t):
            return self * t + vec * (1 - t)

        def cross(self, vec):
            v = vec3(0, 0, 0)
            v.x = (self.y * vec.z) - (self.z * vec.y)
            v.y = (self.z * vec.x) - (self.x * vec.z)
            v.z = (self.x * vec.y) - (self.y * vec.x)
            return v

    class vector():
        def __init__(self, vec0, vec1):
            self.vec0 = vec0
            self.vec1 = vec1

        def __str__(self):
            return vec2.__str__(self.vec0) + " | " + vec2.__str__(self.vec1)

    class triangle():
        def __init__(self, p1, p2, p3):
            self.p1 = p1
            self.p2 = p2
            self.p3 = p3

        def __str__(self):
            return vec2.__str__(self.p1) + " | " + vec2.__str__(self.p2) + " | " + vec2.__str__(self.p3)

        def normal(self):
            line1 = self.p2 - self.p1
            line2 = self.p3 - self.p1

            normal = vec3(0, 0, 0)
            normal.x = (line1.y * line2.z) - (line1.z * line2.y)
            normal.y = (line1.z * line2.x) - (line1.x * line2.z)
            normal.z = (line1.x * line2.y) - (line1.y * line2.x)
            return normal.normalize()

    ##############################################################################################
    # World Class
    class WorldClass:
        def __init__(self):
            self.Objects = {}
            self.Colliders = []

            self.Sun = vec3(1, 1, -1)
            self.SkyColor = "#87CEEB"

            self.Gravity = 9.81
            self.Dampining = .9
            self.CollisionAgressivness = .5

        def update(self, delta):
            # return
            self._getColliders()

            self._updateObjectPhysics(engine.Camera, delta)
            for o in self.Objects.values():
                if not o.non3d:
                    self._updateObjectPhysics(o, delta)

        def _updateObjectPhysics(self, o, delta):
            # return
            if o.Anchored: return
            orig = o.Origin
            pos = o.Position
            vel = o.Velocity
            damp = self.Dampining
            agg = self.CollisionAgressivness

            # Dampen Velocity
            o.Velocity = vec3(vel.x * damp.x, vel.y * damp.y, vel.z * damp.z)
            vel = o.Velocity
            # Apply Gravity
            o.Velocity = vec3(vel.x, vel.y - self.Gravity, vel.z)
            vel = o.Velocity

            newpos = self._getNewPosFromVel(pos, orig, vel, delta)
            xpos = vec3(pos.x + (newpos.x - pos.x), pos.y, pos.z)
            collide, dist = self._stepCollisionOnAxis(o.id, xpos, "x")
            if collide:
                xpos.x = dist.y
                vel.x = 0

            ypos = vec3(xpos.x, pos.y + (newpos.y - pos.y), pos.z)
            collide, dist = self._stepCollisionOnAxis(o.id, ypos, "y")
            if collide:
                ypos.y = dist.y
                vel.y = 0

            zpos = vec3(xpos.x, ypos.y, pos.z + (newpos.z - pos.z))
            collide, dist = self._stepCollisionOnAxis(o.id, zpos, "z")
            if collide:
                zpos.z = dist.y
                vel.z = 0

            # Apply Velocity
            o.Position = zpos

        def _stepCollisionOnAxis(self, id, pos, axis):
            for collider in self.Colliders:
                if collider.id == id: continue
                inbound, b = self._isInBoundingBox(collider.BoundingBox, pos)
                if inbound:
                    if not collider.CanCollide: continue
                    box = collider.BoundingBox
                    return True, self._getAxisDist(getattr(pos, axis), getattr(box.vec0, axis), getattr(box.vec1, axis))

            return False, None

        def _getAxisDist(self, a, b, c):
            dist = 0
            side = c
            percent = ((a - b) * 100) / (c - b)
            if percent >= 50:
                side = c
            else:
                side = b

            return vec3(dist, side, percent)

        def _isInBoundingBox(self, box, pos):
            x = (box.vec0.x < pos.x)
            x2 = (box.vec1.x > pos.x)
            y = (box.vec0.y < pos.y)
            y2 = (box.vec1.y > pos.y)
            z = (box.vec0.z < pos.z)
            z2 = (box.vec1.z > pos.z)
            return (x and y and z and x2 and y2 and z2), vector(vec3(x, y, z), vec3(x2, y2, z2))

        def _getNewPosFromVel(self, pos, orig, vel, delta):
            return vec3(pos.x + (orig.x + vel.x) * delta, pos.y + (vel.y) * delta, pos.z + (orig.z + vel.z) * delta)

        def _getColliders(self):
            self.Colliders = []
            for o in self.Objects.values():
                if not o.non3d:
                    if o.CanTouch:
                        o.getBoundingBox()
                        self.Colliders.append(o)

        def _addObject(self, Object):
            Object.id = len(self.Objects)
            self.Objects[Object.id] = Object

        def findObject(self, objectName):
            obj = None
            for o in self.Objects.values():
                if o.Name == objectName:
                    obj = o
            return obj  # self.Objects.get(objectName)

    ##############################################################################################
    # Object Classes
    class Objects:
        class BaseObject:
            def __init__(self, name):
                self.Name = name
                self.id = 0
                self.Color = "white"

                self.non3d = True
                self.hidden = False

            def addToWorld(self):
                engine.World._addObject(self)
                return self

            def remove(self):
                engine.World.Objects.pop(self.Name)

            def hide(self):
                self.hidden = True
                return self

            def show(self):
                self.hidden = False
                return self

        class Object2D(BaseObject):
            def __init__(self, name):
                engine.Objects.BaseObject.__init__(self, name)
                self.Position = vec2(0, 0)
                self.Origin = vec2(0, 0)
                self.Rotation = vec2(0, 0)
                self.Size = 1

                self.Color = vec3(255, 255, 255)

                self.non3d = True

                self.Verticies = []

            def getAppliedTransformations(self):
                return self.Verticies

        class Object3D(BaseObject):
            def __init__(self, name):
                engine.Objects.BaseObject.__init__(self, name)
                self.Position = vec3(0, 0, 0)
                self.Origin = vec3(0, 0, 0)
                self.Rotation = vec3(0, 0, 0)
                self.Size = vec3(1, 1, 1)

                self.Color = vec3(200, 200, 200)

                self.Velocity = vec3(0, 0, 0)
                self.BoundingBox = vector(vec3(0, 0, 0), vec3(1, 1, 1))
                self.OnTouch = None

                self.Anchored = True
                self.CanCollide = True
                self.CanTouch = True

                self.non3d = False

                self.Verticies = []
                self.Indicies = []

            def getAppliedTransformations(self, Cam=True):
                transformedTriangles = []
                for vec in self.Triangles:
                    tri = engine.Projection.transformObjectTriangle(vec, self, cam=Cam)
                    transformedTriangles.append(tri)
                return transformedTriangles

            def getBoundingBox(self):
                adder = 2
                xmax, ymax, zmax = 0, 0, 0
                xmin, ymin, zmin = 0, 0, 0
                for tri in self.getAppliedTransformations(Cam=False):

                    if tri.p1.x > xmax:
                        xmax = tri.p1.x;
                    elif tri.p1.x < xmin:
                        xmin = tri.p1.x
                    if tri.p1.y > ymax:
                        ymax = tri.p1.y
                    elif tri.p1.y < ymin:
                        ymin = tri.p1.y
                    if tri.p1.z > zmax:
                        zmax = tri.p1.z
                    elif tri.p1.z < zmin:
                        zmin = tri.p1.z

                    if tri.p2.x > xmax:
                        xmax = tri.p2.x;
                    elif tri.p2.x < xmin:
                        xmin = tri.p2.x
                    if tri.p2.y > ymax:
                        ymax = tri.p2.y
                    elif tri.p2.y < ymin:
                        ymin = tri.p2.y
                    if tri.p2.z > zmax:
                        zmax = tri.p2.z
                    elif tri.p2.z < zmin:
                        zmin = tri.p2.z

                    if tri.p3.x > xmax:
                        xmax = tri.p3.x;
                    elif tri.p3.x < xmin:
                        xmin = tri.p3.x
                    if tri.p3.y > ymax:
                        ymax = tri.p3.y
                    elif tri.p3.y < ymin:
                        ymin = tri.p3.y
                    if tri.p3.z > zmax:
                        zmax = tri.p3.z
                    elif tri.p3.z < zmin:
                        zmin = tri.p3.z
                self.BoundingBox = vector(
                    vec3(xmin - adder, ymin - adder, zmin - adder),
                    vec3(xmax + adder, ymax + adder, zmax + adder)
                )
                return self.BoundingBox

            def _touchSignal(self, o):
                if self.OnTouch:
                    self.OnTouch(o)

        class Shapes:
            def Plane():
                Plane = engine.Objects.Object3D("Plane")
                Plane.Color = vec3(200, 200, 200)
                Plane.Triangles = [
                    triangle(vec3(-1, -1, -1), vec3(-1, 1, -1), vec3(1, 1, -1)),
                    triangle(vec3(-1, -1, -1), vec3(1, 1, -1), vec3(1, -1, -1)),
                ]

                return Plane

            def Cube():
                Cube = engine.Objects.Object3D("Cube")
                Cube.Color = vec3(200, 200, 200)
                Cube.Triangles = [
                    triangle(vec3(-1, -1, -1), vec3(-1, 1, -1), vec3(1, 1, -1)),
                    triangle(vec3(-1, -1, -1), vec3(1, 1, -1), vec3(1, -1, -1)),

                    triangle(vec3(1, -1, -1), vec3(1, 1, -1), vec3(1, 1, 1)),
                    triangle(vec3(1, -1, -1), vec3(1, 1, 1), vec3(1, -1, 1)),

                    triangle(vec3(1, -1, 1), vec3(1, 1, 1), vec3(-1, 1, 1)),
                    triangle(vec3(1, -1, 1), vec3(-1, 1, 1), vec3(-1, -1, 1)),

                    triangle(vec3(-1, -1, 1), vec3(-1, 1, 1), vec3(-1, 1, -1)),
                    triangle(vec3(-1, -1, 1), vec3(-1, 1, -1), vec3(-1, -1, -1)),

                    triangle(vec3(-1, 1, -1), vec3(-1, 1, 1), vec3(1, 1, 1)),
                    triangle(vec3(-1, 1, -1), vec3(1, 1, 1), vec3(1, 1, -1)),

                    triangle(vec3(1, -1, 1), vec3(-1, -1, 1), vec3(-1, -1, -1)),
                    triangle(vec3(1, -1, 1), vec3(-1, -1, -1), vec3(1, -1, -1)),
                ]
                return Cube

            def Cone():
                Cone = engine.Objects.Object3D("Cone")
                Cone.Triangles = [
                    triangle(vec3(-1, -1, -1), vec3(1, -1, 1), vec3(-1, -1, 1)),
                    triangle(vec3(-1, -1, -1), vec3(1, -1, -1), vec3(1, -1, 1)),

                    triangle(vec3(-1, -1, -1), vec3(0, 2, 0), vec3(1, -1, -1)),
                    triangle(vec3(-1, -1, 1), vec3(1, -1, 1), vec3(0, 2, 0)),
                    triangle(vec3(1, -1, -1), vec3(0, 2, 0), vec3(1, -1, 1)),
                    triangle(vec3(-1, -1, -1), vec3(-1, -1, 1), vec3(0, 2, 0)),
                ]
                return Cone

            def Sphere(slices, stacks):
                Sphere = engine.Objects.Object3D("Sphere")

                def generateSphere(slices, stacks):
                    def createSpherePoint(i, j, phi):
                        theta = 2 * pi * j / slices
                        x = sine(phi) * cosine(theta)
                        y = cosine(phi)
                        z = sine(phi) * sine(theta)
                        return vec3(x, y, z)

                    for i in range(-1, stacks - 1):
                        phi = pi * (i + 1) / stacks
                        phi2 = pi * (i + 2) / stacks
                        for j in range(slices):
                            vec0 = createSpherePoint(i, j, phi)
                            vec1 = createSpherePoint(i, j, phi2)
                            vec2 = createSpherePoint(i - 1, j - 1, phi)

                            vector0 = vector(vec0, vec1)
                            vector1 = vector(vec0, vec2)
                            Sphere.Verticies.append(vector0)
                            Sphere.Verticies.append(vector1)

                generateSphere(slices, stacks)
                # Sphere.Size = 10
                return Sphere

    ##############################################################################################
    # Camera Class
    class CameraClass:
        def __init__(self, pos, fov):
            self.Position = pos
            self.Origin = vec3(0, 6, 0)
            self.Rotation = vec3(rot(10), rot(-20), rot(0))
            self.id = 0

            self.Sensitivity = .8
            self.Speed = .7

            self.Anchored = True
            self.Velocity = vec3(0, 0, 0)
            self.lookVelocity = vec3(0, 0, 0)

            # Smooths out Movement and Rotation to prevent choppiness. Closer to 1 is smoother
            self.Dampining = .9
            self.lookDampining = .94

            self.fov = fov
            self.nearPlane = 1
            self.farPlane = 100

            self.xClamp = True  # Prevents Camera from flipping upside-down

        def Update(self):
            pos = self.Position
            crot = self.Rotation
            vel = self.Velocity
            lvel = self.lookVelocity
            damp = self.Dampining
            ldamp = self.lookDampining

            # Apply Velocity
            self.Rotation = vec3(crot.x + lvel.x, crot.y + lvel.y, crot.z + lvel.z)

            # Apply Dampining
            self.lookVelocity = vec3((lvel.x * ldamp), (lvel.y * ldamp), (lvel.z * ldamp))

            # If not a physics object then move on its own
            if self.Anchored:
                self.Position = vec3(pos.x + vel.x, pos.y + vel.y, pos.z + vel.z)
                self.Velocity = vec3((vel.x * damp), (vel.y * damp), (vel.z * damp))

            if self.xClamp:
                crot = self.Rotation
                if crot.x > pi / 2.1: self.Rotation = vec3(pi / 2.1, crot.y, crot.z)
                if crot.x < -pi / 2.1: self.Rotation = vec3(-pi / 2.1, crot.y, crot.z)

    ##############################################################################################
    # Projection
    class Projection:
        def transformObjectTriangle(tri, Object, orig=True, size=True, rot=True, cam=False):
            camera = engine.Camera
            p1 = tri.p1
            p2 = tri.p2
            p3 = tri.p3

            pos = Object.Position
            cpos = camera.Position + camera.Origin
            orot = Object.Rotation
            size = Object.Size
            origin = Object.Origin

            # Apply Origin
            if orig:
                p1 = p1 - origin
                p2 = p2 - origin
                p3 = p3 - origin

            # Apply Object Size
            if size:
                p1 = p1 * size
                p2 = p2 * size
                p3 = p3 * size

            # Apply Object Rotation
            if rot:
                p1 = vec3(p1.x, (p1.y * cosine(orot.x)) - (p1.z * sine(orot.x)),
                          (p1.y * sine(orot.x)) + (p1.z * cosine(orot.x)))
                p2 = vec3(p2.x, (p2.y * cosine(orot.x)) - (p2.z * sine(orot.x)),
                          (p2.y * sine(orot.x)) + (p2.z * cosine(orot.x)))
                p3 = vec3(p3.x, (p3.y * cosine(orot.x)) - (p3.z * sine(orot.x)),
                          (p3.y * sine(orot.x)) + (p3.z * cosine(orot.x)))

                p1 = vec3((p1.x * cosine(orot.y)) + (p1.z * sine(orot.y)), p1.y,
                          (p1.z * cosine(orot.y)) - (p1.x * sine(orot.y)))
                p2 = vec3((p2.x * cosine(orot.y)) + (p2.z * sine(orot.y)), p2.y,
                          (p2.z * cosine(orot.y)) - (p2.x * sine(orot.y)))
                p3 = vec3((p3.x * cosine(orot.y)) + (p3.z * sine(orot.y)), p3.y,
                          (p3.z * cosine(orot.y)) - (p3.x * sine(orot.y)))

                p1 = vec3((p1.x * cosine(orot.z)) - (p1.y * sine(orot.z)),
                          (p1.x * sine(orot.z)) + (p1.y * cosine(orot.z)), p1.z)
                p2 = vec3((p2.x * cosine(orot.z)) - (p2.y * sine(orot.z)),
                          (p2.x * sine(orot.z)) + (p2.y * cosine(orot.z)), p2.z)
                p3 = vec3((p3.x * cosine(orot.z)) - (p3.y * sine(orot.z)),
                          (p3.x * sine(orot.z)) + (p3.y * cosine(orot.z)), p3.z)

            # Apply Camera Position and Object Position
            if not cam: cpos = vec3(0, 0, 0)
            p1 = (p1 + pos) - cpos
            p2 = (p2 + pos) - cpos
            p3 = (p3 + pos) - cpos

            return triangle(p1, p2, p3)

        def projectVec3ToCameraSpace(vec):
            camera = engine.Camera
            r = camera.Rotation
            orig = camera.Origin

            # Project to Camera Space
            vec = vec - orig
            sinx, cosx, siny, cosy, sinz, cosz = sine(r.x), cosine(r.x), sine(r.y), cosine(r.y), sine(r.z), cosine(r.z)
            vx, vy, vz = vec.x, vec.y, vec.z

            # Moves all points from world space to Camera space using Projection
            dx = cosy * (sinz * vy + cosz * vx) - siny * vz
            dy = sinx * (cosy * vz + siny * (sinz * vy + cosz * vx)) + cosx * (cosz * vy - sinz * vx)
            dz = cosx * (cosy * vz + siny * (sinz * vy + cosz * vx)) - sinx * (cosz * vy - sinz * vx)
            return vec3(dx, dy, dz)

        def clipTriangleAgainstPlane(plane, tris):
            ctris = []
            clipped = False
            self = engine.Projection

            # return [tris], False, None

            def dist(p):
                f = plane.vec1
                return (p.x * f.x) + (p.y * f.y) + (p.z * f.z) - f.dot(plane.vec0)

            for tri in tris:
                pointsInside = []
                pointsOutside = []
                insideCount = 0
                outsideCount = 0

                d0 = dist(tri.p1)
                d1 = dist(tri.p2)
                d2 = dist(tri.p3)

                if d0 >= 0:
                    pointsInside.insert(0, tri.p1);
                    insideCount += 1
                elif d0 < 0:
                    pointsOutside.insert(0, tri.p1);
                    outsideCount += 1
                if d1 >= 0:
                    pointsInside.insert(1, tri.p2);
                    insideCount += 1
                elif d1 < 0:
                    pointsOutside.insert(1, tri.p2);
                    outsideCount += 1
                if d2 >= 0:
                    pointsInside.insert(2, tri.p3);
                    insideCount += 1
                elif d2 < 0:
                    pointsOutside.insert(2, tri.p3);
                    outsideCount += 1

                if insideCount == 3: ctris.insert(0, tri); continue  # return [tri], False, None # Do nothing
                if insideCount == 0: continue  # Dont Render

                if insideCount == 1 and outsideCount == 2:
                    p1 = pointsInside[0]
                    p2 = self._vec3IntersectPlane(plane, vector(pointsInside[0], pointsOutside[0]))
                    p3 = self._vec3IntersectPlane(plane, vector(pointsInside[0], pointsOutside[1]))
                    t1 = triangle(p1, p2, p3)

                    clipped = True
                    ctris.insert(0, triangle(p1, p2, p3))

                if insideCount == 2 and outsideCount == 1:
                    p1 = pointsInside[0]
                    p2 = pointsInside[1]
                    p3 = self._vec3IntersectPlane(plane, vector(pointsInside[0], pointsOutside[0]))

                    p_1 = pointsInside[1]
                    p_2 = p3
                    p_3 = self._vec3IntersectPlane(plane, vector(pointsInside[1], pointsOutside[0]))
                    t1, t2 = triangle(p1, p2, p3), triangle(p_1, p_2, p_3)

                    clipped = True
                    ctris.insert(0, t1)
                    ctris.insert(1, t2)

            if len(ctris) == 0: return None, True, False
            return ctris, False, clipped

        def projectVec3ToScreenSpace(vec):
            camera = engine.Camera
            bx = (vec.x / vec.z) * camera.fov
            by = (vec.y / vec.z) * camera.fov

            return vec3(bx, by, vec.z)

        def projectTriangle(tri, Object):
            self = engine.Projection
            camera = engine.Camera
            near = camera.nearPlane
            tris = []

            if engine.Renderer.drawNormals == False:
                if self._triVisible(tri) == False: return None, True

            # Apply Projection to Camera Space
            p1 = self.projectVec3ToCameraSpace(tri.p1)
            p2 = self.projectVec3ToCameraSpace(tri.p2)
            p3 = self.projectVec3ToCameraSpace(tri.p3)
            p = triangle(p1, p2, p3)

            # Clip Near and Far Plane
            clippedTris, nodraw, clipped = self.clipTriangleAgainstPlane(
                vector(vec3(0, 0, camera.nearPlane), vec3(0, 0, 1)), [p])
            if nodraw: return None, True
            clippedTris, nodraw, clipped2 = self.clipTriangleAgainstPlane(
                vector(vec3(0, 0, camera.farPlane), vec3(0, 0, -1)), clippedTris)
            if nodraw: return None, True

            # Visualize Normal
            self._createVisualNormal(p, vec3(0, 200, 0))

            # Visualize Clipped Normals
            if clipped or clipped2:
                for ctri in clippedTris:
                    self._createVisualNormal(ctri, vec3(255, 0, 0))

            if engine.Renderer.drawNormals == True:
                if self._triVisible(tri) == False: return None, True

            # Lighting
            litColor = Object.Color.normalize()
            if engine.Renderer.Lighting:
                sun = engine.World.Sun.normalize()
                dp = tri.normal().dot(sun)
                if dp < 0.2: dp = 0.2
                litColor = Object.Color.normalize() * vec3(dp, dp, dp)

            # Project to Screen Space
            projectedTris = []
            for i, ctri in enumerate(clippedTris):
                p1 = self.projectVec3ToScreenSpace(ctri.p1)
                p2 = self.projectVec3ToScreenSpace(ctri.p2)
                p3 = self.projectVec3ToScreenSpace(ctri.p3)
                projectedTris.append(triangle(p1, p2, p3))

            # Screen Clipping
            screenClippedTris = []
            for ctri in projectedTris:
                clippedTris, nodraw, clipped = self.clipTriangleAgainstPlane(
                    vector(vec3(0, screen_height, 0), vec3(0, -1, 0)), [ctri])
                if nodraw: continue
                clippedTris, nodraw, clipped = self.clipTriangleAgainstPlane(
                    vector(vec3(0, -screen_height, 0), vec3(0, 1, 0)), clippedTris)
                if nodraw: continue
                clippedTris, nodraw, clipped = self.clipTriangleAgainstPlane(
                    vector(vec3(screen_width, 0, 0), vec3(-1, 0, 0)), clippedTris)
                if nodraw: continue
                clippedTris, nodraw, clipped = self.clipTriangleAgainstPlane(
                    vector(vec3(-screen_width, 0, 0), vec3(1, 0, 0)), clippedTris)
                if nodraw: continue
                for t in clippedTris: screenClippedTris.append(t)

            for ftri in screenClippedTris:
                zdepth = (ftri.p1.z + ftri.p2.z + ftri.p3.z) / 3
                tris.append(engine.Renderer.rasterTriangle(ftri, zdepth, litColor))

            if len(tris) == 0: return None, True
            return tris, False

        def _createVisualNormal(tri, col):
            if engine.Renderer.drawNormals:
                self = engine.Projection
                midpoint = (tri.p1 + tri.p2 + tri.p3) / 3
                line = midpoint + (tri.normal().normalize() * engine.Renderer.drawNormalLength)

                m = self.projectVec3ToScreenSpace(midpoint)
                l = self.projectVec3ToScreenSpace(line)
                l2 = self.projectVec3ToScreenSpace(midpoint - (line - midpoint))

                engine.Renderer.buffer2d.append(engine.Renderer.rasterVector(vector(m, l), col))
                engine.Renderer.buffer2d.append(engine.Renderer.rasterVector(vector(m, l2), vec3(0, 00, 200)))

        def _triVisible(tri):
            l1 = tri.p2 - tri.p1
            l2 = tri.p3 - tri.p1
            n = l1.cross(l2).normalize()
            ray = tri.p1 - engine.Camera.Origin
            if n.dot(ray) >= 0:
                return False

        def _vec3IntersectPlane(plane, line, epsilon=1e-6):
            u = line.vec1 - line.vec0
            dot = plane.vec1.dot(u)

            if abs(dot) > epsilon:
                w = line.vec0 - plane.vec0
                fact = -plane.vec1.dot(w) / dot
                u = u * fact
                return line.vec0 + u

    ##############################################################################################
    # Rendering
    class RenderClass:
        def __init__(self):
            self.isDrawing = False

            self.lineSize = 20
            self.Wireframe = False
            self.Lighting = True
            self.drawNormals = False
            self.drawNormalLength = .75
            self.fastDraw = True

            self.buffer = []
            self.buffer2d = []
            self.orderedBuffer = {}
            self.bufferIndex = []

            self.delta = float(0)
            self.frametime = 0.016
            self.triangleCounter = 0

            self.drawInfoEnabled = True

        class rasterVector:
            def __init__(self, vec, color):
                self.vec = vec
                self.color = color

        class rasterTriangle:
            def __init__(self, tri, zdepth, color):
                self.tri = tri
                self.zdepth = zdepth
                self.color = color

        def _drawVector(self, rvec):
            vec = rvec.vec
            set_color(rgb2hex(rvec.color))
            pen_up();
            set_position(vec.vec0.x, vec.vec0.y)
            pen_down();
            set_position(vec.vec1.x, vec.vec1.y)

        def _drawTriangle(self, rtri, fill=False):
            tri = rtri.tri
            set_color(rgb2hex(rtri.color))
            # pen_size(self._calcPenSize(rtri.zdepth))
            pen_up();
            set_position(tri.p1.x, tri.p1.y);
            pen_down()
            if fill: begin__fill()
            set_position(tri.p2.x, tri.p2.y)
            set_position(tri.p3.x, tri.p3.y)
            set_position(tri.p1.x, tri.p1.y)
            if fill: end__fill()
            self.triangleCounter += 1
            pen_up()

        def _orderBuffer(self):
            for i, rtri in enumerate(self.buffer):
                zid = rtri.zdepth + (i * 1e-6)
                self.bufferIndex.append(zid)
                self.orderedBuffer[zid] = rtri
            self.bufferIndex.sort(reverse=True)

        def _rasterObject(self, Object):
            if Object.non3d:
                for vec in Object.Verticies:
                    if Object.non3d:
                        self.buffer2d.append(self.rasterVector(vec, Object.Color))
                        continue
                return
            tansformedTriangles = Object.getAppliedTransformations()
            for tri in tansformedTriangles:
                tris, nodraw = engine.Projection.projectTriangle(tri, Object)
                if nodraw: continue
                for ptri in tris:
                    self.buffer.append(ptri)

        def renderScene(self):
            if self.isDrawing: return
            currentclock = time.process_time()
            bg_color(engine.World.SkyColor)

            self.buffer = [];
            self.buffer2d = []
            self.bufferIndex = []
            self.orderedBuffer = {}

            if self.fastDraw:
                turtle_tracer(0, 0)
            self.isDrawing = True
            self.triangleCounter = 0

            # Rasterize Triangles
            for o in engine.World.Objects.values():
                if o.hidden: continue
                self._rasterObject(o)

            # Render Rasterized Scene
            clear_canvas()
            self._orderBuffer()
            for index in self.bufferIndex:
                rtri = self.orderedBuffer[index]
                self._drawTriangle(rtri, fill=not self.Wireframe)

            # Draw 2d Objects
            pen_size(self.lineSize)
            for rvec in self.buffer2d:
                self._drawVector(rvec)

            # Draw Info
            if self.drawInfoEnabled:
                self._drawInfo()

            turtle_update()  # Update canvas with rasterized scene

            self.isDrawing = False
            self.frametime = time.process_time() - currentclock
            self.delta += self.frametime

        def _calcPenSize(self, zdepth):
            size = (-(abs(zdepth) ** .5) / 1.7) + self.lineSize
            if size < 1: size = 1
            return size

        def _drawInfo(self):
            set_color("white")
            pen_up()
            # Write Camera Position
            set_position(40, 185)
            campos = engine.Camera.Position
            roundedPosition = vec3(round(campos.x, 2), round(campos.y, 2), round(campos.z, 2))
            write_text(roundedPosition.__str__(), font=("Monospace", 8))

            # Write Camera Velocity
            set_position(40, 175)
            camvel = engine.Camera.Velocity
            roundedPosition = vec3(round(camvel.x, 2), round(camvel.y, 2), round(camvel.z, 2))
            write_text(roundedPosition.__str__(), font=("Monospace", 8))

            # FPS
            set_position(-190, 185)
            if self.frametime < 0.002: self.frametime = 0.002
            fps = round(1 / self.frametime, 1)
            write_text("FPS: " + str(fps), font=("Monospace", 8))

            # Triangle Count
            set_position(-190, 175)
            triangles = str(self.triangleCounter)
            write_text("#tri: " + triangles, font=("Monospace", 8))


##############################################################################################
# Run
Engine().run(Game)

##############################################################################################
