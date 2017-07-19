# **Finding Lane Lines on the Road** 



---

**Finding Lane Lines on the Road**

The goal of this project is to develop a pipeline that can detect the lane lines in a picture and draw line markers along the lane lines.  The pipeline will be used with some images first, and then with videos. 

---

### Reflection

### 1. Pipeline Description

The pipeline is designed in following stages

1. Convert the input image from RGB space to Gray space. So the pipeline can work with lane markers with any color
2. Blur the gray image with a Gaussian blur function to suppress the noises.
3. Detect the edges by using canny. 
4. Define a region and search the lines only in this region.
5. Fit the edges with lines by using hough transformation.
6. overlay the lines with original input images

Improving the draw_line() function:

With the original version of draw_line function, the lines may be drawn as segments. We want to draw a full extent of the lane. I modified this function as following:

1.  Calculate the slope of the input line segment. If the slope is negative, it should be a left lane, else, it's considered as right lane. If it's a horizontal or vertical line, it will be discarded since the lane is unlikely to be a H/V line due to perspective.
2. Calculate the intersection of the line and the Ymax/Ymin. Here, Ymax is the bottom of the image, and Ymin is the top line of the interest region. The intersection points will be put into 4 lists, for the upper/lower points of the left/right lane.
3. Average the X position in the 4 lists, respectively.
4. Draw 2 lines by using the left and right lists.   


### 2. Shortcoming of this pipeline


This pipeline does not work with curved lanes. It's hard to tune for different scenarios like in different light conditions, different cameras and camera positions on the cars, and images with different edge length. This pipeline may also be hard to calibrate in mass production. 




### 3. Suggest possible improvements to your pipeline

Method 1: Split the image into horizontal slices/windows. They might not be in same size in Y with considering the perspective. Then apply the pipeline in each window. Thus the curved lanes might be able to be highlighted.

Method 2: Try to recover the image by performing a perspective transform on the image. Then use high order polynomial to fit the detected edges.

Method 3: If failed to detect lanes in current frame, keep using lanes from last frame. If the lanes detected in current frame have a big difference than the lanes detected in history, using the lanes from last frame instead. (Or there is a crash we must apply the brake...) 