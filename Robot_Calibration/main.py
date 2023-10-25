import pandas as pd
import numpy as np
import cv2 as cv

def load_data(path):
    return pd.read_csv(path, header=None)

def homogenize_coordinate(coord):
    return f"{coord}:1"

if __name__ == "__main__":
    
    cam_coords_file_path = "Data/Calibration/camera_coords.csv"
    tcp_coords_file_path = "Data/Calibration/tcp_coords.csv"

    cam_coords = load_data(cam_coords_file_path)
    tcp_coords = load_data(tcp_coords_file_path)
    
    print("Raw camera coordiantes\n", cam_coords.shape, cam_coords)
    print("Raw tcp coordiantes\n", tcp_coords.shape, tcp_coords)
    
    # Add ":1" to homogenize the coordinates in camera_coords_data
    cam_coords_homogeneous = cam_coords.applymap(homogenize_coordinate)

    # Add ":1" to homogenize the coordinates in robot_tcp_coords_data
    tcp_coords_homogeneous = tcp_coords.applymap(homogenize_coordinate)
    
    print("Homogenous camera coordiantes\n", cam_coords_homogeneous.shape, cam_coords_homogeneous)
    print("Homogenous tcp coordiantes\n", tcp_coords_homogeneous.shape, tcp_coords_homogeneous)
    
    # # termination criteria
    # criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    # objp = np.zeros((6*7,3), np.float32)
    # objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
    # # Arrays to store object points and image points from all the images.
    # objpoints = [] # 3d point in real world space
    # imgpoints = [] # 2d points in image plane.
    
    # img = cv.imread("Data/Images/rgb_27.png")
    # gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    # ret, corners = cv.findChessboardCorners(gray, (8,6), None)
    
    # # If found, add object points, image points (after refining them)
    # if ret == True:
    #     objpoints.append(objp)
    #     corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
    #     imgpoints.append(corners2)
        
    # # Draw and display the corners
    # cv.drawChessboardCorners(img, (8,6), corners2, ret)
    # cv.imshow('img', img)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    
    # ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    
    # img = cv.imread("Data/Images/rgb_27.png")
    # h, w = img.shape[:2]
    # newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))