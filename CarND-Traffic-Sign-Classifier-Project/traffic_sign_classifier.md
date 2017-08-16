#**Traffic Sign Recognition** 

---

**Build a Traffic Sign Recognition Project**
In this projects, I tried 3 architectures of neural networks which are Lenet, MSNet, and Inception like model. I also compared their performance in the preliminary stage and then choosed to use Inception model and focused on it.
The goals / steps of this project are the following:
* Load the data set (see below for links to the project data set)
* Explore, summarize and visualize the data set
* Design, train and test a model architecture
* Use the model to make predictions on new images
* Analyze the softmax probabilities of the new images
* Summarize the results with a written report



You're reading it! and here is a link to my [project code](./Traffic_Sign_Classifier_v2.ipynb)

##Data Set Summary & Exploration
Using numpy and Pandas, we can get some basic statistics of the German Traffic Sign dataset. 

It consists of 43 traffic sign types with each image has size of 32x32 pixels. And all classes are included in Validation Data and Test Data.

Number of training examples = 34799
Number of validation examples = 4410
Number of testing examples = 12630
Number of classes = 43

I created a Pandas Dataframe and Series of class names so they can be used to get the class name by a given index later in this project.

### Some samples from Dataset
First, some samples from the dataset:

![alt text](/home/lizhang/workspace/Udacity/CarND/CarND-Traffic-Sign-Classifier-Project/examples/speedlmt20.png "samples")

### Image Pre-processing pipeline

source image -> histogram equalization -> rbg2gray -> normalization

As we can see, some of the images are very dark. So I used histogram equalization to enhance all the data before feeding them into the network. I think the network should be able to learn how to handle these pictures even without this enhancement, but doing this in pre-processing may help reducing the training time or increasing the precision.

Then, I converted  these images to gray scale format according to some studies on web. Originally I thought we should keep the color since it may has important information. However, looks like the same class of sign may have different bias in color in different conditions. And gray scale images can mitigate these color bias and still remain enough information for classification.

Finally, I normalized the images into [-1.0, 1.0], to make the training more stable.

###  Augments The Training Data

By checking the example distribution in original training data, we can see some of classes has far less examples than others. And the average number of examples of all the classes is about 800. So I augmented the training data to make all classes have at least 800 examples.

![alt text](/home/lizhang/workspace/Udacity/CarND/CarND-Traffic-Sign-Classifier-Project/examples/distribution_pre.png "image")

The Augmentation I used includes: random brightening, scaling, translating, warping the source images. Here is a sample with these operations:

The final augmented image:

![image](/home/lizhang/workspace/Udacity/CarND/CarND-Traffic-Sign-Classifier-Project/examples/aug_sample.png "augmented")

After applying the augments to all the classes, the final example distribution in training data is as following:

![image](/home/lizhang/workspace/Udacity/CarND/CarND-Traffic-Sign-Classifier-Project/examples/distribution_post.png "distribution post")

## Design and Test a Model Architecture




####2. Describe what your final model architecture looks like including model type, layers, layer sizes, connectivity, etc.) Consider including a diagram and/or table describing the final model.

My final model consisted of the following layers:

|      Layer      |               Description                |
| :-------------: | :--------------------------------------: |
|      Input      |            32x32x3 RGB image             |
| Convolution 3x3 | 1x1 stride, same padding, outputs 32x32x64 |
|      RELU       |                                          |
|   Max pooling   |      2x2 stride,  outputs 16x16x64       |
| Convolution 3x3 |                   etc.                   |
| Fully connected |                   etc.                   |
|     Softmax     |                   etc.                   |
|                 |                                          |
|                 |                                          |



####3. Describe how you trained your model. The discussion can include the type of optimizer, the batch size, number of epochs and any hyperparameters such as learning rate.

To train the model, I used an ....

####4. Describe the approach taken for finding a solution and getting the validation set accuracy to be at least 0.93. Include in the discussion the results on the training, validation and test sets and where in the code these were calculated. Your approach may have been an iterative process, in which case, outline the steps you took to get to the final solution and why you chose those steps. Perhaps your solution involved an already well known implementation or architecture. In this case, discuss why you think the architecture is suitable for the current problem.

My final model results were:
* training set accuracy of ?
* validation set accuracy of ? 
* test set accuracy of ?

If an iterative approach was chosen:
* What was the first architecture that was tried and why was it chosen?
* What were some problems with the initial architecture?
* How was the architecture adjusted and why was it adjusted? Typical adjustments could include choosing a different model architecture, adding or taking away layers (pooling, dropout, convolution, etc), using an activation function or changing the activation function. One common justification for adjusting an architecture would be due to overfitting or underfitting. A high accuracy on the training set but low accuracy on the validation set indicates over fitting; a low accuracy on both sets indicates under fitting.
* Which parameters were tuned? How were they adjusted and why?
* What are some of the important design choices and why were they chosen? For example, why might a convolution layer work well with this problem? How might a dropout layer help with creating a successful model?

If a well known architecture was chosen:
* What architecture was chosen?
* Why did you believe it would be relevant to the traffic sign application?
* How does the final model's accuracy on the training, validation and test set provide evidence that the model is working well?


###Test a Model on New Images

####1. Choose five German traffic signs found on the web and provide them in the report. For each image, discuss what quality or qualities might be difficult to classify.

Here are five German traffic signs that I found on the web:

![alt text][image4] ![alt text][image5] ![alt text][image6] 
![alt text][image7] ![alt text][image8]

The first image might be difficult to classify because ...

####2. Discuss the model's predictions on these new traffic signs and compare the results to predicting on the test set. At a minimum, discuss what the predictions were, the accuracy on these new predictions, and compare the accuracy to the accuracy on the test set (OPTIONAL: Discuss the results in more detail as described in the "Stand Out Suggestions" part of the rubric).

Here are the results of the prediction:

|     Image     |  Prediction   |
| :-----------: | :-----------: |
|   Stop Sign   |   Stop sign   |
|    U-turn     |    U-turn     |
|     Yield     |     Yield     |
|   100 km/h    |  Bumpy Road   |
| Slippery Road | Slippery Road |


The model was able to correctly guess 4 of the 5 traffic signs, which gives an accuracy of 80%. This compares favorably to the accuracy on the test set of ...

####3. Describe how certain the model is when predicting on each of the five new images by looking at the softmax probabilities for each prediction. Provide the top 5 softmax probabilities for each image along with the sign type of each probability. (OPTIONAL: as described in the "Stand Out Suggestions" part of the rubric, visualizations can also be provided such as bar charts)

The code for making predictions on my final model is located in the 11th cell of the Ipython notebook.

For the first image, the model is relatively sure that this is a stop sign (probability of 0.6), and the image does contain a stop sign. The top five soft max probabilities were

| Probability |  Prediction   |
| :---------: | :-----------: |
|     .60     |   Stop sign   |
|     .20     |    U-turn     |
|     .05     |     Yield     |
|     .04     |  Bumpy Road   |
|     .01     | Slippery Road |


For the second image ... 

### (Optional) Visualizing the Neural Network (See Step 4 of the Ipython notebook for more details)
####1. Discuss the visual output of your trained network's feature maps. What characteristics did the neural network use to make classifications?


