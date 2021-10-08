import bgfx

# Create a window.
win = bgfx.Window( 'Basic Images', 200, 200, bg='#000' )

# Create an image. ( Note that rescaling images is not possible as of now. )
# ( No, I don't know why tkinter sucks arse so much. )
img = bgfx.Image( win, 0, 0, 'background.png' )

while win.isOpen:
	win.update()
