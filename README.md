# gamestuff
a houdini interface game engine

# to make it work
* make sure you have houdini 16 installed (i was using 16.0.600)
* launch houdini_launcher.py - it will start houdini version it can find closest to 16.0.600 with environment set to current folder, so all custom node shapes and scripts are available
* open fxproject/animnodes/snekTest00.hip
* you can open source editor to see available functions
* for better experience - open a floating NetworkEditor pane (better to keep only one of them) and adjust the visible area, so the 4 network boxes are in the corners of the pane (i have it set up like that in the video on vimeo, if you came from there) (you may wish to bookmark this view with Ctrl+1 or something else for further convenience)
* start<Something> starts that something. ex: hou.session.startSnek() starts the game of Snek, hou.session.startPlanes() starts game of Planes
* stop any game or test with hou.session.stop()

that should cover it for starters...
