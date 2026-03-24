# musical-worlds-tools
The Musical Worlds is a musical game of collecting various people from history as cartoons who play instruments and sing. Tools created are meant to help in the development process of the game and for others who want to make fan-made content.

## Description
*The Musical Worlds SVG Viewer and Image Exporter* is a tool used to simplify the process of animating **SVGs** in programs such as *[Spriter Pro](https://brashmonkey.com/spriter-pro/)*. *Spriter* only allows images such as **PNG**, so this tool converts **SVG** to **PNG**. It allows hiding and showing the **SVG** paths to export individual **PNG** images. You can zoom in and out, offset the camera, and import **SVG** files from the file system too. SVGs can be created with the ***[Scratch](scratch.mit.edu)*** website, which is what another project named *“The Musical Worlds: Live”* uses. 

This project will be created in ***Python***, and will not require any installation of external libraries.

## How it Works
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

## How to use
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

