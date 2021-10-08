import bgfx

# Create a window and disable the user's cursor when hovering over the window
myWin = bgfx.Window( 'Mouse Input', width=300, height=300, bg='black', cursor=False )

# Create a square to act as a cursor
myCursor = bgfx.Rect( myWin, 0, 0, 10, 10, fill='', outline='white' )

# Start the main loop
while myWin.isOpen:
	
	myCursor.x = myWin.mouseX - 5
	myCursor.y = myWin.mouseY - 5
	
	if myWin.mousePressed:	myCursor.fill = 'white'
	else:			myCursor.fill = ''
	
	myWin.update()
