## Inspiration
Wildfires are a serious problem in Canada. In 2023, 6132 wildfires consumed 16.5 million hectares of trees, which is double the the 1989 record. Wildfires can have serious effects on the surrounding environment and ecosystem, prompting us to build a robot that can detect fires before they get out of control.

## What it does
Our fire-detecting robot Pyrover is an autonomous robot that periodically monitors forests to search for fires. Pyrover has a camera that sends images to a neural network that searches for fires. Upon detecting a fire, Pyrover alerts the main server with the location and time of the fire, giving the local fire department ample time to prevent the fire from spiraling out of control.

## How we built it
We used Roboflow to train the fire-detecting neural network on a dataset of almost 5000 images. 
We used a [Kaggle Wildfire detection dataset](https://www.kaggle.com/datasets/brsdincer/wildfire-detection-image-data/) to source our images, and then we augmented the dataset by changing the brightness for the images to simulate various lighting conditions. 

The model is accessed by the rover through the Roboflow Python API. You can view the classifier on our [project page](https://universe.roboflow.com/firebot/firebot). 

OpenCV is used to receive video from the rover's camera, on which we perform our fire detection inference. 

The rover is built using an Arduino and Raspberry Pi. The Raspberry Pi is the client, which sends camera data and predictions to an AWS EC2 cloud instance, where the server is located.

The Raspi communicates with the Arduino with the serial communication with 9600 baud. After the client detects fire, the Raspi will send signal to the Arduino and it will turn around 180 degree and continue the autonomous driving to detects other fires. 

The server has RESTful API endpoints so we can transmit the data from our client. We also used HTML, CSS, Javascript to build a web dashboard to display the live-feed from the camera and a map pointing to all alert locations. 

Upon clicking an alert location on the map we redirect to another page showing details such as the fire image, prediction confidence level, detection time, and the latitude and longitude so that the responders can put out the fire in a timely manner.

## Challenges we ran into
Material shortage meant that we had to purchase some of the materials. There was also a lack of power in the rover, which made it difficult to function properly. Coding bugs created problems in the proper functioning.

## Accomplishments that we're proud of
The rover functions perfectly, which is our biggest accomplishment. For some of us, it was our first successful hardware project, which is something that we are proud of.

## What we learned
We learned to build a fully functioning robot using a variety of different technologies, including machine learning, computer vision, hardware programming and web development. We also learned to think outside the box and collaborate synchronously and asynchronously on the project.

## What's next for Pyrover
There are many things to improve in Pyrover. For one, better materials and hardware are needed to increase reliability, efficiency and practicality. Software improvements are also necessary to ensure that the platform is robust. Therefore our two main goals for the near future are:

**Transforming Pyrover into a Fire-Resistant Drone**

Enhance the rover's capabilities by transforming it into a fire-resistant drone, providing increased flexibility and aerial surveillance for more effective fire detection and monitoring.

**Create an interconnected fleet of Pyrovers** 

Create a network of Pyrovers capable of navigating our forests efficiently and update their paths if some Pyrover(s) are damaged/trapped.

[Presentation](https://www.canva.com/design/DAF6hKpbGVw/DEAj4yuI4_5vQIQMaKEfow/view?utm_content=DAF6hKpbGVw&utm_campaign=share_your_design&utm_medium=link&utm_source=shareyourdesignpanel)