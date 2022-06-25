#!bin/python3
from PIL import Image

img = Image.open('input.jpg')

sx, sy = img.size[0], img.size[1]
outRes = [(1920, 1080), (2560, 1440), (1080, 1920)]
#out3 = (1920, 1080)

def validate():
	#calculate total output resolution, verify source img resoulution sufficient
	ox, oy = 0, 0

	for i in outRes:
		ox += i[0]

		if i[1] > oy:
			oy = i[1]


	if sx < ox or sy < oy:
		print('Source image too small, resolution must be at least {} x {}, source image is only {} x {}'.format(ox, oy, sx, sy))
		exit(1)


def make(outRes):
	workingX = 0

	for i, j in enumerate(outRes):
		output = img.crop((workingX, (sy - j[1]), (workingX + j[0]), sy))
		workingX += j[0]

		output.save('{}.jpg'.format(i))

validate()
make(outRes)