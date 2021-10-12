'''
Better Tkinter Graphics Wrapper

Provides a nice interface for interacting with tkinter's canvas features.
'''

__version__ = '0.7.0'
__author__ = 'Koerismo'
__credits__ = 'Koerismo'

import tkinter as tk
from types import FunctionType
from typing import Union

class Window():
	def __init__(
				self,
				title:str="Window",
				width:int=256,
				height:int=256,
				master:tk.Tk|tk.Frame=None,
				bg:str='white',
				resizable:bool=False,
				cursor:bool=True
				) -> None:
		'''
			Creates a new BGFX Window object.
		'''
		if master == None:
			self.root = tk.Tk()
			self.root.title( title )
			self.root.resizable( width=resizable, height=resizable )
			self.__geometry = [ width, height ]
		else:
			self.root = master
		self.frame = tk.Frame( self.root, width=width, height=height )
		self.canv = tk.Canvas( self.root, width=width, height=height, bg=bg, bd=-3 )
		if master == None:
			self.canv.pack( fill='both', expand=True )

		if not cursor: self.canv.config(cursor='none')

		self.__open = True
		def __setClosed(): self.__open = False
		self.root.protocol( 'WM_DELETE_WINDOW', __setClosed )

		self.mouseX = 0
		self.mouseY = 0
		self.mousePressed = False
		self.__keysPressed = {}

		self.__setupListeners()

	def __setupListeners( self ):
		def onMouseMoveInternal( event ):
			self.mouseX = event.x
			self.mouseY = event.y
			self.onMouseMove( event.x, event.y )
		self.root.bind( '<Motion>', onMouseMoveInternal )
		def onMousePressedInternal( event ):
			self.mouseX = event.x
			self.mouseY = event.y
			self.mousePressed = True
			self.onMousePressed( event.x, event.y )
		self.root.bind( '<ButtonPress-1>', onMousePressedInternal )
		def onMouseReleasedInternal( event ):
			self.mouseX = event.x
			self.mouseY = event.y
			self.mousePressed = False
			self.onMouseReleased( event.x, event.y )
		self.root.bind( '<ButtonRelease-1>', onMouseReleasedInternal )
		def onKeyPressedInternal( event ):
			self.__keysPressed[event.keysym] = True
			self.onKeyPressed( event.keysym )
		self.root.bind( '<Key>', onKeyPressedInternal )
		def onKeyReleasedInternal( event ):
			self.__keysPressed[event.keysym] = False
			self.onKeyReleased( event.keysym )
		self.root.bind( '<KeyRelease>', onKeyReleasedInternal )

	def onMouseMove( self, x, y ): pass
	def onMousePressed( self, x, y ): pass
	def onMouseReleased( self, x, y ): pass
	def onKeyPressed( self, k ): pass
	def onKeyReleased( self, k ): pass

	@property
	def isOpen( self ) -> bool: return self.__open

	def update( self ) -> None: self.root.update()

	def keyIsDown( self, key ) -> bool: return key in self.__keysPressed and self.__keysPressed[key]

	def mouseOver( self, object: Union['Rect','Oval','Line','Text'] ) -> bool:
		''' Performs a quick-and-dirty bounding box collision check with the mouse. Useful for buttons. '''

		if object._hidden: return False

		box = self.canv.bbox( object.part )
		return (
			self.mouseX > box[0] and
			self.mouseX < box[2] and
			self.mouseY > box[1] and
			self.mouseY < box[3]
		)

	@property
	def width( self ) -> int: return self.canv.winfo_width()
	@property
	def height( self ) -> int: return self.canv.winfo_height()

	@width.setter
	def width( self, val ):
		rval = round(val)
		self.__geometry[0] = rval
		self.root.geometry(f'{rval}x{self.__geometry[1]}')
	@height.setter
	def height( self, val ):
		rval = round(val)
		self.__geometry[1] = rval
		self.root.geometry(f'{self.__geometry[0]}x{rval}')

	@property
	def bg( self ) -> str:
		return self.__bg
	
	@bg.setter
	def bg( self, val:str ):
		self.__bg = val
		self.canv.config( bg=val )

	def __repr__( self ):
		return f'Window(title="{self.root.title()}")'

class __GFXObject():
	def __init__(
		self,
		window:Window,
		x:int, y:int,
		fill:str = 'white',
		outline:str = 'black',
		outlineWidth:int = 1
	):
		self.gfx = window
		self._fill = fill
		self._outline = outline
		self._outlineWidth = outlineWidth
		self._hidden = False
		self._pos = [ x, y ]

	@property
	def x( self ) -> int: return self._pos[0]

	@property
	def y( self ) -> int: return self._pos[1]

	@x.setter
	def x( self, val:int ):
		rval = round( val )
		if self._pos[0] == rval: return
		self._pos[0] = rval
		self.gfx.canv.moveto( self.part, self._pos[0], self._pos[1] )

	@y.setter
	def y( self, val:int ):
		rval = round( val )
		if self._pos[1] == rval: return
		self._pos[1] = rval
		self.gfx.canv.moveto( self.part, self._pos[0], self._pos[1] )

	@property
	def fill( self ) -> str: return self._fill

	@property
	def outline( self ) -> str: return self._outline

	@property
	def outlineWidth( self ) -> int: return self._outlineWidth

	@fill.setter
	def fill( self, val ):
		if val == self._fill: return
		self._fill = val
		self.gfx.canv.itemconfig( self.part, fill=val )

	@outline.setter
	def outline( self, val ):
		if val == self._outline: return
		self._outline = val
		self.gfx.canv.itemconfig( self.part, outline=val )

	@outlineWidth.setter
	def outlineWidth( self, val ):
		if val == self._outlineWidth: return
		self._outlineWidth = val
		self.gfx.canv.itemconfig( self.part, width=val )

	def hide( self ):
		self._hidden = True
		self.gfx.canv.itemconfig( self.part, state='hidden' )

	def show( self ):
		self._hidden = False
		self.gfx.canv.itemconfig( self.part, state='normal' )

	def destroy( self ):
		self.gfx.canv.delete( self.part )

class __GFXBBOXObject(__GFXObject):
	def __init__(
		self,
		window:Window,
		x:int, y:int,
		w:int, h:int,
		fill:str = 'white',
		outline:str = 'black',
		outlineWidth:int = 1
	) -> None:
		super().__init__( window, x, y, fill=fill, outline=outline, outlineWidth=outlineWidth )
		self._pos = [x,y,w,h]

	@property
	def width( self ) -> int: return self._pos[2]

	@property
	def height( self ) -> int: return self._pos[3]

	@width.setter
	def width( self, val:int ):
		self._pos[2] = round( val )
		self.gfx.canv.coords(	# No, you can't use .itemconfig.
			self.part,			# It doesn't properly display shapes such as the oval.
			self._pos[0],
			self._pos[1],
			self._pos[2] + self._pos[0],
			self._pos[3] + self._pos[1],
		)

	@height.setter
	def height( self, val:int ):
		self._pos[3] = round( val )
		self.gfx.canv.coords(
			self.part,
			self._pos[0],
			self._pos[1],
			self._pos[2] + self._pos[0],
			self._pos[3] + self._pos[1],
		)

class Rect(__GFXBBOXObject):
	def __init__(
		self,
		window:Window,
		x:int, y:int,
		w:int, h:int,
		fill:str='white',
		outline:str='black',
		outlineWidth:int=1
	) -> None:
		super().__init__( window, x, y, w, h, fill=fill, outline=outline, outlineWidth=outlineWidth )
		self.part = window.canv.create_rectangle( x, y, x+w, y+h, fill=fill, outline=outline )

	def __repr__( self ):
		return f'Rect(x={self._pos[0]},y={self._pos[1]},width={self._pos[2]},height={self._pos[3]})'

class Oval(__GFXBBOXObject):
	def __init__(
		self,
		window:Window,
		x:int, y:int,
		w:int, h:int,
		fill:str='white',
		outline:str='black',
		outlineWidth:int=1
	) -> None:
		super().__init__( window, x, y, w, h, fill=fill, outline=outline, outlineWidth=outlineWidth )
		self.part = window.canv.create_oval( x, y, x+w, y+h, fill=fill, outline=outline )

	def __repr__( self ):
		return f'Oval(x={self._pos[0]},y={self._pos[1]},width={self._pos[2]},height={self._pos[3]})'

class Line():
	def __init__(
		self,
		gfxWindow:Window,
		x1:int, y1:int,
		x2:int, y2:int,
		width:int=1,
		fill:str='black'
	) -> None:
		self.gfx = gfxWindow
		self._pos = [ x1, y1, x2, y2 ]
		self._fill = fill
		self._width = width
		self._hidden = False
		self.part = gfxWindow.canv.create_line( x1, y1, x2, y2, width=width, fill=fill )

	@property
	def x1( self ) -> int: return self._pos[0]

	@property
	def y1( self ) -> int: return self._pos[1]

	@property
	def x2( self ) -> int: return self._pos[2]

	@property
	def y2( self ) -> int: return self._pos[3]

	@x1.setter
	def x1( self, val:int ) -> None:
		self._pos[0] = val
		self.gfx.canv.coords( self.part, val, self._pos[1], self._pos[2], self._pos[3] )

	@y1.setter
	def y1( self, val:int ) -> None:
		self._pos[1] = val
		self.gfx.canv.coords( self.part, self._pos[0], val, self._pos[2], self._pos[3] )

	@x2.setter
	def x2( self, val:int ) -> None:
		self._pos[2] = val
		self.gfx.canv.coords( self.part, self._pos[0], self._pos[1], val, self._pos[3] )

	@y2.setter
	def y2( self, val:int ) -> None:
		self._pos[3] = val
		self.gfx.canv.coords( self.part, self._pos[0], self._pos[1], self._pos[2], val )

	@property
	def fill( self ) -> str: return self._fill

	@fill.setter
	def fill( self, val ):
		if val == self._fill: return
		self._fill = val
		self.gfx.canv.itemconfig( self.part, fill=val )

	@property
	def width( self ) -> int:
		return self._width

	@width.setter
	def width( self, val:int ):
		self._width = val
		self.gfx.canv.itemconfig( self.part, width=val )

	def hide( self ):
		self._hidden = True
		self.gfx.canv.itemconfig( self.part, state='hidden' )

	def show( self ):
		self._hidden = False
		self.gfx.canv.itemconfig( self.part, state='normal' )

	def destroy( self ):
		self.gfx.canv.delete( self.part )

	def __repr__( self ):
		return f'Line(x1={self._pos[0]},y1={self._pos[1]},x2={self._pos[2]},y2={self._pos[3]})'

class Text(__GFXObject):
	def __init__(
		self,
		window: Window,
		x: int,
		y: int,
		content: str,
		fill: str = 'black',
		outline: str = '',
		outlineWidth: int = 1,
		fontFamily: str = 'Helvetica',
		fontSize: Union[int,float] = 12,
		fontVariant: str = 'normal',
		anchor: str = 'center'
		#alignX: int = 0,
		#alignY: int = 0
	) -> None:
		# Convert alignX and alignY into anchor form. This is pretty painful.
		# See: https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/anchors.html
		'''
		anchor = ''
		match (alignX, alignY):
			case -1, -1: anchor = 'nw'
			case  0, -1: anchor = 'n'
			case  1, -1: anchor = 'ne'
			case  -1, 0: anchor = 'w'
			case  0,  0: anchor = 'center'
			case  1,  0: anchor = 'e'
			case  -1, 1: anchor = 'sw'
			case  0,  1: anchor = 's'
			case  1,  1: anchor = 'se'
		'''

		super().__init__( window, x, y, fill=fill, outline=outline, outlineWidth=outlineWidth )
		self.part = window.canv.create_text(
			x, y,
			text=content,
			fill=fill,
			font=(fontFamily, fontSize, fontVariant),
			anchor=anchor
		)

	@property
	def width( self ):
		bbox = self.gfx.canv.bbox( self.part )
		return bbox[2] - bbox[0]

	@property
	def height( self ):
		bbox = self.gfx.canv.bbox( self.part )
		return bbox[3] - bbox[1]

	@property
	def content( self ):
		return self.gfx.canv.itemcget( self.part, 'text' )

	@content.setter
	def content( self, val:str ):
		self.gfx.canv.itemconfig( self.part, text=val )

	def __repr__( self ):
		return f'Text(x={self._pos[0]},y={self._pos[1]})'

class Poly(__GFXObject):
	def __init__(
		self,
		window: Window,
		points: list[int],
		fill: str = 'white',
		outline: str = 'black',
		outlineWidth: int = 1,
	) -> None:
		''' Represents a polygon created from an array of [ x0, y0, x1, y1, ... x100, y100, ... ] and so on. Unfortunately, verts cannot be modified at runtime. '''
		super().__init__( window, 0, 0, fill=fill, outline=outline, outlineWidth=outlineWidth )
		self.part = window.canv.create_polygon( *points, fill=fill, outline=outline )
		self._pos = window.canv.bbox( self.part )[:2]

	def __repr__( self ):
		return 'Poly()'

class Image():
	def __init__(
		self,
		window:Window,
		x:int, y:int,
		file:str|tk.PhotoImage,
		anchor:str = 'nw'
	) -> None:
		''' Represents an image retreived from a filepath. '''
		self.gfx = window
		self.photo = tk.PhotoImage( file=file, master=window.root )
		self.part = window.canv.create_image( x, y, image=self.photo, anchor=anchor )
		self._pos = [ x, y, self.photo.width(), self.photo.height() ]

	@property
	def x( self ) -> int: return self._pos[0]

	@property
	def y( self ) -> int: return self._pos[1]

	@property
	def width( self ) -> int: return self._pos[2]

	@property
	def height( self ) -> int: return self._pos[3]

	@x.setter
	def x( self, val:int ):
		rval = round( val )
		if self._pos[0] == rval: return
		self._pos[0] = rval
		self.gfx.canv.moveto( self.part, self._pos[0], self._pos[1] )

	@y.setter
	def y( self, val:int ):
		rval = round( val )
		if self._pos[1] == rval: return
		self._pos[1] = rval
		self.gfx.canv.moveto( self.part, self._pos[0], self._pos[1] )

	def destroy( self ):
		self.gfx.canv.delete( self.part )

	def __repr__( self ):
		return f'Image(x={self._pos[0]},y={self._pos[1]})'

''' MODULE TEST '''

if __name__ == '__main__':

		from random import choice

		myWin		= Window( 'BGFX Demonstration', width=350, height=200, bg='#111' )
		myTitle		= Text( myWin, 175, 100, 'Hello, world!', fill='#999', fontSize=30 )
		mySubtitle	= Text( myWin, 175, 120, 'Import this file to use it as a module.', fill='#555', fontSize=10 )

		def doClick( mouseX, mouseY ):
			myTitle.content = choice(['Hello, world!', 'Another title!', 'How??', 'What??', 'Amazing!'])
		myWin.onMousePressed = doClick

		while myWin.isOpen:
			if myWin.mouseOver( myTitle ):	myTitle.fill = '#fff'
			else:							myTitle.fill = '#999'
			myWin.update()
