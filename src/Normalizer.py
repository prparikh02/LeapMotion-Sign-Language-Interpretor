class Normalizer(object):
	"""
	This class will normalize the data
    
    Sample Use:
    
    import numpy as np
    from Normalizer import Normalizer
    
    myNorm = Normalizer()
    kienVec = np.load('testdata.npy')
    normed = myNorm.affine(kienVec, file)
	"""

	# do an affine normalization of the x, y, z coordinated on the hand by moving the palm to the origin 
	def affine(self, numpyArrayFromKien, mapFile):
		"""
		This function does an affine translation of the hand by centering the palm at the origin.
		Input: a numpyArrayFromKien and a path to a file with the lines defining the elements of the numpy array
		Output: an adjusted numpy Array
		"""

		# open the file
		mapper  = open(mapFile, 'r')

		# determine how many lines are in the file
		for i, l in enumerate(mapper):
			pass
		file_len = i+1

		# initialize vectors for determining which lines end in x, y, z
		xs_left = [0] * file_len
		ys_left = [0] * file_len
		zs_left = [0] * file_len
		xs_right = [0] * file_len
		ys_right = [0] * file_len 
		zs_right = [0] * file_len

		# variables to hold vector location of palm position 
		leftx = lefty = leftz = rightx = righty = rightz = 0

		mapper  = open(mapFile, 'r')

		# note which lines have x, y, z at the end
		for j, line in enumerate(mapper):
			line = line.rstrip('\n')
			length = len(line)
			if (line[12] == 'l'):
				if (line[length-1] == 'x'):
					xs_left[j] = 1
				elif (line[length-1] == 'y'):
					ys_left[j] = 1
				elif (line[length-1] == 'z'):
					zs_left[j] = 1

			else:
				if (line[length-1] == 'x'):
					xs_right[j] = 1
				elif (line[length-1] == 'y'):
					ys_right[j] = 1
				elif (line[length-1] == 'z'):
					zs_right[j] = 1

			# record vector location of palm parameters 
			if (line == 'frame.hands.left.palm_pos.x'):
				leftx = j
			elif (line == 'frame.hands.left.palm_pos.y'):
				lefty = j
			elif (line == 'frame.hands.left.palm_pos.z'):
				leftz = j	

			elif (line == 'frame.hands.right.palm_pos.x'):
				rightx = j
			elif (line == 'frame.hands.right.palm_pos.y'):
				righty = j
			elif (line == 'frame.hands.right.palm_pos.z'):
				rightz = j

		# close the file
		mapper.close()

		# go through every row of matrix
		# find amount to shift each x, y, z and conduct the affine transformation 
		for row in numpyArrayFromKien:
			
			# record the actual palm location of the left hand
			xDiff_Left = row[leftx]
			yDiff_Left = row[lefty]
			zDiff_Left = row[leftz]

			# record the actual palm location of the right hand
			xDiff_Right = row[rightx]
			yDiff_Right = row[righty]
			zDiff_Right = row[rightz]		

			# loop through each row of the matrix
			for i, val in enumerate(row):
				if (xs_left[i] == 1):
					row[i] -= xDiff_Left
				elif (ys_left[i] == 1):
					row[i] -= yDiff_Left
				elif (zs_left[i] == 1):
					row[i] -= zDiff_Left

				elif (xs_right[i] == 1):
					row[i] -= xDiff_Right
				elif (ys_right[i] == 1):
					row[i] -= yDiff_Right
				elif (zs_right[i] == 1):
					row[i] -= zDiff_Right

		return numpyArrayFromKien














