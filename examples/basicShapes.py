import bgfx

# Create window
myWin = bgfx.Window( 'Basic Shapes', width=420, height=140, bg='#222' )

# Create shapes
shapeA = bgfx.Rect( myWin, 20,  20, 100, 100, fill='#333', outline='white' )
shapeB = bgfx.Oval( myWin, 160, 20, 100, 100, fill='#333', outline='white' )
shapeC = bgfx.Line( myWin, 300, 20, 300+100, 20+100, fill='white', width=2 )

# Start main loop
while myWin.isOpen:
  myWin.update()
