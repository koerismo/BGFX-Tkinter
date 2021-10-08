# Create a window
myWin	= Window( 'BGFX Demonstration', width=350, height=200, bg='#111' )

# Create a text object
myTitle	= Text( myWin, 175, 100, 'Hello, world!', fill='#999', fontSize=30 )

# Start window loop
while myWin.isOpen:
	if myWin.mouseOver( myTitle ):	myTitle.fill = '#fff'
	else:				myTitle.fill = '#999'
	myWin.update()
