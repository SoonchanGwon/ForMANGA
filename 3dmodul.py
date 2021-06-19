import tkinter as tk
import turtle as t
import numpy as np
import copy


# Made by Juho Kim

#General Class/ Function
def rotx(x):
    return np.array([[1,0,0]
                     ,[0,np.cos(x),-np.sin(x)]
                     ,[0,np.sin(x),np.cos(x)]])
def roty(x):
    return np.array([[np.cos(x),0,np.sin(x)]
                     ,[0,1,0]
                     ,[-np.sin(x),0,np.cos(x)]])
def rotz(x):
    return np.array([[np.cos(x),-np.sin(x),0]
                     ,[np.sin(x),np.cos(x),0]
                     ,[0,0,1]])


class _3DClass:
    geo = []
    def __init__(self):
        self.screen = tk.Tk()
        self.screen.title("3D Graphic")
        self.screen.geometry("500x600")
        self.screen.resizable(False,False)

        self.__buf1 = tk.Canvas(master = self.screen, width=500,height=500)
        self.__buf2 = tk.Canvas(master = self.screen, width=500,height=500)
        self.__buffer1 = t.TurtleScreen(self.__buf1)
        self.__buffer2 = t.TurtleScreen(self.__buf2)
        self.__buf2.pack_forget()
        self.__buf1.pack()
        self.__current = 1
        self.__t1 = t.RawTurtle(self.__buffer1)
        self.__t2 = t.RawTurtle(self.__buffer2)
        self.__t1.speed(0)
        self.__t2.speed(0)
        self.__t1.hideturtle()
        self.__t2.hideturtle()
        self.__t2.color("blue")
        self.__t1.penup()
        self.__t1.penup()



    def ChangeBuffer(self):
        if self.__current == 1:
            self.__buf1.pack_forget()
            self.__buf2.pack()

            self.__current = 2
            return
        if self.__current == 2:
            self.__buf2.pack_forget()
            self.__buf1.pack()

            self.__current = 1
            return

    def getBackBuffer(self):
        if self.__current == 1:
            return self.__buffer2
        if self.__current == 2:
            return self.__buffer1

    def getBackTurtle(self):
        if self.__current == 1:
            return self.__t2
        if self.__current == 2:
            return self.__t1

class Geometry:

    def __init__(self,name = "Geometry",planes = [],pos = np.array([0,0,0]),angle = np.array([0,0,0])):
        self.name = name
        self.plane = planes
        self.pos = pos
        self.angle = angle

    def getRadAngle(self):
        return self.angle / 180 * np.pi
    def DrawGeometry(self,_turtle: t.RawTurtle):
        self.angle = self.angle % 360
        planes = copy.deepcopy(self.plane)
        p = copy.deepcopy(self.pos)
        a = copy.deepcopy(self.getRadAngle())
        for pl in planes:
            vertexs = pl[0]
            _turtle.color(pl[1])
            for i,v in enumerate(vertexs):
                v = np.dot(v,rotx(a[0]))
                v = np.dot(v,roty(a[1]))
                v = np.dot(v,rotz(a[2]))
                vertexs[i] = v + p


            avec = vertexs[1]-vertexs[0]
            bvec = vertexs[2]-vertexs[1]
            cross = np.cross(avec,bvec)
            _d = np.mean(vertexs,axis = 0)
            d = np.array([_d[0],_d[1],-(_d[2]+30)])
            _turtle.goto(vertexs[0][0]*(vertexs[0][2]+30)/2,vertexs[0][1]*(vertexs[0][2]+30)/2)
            if np.dot(cross,d) > 0:
                _turtle.pendown()
                _turtle.begin_fill()
            for v in vertexs:
                _turtle.goto(v[0]*(v[2]+30)/2,v[1]*(v[2]+30)/2)
            _turtle.end_fill()
            _turtle.penup()

    def Cube(self,x,y,z):
        a = np.array([x/2,y/2,z/2])
        b = np.array([x/2,-y/2,z/2])
        c = np.array([-x/2,-y/2,z/2])
        d = np.array([-x/2,y/2,z/2])
        e = np.array([x/2,y/2,-z/2])
        f = np.array([x/2,-y/2,-z/2])
        g = np.array([-x/2,-y/2,-z/2])
        h = np.array([-x/2,y/2,-z/2])
        self.plane = [[[a,b,c,d],"red"]
                  ,[[d,c,g,h],"orange"]
                  ,[[h,g,f,e],"yellow"]
                  ,[[e,f,b,a],"green"]
                  ,[[a,d,h,e],"blue"]
                  ,[[b,f,g,c],"purple"]]



def Update(td: _3DClass):
    Draw(td)
    cubeControl.Update()
    td.screen.after(1,Update(td))

def Draw(td: _3DClass):
    geometries = td.geo
    td.getBackBuffer().clear()
    for geo in geometries:
        geo.DrawGeometry(td.getBackTurtle())
    td.ChangeBuffer()



#cube Geometry Control

class CubeController:
    def Update(self):
        self.Ax.set(str(cube.angle[0]))
        self.Ay.set(str(cube.angle[1]))
        self.Az.set(str(cube.angle[2]))
        self.Px.set(str(cube.pos[0]))
        self.Py.set(str(cube.pos[1]))
        self.Pz.set(str(cube.pos[2]))
        for i,r in enumerate(self.Rot):
            if r:
                cube.angle[i] += 10
    def changeAngle(self):
        self.a = cube.angle
        if(self.AngleX.get() != ""):
            self.a[0] = float(self.AngleX.get())
        if(self.AngleY.get() != ""):
            self.a[1] = float(self.AngleY.get())
        if(self.AngleZ.get() != ""):
            self.a[2] = float(self.AngleZ.get())

    def changePos(self):
        self.p = cube.pos
        if(self.PosX.get() != ""):
            self.p[0] = float(self.PosX.get())
        if(self.PosY.get() != ""):
            self.p[1] = float(self.PosY.get())
        if(self.PosZ.get() != ""):
            self.p[2] = float(self.PosZ.get())
    def changex(self):
        self.Rot[0] = not(self.Rot[0])
    def changey(self):
        self.Rot[1] = not(self.Rot[1])
    def changez(self):
        self.Rot[2] = not(self.Rot[2])
    def __init__(self):
        self.Rot = [False,True,False]
        self.Ax = tk.StringVar()
        self.Ay = tk.StringVar()
        self.Az = tk.StringVar()
        self.Ax.set("UNKNOWN")
        self.Ay.set("UNKNOWN")
        self.Az.set("UNKNOWN")
        self.Angle = tk.Label(TD.screen,text="Rotation",width=50,height=25, fg="Black")
        self.Anglex = tk.Label(TD.screen,textvariable = self.Ax,width=50,height=25, fg="Red")
        self.Angley = tk.Label(TD.screen,textvariable = self.Ay,width=50,height=25, fg="Green")
        self.Anglez = tk.Label(TD.screen,textvariable = self.Az,width=50,height=25, fg="Blue")
        self.AngleX = tk.Entry(TD.screen)
        self.AngleY = tk.Entry(TD.screen)
        self.AngleZ = tk.Entry(TD.screen)
        self.AngleButton = tk.Button(TD.screen,text="변경",command = self.changeAngle)
        self.RotX = tk.Button(TD.screen,text="x회전",command = self.changex)
        self.RotY = tk.Button(TD.screen,text="y회전",command = self.changey)
        self.RotZ = tk.Button(TD.screen,text="z회전",command = self.changez)
        self.Angle.place(x=0,y=500,width=50,height=25)
        self.Anglex.place(x=50,y=550,width=50,height=25)
        self.Angley.place(x=100,y=550,width=50,height=25)
        self.Anglez.place(x=150,y=550,width=50,height=25)
        self.AngleX.place(x=50, y=500, width=50, height=25)
        self.AngleY.place(x=100, y=500, width=50, height=25)
        self.AngleZ.place(x=150, y=500, width=50, height=25)
        self.RotX.place(x=50, y=525, width=50, height=25)
        self.RotY.place(x=100, y=525, width=50, height=25)
        self.RotZ.place(x=150, y=525, width=50, height=25)
        self.AngleButton.place(x=200, y=500, width=50, height=25)

        self.Px = tk.StringVar()
        self.Py = tk.StringVar()
        self.Pz = tk.StringVar()
        self.Px.set("UNKNOWN")
        self.Py.set("UNKNOWN")
        self.Pz.set("UNKNOWN")
        self.Pos = tk.Label(TD.screen,text="Position",width=50,height=25, fg="Black")
        self.Posx = tk.Label(TD.screen,textvariable = self.Px,width=50,height=25, fg="Red")
        self.Posy = tk.Label(TD.screen,textvariable = self.Py,width=50,height=25, fg="Green")
        self.Posz = tk.Label(TD.screen,textvariable = self.Pz,width=50,height=25, fg="Blue")
        self.PosX = tk.Entry(TD.screen)
        self.PosY = tk.Entry(TD.screen)
        self.PosZ = tk.Entry(TD.screen)
        self.PosButton = tk.Button(TD.screen,text="변경",command = self.changePos)
        self.Pos.place(x=250,y=500,width=50,height=25)
        self.Posx.place(x=300,y=550,width=50,height=25)
        self.Posy.place(x=350,y=550,width=50,height=25)
        self.Posz.place(x=400,y=550,width=50,height=25)
        self.PosX.place(x=300, y=500, width=50, height=25)
        self.PosY.place(x=350, y=500, width=50, height=25)
        self.PosZ.place(x=400, y=500, width=50, height=25)
        self.PosButton.place(x=450, y=500, width=50, height=25)



#Main
TD = _3DClass()

cube = Geometry(name = "Cube")
cube.Cube(10,10,10)
TD.geo.append(cube)

cubeControl = CubeController()
Update(TD)
