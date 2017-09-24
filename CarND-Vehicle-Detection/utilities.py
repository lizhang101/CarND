import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# evenly sampled time at 200ms intervals


def draw_boxes(img, bboxes, color=(0, 0, 255), thick=6):
    # Make a copy of the image
    draw_img = np.copy(img)
    # Iterate through the bounding boxes
    for bbox in bboxes:
        # Draw a rectangle given bbox coordinates
        cv2.rectangle(draw_img, bbox[0], bbox[1], color, thick)
    # Return the image copy with boxes drawn
    return draw_img

class ColorHist:
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
    def cvtColor(self, to):
        if to not in valid_formats:
            print ("invalid color for converting to:", to)
        return
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


#fireworks
#roll in the deep
#strip that down (feat. Quavo)
#cool kids
#feel it still
#E.T
