#!/usr/bin/env python3	
# -*- coding: utf-8 -*-

import numpy as np
from matplotlib import pyplot as plt
import cv2
import glob
import time
import pickle
import sys


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
cap.set(cv2.CAP_PROP_FRAME_WIDTH,600);
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,400);

while(True):
    
    # Capture frame-by-frame ignoring camera buffer
    for i in range(5):
        ret, frame = cap.read()
    
    # Change color and print
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (9,6),None)
    print(ret)
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp*size_pattern)
        print(len(objpoints))
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(gray, (9,6), corners2,ret)
        cv2.imshow('img',img)
        cv2.waitKey(50)
        #cv2.destroyAllWindows()

    if len(objpoints)>49:
        cap.release()
        break

# Release the capture
cv2.destroyAllWindows()
cap.release()


print('calculating...')
ret, camera_matrix, dist_coef, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)


# Save calibration data
print('saving data...')
data = {"camera_matrix":camera_matrix, "dist_coef":dist_coef}

path = sys.argv[1] + '/data.pkl')
output = open(path, 'wb')
pickle.dump(data, output)
output.close()

'''
# Load calibration data
pkl_file = open('data.pkl', 'rb')
data2 = pickle.load(pkl_file)
pkl_file.close()

camera_matrix = data2['camera_matrix']
dist_coef = data2['dist_coef']


# 2D image points.
image_points = np.array([(32, 623), (1237, 650), (1016, 229), (318, 224)], dtype="double")
 
# 3D model points.
model_points = np.array([(0, 0, 0), (297, 0, 0), (297, 210, 0), (0, 210, 0)], dtype="double")


# Find rotation and translation
(success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coef, cv2.SOLVEPNP_P3P)

# Estimate 2D point
(point2D, jacobian) = cv2.projectPoints(np.array([(279, 0, 0)], dtype="double"), rotation_vector, translation_vector, camera_matrix, dist_coef)


camera_matrix_inv = np.linalg.inv(camera_matrix)

rotation_matrix = cv2.Rodrigues(rotation_vector)[0]
rotation_matrix_inv = np.linalg.inv(rotation_matrix)


# Estimate 3D point
z = 0
uvPoint = np.array([1237,650,1]).reshape(3,1)

s = (z + np.matmul(rotation_matrix_inv, translation_vector)[2])/(np.matmul(np.matmul(rotation_matrix_inv, camera_matrix_inv),uvPoint)[2])
p = np.matmul(rotation_matrix_inv, (np.matmul(camera_matrix_inv, s * uvPoint) - translation_vector))
'''

