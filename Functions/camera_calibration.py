
# coding: utf-8

# In[1]:


import numpy as np
from matplotlib import pyplot as plt
import cv2
import glob
import time
import pickle



# Termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)

# Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((9*6,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
size_pattern = 22.5 # mm




cap = cv2.VideoCapture(0)
#cap.set(cv2.CAP_PROP_BUFFERSIZE,1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280);
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720);

while(True):
    
    # Capture frame-by-frame ignoring camera buffer
    for i in range(5):
        ret, frame = cap.read()
    
    # Change color and print
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    plt.imshow(gray,cmap='gray')
    plt.show()
    plt.close()
    
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (9,6),None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp*size_pattern)
        print(len(objpoints))
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(gray, (9,6), corners2,ret)
        #cv2.imshow('img',img)
        #cv2.waitKey(500)
        #cv2.destroyAllWindows()

    if len(objpoints)>50:
        cap.release()
        break

# Release the capture
cap.release()


# In[4]:


ret, camera_matrix, dist_coef, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)


# In[5]:


# Save calibration data
data = {"camera_matrix":camera_matrix, "dist_coef":dist_coef}

output = open('data.pkl', 'wb')
pickle.dump(data, output)
output.close()


# In[ ]:


# Load calibration data
pkl_file = open('data.pkl', 'rb')
data2 = pickle.load(pkl_file)
pkl_file.close()

camera_matrix = data2['camera_matrix']
dist_coef = data2['dist_coef']


# In[6]:


# 2D image points.
image_points = np.array([(32, 623), (1237, 650), (1016, 229), (318, 224)], dtype="double")
 
# 3D model points.
model_points = np.array([(0, 0, 0), (297, 0, 0), (297, 210, 0), (0, 210, 0)], dtype="double")


# In[7]:


# Find rotation and translation
(success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coef, cv2.SOLVEPNP_P3P)


# In[33]:


# Estimate 2D point
(point2D, jacobian) = cv2.projectPoints(np.array([(279, 0, 0)], dtype="double"), rotation_vector, translation_vector, camera_matrix, dist_coef)


# In[34]:


point2D


# In[35]:


camera_matrix_inv = np.linalg.inv(camera_matrix)

rotation_matrix = cv2.Rodrigues(rotation_vector)[0]
rotation_matrix_inv = np.linalg.inv(rotation_matrix)


# In[51]:


# Estimate 3D point
z = 0
uvPoint = np.array([1237,650,1]).reshape(3,1)

s = (z + np.matmul(rotation_matrix_inv, translation_vector)[2])/(np.matmul(np.matmul(rotation_matrix_inv, camera_matrix_inv),uvPoint)[2])
p = np.matmul(rotation_matrix_inv, (np.matmul(camera_matrix_inv, s * uvPoint) - translation_vector))


# In[52]:


s


# In[53]:


p


# In[ ]:


camera_matrix


# In[ ]:


dist


# In[ ]:


rotation_vector


# In[ ]:


translation_vector


# In[ ]:


cv2.__file__


# In[ ]:





# In[ ]:




