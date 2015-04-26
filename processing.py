__author__ = 'Brian Diaz'
import cv2
import numpy as np
from image import Image

min_radius = 7
max_radius = 20

class Processing:
    def __init__(self, image):
        self.image = image
        self.image_data = image.load()

    # Save a Image to local path
    def save_image(self, image, path):
        cv2.imwrite(path, image)

    # Set Gray Scale image for a better algorithm efficiency
    def gray_scale(self):
        return cv2.cvtColor(self.image_data, cv2.COLOR_BGR2GRAY)

    #Draw Gaussian Blur
    def gaussian_blur(self):
        return cv2.GaussianBlur(self.gray_scale(),(5,5),0)

    # Get a more resistant to noise operator that joints Gaussian smoothing plus differentiation operation
    def gradient(self):
        return cv2.Sobel(self.gaussian_blur(), cv2.CV_8U, 1, 0, ksize=3)


    def umbral(self):
        _,umbral = cv2.threshold(self.gradient(), 170, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return umbral

    # Get all Ellipses
    def structuring_elements(self):
        return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    # Get all morphologies of the umbral data
    def morphology_elements(self):
        return cv2.morphologyEx(self.umbral(), cv2.MORPH_CLOSE, self.structuring_elements())

    def get_domino_points(self):
        contours,_ = cv2.findContours(self.morphology_elements(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        print("Circles: "+ str(len(contours)))

        circles = self.draw_circles(self.image_data, contours)
        text = str(len(circles)) + " Points"
        
        print text
        cv2.putText(self.image_data, text, (20, self.image.height - 20), cv2.FONT_ITALIC, 1, (0,0,0))

        cv2.imwrite('result.jpg',self.image_data)
        Image.show(self.image_data)

    # Draw Circles in the image
    def draw_circles(self, image, contours):
        circles = []
        for cnt in contours:
            # Getting the circle (x,y position and radius) of the contour.
            (x,y),radius = cv2.minEnclosingCircle(cnt)
            center = (int(x),int(y))
            radius = int(radius)
            # Possible Domino point.
            if radius >= min_radius and radius <= max_radius: 
                # Draw the circle in the image with green color.
                cv2.circle(self.image_data,center,radius,(0,255,0),2)
                circles.append(cnt)
        return circles