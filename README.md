# The Musical Worlds Live | SVG Viewer and Image Exporter

## Project Thumbnail

<img width="1780" height="924" alt="image" src="https://github.com/user-attachments/assets/3cfb66c3-a418-4aa1-b8f4-8943afda14b4" />

## Team Name
The Musical Worlds Dev

(Development of The Musical Worlds: Live Project)

## Project Title
The Musical Worlds Live | SVG Viewer and Image Exporter

## Project Description
The Musical Worlds is a musical game of collecting various people from history as cartoons who play instruments and sing. This tool has been created to help in the development process of the game and for others who want to make fan-made content.

*The Musical Worlds Live: SVG Viewer and Image Exporter* is a tool used to simplify the process of animating **SVGs** in programs such as *[Spriter Pro](https://brashmonkey.com/spriter-pro/)*. *Spriter* only allows images such as **PNG**, so this tool converts **SVG** to **PNG**. It allows hiding and showing the **SVG** paths to export individual **PNG** images. You can zoom in and out, offset the camera, and import **SVG** files from the file system too. SVGs can be created with the ***[Scratch](scratch.mit.edu)*** website, which is what another project named *“The Musical Worlds: Live”* uses. 

This project will be created in ***Python***, and will not require any installation of external libraries.

### How it Works
Here are the only imports used:
```
import turtle
import struct
import time
import zlib
import tkinter as tk
from tkinter import filedialog as fd
```
The `turtle` and `tkinter` modules allow for drawing the SVGs and viewport to the canvas. The SVG is decoded by splitting blocks by `<>` and then finding certain characters in them. Quotes (`""`) mark the start of a value.
The  `filedialog ` module allows for importing SVG files from the system. Not all SVGs work; it has to be from the "The Musical Worlds: Live" game.
The `time` module allows for appending a time stamp to the end of output files to make them unique.
Tthe `struct` and `zlib` modules help with exporting to PNG. Note that the canvas cannot directly be exported, but individual values of x and y can. For fill paths, each path outline is scaled down multiple times to create the illusion of filling in the shape.

### How to use
You can experiment with the default SVG "Riele.svg", which is loaded on program start, or import one from resources -> example -> Audtions.sprite3
1. Import the Audtiions.sprite3 to [Scratch](scratch.mit.edu)
2. Export any of them in the current format. No need to covnert to bitmap.
3. In the Musical Worlds SVG Viewer, press I and then select the file.

You can click on the circles on the right side. This selects a certain path.
Pressing the H Key on your keyboard shows and hides the path.

You can use the zoom in out slider at the bottom to change the camera zoom, and click and drag to move the camera.
You can also reset the view position with the R key.

When you are comfortable with your image, press the E key. Note it will take some time to export.
You can then import your images to software such as [Spriter Pro](https://brashmonkey.com/spriter-pro/) for animation.

## My Project Experience

### About this project
This project was originally going to be an animation editor, inspired by [MSM Aniviewer](https://gamebanana.com/tools/21316).
I figured it would take much longer and be even more difficult with the library limitation.
I wanted it to be with no external llbraries so anyone with Python can run it out of the box without pip.

### The Idea
I have been animating with Spriter Pro and it has been complicated to import my Scratch vector art into it. I draw in vector SVG because it is easier to edit if I want to change things around. To animate with this program, the vector must be exported as individual PNG images. 
Which means in Scratch I would:

1. Duplicate the sprite for every part I want to animate (Which can be a lot of parts such as 30+)
2. Individual delete all other parts of every SVG except for the part I want to keep
3. Convert every part to bitmap
4. I have to right click, click download from the list, wait for the file prompt, rename the file (because its name is not unique) and click save as for all parts

This program simplifies the process.

### Project Challenges
A lot of times I would get stuck on code and encounter unknown errors. So I would have to add print statements to see what went wrong. Some included:
1. Zooming / positing the camera errors
2. Image looking warped when exported
3. SVG import missing colors and erroring
4. Image looking completely black when exported
5. Hex color conversion trouble
6. Scaling the lines to get a correct fill problems
7. Python often skipping over values and joining incorrect strings
8. The entire program would go invisible and I had layering problems

### Satisfaction
Despite all the major challenges and this taking multiple hours, I enjoyed making this project. 
I learned alot about python and in the future I may work on it more and make it even better.
