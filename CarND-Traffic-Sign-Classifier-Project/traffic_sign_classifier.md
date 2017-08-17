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

I've tried 3 model architectures, including LeNet, MSNet, and Incept model.

I first tried LeNet. I didn't keep the latest result in my notebook, likely close to 90% accuracy on validation data in 20 epochs. I believe with more epochs, or adding 1 or 2 layers I can push the validation accuracy more than 93%.

Then I tried the MSNet which is mentioned the the paper given in the project. The validation accuracy was slightly better than LeNet with similar number of epochs. 

I know about the popular Google Inception model so I wanted to try this architecture also, that I focused in this project.

I encapsulated some basic functions like building a conv2d layer, fully connection layer, train, test etc into a SignClassifer class, then all other models derive it. This makes it relatively more convenient to switch among different model architectures. But I didn't split the tenssor session. 

The Inception model 

[Inception Model](https://arxiv.org/pdf/1409.4842.pdf	"inception Model")

The classifier model I was using is built by stacking 2 level of inception models with dimension reduction. 

###Model Architecture

My final model consisted of the following layers:

|         Layer          |               Description                |
| :--------------------: | :--------------------------------------: |
|         Input          |         32x32x1 Gray scale image         |
|    Convolution 1x1     | 1x1 stride, same padding, outputs 32x32x16 |
|          RELU          |                                          |
|    Convolution 3x3     | 3x3 stride, same padding, outputs 32x32x32 |
|          RELU          |                                          |
|     InceptionModel     |            outputs 32x32x128             |
|      Max pooling       |      2x2 stride,  outputs 16x16x128      |
|    InceptionModel3     |             output 16x16x256             |
|      Max pooling       |  2x2 kernel, 3x3 stride, output 8x8x256  |
|    Convolution 1x1     | 1x1 stride, same padding, output 8x8x512. |
|          RELU          |                                          |
|        dropout         |        keep probability used 0.5.        |
|        flatten         |              output: 32768               |
| Fully connection +RELU |        input: 32768, output: 2048        |
| Fully connection +RELU |         input: 2048, output: 512         |
|        Dropout         |       keep probablitity used 0.5.        |
|    Fully Connection    |           input 512, output 43           |
|        Softmax         |                                          |
|                        |                                          |
|                        |                                          |



 ### Model Training

* Optimizer: AdamOptimizer. 
* Learning Rate: 0.0008
* Batch Size: 128
* epochs: 15 in total
* shuffle the training data each time when start a new epoch. 

### Model Tuning

First, I trained the model without any data augmentation. With 10 epochs, the validation accuracy got ~91% while the training accuracy getting very high, close to 100%, which may indicate the model start overfitting or not enough training data. So I did some random scaling, translating on the training images to get some artificial training images. These augmentation is to emulate the images that may be got when taking a video on the road. After this, the validation accuracy increased to ~97% with 10 epochs. I was still concerned about the overfitting issue so I added 2 more dropout layers. Then I re-train the model with 15 epochs, reached 98.5% on validation data and 100% on training data. Still looks like having overfitting issue. I may need to generate more images or applying more transformations.

Final results:

* training set accuracy of 100%
* validation set accuracy of 98.5%
* test set accuracy of 95.2%

#### Describe the approach taken for finding a solution and getting the validation set accuracy to be at least 0.93. Include in the discussion the results on the training, validation and test sets and where in the code these were calculated. Your approach may have been an iterative process, in which case, outline the steps you took to get to the final solution and why you chose those steps. Perhaps your solution involved an already well known implementation or architecture. In this case, discuss why you think the architecture is suitable for the current problem.



##Test a Model on New Images

### Choose five German traffic signs found on the web and provide them in the report. For each image, discuss what quality or qualities might be difficult to classify.

Here are five German traffic signs that I found on the web:

![image](/home/lizhang/workspace/Udacity/CarND/CarND-Traffic-Sign-Classifier-Project/examples/web_images.png)



The 9th image might be difficult: having partial of another sign at behind.

The 10th might be difficult too : having some slash lines crossing the number.

The Top5 results:

![image](/home/lizhang/workspace/Udacity/CarND/CarND-Traffic-Sign-Classifier-Project/examples/top5.png)

###Performance Analysys
The accuracy only reached 81.8% on these new images. So, compared to  accuracy of 95.2% on test set, I think this model is overfitting. The very high accuracy on training data (100%) also indicates this. I think I may need more training data, or use more random transformations on the training data.



