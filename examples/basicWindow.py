import bgfx

# Create a window
myWin = bgfx.Window( 'BGFX Demonstration', width=350, height=200, bg='#111' )

# Start window loop
while myWin.isOpen: myWin.update()
