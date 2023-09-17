# Python-Scripting-in-Blender

<a href="https://www.packtpub.com/product/python-scripting-in-blender-3x/9781803234229?utm_source=github&utm_medium=repository&utm_campaign=9781803235851"><img src="https://content.packt.com/B18375/cover_image_small.png" alt="" height="256px" align="right"></a>

This is the code repository for [Python Scripting in Blender](https://www.packtpub.com/product/python-scripting-in-blender-3x/9781803234229?utm_source=github&utm_medium=repository&utm_campaign=9781803235851), published by Packt.

**Extend the power of Blender using Python to create objects, animations, and effective add-ons**

## What is this book about?
Blender, a powerful open source 3D software, can be extended and powered up using the Python programming language. This book teaches you how to automate laborious operations using scripts, and expand the set of available commands, graphic interfaces, tools, and event responses, which will enable you to add custom features to meet your needs and bring your creative ideas to life.

This book covers the following exciting features:                                 
* Understand the principles of 3D and programming, and learn how they operate in Blender
* Build engaging and navigation-friendly user interfaces that integrate with the native look and feel
* Respect coding guidelines and deliver readable and compliant code without the loss of originality
* Package your extensions into a complete add-on, ready for installation and distribution
* Create interactive tools with a direct response to the user's action
* Code comfortably and safely using version control

If you feel this book is for you, get your [copy](https://www.amazon.com/dp/1803234229) today!

<a href="https://www.packtpub.com/?utm_source=github&utm_medium=banner&utm_campaign=GitHubBanner"><img src="https://raw.githubusercontent.com/PacktPublishing/GitHub/master/GitHub.png" 
alt="https://www.packtpub.com/" border="5" /></a>

## Instructions and Navigations
All of the code is organized into folders. For example, Chapter02.

The code will look like the following:
```
bl_info = {
    "name": "Object Shaker",
    "author": "Packt Man",
    "version": (1, 0),
    "blender": (3, 00, 0),
    "description": "Add Shaky motion to active object",
    "location": "Object Right Click -> Add Object Shake",
    "category": "Learning",
}
```

**Following is what you need for this book:**
This book is for Blender users who want to expand their skills and learn scripting, technical directors looking to automate laborious tasks, and professionals and hobbyists who want to learn more about the Python architecture underlying the Blender interface. Prior experience with Blender is a prerequisite, along with a basic understanding of the Python syntax—however, the book does provide quick explanations to bridge potential gaps in your background knowledge.

With the following software and hardware list you can run all code files present in the book (Chapter 1-12).
### Software and Hardware List
| Chapter | Software required | OS required |
| -------- | ------------------------------------ | ----------------------------------- |
| 1-12 | Blender 3.3 | Windows, Mac OS X, and Linux (Any) |
| 1-12 | Visual Studio Code 1.70 or later | Windows, Mac OS X, and Linux (Any) |

We also provide a PDF file that has color images of the screenshots/diagrams used in this book. [Click here to download it](https://packt.link/G1mMt).

### Related products
* Blender 3D Incredible Models [[Packt]](https://www.packtpub.com/product/blender-3d-incredible-models/9781801817813?utm_source=github&utm_medium=repository&utm_campaign=9781801817813) [[Amazon]](https://www.amazon.com/dp/B0B1QMV8LR)

* Squeaky Clean Topology in Blender [[Packt]](https://www.packtpub.com/product/squeaky-clean-topology-in-blender/9781803244082?utm_source=github&utm_medium=repository&utm_campaign=9781803244082) [[Amazon]](https://www.amazon.com/dp/1803244089)

## Errata 
 * Page 45 (second last code block):
``` 
import bpy
for ob in bpy.context.selected_objects:
ob.select_set(False)
```
**_should be_**
``` 
 import bpy
 for ob in bpy.context.selected_objects:
     ob.select_set(False)
 ```

 * Page 62 (second last code block):
``` 
try:
    mesh_cl = bpy.data.collections.new['Mesh']
except KeyError:
    mesh_cl = bpy.data.collections.new("Mesh")
```
**_should be_**
``` 
try:
    mesh_cl = bpy.data.collections['Mesh']
except KeyError:
    mesh_cl = bpy.data.collections.new("Mesh")
 ```

## Get to Know the Author
**Paolo Acampora** is a software developer at Binary Alchemy and a veteran technical director for animation, visual effects, and prototyping. He is a long-time Blender user and advocates for the widespread adoption of open source software and code literacy.
He works with studios to kickstart their computer graphics pipelines and shares his tools with the Blender community.
