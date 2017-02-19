list1 = 'frame'
list2 = 'hands'
list3 = ['left', 'right']
list4 = 'fingers'
list5 = ['index', 'middle', 'pinky', 'thumb', 'ring']
list6 = 'bones'
list7 = ['metacarpal', 'proximal', 'distal', 'intermediate']
list8 = ['direction', 'nextJoint', 'prevJoint']
list9 = ['x', 'y', 'z']
list10 = 'palmPosition'
list11 = ['pitch', 'yaw', 'roll']

f = open("mapperVec.txt","w") 

for i in list3:
	for j in list5:
		for k in list7:
			for l in list8: 
				for m in list9:
					toPrint = [list1, list2, i, list4, j, list6, k, l, m]
					f.write('.'.join( toPrint) + '\n')

for i in list3:
	for j in list9:
		f.write('.'.join([list1, list2, i, list10, j]) + '\n')
	for k in list11:
		f.write('.'.join([list1, list2, i, k]) + '\n')

# left also has palm position which has xyz. left also has pitch, yaw, and roll