import numpy as np

#data published on raw depth_image topic by talker.cpp

#convert string data into 8-bit unsigned integers
idata1D = np.array(astring.split(','), dtype=np.uint8)
idata2D = np.ndarray(shape=(480,640), dtype=np.uint16, order='C') 

print('size of raw array')
print(idata1D.size)

row_col = np.array([1, 1], dtype=np.uint16)

#convert 8-bit 1-D unsigned integer array into 16-bit unsigned 
#integers (using 2 elements of 1-D array for each 16-bit unsigned 
#integer element) and into 480x640 (row, col) shape

for i in range(0, (idata1D.size) - 2, 2):
    row_col[0] = i/(640*2)
    row_col[1] = (i/2)%640

    idata2D[row_col[0]][row_col[1]] = (idata1D[i+1] << 8)
    idata2D[row_col[0]][row_col[1]] = idata2D[row_col[0]][row_col[1]] | idata1D[i]

#print the row which represents the scan line (centre one among 480 rows)
print(idata2D[240])

#idata1D = np.array([1, 1], dtype=np.uint8)
#idata2D = np.array([1, 1], dtype=np.uint16)

#idata2D[0] = (idata1D[0] << 8)
#idata2D[0] = idata2D[0] | idata1D[0]
