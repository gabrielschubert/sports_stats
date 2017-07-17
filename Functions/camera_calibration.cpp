#include "opencv2/opencv.hpp"
#include <iostream>
#include <vector>
#include <unistd.h>

using namespace std;
using namespace cv;

int main(){

	int numBoards = 100;
	int board_w = 9;
	int board_h = 6;
	int success = 0;
	float squareLenght = 22.5;

	Size board_sz = Size(board_w, board_h);
	int board_n = board_w*board_h;


	vector<vector<Point3f> > calib_objectPoints;
	vector<vector<Point2f> > calib_imagePoints;
	vector<Point2f> corners;

	vector<Point3f> obj;
        for(int i = 0; i<board_h; i++){
            for(int j=0;j<board_w;j++){
                obj.push_back(cv::Point3f(float(i)*squareLenght,float(j)*squareLenght,0.0f));
            }
        }

	VideoCapture cap(-1); 
	if(!cap.isOpened()){
		cout << "Error opening video stream or file" << endl;
		return -1;
	}
	
	cap.set(CV_CAP_PROP_FRAME_WIDTH,1280);
	cap.set(CV_CAP_PROP_FRAME_HEIGHT,720);
	int frame_width = cap.get(CV_CAP_PROP_FRAME_WIDTH);
	int frame_height = cap.get(CV_CAP_PROP_FRAME_HEIGHT);


	Mat frame;
	Mat gray;

	while (success<numBoards)
	{		
	
		cap >> frame;
		cvtColor(frame, gray, CV_BGR2GRAY);
		bool patternfound = findChessboardCorners(gray,board_sz,corners);

		if (patternfound)
		{
			calib_imagePoints.push_back(corners);
			calib_objectPoints.push_back(obj);
			printf ("Corners stored\n");
			success++;

		cornerSubPix(gray, corners, Size(11, 11), Size(-1, -1), TermCriteria(CV_TERMCRIT_EPS | CV_TERMCRIT_ITER, 30, 0.1));	
		drawChessboardCorners(frame, board_sz, Mat(corners), patternfound);

		}

		imshow( "Frame", frame );
		usleep(100000);


		char c = (char)waitKey(33);
		if( c == 27 ) break;
	}
	
	cvDestroyAllWindows();
	cap.release();
	
	
	std::cout << "Stored points: " << calib_imagePoints.size() << "\n";

	Mat cameraMatrix = Mat(3, 3, CV_32FC1);
	Mat distCoeffs;
	vector<Mat> calib_rvec, calib_tvec;

	cameraMatrix.at<float>(0, 0) = 1;
	cameraMatrix.at<float>(1, 1) = 1;
	
	calibrateCamera(calib_objectPoints, calib_imagePoints, frame.size(), cameraMatrix, distCoeffs, calib_rvec, calib_tvec);


	// Read points
	std::vector<Point2f> imagePoints;
	imagePoints.push_back(Point2f(32, 623));
	imagePoints.push_back(Point2f(1237, 650));
	imagePoints.push_back(Point2f(1016, 229));
	imagePoints.push_back(Point2f(318, 224));


	std::vector<Point3f> objectPoints;
	objectPoints.push_back(Point3f(0, 0, 0));
	objectPoints.push_back(Point3f(297, 0, 0));
	objectPoints.push_back(Point3f(297, 210, 0));
	objectPoints.push_back(Point3f(0, 210, 0));


	std::cout << "There are " << imagePoints.size() << " imagePoints and " << objectPoints.size() << " objectPoints." << std::endl;


	cv::Mat rvec(3,1,cv::DataType<double>::type);
	cv::Mat tvec(3,1,cv::DataType<double>::type);

	cv::solvePnP(objectPoints, imagePoints, cameraMatrix, distCoeffs, rvec, tvec);

	std::cout << "rvec: " << rvec << std::endl;
	std::cout << "tvec: " << tvec << std::endl;

	std::vector<cv::Point2f> projectedPoints;
	cv::projectPoints(objectPoints, rvec, tvec, cameraMatrix, distCoeffs, projectedPoints);

	for(unsigned int i = 0; i < projectedPoints.size(); ++i)
	{
	std::cout << "Image point: " << imagePoints[i] << " Projected to " << projectedPoints[i] << std::endl;
	}
	
	cv::Mat rotationMatrix(3,3,cv::DataType<double>::type);
	cv::Rodrigues(rvec,rotationMatrix);

	cv::Mat uvPoint = cv::Mat::ones(3,1,cv::DataType<double>::type);
	uvPoint.at<double>(0,0) = 32.;
	uvPoint.at<double>(1,0) = 623.;
	cv::Mat tempMat, tempMat2;
	double s;
	int z = 0;
	tempMat = rotationMatrix.inv() * cameraMatrix.inv() * uvPoint;
	tempMat2 = rotationMatrix.inv() * tvec;
	s = z + tempMat2.at<double>(2,0);
	s /= tempMat.at<double>(2,0);
	std::cout << "P = " << rotationMatrix.inv() * (s * cameraMatrix.inv() * uvPoint - tvec) << std::endl;


	return 0;
}
