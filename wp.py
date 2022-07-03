#!bin/python3
from PIL import Image

img = Image.open('x.jpg')


#Min source dimensions 6560 * 1920

sourceX, sourceY = img.size[0], img.size[1]
outRes = [(1920, 1080, 27), (2560, 1440, 32), (1080, 1920, 27)]


def getLargestAxis(outRes):
	"""Returns the largest axis from 'outRes' as 
	largestAxis[(0=x, 1=y), largest x axis, largest y axis, (largest landscape display), (largest port display)]
	"""

	largestAxis = [0, 0, 0, 0, 0]

	for i in outRes:
		
		for j in range(0, len(i)):

			if i[0] > largestAxis[1]:
				#new x axis
				largestAxis[1] = i[0]
				largestAxis[3] = (i[0], i[1], i[2])
				anchorDisplay = largestAxis[3]

			if i[1] > largestAxis[2]:
				#new y axis
				largestAxis[2] = i[1]
				largestAxis[4] = (i[0], i[1])

			if largestAxis[1] > largestAxis[2]:
				#what is the primary orientation of the displays (0 = lscape, 1 = port)
				largestAxis[0] = '0'
			else:
				largestAxis[0] = '1'


	return largestAxis, anchorDisplay


def validate(largestAxis):
	"""calculate total output resolution, verify source img resoulution sufficient
	"""

	def createResized(x, y):
		"""IN PROGRESS - RESIZE SOURCE IMAGE TO LARGEST AXIS"""

		if x > y:
			ratio = sourceY / sourceX

			x = sourceX * ratio
			y = sourceY * ratio

		print('source x {} source y {} \nscreen x {} screen y {} \nrezized x {} resized y {}'.format(sourceX, sourceY, totalX, totalY, x, y))



	#minimum output resolution required (based on 'outRes')
	totalX, totalY = 0, 0

	if largestAxis[0] == 0:
		totalX = largestAxis[1]
	else:
		totalY = largestAxis[2]

	for i in outRes:
		#assumes display is landscape
		pixelsToMultiply = largestAxis[3][0]

		if i[1] > i[0]:
			#display is portrait
			pixelsToMultiply = largestAxis[3][1]

		totalX += int((i[0] * (pixelsToMultiply / i[0])))

	print("Minimum image dimensions         {} x {}".format(totalX, totalY))
	print("Supplied source image dimensions {} x {}".format(sourceX, sourceY))

	if (sourceX < totalX) or (sourceY < totalY):
		print("Source image too small")
		exit(1)

	createResized(totalX, totalY)

def calcTempDims():
	"""calculate initial output image dimensions prior to resizing"""

	tempDims = []

	for i in outRes:

		tempx = i[0]
		tempy = i[1]
		
		if tempx > tempy:
			#landscape
			x = tempx * (largestAxis[3][0] / tempx)
			y = tempy * (largestAxis[3][1] / tempy)

		else:
			#portrait
			x = tempx * (largestAxis[3][1] / tempx)
			y = tempy * (largestAxis[3][0] / tempy)

		tempDims.append((int(x), int(y)))

	return tempDims


def make():
	#Crops the images out of the source at the highest resolution required

	def resize(tempImg, x, y, z):

		ox = tempImg.size[0]
		oy = tempImg.size[1]


		if y > x:
			tempImg.rotate(90)
			cropPercent = ((largestAxis[3][0] / x) * (anchorDisplay[2] / z *.095))
			tempImg = tempImg.crop((ox * cropPercent, (oy * cropPercent), ox, oy))
			tempImg.rotate(270)
			tempImg = tempImg.resize((x, y))
		
		else:
			cropPercent = ((largestAxis[3][1] / y) * (anchorDisplay[2] / z *.095))
			tempImg = tempImg.crop((ox * cropPercent, (oy * cropPercent), ox, oy))
			tempImg = tempImg.resize((x, y))

		return tempImg



	#list containing the output images
	outImages = []
	workingX = 0
	
	#compensate for display bezels (L-R)
	bezels = [80, 60]

	#allows for vert display to have base below the other ones.
	#set to 0 if base of vert display is level with the others.
	vertMonOffset = 300


	for h, i in enumerate(tempDims):

		#set endY to a lower point if offset is required
		if i[0] > i[1]:
			endY = (sourceY - vertMonOffset)
		else:
			endY = sourceY

		outImage = img.crop((workingX, (sourceY - (i[1] + vertMonOffset)), (i[0] + workingX), endY))

		workingX += i[0]

		#allows for bezel offset
		try:
			workingX += bezels[h]
		except:
			pass

		#outImage.save(str(h) + '000.jpg')

		if (outRes[h][0] != anchorDisplay[0]) and (outRes[h][1] != anchorDisplay[1]):
			outImage = resize(outImage, outRes[h][0], outRes[h][1], outRes[h][2])

		outImage.save(str(h) + '.jpg')




largestAxis, anchorDisplay = getLargestAxis(outRes)

validate(largestAxis)

tempDims = calcTempDims()

make()
exit(0)