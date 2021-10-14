import bgfx

# Create a window and disable the user's cursor when hovering over the window
myWin = bgfx.Window( 'Mouse Input Events', width=300, height=300, bg='black', cursor=False )

# Create a square to act as a cursor
myCursor = bgfx.Rect( myWin, 0, 0, 10, 10, fill='', outline='white' )

# Create new events for mouse actions.
def onMove( mouseX, mouseY ):
	myCursor.x = mouseX - 5
	myCursor.y = mouseY - 5

def onPress( mouseX, mouseY, mouseButton ):	myCursor.fill = 'white'
def onRelease( mouseX, mouseY, mouseButton ):	myCursor.fill = ''

# Register the events with the window
myWin.onMouseMove = onMove
myWin.onMousePressed = onPress
myWin.onMouseReleased = onRelease

# Start the main loop
while myWin.isOpen:
	myWin.update()
