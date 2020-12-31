'''
Python raw framebuffer library (for Linux)
Copyright @raspiduino 2020
Date created 8:30 PM 31/12/2020
'''

import os
import mmap # Memory map library
import getpass

class Framebuffer():
	'''
	Framebuffer class
		Varriables:
			screenx: x screen size
			screeny: y screen size
			bpp    : Bit per pixel
			fbpath : Framebuffer path
			fbdev  : Framebuffer opened as normal file
			fb     : Framebuffer memory mapped object
		Functions:
			__init__ : init function
			drawpixel: function to draw a single pixel
			clear    : function to clear the screen

	'''
	def __init__(self, fbpath="/dev/fb0"):
		'''
		__init__ function
		Optional: Require frame buffer path. Default is /dev/fb0
		Note: Please add your current user to video group. If not,
		the library will add this for you, require root.
		'''
		if os.system('getent group video | grep -q "\b'+ getpass.getuser() +'\b"') == 1:
			# User not in video group
			print("This command will be run as root, please allow it in order to get framebuffer work!")
			os.system("sudo adduser " + getpass.getuser() + " video")
			print("Done! Now you can use framebuffer without root!")

		# Now user in video group
		# Get screen info

		# Get screen size
		_ = open("/sys/class/graphics/fb0/virtual_size", "r")
		__ = _.read()
		self.screenx = int(__[:4])
		self.screeny = int(__[5:8])
		_.close()

		# Get bit per pixel
		_ = open("/sys/class/graphics/fb0/bits_per_pixel", "r")
		self.bpp = int(_.read()[:2])
		_.close()

		# Open the framebuffer device
		self.fbpath = fbpath
		self.fbdev = os.open(self.fbpath, os.O_RDWR)

		# Map framebuffer to memory
		self.fb = mmap.mmap(self.fbdev, screenx*screeny*bpp//8, mmap.MAP_SHARED, mmap.PROT_WRITE|mmap.PROT_READ, offset=0)

	def drawpixel(self, x, y, r, g, b, t=0):
		'''
		drawpixel function
		Draw a single pixel with color
		Require:
			x: x coordinate of the pixel
			y: y coordinate of the pixel
			
			RGB color:
				r: Red color (0 -> 255)
				g: Green color (0 -> 255)
				b: Blue color (0 -> 255)

			t: transparency (default set to 0)
		'''
		self.fb.seek(x*y*self.bpp//8) # Set the pixel location

		if self.bpp == 32:
			# 32 bit per pixel
			self.fb.write(b.to_bytes(1, byteorder='little')) # Write blue
			self.fb.write(g.to_bytes(1, byteorder='little')) # Write green
			self.fb.write(r.to_bytes(1, byteorder='little')) # Write red
			self.fb.write(t.to_bytes(1, byteorder='little')) # Write transparency

		else:
			# 16 bit per pixel
			self.fb.write(r.to_bytes(1, byteorder='little') << 11 | g.to_bytes(1, byteorder='little') << 5 | b.to_bytes(1, byteorder='little'))

	def clear(self, r, g, b, t=0):
		'''
		clear function
		Clear the screen with color
		Require:
			RGB color:
					r: Red color (0 -> 255)
					g: Green color (0 -> 255)
					b: Blue color (0 -> 255)

			t: transparency (default set to 0)
		'''
		for y in range(self.screeny):
			for x in range(self.screenx):
				self.drawpixel(x, y, r, g, b, t)

if __name__ == "__main__":
	fb0 = Framebuffer("/dev/fb0")
	fb0.clear()
	for y in range(fb0.screeny):
		for x in range(fb0.screenx):
			fb0.drawpixel(x, y, x%300, y%400, (x+y)%500)
