#!bin/python3
from PIL import Image

img = Image.open('t.jpg')


#1: 1920x1024 27in // 2: 2560x1140 31in // 3: 1024x1920 27in

#Min source dimensions 2560 * 6560

sx, sy = img.size[0], img.size[1]
#outRes = [(1920, 1080, 27), (2560, 1440, 32), (1080, 1920, 27)]

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
#make(outRes)

bezels0 = 80
bezels1 = 60

#allows for vert mount monitor with base below the other ones
vertMonOffset = 300

workingX = 0

out0 = img.crop((workingX, (sy - (1440 + vertMonOffset)), (workingX + 2560), (sy - vertMonOffset)))
workingX =+ 2560

ox = out0.size[0]
oy = out0.size[1]

out0 = out0.crop(((ox * .15), (oy * .15), ox, oy))
out0 = out0.resize((1920, 1080))
out0.save('0.jpg')

out1 = img.crop((workingX + bezels0, (sy - (1440 + vertMonOffset)), (workingX + bezels0 + 2560), (sy - vertMonOffset)))
out1.save('1.jpg')

workingX += (2560 + bezels0 + bezels1)

out2 = img.crop((workingX, (sy - 2560), workingX + 1440, sy))

ox = out0.size[0]
oy = out0.size[1]

out0 = out0.crop(((ox * .15), (oy * .15), ox, oy))
out2 = out2.resize((1080, 1920))
out2.save('2.jpg')


