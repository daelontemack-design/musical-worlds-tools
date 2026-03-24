import turtle
import struct
import time
import zlib
import tkinter as tk
from tkinter import filedialog as fd
root = tk.Tk()
root.withdraw()
global scaleValue
scaleValue = 1
global posX1
global posY1
posX1 = 0
posY1 = 0
global posX
global posY
posX = 0
posY = 0
global posX2
global posY2
posX2 = 0
posY2 = 0
global turtleElements
turtleElements = []
global lastR
global lastG
global lastB
lastR = 0
lastG = 0
lastB = 0
screen = turtle.Screen()
screen.setup(1800,950)
screen.title("The Musical Worlds : Live | SVG Viewer and Image Exporter")
screen.tracer(False)
turtle.colormode(255)
global selected
selected = -1
global colR
global colB
global colG
colR = []
colB = []
colG = []
global hiddenPaths
hiddenPaths = []
global exporting
exporting = False
global detailExp

detailExp = 20
global scaleQ
scaleQ = 1
def createPNG(filename):
    global colorExport
    global xExport
    global yExport
    global minW
    global maxW
    global minH
    global maxH
    global scaleQ
    scale = scaleQ
    # Raw pixel data (RGB)
    # Each scanline starts with a filter byte (0 = no filter)
    # Format: [filter][R][G][B]...
    raw_image_data = b''
    comp_data = []
    color = []
    colsExport = []
    posExport = []
    minW = min(xExport) * scale
    maxW = max(xExport) * scale
    minH = min(yExport) * scale
    maxH = max(yExport) * scale
    width = round((maxW - minW))
    height = round((maxH - minH))
    png_signature = b'\x89PNG\r\n\x1a\n'

  
    ihdr_data = struct.pack("!IIBBBBB",
                            width, height,
                            8,      
                            6,      
                            0,      
                            0,      
                            0)      
    ihdr_chunk = buildChunk(b'IHDR', ihdr_data)
    for q in range(len(xExport)):
        vvq = (len(xExport) - 1) - q
        posExport.append([round((((xExport[vvq] * scale) - minW))), round(((((yExport[vvq] * scale) - minH))))])
        colsExport.append(colorExport[vvq])
    
    for j in range(height):
        row = b'\x00'
        if j == 0:
            raw_image_data = row
        else:
            raw_image_data = raw_image_data + row


        for i in range(width):
            foundv = False
            ival = i
            jval = (height - 1) - j
            
            zv9 = -1
            try:
                zv9 = posExport.index([ival,jval])
                if zv9 > -1:
                    foundv = True
                    color = colsExport[zv9]
            except:
                zv9 = -1
                foundv = False
                
                        
            if foundv == True:
                rv = str(color[0])
                gv = str(color[1])
                bv = str(color[2])
                
                rv1 = rv.lstrip("0x")
                gv1 = gv.lstrip("0x")
                bv1 = bv.lstrip("0x")
                
                if rv1 == '':
                    rv1 = '00'
                if gv1 == '':
                    gv1 = '00'
                if bv1 == '':
                    bv1 = '00'

                if len(rv1) == 1:
                    rv1 = "0" + rv1
                if len(gv1) == 1:
                    gv1 = "0" + gv1
                if len(bv1) == 1:
                    bv1 = "0" + bv1
                    
                hexCol = "" + str(rv1) + str(gv1) + str(bv1) + "ff"
                hc = bytes.fromhex(hexCol.lower())
                row = hc
                raw_image_data = raw_image_data + row

            else:
                row = b'\x00\x00\x00\x00'
                raw_image_data = raw_image_data + row

        
    compData = zlib.compress(raw_image_data)
    imChunk = buildChunk(b'IDAT', compData)
        
    iend_chunk = buildChunk(b'IEND', b'')
    with open(filename, 'wb') as f:
        f.write(png_signature)
        f.write(ihdr_chunk)
        f.write(imChunk)
        f.write(iend_chunk)
    fixText()

    text.goto(-880,-438)

    text.write("Sucessfully exported as '" + str(filename) + "' !", align="left", font=("Courier", 8, "bold"))
    

def buildChunk(chunk_type, data):
    chunk = chunk_type + data
    length = struct.pack("!I", len(data))
    crc = struct.pack("!I", zlib.crc32(chunk) & 0xffffffff)
    return length + chunk + crc

def fixText():
    global scaleValue
    global selected
    global posX1
    global posY1
    global myPath
    text.penup()
    text.hideturtle()
    text.clear()
    text.goto(-25,-438)
    text.color(255,255,255)
    text.write("X-Offset: " + str(round(posX1, 4)) + " | Y-Offset: " + str(round(posY1, 4)) + " | Zoom: " + str((scaleValue * 100)) + "%", align="right", font=("Courier", 16, "bold"))
    text.goto(880,438)
    text.write("Paths (Selected ID: " + str(selected) + ")", align="right", font=("Courier", 12, "bold"))
    text.goto(880,412)
    text.write("Click to select a path and press the H key to toggle its visiblity", align="right", font=("Courier", 16, "bold"))
    text.goto(-880,412)
    text.write("Press the R key to reset the view position", align="left", font=("Courier", 16, "bold"))
    text.goto(-880,438)
    text.write("Loaded SVG: '" + myPath + "' | Press the I key to import SVG and E key to export current view as PNG", align="left", font=("Courier", 12, "bold"))


def clickPos(event):
    x = event.x - screen.window_width() / 2.0
    y = screen.window_height() / 2.0 - event.y
    global selected
    global posX2
    global posY2
    global lastR
    global lastG
    global lastB
    global turtleElements
    global colR
    global colB
    global colG

    if x < 825:
        if selected >= 0 and selected < len(turtleElements):
            lastR = colR[selected]
            lastG = colG[selected]
            lastB = colB[selected]

            turtleElements[selected].fillcolor(lastR,lastG,lastB)
            screen.update()

        selected = -1
        if y > -350 and y < 350:

            posX2 = x * 0.2 
            posY2 = y * 0.2
    else:
        if selected >= 0 and selected < len(turtleElements):
            lastR = colR[selected]
            lastG = colG[selected]
            lastB = colB[selected]
            turtleElements[selected].fillcolor(lastR,lastG,lastB)

        selected = round(40 - (y / 10.0))
        if selected < 0:
            selected = 0
        if selected < len(turtleElements):
            turtleElements[selected].fillcolor(0,255,0)
        screen.update()

        redraw()
    fixText()

def movePos(event):
    x = event.x - screen.window_width() / 2.0
    y = screen.window_height() / 2.0 - event.y
    global posX1
    global posY1
    global posX2
    global posY2
    if x < 825:

        if y > -350 and y < 350:
            posX1 = posX2 - (x * 0.2)
            posY1 = posY2 - (y * 0.2)
            screen.update()
            dragScreen.stamp()
            redraw()
            screen.update()
    fixText()
    
def zoomIn(x,y):
    global posX1
    global posY1
    global scaleValue
    scaleValue = 0.01 * x
    if scaleValue < 0.01:
        scaleValue = 0.01
    if scaleValue > 8.0:
        scaleValue = 8.0
    button.goto(scaleValue * 100, -425)
    screen.update()
    dragScreen.stamp()
    posX1 = 0
    posY1 = 0
    redraw()
    screen.update()
    fixText()

def res():
    global posX
    global posY
    global posX1
    global posY1
    global posX2
    global posY2
    posX = 0
    posY = 0
    posX1 = 0
    posY1 = 0
    posX2 = 0
    posY2 = 0
    redraw()
    screen.update()
    fixText()

def expo():
    global selected
    global scaleValue
    global turtleElements
    global colR
    global colG
    global colB
    global exporting

    if selected >= 0 and selected < len(turtleElements):
     
        lastR = colR[selected]
        lastG = colG[selected]
        lastB = colB[selected]

        turtleElements[selected].fillcolor(lastR,lastG,lastB)
        screen.update()
    exporting = True

    selected = -1
    scaleValue = 1
    res()
    fixText()
    text.goto(-880,-438)
    text.write("Exporting...", align="left", font=("Courier", 8, "bold"))
    screen.update()
    createPNG("output-" + str(round(time.time())) + ".png")

    exporting = False

    
def hide():
    global posX
    global posY
    global posX1
    global posY1
    global posX2
    global posY2
    posX = 0
    posY = 0
    posX1 = 0
    posY1 = 0
    posX2 = 0
    posY2 = 0
    global selected
    global turtleElements
    global hiddenPaths
    if selected >= 0 and selected < len(turtleElements):
        zq2 = -1
        try:
            zq2 = hiddenPaths.index(selected)
        except:
            zq2 = -1
        if zq2 > -1:
            turtleElements[selected].shape("circle")
            del hiddenPaths[zq2]
        else:
            turtleElements[selected].shape("triangle")
            hiddenPaths.append(selected)
        screen.update()

        redraw()
    fixText()

def im():
    global myPath

    filetypes = (
    ("SVG files", "*.svg"),
    ("All files", "*.*")
    )
    filename = fd.askopenfilename(
    title="Open SVG file",
    initialdir="/",
    filetypes=filetypes
    )

    try:
        myPath = filename
        global scaleValue
        scaleValue = 1
        global posX1
        global posY1
        posX1 = 0
        posY1 = 0
        global posX
        global posY
        posX = 0
        posY = 0
        global posX2
        global posY2
        posX2 = 0
        posY2 = 0
        global turtleElements
        for i in range(len(turtleElements)):
            turtleElements[i].hideturtle()
        turtleElements = []
        global lastR
        global lastG
        global lastB
        lastR = 0
        lastG = 0
        lastB = 0

        global selected
        selected = -1
        global colR
        global colB
        global colG
        colR = []
        colB = []
        colG = []
        global hiddenPaths
        hiddenPaths = []
        global exporting
        exporting = False
        global detailExp

        global svgList
        svgList = [] 

        global gradientList
        gradientList = []

        global gradMode
        global pathMode
        global pathStarted

        global cx
        global cy
        global r
        global hex1
        global hex2
        global o1

        global o2
        global types
        global offX 
        global offY
        global offset

        global val0
        global x0
        global y0
        global curPoint
        global px0
        global py0
        global px1
        global py1
        global px2
        global py2
        global px3
        global py3
        global begx
        global begy
        global hex3
        global stroke
        global strokeWidth
        global begy2
        global begx2
        global fill

        global maxW
        global maxH
        global minW
        global minH
        maxW = -9999999.0
        minW = 9999999.0
        maxH = -9999999.0
        minH = 9999999.0
        gradMode = False 
        pathMode = False 
        pathStarted = False 

        cx = "" 
        cy = "" 
        r = "" 
        hex1 = ""
        hex2 = ""
        o1 = "1" 
        o2 = "1" 
        types = "MLHVCQAZmlhvcqaz"
        offX = 999999
        offY = 999999
        offset = 0

        val0 = "" 
        x0 = ""
        y0 = ""
        curPoint = 1 
        px0 = "0"
        py0 = "0"
        px1 = "0"
        py1 = "0"
        px2 = "0"
        py2 = "0"
        px3 = "0"
        py3 = "0"
        begx = "0" 
        begy = "0" 
        hex3 = "" 
        stroke = ""
        strokeWidth = "" 
        begy2 = 0
        begx2 = 0
        global lasttypeV
        global typeV2
        global begx3
        global begy3
        begx3 = 0
        begy3 = 0
        typeV2 = ""
        lasttypeV = ""
        fill = False
        with open(myPath, "r" ) as file: 
            content = file.read() 
            g = ""
            for i in range(len(content)): 
                c = content[i]
                g = "" + str(g) + "" + str(c) + ""
                if c == '<': 
                    g = "" 
                if (i + 1) < len(content): 
                    if content[i + 1] == '>': 
                        svgList.append(g) 
                if (i - 1) >= 0: 
                    if c == '>': 
                        g = "" 
        global typeV
        typeV = "~"
        global setup
        setup = True
        global xVal
        global yVal
        global typeVal
        global strokeVal
        global strokeWidthVal
        global hexVal
        global drawing
        global elemVal2
        elemVal2 = []
        drawing = False
        xVal = []
        yVal = []
        typeVal = []
        strokeVal = []
        strokeWidthVal = []
        hexVal = []
        global elemVal
        elemVal = []

        global xExport
        global yExport

        global colorExport
        colorExport = []

        xExport = []
        yExport = []

        redraw()

        jkl = -1
        turts = -1

        for i in range(len(elemVal)):
            
            if not elemVal[i] == jkl:
                jkl = elemVal[i]
                
                tv = turtle.Turtle()
                tv.shape("circle")
                turtleElements.append(tv)
                tv.shapesize(stretch_wid=0.5, stretch_len = 0.5)
                turts = turts + 1
                stroke = strokeVal[i]
                strokeWidth = strokeWidthVal[i]
                hex3 = hexVal[i]
                tv.penup()
                tv.goto(850, (410 - (len(turtleElements) * 10)))
                if stroke.find("none") > -1:
                    tv.color(bgF,bgF,bgF) 
                    strokeWidth = ""
                elif stroke.find("url(#color-") > -1:
                    s4 = ""
                    if len(stroke) > 11:
                        s4 = "" + s4 + "" + str(stroke[11])
                    if len(stroke) > 12:
                        s4 = "" + s4 + "" + str(stroke[12])
                    if len(stroke) > 13:
                        s4 = "" + s4 + "" + str(stroke[13])
                    if len(stroke) > 14:
                        s4 = "" + s4 + "" + str(stroke[14])                                        
                        
                    if s4.find('r') > -1:
                        s4 = s4.rstrip('r')
                    if s4.find('u') > -1:
                        s4 = s4.rstrip('u')
                    if s4.find(')') > -1:
                        s4 = s4.rstrip(')')

                    s3 = int(s4) - 1
                    
                    z9 = gradientList[s3][3]
                    a0 = gradientList[s3][5]
                    a1 = gradientList[s3][6]

                    h = z9.upper().lstrip("#")
                    r8 = int(h[0:2], 16)
                    g8 = int(h[2:4], 16)
                    b8 = int(h[4:6], 16)

                    z91 = gradientList[s3][4]
                    h9 = z91.upper().lstrip("#")
                    r89 = int(h9[0:2], 16)
                    g89 = int(h9[2:4], 16)
                    b89 = int(h9[4:6], 16)

                    avg_r = round((r8 + r89) / 2)
                    avg_g = round((g8 + g89) / 2) 
                    avg_b = round((b8 + b89) / 2) 
                    avg_a = round((a0 + a1) / 2)

                    tv.color(avg_r,avg_g,avg_b) 
                    
                elif stroke == "": 
                    tv.color(bgF,bgF,bgF) 
                    strokeWidth = ""

                else:
                    h = stroke.upper().lstrip("#")
                    r8 = int(h[0:2], 16)
                    g8 = int(h[2:4], 16)
                    b8 = int(h[4:6], 16)
                    tv.color(r8,g8,b8) 

                if hex3.find("none") > -1:
                    tv.fillcolor(bgF,bgF,bgF)
                    colR.append(bgF)
                    colG.append(bgF)
                    colB.append(bgF)

                elif hex3.find("url(#color-") > -1: 
                    s4 = ""
                    if len(hex3) > 11:
                        s4 = "" + s4 + "" + str(hex3[11])
                    if len(hex3) > 12:
                        s4 = "" + s4 + "" + str(hex3[12])
                    if len(hex3) > 13:
                        s4 = "" + s4 + "" + str(hex3[13])
                    if len(hex3) > 14:
                        s4 = "" + s4 + "" + str(hex3[14])
                        
                    if s4.find('r') > -1:
                        s4 = s4.rstrip('r')
                    if s4.find('u') > -1:
                        s4 = s4.rstrip('u')
                    if s4.find(')') > -1:
                        s4 = s4.rstrip(')')
                    s3 = int(s4) - 1
                    
                    z9 = gradientList[s3][3]
                    a0 = gradientList[s3][5]
                    a1 = gradientList[s3][6]

                    h = z9.upper().lstrip("#")
                    r8 = int(h[0:2], 16)
                    g8 = int(h[2:4], 16)
                    b8 = int(h[4:6], 16)

                    z91 = gradientList[s3][4]
                    h9 = z91.upper().lstrip("#")
                    r89 = int(h9[0:2], 16)
                    g89 = int(h9[2:4], 16)
                    b89 = int(h9[4:6], 16)

                    avg_r = round((r8 + r89) / 2) 
                    avg_g = round((g8 + g89) / 2) 
                    avg_b = round((b8 + b89) / 2) 
                    avg_a = round((a0 + a1) / 2) 

                    tv.fillcolor(avg_r,avg_g,avg_b)
                    colR.append(avg_r)
                    colG.append(avg_g)
                    colB.append(avg_b)
                    
                elif hex3 == "": 
                    tv.fillcolor(bgF,bgF,bgF)
                    colR.append(bgF)
                    colG.append(bgF)
                    colB.append(bgF)
                else:
                    h = hex3.upper().lstrip("#")
                    r8 = int(h[0:2], 16)
                    g8 = int(h[2:4], 16)
                    b8 = int(h[4:6], 16)
                    tv.fillcolor(r8,g8,b8)
                    colR.append(r8)
                    colG.append(g8)
                    colB.append(b8)
                if strokeWidth == "":
                    tv.pensize(0) 
                else: 
                    tv.pensize(float(strokeWidth) * scaleValue) 
            elemVal2.append(turts)
    
        screen.update()
        fixText()
        text.goto(-880,-438)
        text.write("Successfully Imported!", align="left", font=("Courier", 8, "bold"))

    except:
        screen.update()

        fixText()
        text.goto(-880,-438)
        text.write("ERROR: Could not import file", align="left", font=("Courier", 8, "bold"))

    
canvas = screen.getcanvas()
canvas.bind("<ButtonRelease-1>", movePos)
canvas.bind("<ButtonPress-1>", clickPos)
bgF = 50
dragScreen = turtle.Turtle()
dragScreen.shape("square")
dragScreen.shapesize(stretch_wid=40, stretch_len = 80)
dragScreen.fillcolor(bgF,bgF,bgF)
dragScreen.penup()
dragScreen.goto(0,0)
dragScreen.hideturtle()

dragScreen.stamp()

bar2 = turtle.Turtle()
bar2.shape("square")
bar2.fillcolor(0,0,0)
bar2.shapesize(stretch_wid=10, stretch_len = 80)
bar2.penup()
bar2.goto(0,-500)

bar0 = turtle.Turtle()
bar0.shape("square")
bar0.fillcolor(0,0,0)
bar0.shapesize(stretch_wid=10, stretch_len = 80)
bar0.penup()
bar0.goto(0,500)

bar1 = turtle.Turtle()
bar1.shape("square")
bar1.fillcolor(0,0,0)
bar1.shapesize(stretch_wid=80, stretch_len = 10)
bar1.penup()
bar1.goto(900,0)

bar3 = turtle.Turtle()
bar3.shape("square")
bar3.fillcolor(0,0,0)
bar3.shapesize(stretch_wid=80, stretch_len = 10)
bar3.penup()
bar3.goto(-900,0)

bar = turtle.Turtle()
bar.shape("square")
bar.fillcolor(200,200,200)
bar.shapesize(stretch_wid=0.2, stretch_len = 40)
bar.penup()
bar.goto(400,-425)

button = turtle.Turtle()
button.shape("circle")
button.shapesize(stretch_wid=1, stretch_len = 1)
button.fillcolor(0,127,255)
button.penup()
button.goto(0,-425)
button.ondrag(zoomIn)

screen.onkey(res, "r")
screen.onkey(hide, "h")
screen.onkey(expo, "e")
screen.onkey(im, "i")

t = turtle.Turtle()
t.speed(0)
t.penup()
t.pensize(0)
t.hideturtle()

text = turtle.Turtle()
text.penup()
text.hideturtle()
text.clear()
text.goto(-200,-410)
text.color(255,255,255)

global myPath
myPath = "resources/example/Riele.svg"


global svgList
svgList = [] 

global gradientList
gradientList = []

global gradMode
global pathMode
global pathStarted

global cx
global cy
global r
global hex1
global hex2
global o1

global o2
global types
global offX 
global offY
global offset

global val0
global x0
global y0
global curPoint
global px0
global py0
global px1
global py1
global px2
global py2
global px3
global py3
global begx
global begy
global hex3
global stroke
global strokeWidth
global begy2
global begx2
global fill

global maxW
global maxH
global minW
global minH
maxW = -9999999.0
minW = 9999999.0
maxH = -9999999.0
minH = 9999999.0
gradMode = False 
pathMode = False 
pathStarted = False 

cx = "" 
cy = "" 
r = "" 
hex1 = ""
hex2 = ""
o1 = "1" 
o2 = "1" 
types = "MLHVCQAZmlhvcqaz"
offX = 999999
offY = 999999
offset = 0

val0 = "" 
x0 = ""
y0 = ""
curPoint = 1 
px0 = "0"
py0 = "0"
px1 = "0"
py1 = "0"
px2 = "0"
py2 = "0"
px3 = "0"
py3 = "0"
begx = "0" 
begy = "0" 
hex3 = "" 
stroke = ""
strokeWidth = "" 
begy2 = 0
begx2 = 0
global lasttypeV
global typeV2
global begx3
global begy3
begx3 = 0
begy3 = 0
typeV2 = ""
lasttypeV = ""
fill = False
with open(myPath, "r" ) as file: 
    content = file.read() 
    g = ""
    for i in range(len(content)): 
        c = content[i]
        g = "" + str(g) + "" + str(c) + ""
        if c == '<': 
            g = "" 
        if (i + 1) < len(content): 
            if content[i + 1] == '>': 
                svgList.append(g) 
        if (i - 1) >= 0: 
            if c == '>': 
                g = "" 

global typeV
typeV = "~"
global setup
setup = True
global xVal
global yVal
global typeVal
global strokeVal
global strokeWidthVal
global hexVal
global drawing
global elemVal2
elemVal2 = []
drawing = False
xVal = []
yVal = []
typeVal = []
strokeVal = []
strokeWidthVal = []
hexVal = []
global elemVal
elemVal = []

global xExport
global yExport

global colorExport
colorExport = []

xExport = []
yExport = []
def redraw():
    try:
        global drawing
        if drawing == False:
            t.clear()
            global setup
            global exporting
            global elemVal
            global elemVal2
            global maxW
            global maxH
            global minW
            global minH
            global posX2
            global posY2
            global posX1
            global posY1
            global typeV
            global typeV2
            global xVal
            global yVal
            global typeVal
            global posX
            global posY
            posX = posX + posX1
            posY = posY + posY1

            global svgList

            global gradientList

            global gradMode
            global pathMode
            global pathStarted

            global cx
            global cy
            global r
            global lasttypeV

            global hex1
            global hex2
            global o1
            global o2
            global types
            global offX 
            global offY
            global offset

            global val0
            global x0
            global y0
            global curPoint
            global px0
            global py0
            global px1
            global py1
            global px2
            global py2
            global px3
            global py3
            global begx
            global begy
            global hex3
            global stroke
            global strokeWidth
            global begy2
            global begx2
            global detailExp
            global xExport
            global yExport
            global begx3
            global begy3
            maxW = -9999999.0
            minW = 9999999.0
            maxH = -9999999.0
            minH = 9999999.0
            xExport = []
            yExport = []
            global colorExport
            colorExport = []
            
            global fill

            global strokeVal
            global strokeWidthVal
            global hexVal
            global selected
            global scaleQ
            global hiddenPaths

            offX = 999999
            offY = 999999
            vq = 0
            if setup == True:
                for i in range(len(svgList)):
                    if svgList[i] == "/stop":
                        svgList[i] = ""
                for i in range(len(svgList)): 
                    
                    if svgList[i].find("defs") > -1:
                        if gradMode == False:
                            gradMode = True 
                        else:
                            gradMode = False
                    for j in range(len(svgList[i])): 
                        
                        if gradMode == True: 
                            if svgList[i].find("/radialGradient") > -1 or svgList[i].find("/linearGradient") > -1: 
                                
                                gradientList.append([float(cx), float(cy), float(r), hex1, hex2, float(o1), float(o2)]) 
                                cx = "" 
                                cy = "" 
                                r = "" 
                                hex1 = "" 
                                hex2 = ""
                                o1 = "1" 
                                o2 = "1" 
                                break

                            if svgList[i].find("radialGradient cx") > -1: 
                                if not typeV == "~": 
                                    if svgList[i][j] == '"': 
                                        typeV = "~" 
                                    if typeV == "x": 
                                        cx = "" + str(cx) + "" + str(svgList[i][j]) 
                                    if typeV == "y": 
                                        cy = "" + str(cy) + "" + str(svgList[i][j]) 
                                    if typeV == "r": 
                                        r = "" + str(r) + "" + str(svgList[i][j])
                                        
                                if j >= 5: 
                                    if svgList[i][j - 5] == ' ': 
                                        if svgList[i][j - 4] == 'c': 
                                            if svgList[i][j - 3] == 'x': 
                                                if svgList[i][j - 2] == '=': 
                                                    if svgList[i][j - 1] == '"': 
                                                        cx = svgList[i][j]
                                                        typeV = "x" 
                                            elif svgList[i][j - 3] == 'y': 
                                                if svgList[i][j - 2] == '=': 
                                                    if svgList[i][j - 1] == '"': 
                                                        cy = svgList[i][j]
                                                        typeV = "y" 
                                    if svgList[i][j - 3] == 'r': 
                                        if svgList[i][j - 2] == '=': 
                                            if svgList[i][j - 1] == '"': 
                                                r = svgList[i][j]
                                                typeV = "r"
                            if svgList[i].find("linearGradient x1") > -1: 
                                if not typeV == "~": 
                                    if svgList[i][j] == '"': 
                                        typeV = "~" 
                                    if typeV == "x": 
                                        cx = "" + str(cx) + "" + str(svgList[i][j]) 
                                    if typeV == "y": 
                                        cy = "" + str(cy) + "" + str(svgList[i][j]) 
                                    if typeV == "r": 
                                        r = "" + str(r) + "" + str(svgList[i][j])
                                        
                                if j >= 5: 
                                    if svgList[i][j - 5] == ' ': 
                                        if svgList[i][j - 4] == 'x': 
                                            if svgList[i][j - 3] == '1': 
                                                if svgList[i][j - 2] == '=': 
                                                    if svgList[i][j - 1] == '"': 
                                                        cx = svgList[i][j]
                                                        typeV = "x" 
                                            elif svgList[i][j - 3] == '2': 
                                                if svgList[i][j - 2] == '=': 
                                                    if svgList[i][j - 1] == '"': 
                                                        cx = svgList[i][j]
                                                        typeV = "x"
                                        elif svgList[i][j - 4] == 'y': 
                                            if svgList[i][j - 3] == '1': 
                                                if svgList[i][j - 2] == '=': 
                                                    if svgList[i][j - 1] == '"': 
                                                        cy = svgList[i][j]
                                                        typeV = "y" 
                                            elif svgList[i][j - 3] == '2': 
                                                if svgList[i][j - 2] == '=': 
                                                    if svgList[i][j - 1] == '"': 
                                                        cy = svgList[i][j]
                                                        typeV = "y" 
                                    r = 1

                            elif svgList[i].find('stop offset="0"') > -1: 
                                if not typeV == "~": 
                                    if svgList[i][j] == '"': 
                                        typeV = "~"
                                    if typeV == "c":
                                        hex1 = "" + str(hex1) + "" + str(svgList[i][j]) 
                                    
                                if svgList[i][j] == '#': 
                                    hex1 = "" + str(hex1) + "" + svgList[i][j] + ""
                                    typeV = "c" 

                                if j >= 5: 
                                    
                                    if svgList[i][j - 5] == 'i': 
                                        if svgList[i][j - 4] == 't': 
                                           if svgList[i][j - 3] == 'y': 
                                               if svgList[i][j - 2] == '=': 
                                                   if svgList[i][j - 1] == '"': 
                                                       o1 = str(svgList[i][j]) 
                                    
                            elif svgList[i].find('stop offset="1"') > -1: 
                                if not typeV == "~": 
                                    if svgList[i][j] == '"': 
                                        typeV = "~" 
                                    if typeV == "c": 
                                        hex2 = "" + str(hex2) + "" + str(svgList[i][j]) 
                                    
                                if svgList[i][j] == '#': 
                                    hex2 = "" + str(hex2) + "" + svgList[i][j] + "" 
                                    typeV = "c" 
                                    
                                if j >= 5: 
                                    
                                    if svgList[i][j - 5] == 'i': 
                                        if svgList[i][j - 4] == 't': 
                                           if svgList[i][j - 3] == 'y': 
                                               if svgList[i][j - 2] == '=': 
                                                   if svgList[i][j - 1] == '"': 
                                                       o2 = str(svgList[i][j]) 

                        if pathMode == False:
                            if svgList[i].find("path d=") > -1:
                                if j - 6 >= 0:
                                    if svgList[i][j - 6] == 'a': 
                                        if svgList[i][j - 5] == 't': 
                                            if svgList[i][j - 4] == 'h': 
                                                if svgList[i][j - 3] == ' ': 
                                                    if svgList[i][j - 2] == 'd': 
                                                        if svgList[i][j - 1] == '=': 
                                                            if pathMode == False:
                                                                pathMode = True
                            if i > 0:
                                if not svgList[i - 1].find("g ") > -1:
                                    hex3 = "" 
                                    stroke = "" 
                                    strokeWidth = ""
                            if svgList[i].find("path d=") > -1 or svgList[i].find("g ") > -1:
                            
                                for k in range(len(svgList[i])):
                                    if k >= 6: 
                                        if svgList[i][k - 6] == 'f': 
                                            if svgList[i][k - 5] == 'i': 
                                                if svgList[i][k - 4] == 'l': 
                                                    if svgList[i][k - 3] == 'l': 
                                                        if svgList[i][k - 2] == '=': 
                                                            if svgList[i][k - 1] == '"': 
                                                                cx = svgList[i][k]
                                                                typeV = "0"
                                        if svgList[i][k - 6] == 'r': 
                                            if svgList[i][k - 5] == 'o': 
                                                if svgList[i][k - 4] == 'k': 
                                                    if svgList[i][k - 3] == 'e': 
                                                        if svgList[i][k - 2] == '=': 
                                                            if svgList[i][k - 1] == '"': 
                                                                cx = svgList[i][k] 
                                                                typeV = "1"
                                        if svgList[i][k - 6] == 'i': 
                                            if svgList[i][k - 5] == 'd': 
                                                if svgList[i][k - 4] == 't': 
                                                    if svgList[i][k - 3] == 'h': 
                                                        if svgList[i][k - 2] == '=': 
                                                            if svgList[i][k - 1] == '"': 
                                                                cx = svgList[i][k] 
                                                                typeV = "2" 
                                        if svgList[i][k] == " ":
                                            typeV = "~"
                                    if svgList[i][k] == '"': 
                                        typeV = "~"
                                    if typeV == "0": 
                                        hex3 = "" + str(hex3) + "" + str(svgList[i][k])
                                    if typeV == "1": 
                                        stroke = "" + str(stroke) + "" + str(svgList[i][k]) 
                                    if typeV == "2": 
                                        strokeWidth = "" + str(strokeWidth) + "" + str(svgList[i][k]) 
                                    if svgList[i][k] == ">":
                                        hex3 = ""
                                        stroke = "" 
                                        strokeWidth = "" 
                        
                        if pathMode == True: 

                            m = str(svgList[i][j])
                
                            if pathMode == True:
                                val0 = "" + str(val0) + "" + str(m) + ""  
             
                                if types.find(m) > -1 or m == " " or m == "," or m == '"': 
                                    
                                    if m == ",":
                                        val0 = val0.rstrip(",")
                                        x0 = val0

                                        val0 = ""
                                            
                                    else:
                                        val0 = val0.rstrip(m)
                                        
                                        if val0.find('"') > -1:
                                            val0 = val0.rstrip('"')
                                        
                                        if not (val0 == "" or val0 == '"'):
                                            
                                            try:
                                                if typeV == "h":
                                                   y0 = str(float(val0))
                                                   
                                                else:
                                                    
                                                    y0 = str(float(val0) * -1)
                                                val0 = ""
                                                
                                                typeVal.append(typeV)
                                                elemVal.append(i)
                                                xVal.append(x0)
                                                yVal.append(y0)
                                                strokeVal.append(stroke)
                                                strokeWidthVal.append(strokeWidth)
                                                hexVal.append(hex3)                                        

                                            except:
                                                vq = 0
                                            
                                if pathMode == True:

                                    if typeV == "M": 
                                        if not x0 == "":
                                            t.penup()
                                        if not y0 == "":
                                            if pathStarted == False: 
                                                pathStarted = True 

                                                if stroke.find("none") > -1:
                                                    t.color(0,0,0) 
                                                    strokeWidth = ""
                                                elif stroke.find("url(#color-") > -1: 
                                                    s4 = ""
                                                    if len(stroke) > 11:
                                                        s4 = "" + s4 + "" + str(stroke[11])
                                                    if len(stroke) > 12:
                                                        s4 = "" + s4 + "" + str(stroke[12])
                                                    if len(stroke) > 13:
                                                        s4 = "" + s4 + "" + str(stroke[13])
                                                    if len(stroke) > 14:
                                                        s4 = "" + s4 + "" + str(stroke[14])                                        
                                                        
                                                    if s4.find('r') > -1:
                                                        s4 = s4.rstrip('r')
                                                    if s4.find('u') > -1:
                                                        s4 = s4.rstrip('u')
                                                    if s4.find(')') > -1:
                                                        s4 = s4.rstrip(')')

                                                    s3 = int(s4) - 1
                                                    
                                                    z9 = gradientList[s3][3]
                                                    a0 = gradientList[s3][5]
                                                    a1 = gradientList[s3][6]

                                                    h = z9.upper().lstrip("#") 
                                                    r8 = int(h[0:2], 16) 
                                                    g8 = int(h[2:4], 16) 
                                                    b8 = int(h[4:6], 16) 
             
                                                    z91 = gradientList[s3][4]
                                                    h9 = z91.upper().lstrip("#")
                                                    r89 = int(h9[0:2], 16)
                                                    g89 = int(h9[2:4], 16)
                                                    b89 = int(h9[4:6], 16)

                                                    avg_r = round((r8 + r89) / 2)
                                                    avg_g = round((g8 + g89) / 2)
                                                    avg_b = round((b8 + b89) / 2)
                                                    avg_a = round((a0 + a1) / 2)

                                                    t.color(avg_r,avg_g,avg_b)

                                                elif stroke == "":
                                                    t.color(0,0,0) 
                                                    strokeWidth = ""

                                                else:
                                                    h = stroke.upper().lstrip("#")
                                                    r8 = int(h[0:2], 16)
                                                    g8 = int(h[2:4], 16)
                                                    b8 = int(h[4:6], 16)
                                                    t.color(r8,g8,b8) 

                                                if hex3.find("none") > -1: 
                                                    t.fillcolor(0,0,0) 
                                                    fill = False

                                                elif hex3.find("url(#color-") > -1: 
                
                                                    s4 = ""
                                                    if len(hex3) > 11:
                                                        s4 = "" + s4 + "" + str(hex3[11])
                                                    if len(hex3) > 12:
                                                        s4 = "" + s4 + "" + str(hex3[12])
                                                    if len(hex3) > 13:
                                                        s4 = "" + s4 + "" + str(hex3[13])
                                                    if len(hex3) > 14:
                                                        s4 = "" + s4 + "" + str(hex3[14])

                                                    if s4.find('r') > -1:
                                                        s4 = s4.rstrip('r')
                                                    if s4.find('u') > -1:
                                                        s4 = s4.rstrip('u')
                                                    if s4.find(')') > -1:
                                                        s4 = s4.rstrip(')')

                                                    s3 = int(s4) - 1
                                                    z9 = gradientList[s3][3]
                                                    a0 = gradientList[s3][5]
                                                    a1 = gradientList[s3][6]

                                                    h = z9.upper().lstrip("#")
                                                    r8 = int(h[0:2], 16)
                                                    g8 = int(h[2:4], 16)
                                                    b8 = int(h[4:6], 16)
              
                                                    z91 = gradientList[s3][4]
                                                    h9 = z91.upper().lstrip("#")
                                                    r89 = int(h9[0:2], 16)
                                                    g89 = int(h9[2:4], 16)
                                                    b89 = int(h9[4:6], 16)

                                                    avg_r = round((r8 + r89) / 2)
                                                    avg_g = round((g8 + g89) / 2) 
                                                    avg_b = round((b8 + b89) / 2) 
                                                    avg_a = round((a0 + a1) / 2) 
                                                    
                                                    t.fillcolor(avg_r,avg_g,avg_b) 
                                                    fill = True

                                                elif hex3 == "": 
                                                    t.fillcolor(0,0,0) 
                                                    fill = False
                                                else:
                                                    h = hex3.upper().lstrip("#")
                                                    r8 = int(h[0:2], 16)
                                                    g8 = int(h[2:4], 16)
                                                    b8 = int(h[4:6], 16)
                                                    t.fillcolor(r8,g8,b8)
                                                    fill = True

                                                if strokeWidth == "": 
                                                    t.pensize(0) 
                                                    t.penup() 

                                                else: 
                                                    t.pensize(float(strokeWidth) * scaleValue) 
                                                
                                                if y0.find("c") > -1:
                                                    y0 = y0.rstrip("c")
                                                if y0.find("l") > -1:
                                                    y0 = y0.rstrip("l")
                                                if round(offX) == 999999:
                                                    offX = (float(x0) * -1) - posX
                                                if not round(offX) == 999999:
                                                    x0 = str(float(x0) + (offX))
                                                if round(offY) == 999999:
                                                    offY = (float(y0) * -1)  - posY
                                                if not round(offY) == 999999:
                                                    y0 = str(float(y0) + (offY))
                                                t.goto(float(x0) * 1, float(y0)  * 1)
                                                t.pendown()
                                                if strokeWidth == "":
                                                    t.pensize(0) 
                                                    t.penup() 
                                                
                                                if fill == True:
                                                    t.begin_fill() 
                                                begx = float(x0) 
                                                begy = float(y0) 
                                                
                                                begy2 = begy
                                                begx2 = begx
                                                              
                                    if typeV == "m": 

                                        if x0 == "": 
                                            x0 = val0 
                                            t.penup() 
                                            t.goto(t.xcor() + (float(x0)  * 1), t.ycor() + 0)
                                        else: 
                                            y0 = val0 
                                            t.penup() 
                                            t.goto(t.xcor() + (float(x0)  * 1), t.ycor() + (float(y0) * 1))
                                              
                                    if typeV == "v":
                                    
                                        if not y0 == "":
                                            if y0.find("v") > -1:
                                                y0 = y0.rstrip("v")
                                                            
                                            t.goto(t.xcor(),(float(begy)  + float(y0)) * 1)
                                            begy = float(begy) + float(y0)
                                            
                                            curPoint = 1
                                    if typeV == "h": 
                                      
                                        if (not y0 == "") and (not y0 == " "):
                                            if not y0.find("p") > -1:
                                                if not y0.find("a") > -1:
                                                    if not y0.find("t") > -1:
                                                        if y0.find("h") > -1:
                                                            y0 = y0.rstrip("h")
                                                        if y0.find("M") > -1:
                                                            typeV = "M"
                                                            
                                                        else:
                                                            if y0.find(",") > -1:
                                                                y0 = y0.rstrip(",")

                                                            t.goto((float(begx) + float(y0)) * 1, t.ycor())
                                                            begx = float(begx) + float(y0)
                                                            
                                                            curPoint = 1 
                                        
                                    if typeV == "l": 
                                        
                                        if (not y0 == ""):

                                            begx = float(begx) + float(x0)
                                            begy = float(begy) + float(y0)

                                            t.goto(begx, begy)
                                            
                                    if typeV == "c":
                             
                                        if x0.find("M") > -1:
                                            typeV = "M"
                                            x0 = ""
                                        if (not y0 == ""):
                                            curPoint = curPoint + 2

                                            if curPoint == 3 :
                                                px0 = float(begx)
                                                px1 = x0 
                                                py0 = float(begy) 
                                                py1 = y0
                                                
                                            if curPoint == 5: 
                                                px2 = x0 
                                                py2 = y0 

                                            if curPoint == 7: 
                                                px3 = x0 
                                                py3 = y0 

                                        if curPoint == 7: 

                                            if px1.find(",") > -1:
                                                px1 = px1.rstrip(",")
                                            if px2.find(",") > -1:
                                                px2 = px2.rstrip(",")
                                            if px3.find(",") > -1:
                                                px3 = px3.rstrip(",")

                                            if py1.find("c") > -1:
                                                py1 = py1.rstrip("c")
                                            if py2.find("c") > -1:
                                                py2 = py2.rstrip("c")
                                            if py3.find("c") > -1:
                                                py3 = py3.rstrip("c")

                                            if py3.find('z" ') > -1:
                                                py3 = py3.rstrip('z" ')

                                            if py3.find('l') > -1:
                                                py3 = py3.rstrip('l')

                                            if py3.find('v') > -1:
                                                py3 = py3.rstrip('v')

                                            if py3.find('z') > -1:
                                                py3 = py3.rstrip('z')

                                            xv0 = 0 
                                            xv1 = float(px1)
                                            xv2 = float(px2)
                                            xv3 = float(px3)
                                            yv0 = 0 

                                            yv1 = float(py1)
                                            yv2 = float(py2)
                                            yv3 = float(py3)
                                            
                                            for tm in range(25): 
                                                pt = tm / 24.0 
                                                xFinal = (((pow((1 - pt), 3) * xv0)) + ((3 * (pow((1 - pt), 2)) * pt) * xv1) + (((3 * (1 - pt)) * (pow(pt, 2))) * xv2) + (pow(pt,3) * xv3))
                                                yFinal = (((pow((1 - pt), 3) * yv0)) + ((3 * (pow((1 - pt), 2)) * pt) * yv1) + (((3 * (1 - pt)) * (pow(pt, 2))) * yv2) + (pow(pt,3) * yv3))
                                                t.goto((float(px0) * 1) + (float(xFinal) * 1), (float(py0) * 1) + (float(yFinal) * 1))
                                            curPoint = 1 
                                            begx = float(px0) + float(xFinal)
                                            begy = float(py0) + float(yFinal)
                                             
                                    if (svgList[i][j] == '"' and svgList[i][j + 1] == " " and svgList[i][j + 2] == "f" and svgList[i][j + 3] == "i" and not typeV == "z") or typeV == "z" or typeV == "Z":
                                        pathMode = False 
                                        pathStarted = False 

                                        t.penup()
                                        t.goto(float(begx2) * 1, float(begy2) * 1)
                                        if (typeV == "z" or typeV == "Z"):
                                            typeVal.append(typeV)
                                            xVal.append(x0)
                                            yVal.append(y0)
                                            strokeVal.append(stroke)
                                            strokeWidthVal.append(strokeWidth)
                                            hexVal.append(hex3)
                                            elemVal.append(i)

                                        if fill == True:
                                            t.end_fill()
                                        typeV = "~" 
                                        val0 = ""
                                        
                                        if (typeV == "z" or typeV == "Z") or (not typeV == "l"):

                                            x0 = "" 
                                            y0 = "" 
                                            px0 = "0"
                                            py0 = "0"
                                            px1 = "0"
                                            py1 = "0"
                                            px2 = "0"
                                            py2 = "0"
                                            px3 = "0"
                                            py3 = "0"
                                            
                                        hex3 = "" 
                                        stroke = ""
                                        strokeWidth = "" 
                                        curPoint = 1
                                        
                                if (not m == " ") and types.find(m) > -1:
                                    typeV = m

                                if str(svgList[i][j]) == ',' or str(svgList[i][j]) == ' ': 

                                    if typeV == "M": 

                                        if x0 == "": 
                                            if val0.find(",") > -1:
                                                val0 = val0.rstrip(",")
                                        
                                            if not val0 == "":
                                                x0 = val0 
                                                t.penup() 
                                        
                                        if not x0 == "":
                                            t.penup() 

                                        if not y0 == "":
                                           
                                            t.penup()

                                            if pathStarted == False: 
                                                pathStarted = True 
                                                if stroke.find("none") > -1:
                                                    t.color(0,0,0) 
                                                    strokeWidth = ""
                                                elif stroke.find("url(#color-") > -1:
                                                    s4 = ""
                                                    if len(stroke) > 11:
                                                        s4 = "" + s4 + "" + str(stroke[11])
                                                    if len(stroke) > 12:
                                                        s4 = "" + s4 + "" + str(stroke[12])
                                                    if len(stroke) > 13:
                                                        s4 = "" + s4 + "" + str(stroke[13])
                                                    if len(stroke) > 14:
                                                        s4 = "" + s4 + "" + str(stroke[14])                                        
                                                        
                                                    if s4.find('r') > -1:
                                                        s4 = s4.rstrip('r')
                                                    if s4.find('u') > -1:
                                                        s4 = s4.rstrip('u')
                                                    if s4.find(')') > -1:
                                                        s4 = s4.rstrip(')')

                                                    s3 = int(s4) - 1
                                                    
                                                    z9 = gradientList[s3][3]
                                                    a0 = gradientList[s3][5]
                                                    a1 = gradientList[s3][6]

                                                    h = z9.upper().lstrip("#")
                                                    r8 = int(h[0:2], 16)
                                                    g8 = int(h[2:4], 16)
                                                    b8 = int(h[4:6], 16)

                                                    z91 = gradientList[s3][4]
                                                    h9 = z91.upper().lstrip("#")
                                                    r89 = int(h9[0:2], 16)
                                                    g89 = int(h9[2:4], 16)
                                                    b89 = int(h9[4:6], 16)

                                                    avg_r = round((r8 + r89) / 2)
                                                    avg_g = round((g8 + g89) / 2) 
                                                    avg_b = round((b8 + b89) / 2) 
                                                    avg_a = round((a0 + a1) / 2)

                                                    t.color(avg_r,avg_g,avg_b) 
                                                    
                                                elif stroke == "": 
                                                    t.color(0,0,0) 
                                                    strokeWidth = ""

                                                else:
                                                    h = stroke.upper().lstrip("#")
                                                    r8 = int(h[0:2], 16)
                                                    g8 = int(h[2:4], 16)
                                                    b8 = int(h[4:6], 16)
                                                    t.color(r8,g8,b8) 

                                                if hex3.find("none") > -1:
                                                    t.fillcolor(0,0,0) 
                                                    fill = False
                                                elif hex3.find("url(#color-") > -1: 
                                                    s4 = ""
                                                    if len(hex3) > 11:
                                                        s4 = "" + s4 + "" + str(hex3[11])
                                                    if len(hex3) > 12:
                                                        s4 = "" + s4 + "" + str(hex3[12])
                                                    if len(hex3) > 13:
                                                        s4 = "" + s4 + "" + str(hex3[13])
                                                    if len(hex3) > 14:
                                                        s4 = "" + s4 + "" + str(hex3[14])
                                                        
                                                    if s4.find('r') > -1:
                                                        s4 = s4.rstrip('r')
                                                    if s4.find('u') > -1:
                                                        s4 = s4.rstrip('u')
                                                    if s4.find(')') > -1:
                                                        s4 = s4.rstrip(')')
                                                    s3 = int(s4) - 1
                                                    
                                                    z9 = gradientList[s3][3]
                                                    a0 = gradientList[s3][5]
                                                    a1 = gradientList[s3][6]

                                                    h = z9.upper().lstrip("#")
                                                    r8 = int(h[0:2], 16)
                                                    g8 = int(h[2:4], 16)
                                                    b8 = int(h[4:6], 16)

                                                    z91 = gradientList[s3][4]
                                                    h9 = z91.upper().lstrip("#")
                                                    r89 = int(h9[0:2], 16)
                                                    g89 = int(h9[2:4], 16)
                                                    b89 = int(h9[4:6], 16)

                                                    avg_r = round((r8 + r89) / 2) 
                                                    avg_g = round((g8 + g89) / 2) 
                                                    avg_b = round((b8 + b89) / 2) 
                                                    avg_a = round((a0 + a1) / 2) 

                                                    t.fillcolor(avg_r,avg_g,avg_b)
                                                    fill = True
                                                elif hex3 == "": 
                                                    t.fillcolor(0,0,0) 
                                                    fill = False
                                                else:
                                                    h = hex3.upper().lstrip("#")
                                                    r8 = int(h[0:2], 16)
                                                    g8 = int(h[2:4], 16)
                                                    b8 = int(h[4:6], 16)
                                                    t.fillcolor(r8,g8,b8)
                                                    fill = True
                                               
                                                if strokeWidth == "":
                                                    t.pensize(0) 
                                                else: 
                                                    t.pensize(float(strokeWidth) * scaleValue) 
                                                if y0.find("c") > -1:
                                                    y0 = y0.rstrip("c")
                                                if round(offX) == 999999:
                                                    offX = (float(x0) * -1) - posX
                                                if not round(offX) == 999999:
                                                    x0 = str(float(x0) + (offX))
                                                if round(offY) == 999999:
                                                    offY = (float(y0) * -1) - posY
                                                if not round(offY) == 999999:
                                                    y0 = str(float(y0) + (offY))
                                                t.goto(float(x0) * 1, float(y0)  * 1)

                                                t.pendown() 
                                                if fill == True:
                                                    t.begin_fill() 
                                                begx = float(x0)
                                                begy = float(y0)
                                                
                                                begy2 = begy
                                                begx2 = begx

                                    if typeV == "m": 
                                        if x0 == "": 
                                            x0 = val0 
                                            t.penup() 
                                            t.goto(t.xcor() + (float(x0) * 1), t.ycor() + 0)
                                        else: 
                                            y0 = val0 
                                            t.penup() 
                                            t.goto(t.xcor() + (float(x0) * 1), t.ycor() + (float(y0) * 1))
                                    
                                if not y0 == "":
                                    if val0 == "":
                                        x0 = ""
                                        y0 = ""
                setup = False
                            
            else:
                hr0 = hex(0)
                hg0 = hex(0)
                hb0 = hex(0)
                tempPos = []
                for n in range(len(yVal)):
                   
                    x0 = xVal[n]
                    y0 = yVal[n]
                    typeV = typeVal[n]

                    if not x0 == "":
                        x0 = str(float(x0) * scaleValue)
                        if float(x0) >= maxW:
                            maxW = float(x0)
                        if float(x0) <= minW:
                            minW = float(x0)
                    if not y0 == "":
                        y0 = str(float(y0) * scaleValue)
                        if typeV == "h":
                            if float(y0) >= maxW:
                                maxW = float(y0)
                            if float(y0) <= minW:
                                minW = float(y0)
                        else:  
                            if float(y0) >= maxH:
                                maxH = float(y0)
                            if float(y0) <= minH:
                                minH = float(y0)
                    stroke = strokeVal[n]
                    hex3 = hexVal[n]
                    strokeWidth = strokeWidthVal[n]
                    if n < len(elemVal2):
                        sele = elemVal2[n]
                        if selected == sele:
                            hex3 = "#00ff00"
                            stroke = "#000000"
                            strokeWidth = "0.5"
                        zval = -1
                        try:
                            zval = hiddenPaths.index(sele)
                            
                        except:
                            zval = -1
                        if zval > -1:
                                continue
                        
                    if setup == False:
                        if setup == False:
                            if setup == False:
                                if setup == False:
                                    if typeV == "M": 
                                        if not x0 == "":
                                            t.penup()
                                        if not y0 == "":
                                            if setup == False:

                                                if stroke.find("none") > -1:
                                                    t.color(0,0,0) 
                                                    strokeWidth = ""
                                                elif stroke.find("url(#color-") > -1: 
                                                    s4 = ""
                                                    if len(stroke) > 11:
                                                        s4 = "" + s4 + "" + str(stroke[11])
                                                    if len(stroke) > 12:
                                                        s4 = "" + s4 + "" + str(stroke[12])
                                                    if len(stroke) > 13:
                                                        s4 = "" + s4 + "" + str(stroke[13])
                                                    if len(stroke) > 14:
                                                        s4 = "" + s4 + "" + str(stroke[14])                                        
                                                        
                                                    if s4.find('r') > -1:
                                                        s4 = s4.rstrip('r')
                                                    if s4.find('u') > -1:
                                                        s4 = s4.rstrip('u')
                                                    if s4.find(')') > -1:
                                                        s4 = s4.rstrip(')')

                                                    s3 = int(s4) - 1
                                                    
                                                    z9 = gradientList[s3][3]
                                                    a0 = gradientList[s3][5]
                                                    a1 = gradientList[s3][6]

                                                    h = z9.upper().lstrip("#") 
                                                    r8 = int(h[0:2], 16) 
                                                    g8 = int(h[2:4], 16) 
                                                    b8 = int(h[4:6], 16) 
             
                                                    z91 = gradientList[s3][4]
                                                    h9 = z91.upper().lstrip("#")
                                                    r89 = int(h9[0:2], 16)
                                                    g89 = int(h9[2:4], 16)
                                                    b89 = int(h9[4:6], 16)

                                                    avg_r = round((r8 + r89) / 2)
                                                    avg_g = round((g8 + g89) / 2)
                                                    avg_b = round((b8 + b89) / 2)
                                                    avg_a = round((a0 + a1) / 2)

                                                    t.color(avg_r,avg_g,avg_b)
                                                    hr0 = hex(avg_r)
                                                    hg0 = hex(avg_g)
                                                    hb0 = hex(avg_b)
                                                elif stroke == "":
                                                    t.color(0,0,0) 
                                                    strokeWidth = ""

                                                else:
                                                    h = stroke.upper().lstrip("#")
                                                    r8 = int(h[0:2], 16)
                                                    g8 = int(h[2:4], 16)
                                                    b8 = int(h[4:6], 16)
                                                    t.color(r8,g8,b8)
                                                    hr0 = hex(r8)
                                                    hg0 = hex(g8)
                                                    hb0 = hex(b8)

                                                if hex3.find("none") > -1: 
                                                    t.fillcolor(0,0,0) 
                                                    fill = False
                                                    

                                                elif hex3.find("url(#color-") > -1: 
                
                                                    s4 = ""
                                                    if len(hex3) > 11:
                                                        s4 = "" + s4 + "" + str(hex3[11])
                                                    if len(hex3) > 12:
                                                        s4 = "" + s4 + "" + str(hex3[12])
                                                    if len(hex3) > 13:
                                                        s4 = "" + s4 + "" + str(hex3[13])
                                                    if len(hex3) > 14:
                                                        s4 = "" + s4 + "" + str(hex3[14])

                                                    if s4.find('r') > -1:
                                                        s4 = s4.rstrip('r')
                                                    if s4.find('u') > -1:
                                                        s4 = s4.rstrip('u')
                                                    if s4.find(')') > -1:
                                                        s4 = s4.rstrip(')')

                                                    s3 = int(s4) - 1
                                                    z9 = gradientList[s3][3]
                                                    a0 = gradientList[s3][5]
                                                    a1 = gradientList[s3][6]

                                                    h = z9.upper().lstrip("#")
                                                    r8 = int(h[0:2], 16)
                                                    g8 = int(h[2:4], 16)
                                                    b8 = int(h[4:6], 16)
              
                                                    z91 = gradientList[s3][4]
                                                    h9 = z91.upper().lstrip("#")
                                                    r89 = int(h9[0:2], 16)
                                                    g89 = int(h9[2:4], 16)
                                                    b89 = int(h9[4:6], 16)

                                                    avg_r = round((r8 + r89) / 2)
                                                    avg_g = round((g8 + g89) / 2) 
                                                    avg_b = round((b8 + b89) / 2) 
                                                    avg_a = round((a0 + a1) / 2) 
                                                    
                                                    t.fillcolor(avg_r,avg_g,avg_b)

                                                    

                                                    hr0 = hex(avg_r)
                                                    hg0 = hex(avg_g)
                                                    hb0 = hex(avg_b)

                                                    fill = True

                                                elif hex3 == "": 
                                                    t.fillcolor(0,0,0) 
                                                    fill = False
                                                else:
                                                    h = hex3.upper().lstrip("#")
                                                    r8 = int(h[0:2], 16)
                                                    g8 = int(h[2:4], 16)
                                                    b8 = int(h[4:6], 16)
                                                    t.fillcolor(r8,g8,b8)
                                                    fill = True
                                                    hr0 = hex(r8)
                                                    hg0 = hex(g8)
                                                    hb0 = hex(b8)

                                                if strokeWidth == "": 
                                                    t.pensize(0) 
                                                    t.penup() 

                                                else: 
                                                    t.pensize(float(strokeWidth) * scaleValue) 
                                                
                                                if y0.find("c") > -1:
                                                    y0 = y0.rstrip("c")
                                                if y0.find("l") > -1:
                                                    y0 = y0.rstrip("l")
                                                if round(offX) == 999999:
                                                    offX = (float(x0) * -1) - posX
                                                if not round(offX) == 999999:
                                                    x0 = str(float(x0) + (offX))
                                                if round(offY) == 999999:
                                                    offY = (float(y0) * -1)  - posY
                                                if not round(offY) == 999999:
                                                    y0 = str(float(y0) + (offY))
                                                t.goto(float(x0) * 1, float(y0)  * 1)
                                                t.pendown()
                                                if strokeWidth == "":
                                                    t.pensize(0) 
                                                    t.penup() 
                                                
                                                if fill == True:
                                                    t.begin_fill()
                                                    tempPos = []
                                                begx = float(x0) 
                                                begy = float(y0) 
                                                
                                                begy2 = begy
                                                begx2 = begx
                                                xExport.append(float(x0))
                                                yExport.append(float(y0))
                                                colorExport.append([hr0,hg0,hb0])
                                                tempPos.append([xExport[len(xExport) - 1], yExport[len(yExport) - 1]])
                                                if fill == True:
                                                    del xExport[len(xExport) - 1]
                                                    del yExport[len(yExport) - 1]
                                                    del colorExport[len(colorExport) - 1]


                                                              
                                    if typeV == "m": 

                                        if x0 == "": 
                                            x0 = val0 
                                            t.penup() 
                                            t.goto(t.xcor() + (float(x0)  * 1), t.ycor() + 0)
                                        else: 
                                            y0 = val0 
                                            t.penup() 
                                            t.goto(t.xcor() + (float(x0)  * 1), t.ycor() + (float(y0) * 1))
                                              
                                    if typeV == "v":
                                    
                                        if not y0 == "":
                                            if y0.find("v") > -1:
                                                y0 = y0.rstrip("v")
                                                
                                            pointX1 = t.xcor()
                                            pointY1 = t.ycor()
                                            t.goto(t.xcor(),(float(begy)  + float(y0)) * 1)
                                            begy = float(begy) + float(y0)
                                            
                                            curPoint = 1
                                            pointX2 = t.xcor()
                                            pointY2 = t.ycor()

                                            pointX3 = pointX2 - pointX1
                                            pointY3 = pointY2 - pointY1
                                            if exporting == True:
                                                for i in range(detailExp):
                                                    g0 = (1 / detailExp) * i
                                                    xExport.append(pointX1 + (pointX3 * g0))
                                                    yExport.append(pointY1 + (pointY3 * g0))
                                                    colorExport.append([hr0,hg0,hb0])

                                                    tempPos.append([xExport[len(xExport) - 1], yExport[len(yExport) - 1]])
                                                    if fill == True:
                                                        del xExport[len(xExport) - 1]
                                                        del yExport[len(yExport) - 1]
                                                        del colorExport[len(colorExport) - 1]

                                    if typeV == "h": 
                                      
                                        if (not y0 == "") and (not y0 == " "):
                                            if not y0.find("p") > -1:
                                                if not y0.find("a") > -1:
                                                    if not y0.find("t") > -1:
                                                        if y0.find("h") > -1:
                                                            y0 = y0.rstrip("h")
                                                        if y0.find("M") > -1:
                                                            typeV = "M"
                                                            
                                                        else:
                                                            if y0.find(",") > -1:
                                                                y0 = y0.rstrip(",")
                                                            pointX1 = t.xcor()
                                                            pointY1 = t.ycor()
                                                            t.goto((float(begx) + float(y0)) * 1, t.ycor())
                                                            begx = float(begx) + float(y0)
                                                            pointX2 = t.xcor()
                                                            pointY2 = t.ycor()

                                                            pointX3 = pointX2 - pointX1
                                                            pointY3 = pointY2 - pointY1
                                                            if exporting == True:
                                                                for i in range(detailExp):
                                                                    g0 = (1 / detailExp) * i
                                                                    xExport.append(pointX1 + (pointX3 * g0))
                                                                    yExport.append(pointY1 + (pointY3 * g0))
                                                                    colorExport.append([hr0,hg0,hb0])

                                                                    tempPos.append([xExport[len(xExport) - 1], yExport[len(yExport) - 1]])
                                                                    if fill == True:
                                                                        del xExport[len(xExport) - 1]
                                                                        del yExport[len(yExport) - 1]
                                                                        del colorExport[len(colorExport) - 1]

                                                            curPoint = 1 
                                        
                                    if typeV == "l": 
                                        
                                        if (not y0 == ""):
                                            pointX1 = t.xcor()
                                            pointY1 = t.ycor()
                                            begx = float(begx) + float(x0)
                                            begy = float(begy) + float(y0)
                                            t.goto(begx, begy)
                                            pointX2 = t.xcor()
                                            pointY2 = t.ycor()

                                            pointX3 = pointX2 - pointX1
                                            pointY3 = pointY2 - pointY1
                                            if exporting == True:
                                                for i in range(detailExp * scaleQ * 3):
                                                    g0 = (1 / (detailExp * scaleQ * 3)) * i
                                                    xExport.append(pointX1 + (pointX3 * g0))
                                                    yExport.append(pointY1 + (pointY3 * g0))
                                                    colorExport.append([hr0,hg0,hb0])

                                                    tempPos.append([xExport[len(xExport) - 1], yExport[len(yExport) - 1]])
                                                    if fill == True:
                                                        del xExport[len(xExport) - 1]
                                                        del yExport[len(yExport) - 1]
                                                        del colorExport[len(colorExport) - 1]

                                            #pointX4 = pointX3 / pointX3
                                            #pointY4 = pointY3 / pointX3


                                            
                                    if typeV == "c":
                             
                                        if x0.find("M") > -1:
                                            typeV = "M"
                                            x0 = ""
                                        if (not y0 == ""):
                                            curPoint = curPoint + 2

                                            if curPoint == 3 :
                                                px0 = float(begx)
                                                px1 = x0 
                                                py0 = float(begy) 
                                                py1 = y0
                                                
                                            if curPoint == 5: 
                                                px2 = x0 
                                                py2 = y0 

                                            if curPoint == 7: 
                                                px3 = x0 
                                                py3 = y0 

                                        if curPoint == 7: 

                                            if px1.find(",") > -1:
                                                px1 = px1.rstrip(",")
                                            if px2.find(",") > -1:
                                                px2 = px2.rstrip(",")
                                            if px3.find(",") > -1:
                                                px3 = px3.rstrip(",")

                                            if py1.find("c") > -1:
                                                py1 = py1.rstrip("c")
                                            if py2.find("c") > -1:
                                                py2 = py2.rstrip("c")
                                            if py3.find("c") > -1:
                                                py3 = py3.rstrip("c")

                                            if py3.find('z" ') > -1:
                                                py3 = py3.rstrip('z" ')

                                            if py3.find('l') > -1:
                                                py3 = py3.rstrip('l')

                                            if py3.find('v') > -1:
                                                py3 = py3.rstrip('v')

                                            if py3.find('z') > -1:
                                                py3 = py3.rstrip('z')

                                            xv0 = 0 
                                            xv1 = float(px1)
                                            xv2 = float(px2)
                                            xv3 = float(px3)
                                            yv0 = 0 

                                            yv1 = float(py1)
                                            yv2 = float(py2)
                                            yv3 = float(py3)

                                            
                                            
                                            

                                            

                                            for tm in range(25): 
                                                pt = tm / 24.0 
                                                xFinal = (((pow((1 - pt), 3) * xv0)) + ((3 * (pow((1 - pt), 2)) * pt) * xv1) + (((3 * (1 - pt)) * (pow(pt, 2))) * xv2) + (pow(pt,3) * xv3))
                                                yFinal = (((pow((1 - pt), 3) * yv0)) + ((3 * (pow((1 - pt), 2)) * pt) * yv1) + (((3 * (1 - pt)) * (pow(pt, 2))) * yv2) + (pow(pt,3) * yv3))
                                                pointX1 = t.xcor()
                                                pointY1 = t.ycor()
                                                t.goto((float(px0) * 1) + (float(xFinal) * 1), (float(py0) * 1) + (float(yFinal) * 1))
                                                pointX2 = t.xcor()
                                                pointY2 = t.ycor()

                                                pointX3 = pointX2 - pointX1
                                                pointY3 = pointY2 - pointY1
                                                if exporting == True:
                                                    g0 = 1
                                                    #for i in range(detailExp + 1):
                                                        #g0 = (1 / detailExp) * i
                                                    xExport.append(pointX1 + (pointX3 * g0))
                                                    yExport.append(pointY1 + (pointY3 * g0))
                                                    colorExport.append([hr0,hg0,hb0])
                                                    tempPos.append([xExport[len(xExport) - 1], yExport[len(yExport) - 1]])
                                                    if fill == True:
                                                        del xExport[len(xExport) - 1]
                                                        del yExport[len(yExport) - 1]
                                                        del colorExport[len(colorExport) - 1]


                                            curPoint = 1 
                                            begx = float(px0) + float(xFinal)
                                            begy = float(py0) + float(yFinal)

                                    if typeV == "z" or typeV == "Z":
                                         
                                        t.penup()
                                        pointX1 = t.xcor()
                                        pointY1 = t.ycor()
                                        t.goto(float(begx2) * 1, float(begy2) * 1)
                                        pointX2 = t.xcor()
                                        pointY2 = t.ycor()
                                        pointX3 = pointX2 - pointX1
                                        pointY3 = pointY2 - pointY1
                                        if exporting == True:
                                            for i in range(detailExp):
                                                g0 = (1 / detailExp) * i
                                                xExport.append(pointX1 + (pointX3 * g0))
                                                yExport.append(pointY1 + (pointY3 * g0))
                                                colorExport.append([hr0,hg0,hb0])

                                                tempPos.append([xExport[len(xExport) - 1], yExport[len(yExport) - 1]])
                                                if fill == True:
                                                    del xExport[len(xExport) - 1]
                                                    del yExport[len(yExport) - 1]
                                                    del colorExport[len(colorExport) - 1]

                                        if fill == True:
                                            t.end_fill()
                                            if exporting == True:
                                                xd = []
                                                yd = []
                                                for ig in range(len(tempPos)):
                                                    xd.append(tempPos[ig][0])
                                                    yd.append(tempPos[ig][1])
                                                minX = min(xd)
                                                maxX = max(xd)
                                                minY = min(yd)
                                                maxY = max(yd)
                                                centerX = ((maxX + minX) / 2.0)
                                                centerY = ((maxY + minY) / 2.0)
                                                for ig in range(len(xd)):
                                                    varx = xd[ig] - centerX
                                                    vary = yd[ig] - centerY
                                                    for ih in range((detailExp * scaleQ)):
                                                        varx2 = varx * ((1 / (detailExp * scaleQ)) * ih)
                                                        vary2 = vary * ((1 / (detailExp * scaleQ)) * ih)
                                                        cxv = varx2 + centerX
                                                        cyv = vary2 + centerY
                                                        xExport.append(cxv)
                                                        yExport.append(cyv)
                                                        colorExport.append([hr0,hg0,hb0])
                                                tempPos = []

                                                        
                                        typeV = "~" 
                                        val0 = ""
                                        if (typeV == "z" or typeV == "Z") or (not typeV == "l"):

                                            px0 = "0"
                                            py0 = "0"
                                            px1 = "0"
                                            py1 = "0"
                                            px2 = "0"
                                            py2 = "0"
                                            px3 = "0"
                                            py3 = "0"
                                            
                                        fill = False
                                        curPoint = 1 
    except:
        fixText()

        text.goto(-880,-438)

        text.write("An unexpected error occured.", align="left", font=("Courier", 8, "bold"))
redraw()
jkl = -1
turts = -1

for i in range(len(elemVal)):
    
    if not elemVal[i] == jkl:
        jkl = elemVal[i]
        
        tv = turtle.Turtle()
        tv.shape("circle")
        turtleElements.append(tv)
        tv.shapesize(stretch_wid=0.5, stretch_len = 0.5)
        turts = turts + 1
        stroke = strokeVal[i]
        strokeWidth = strokeWidthVal[i]
        hex3 = hexVal[i]
        tv.penup()
        tv.goto(850, (410 - (len(turtleElements) * 10)))
        if stroke.find("none") > -1:
            tv.color(bgF,bgF,bgF) 
            strokeWidth = ""
        elif stroke.find("url(#color-") > -1:
            s4 = ""
            if len(stroke) > 11:
                s4 = "" + s4 + "" + str(stroke[11])
            if len(stroke) > 12:
                s4 = "" + s4 + "" + str(stroke[12])
            if len(stroke) > 13:
                s4 = "" + s4 + "" + str(stroke[13])
            if len(stroke) > 14:
                s4 = "" + s4 + "" + str(stroke[14])                                        
                
            if s4.find('r') > -1:
                s4 = s4.rstrip('r')
            if s4.find('u') > -1:
                s4 = s4.rstrip('u')
            if s4.find(')') > -1:
                s4 = s4.rstrip(')')

            s3 = int(s4) - 1
            
            z9 = gradientList[s3][3]
            a0 = gradientList[s3][5]
            a1 = gradientList[s3][6]

            h = z9.upper().lstrip("#")
            r8 = int(h[0:2], 16)
            g8 = int(h[2:4], 16)
            b8 = int(h[4:6], 16)

            z91 = gradientList[s3][4]
            h9 = z91.upper().lstrip("#")
            r89 = int(h9[0:2], 16)
            g89 = int(h9[2:4], 16)
            b89 = int(h9[4:6], 16)

            avg_r = round((r8 + r89) / 2)
            avg_g = round((g8 + g89) / 2) 
            avg_b = round((b8 + b89) / 2) 
            avg_a = round((a0 + a1) / 2)

            tv.color(avg_r,avg_g,avg_b) 
            
        elif stroke == "": 
            tv.color(bgF,bgF,bgF) 
            strokeWidth = ""

        else:
            h = stroke.upper().lstrip("#")
            r8 = int(h[0:2], 16)
            g8 = int(h[2:4], 16)
            b8 = int(h[4:6], 16)
            tv.color(r8,g8,b8) 

        if hex3.find("none") > -1:
            tv.fillcolor(bgF,bgF,bgF)
            colR.append(bgF)
            colG.append(bgF)
            colB.append(bgF)

        elif hex3.find("url(#color-") > -1: 
            s4 = ""
            if len(hex3) > 11:
                s4 = "" + s4 + "" + str(hex3[11])
            if len(hex3) > 12:
                s4 = "" + s4 + "" + str(hex3[12])
            if len(hex3) > 13:
                s4 = "" + s4 + "" + str(hex3[13])
            if len(hex3) > 14:
                s4 = "" + s4 + "" + str(hex3[14])
                
            if s4.find('r') > -1:
                s4 = s4.rstrip('r')
            if s4.find('u') > -1:
                s4 = s4.rstrip('u')
            if s4.find(')') > -1:
                s4 = s4.rstrip(')')
            s3 = int(s4) - 1
            
            z9 = gradientList[s3][3]
            a0 = gradientList[s3][5]
            a1 = gradientList[s3][6]

            h = z9.upper().lstrip("#")
            r8 = int(h[0:2], 16)
            g8 = int(h[2:4], 16)
            b8 = int(h[4:6], 16)

            z91 = gradientList[s3][4]
            h9 = z91.upper().lstrip("#")
            r89 = int(h9[0:2], 16)
            g89 = int(h9[2:4], 16)
            b89 = int(h9[4:6], 16)

            avg_r = round((r8 + r89) / 2) 
            avg_g = round((g8 + g89) / 2) 
            avg_b = round((b8 + b89) / 2) 
            avg_a = round((a0 + a1) / 2) 

            tv.fillcolor(avg_r,avg_g,avg_b)
            colR.append(avg_r)
            colG.append(avg_g)
            colB.append(avg_b)
            
        elif hex3 == "": 
            tv.fillcolor(bgF,bgF,bgF)
            colR.append(bgF)
            colG.append(bgF)
            colB.append(bgF)
        else:
            h = hex3.upper().lstrip("#")
            r8 = int(h[0:2], 16)
            g8 = int(h[2:4], 16)
            b8 = int(h[4:6], 16)
            tv.fillcolor(r8,g8,b8)
            colR.append(r8)
            colG.append(g8)
            colB.append(b8)
        if strokeWidth == "":
            tv.pensize(0) 
        else: 
            tv.pensize(float(strokeWidth) * scaleValue) 
    elemVal2.append(turts)
    
redraw()
screen.update()
fixText()

screen.listen()
screen.mainloop()


                            

