import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from mpl_toolkits.mplot3d import Axes3D
# evenly sampled time at 200ms intervals


#def draw_boxes(img, bboxes, preds, show_all=False, color_p=(0, 0, 255), color_f=(128, 128, 128), thick=6):
def draw_boxes(img, bboxes, color=(0, 0, 255), color_f=(128, 128, 128), thick=6, in_place=False):
    # Make a copy of the image
    if not in_place:
        draw_img = np.copy(img)
    else:
        draw_img = img;
    # Iterate through the bounding boxes
    for bbox in bboxes:
        # Draw a rectangle given bbox coordinates
        cv2.rectangle(draw_img, bbox[0], bbox[1], color, thick)
    # Return the image copy with boxes drawn
    return draw_img

class ColorHist:
    #based on color_hist() from lession.py
    def __init__(self, img, nbins=32, bins_range=(0, 256)):
        self.img = img
        # Compute the histogram of the RGB channels separately
        self.rhist = np.histogram(img[:,:,0], bins=nbins, range=bins_range)
        self.ghist = np.histogram(img[:,:,1], bins=nbins, range=bins_range)
        self.bhist = np.histogram(img[:,:,2], bins=nbins, range=bins_range)
        # Concatenate the histograms into a single feature vector
        self.hist_features = np.concatenate((self.rhist[0], self.ghist[0], self.bhist[0]))

    def show(self):
        # Plot a figure with all three bar charts
        bin_edges = self.rhist[1]
        bin_centers = (bin_edges[1:]  + bin_edges[0:len(bin_edges)-1])/2
        if self.rhist is not None:
            fig = plt.figure(figsize=(12,3))
            """ 
            plt.subplot(231)
            plt.imshow(self.img[:,:,0], cmap='gray')
            plt.title('R ')
            plt.subplot(232)
            plt.imshow(self.img[:,:,1], cmap='gray')
            plt.title('G ')
            plt.subplot(233)
            plt.imshow(self.img[:,:,2], cmap='gray')
            plt.title('B ')
            """

            plt.subplot(141)
            plt.imshow(self.img)
            plt.title('Image')

            plt.subplot(142)
            plt.bar(bin_centers, self.rhist[0])
            plt.xlim(0, 256)
            plt.title('R Histogram')

            plt.subplot(143)
            plt.bar(bin_centers, self.ghist[0])
            plt.xlim(0, 256)
            plt.title('G Histogram')

            plt.subplot(144)
            plt.bar(bin_centers, self.bhist[0])
            plt.xlim(0, 256)
            plt.title('B Histogram')

            fig.tight_layout()
            return fig
        else:
            print('Your function is returning None for at least one variable...')

class ColorSpace:
    valid_formats = ('rgb', 'hsv', 'hls', 'yrb', 'lab')
    def __init__(self, img, to='rgb'):
        self.img = img
        self.format = to
        self.cvtColor(to)
    def cvtColor(self, to='rgb'):
        if to not in self.valid_formats:
            print ("invalid color for converting to:", to)
            return
        if to=='rgb':
            self.cvt_img = self.img
        if to=='hsv':
            self.cvt_img = cv2.cvtColor(self.img, cv2.COLOR_RGB2HSV)
        if to=='hls':
            self.cvt_img = cv2.cvtColor(self.img, cv2.COLOR_RGB2HLS)
        if to=='gray':
            gray = cv2.cvtColor(self.img, cv2.COLOR_RGB2HLS)
            self.cvt_img = [gray, gray, gray]
        if to=='yrb':
            self.cvt_img = cv2.cvtColor(self.img, cv2.COLOR_RGB2YCrCb)
        if to=='lab':
            self.cvt_img = cv2.cvtColor(self.img, cv2.COLOR_RGB2LAB)

    def show(self):
        fig = plt.figure(figsize=(12,3))
        plt.subplot(141)
        plt.imshow(self.img)
        plt.title('RGB')

        plt.subplot(142)
        plt.imshow(self.cvt_img[:,:,0], cmap='gray')
        plt.title(self.format+':0')

        plt.subplot(143)
        plt.imshow(self.cvt_img[:,:,1], cmap='gray')
        plt.title(self.format+':1')

        plt.subplot(144)
        plt.imshow(self.cvt_img[:,:,2], cmap='gray')
        plt.title(self.format+':2')

        fig.tight_layout()
        return fig


    def plot3d(self, pixels, colors_rgb, axis_labels=list("RGB"), axis_limits=[(0, 255), (0, 255), (0, 255)]):
        """Plot pixels in 3D."""

        # Create figure and 3D axes
        fig = plt.figure(figsize=(8, 8))
        ax = Axes3D(fig)
    
        # Set axis limits
        ax.set_xlim(*axis_limits[0])
        ax.set_ylim(*axis_limits[1])
        ax.set_zlim(*axis_limits[2])
    
        # Set axis labels and sizes
        ax.tick_params(axis='both', which='major', labelsize=14, pad=8)
        ax.set_xlabel(axis_labels[0], fontsize=16, labelpad=16)
        ax.set_ylabel(axis_labels[1], fontsize=16, labelpad=16)
        ax.set_zlabel(axis_labels[2], fontsize=16, labelpad=16)
    
        # Plot pixel values with colors given in colors_rgb
        ax.scatter(
            pixels[:, :, 0].ravel(),
            pixels[:, :, 1].ravel(),
            pixels[:, :, 2].ravel(),
            c=colors_rgb.reshape((-1, 3)), edgecolors='none')
    
        return ax  # return Axes3D object for further manipulation
    
    def plot_color_3d(self): 
        # Select a small fraction of pixels to plot by subsampling it
        scale = max(self.img.shape[0], self.img.shape[1], 64) / 64  # at most 64 rows and columns
        img_small_RGB = cv2.resize(self.img, (np.int(self.img.shape[1] / scale), np.int(self.img.shape[0] / scale)), interpolation=cv2.INTER_NEAREST)
        img_small_rgb = img_small_RGB / 255.  # scaled to [0, 1], only for plotting
        img_small_cvt = cv2.resize(self.cvt_img, (np.int(self.img.shape[1] / scale), np.int(self.img.shape[0] / scale)), interpolation=cv2.INTER_NEAREST)
        
        # Plot and show
        self.plot3d(img_small_RGB, img_small_rgb)
        plt.show()
        
        self.plot3d(img_small_cvt, img_small_rgb, axis_labels=list(self.format))
        plt.show()


from sklearn.preprocessing import StandardScaler

from skimage.feature import hog
# Define a function to return HOG features and visualization
def get_hog_features(img, orient, pix_per_cell, cell_per_block, 
                        vis=False, feature_vec=True):
    # Call with two outputs if vis==True
    if vis == True:
        features, hog_image = hog(img, orientations=orient, 
                                  pixels_per_cell=(pix_per_cell, pix_per_cell),
                                  cells_per_block=(cell_per_block, cell_per_block), 
                                  transform_sqrt=True, 
                                  visualise=vis, feature_vector=feature_vec)
        return features, hog_image
    # Otherwise call with one output
    else:      
        features = hog(img, orientations=orient, 
                       pixels_per_cell=(pix_per_cell, pix_per_cell),
                       cells_per_block=(cell_per_block, cell_per_block), 
                       transform_sqrt=True, 
                       visualise=vis, feature_vector=feature_vec)
        return features

# Define a function to compute binned color features  
def bin_spatial(img, size=(32, 32)):
    # Use cv2.resize().ravel() to create the feature vector
    features = cv2.resize(img, size).ravel() 
    # Return the feature vector
    return features

def add_heat(heatmap, bbox_list, th=0):
    #heatmap = np.zeros_like(img)
    # Iterate through list of bboxes
    for box in bbox_list:
        # Add += 1 for all pixels inside each bbox
        # Assuming each "box" takes the form ((x1, y1), (x2, y2))
        heatmap[box[0][1]:box[1][1], box[0][0]:box[1][0]] += 1
    heatmap[heatmap<=th] = 0

    # Return updated heatmap
    return heatmap

from scipy.ndimage.measurements import label
def draw_labeled_bboxes(img, heatmap):
    # Iterate through all detected cars
    labels=label(heatmap)
    rects = []
    for car_number in range(1, labels[1]+1):
        # Find pixels with each car_number label value
        nonzero = (labels[0] == car_number).nonzero()
        # Identify x and y values of those pixels
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])
        # Define a bounding box based on min/max x and y
        bbox = ((np.min(nonzerox), np.min(nonzeroy)), (np.max(nonzerox), np.max(nonzeroy)))
        rects.append(bbox)
        # Draw the box on the image
        cv2.rectangle(img, bbox[0], bbox[1], (0,0,255), 6)
    # Return the image and final rectangles
    return img, rects

#fireworks
#roll in the deep
#strip that down (feat. Quavo)
#cool kids
#feel it still
#E.T
#Praying
#Stay
#love so soft
#cake by the ocean
#teenage dream
#too good at goodbyes
#rumor has it
#handclap
