import bgfx

# Create a new window
myWin = bgfx.Window( 'Keyboard Input', width=200, height=150 )

# Create a red oval to represent our character
character = bgfx.Oval( myWin, 0, 0, 40, 40, fill='red', outline='' )

# While the window is open, test whether the arrow keys are pressed and move the character accordingly.
while myWin.isOpen:
	
	if myWin.keyIsDown( 'Left' ) and (character.x > 0):			character.x -= 4
	if myWin.keyIsDown( 'Right') and (character.x < myWin.width - 40):	character.x += 4
	if myWin.keyIsDown( 'Up'   ) and (character.y > 0):			character.y -= 4
	if myWin.keyIsDown( 'Down' ) and (character.y < myWin.height - 40):	character.y += 4
		
	myWin.update()
