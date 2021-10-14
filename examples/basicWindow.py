import bgfx

# Create a window
myWin = bgfx.Window( 'BGFX Demonstration', width=350, height=200, bg='white', resizable=False )

# Start window loop
while myWin.isOpen: myWin.update()
