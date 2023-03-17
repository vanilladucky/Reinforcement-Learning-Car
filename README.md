# Self driving car using NeuroEvolution of Augmenting Topologies

# Table of Content
* Project
* Algorithm used 
* Files 
* How to run - Mac OS
* How to run - Window OS
* Areas under progress

# Project 
#### This is a project that is centered around the idea of [Reinforcement Learning](https://en.wikipedia.org/wiki/Reinforcement_learning) (RL). It is a machine learning approach where there is no need for a huge dataset and specific instructions, but just neural networks that will learn the optimal solution through achieving rewards. 

#### This idea has been one of the three most fundemental approaches of machine learning, beside supervised and unsupervised learning. It is a intuitive idea as we all can believe how the machine would likely learn the optimal solution, by trying to maximize its reward, like how a puppy learns to sit in order to reeive that treat or in this case, like how a car learns how to drive around a track to maximize its reward. 

#### This project uses an approach similar to that of RL which is another field called [Genetic Algorithms](https://medium.com/xrpractices/reinforcement-learning-vs-genetic-algorithm-ai-for-simulations-f1f484969c56) (GA). GAs are heavily influenced by Charles Darwin's theory of natural evolution and if one has a simple knowledge of the theory, it won't be hard to see how GAs function. 

# Algorithm used
#### The specific GA used in this project is called NeuroEvolution of Augmenting Topologies or NEAT. It was proposed in 2002 by Kenneth O. Stanley and Risto Miikkulainen. I admit it is not the state of the art but as of then, as you can see from the [paper](https://nn.cs.utexas.edu/downloads/papers/stanley.cec02.pdf), its performance is unparalled to other similar models. It introduces some new and interesting concepts such as Historical Markings, which reduces the computation needed to analysis every single genomes and makes traversing through topologies unnecessary. It also mentions Speciation, the introduction of species, and this greatly improves the performance of the algorithm as it allows genomes of its own species to compete with their own, leading to less 'accidental' removal of those genomes with great potential. 

#### The idea is truly fascinating and this paper is only 6 pages long so if you do have an hour to spare, please give it a go and try reading the paper. It is explained in a way that makes this frightening sounding algorithm feel like a run of the mill algorithm.

# Files
#### "codes" folder contains all the codes. The main, functional code is in main.py while the other file contains the saving of the algorithm. However, this file is still under progress as I have yet to figure out a way to load the saved model. I will update the file as soon as I figure out a way how to.
#### "images" folder contains all the images of the car and the different maps. You can insert in the maps in the main.py file to train the car on different maps. 
#### "config.txt" file is where the parameters are stored for our NEAT algorithm. Please read the NEAT [documentation](https://neat-python.readthedocs.io/en/latest/) where they elaborate very clearly about the parameters. Apart from this documentation, the paper itself showcases different parameters in the algorithm. Please do take a look and hopefully altering them yourself could produce a better result. 

# How to run - Mac OS
#### Clone this repository into your local computer. 
#### Make sure to have python3 installed. You can download python from its [official website](https://www.python.org/downloads/)
#### Once you have cloned it, go into the cloned directory and in your terminal, type in `python3 codes/main.py`

# How to run - Windows OS
#### Clone this repository into your local computer. 
#### Make sure to have python3 installed. You can download python from its [official website](https://www.python.org/downloads/)
#### Once you have cloned it, go into the cloned directory and in your terminal, type in `python codes/main.py`

# Areas under progress
#### As I have mentioned, I still have yet to find a way to load the saved file so that I can resume training or testing with the trained mdoel. 
#### This brings me to another portion that needs improvement which is to test the trained algorithm on a different map. This is due to the fact that the model can be overfitting to the specific map which in some case I can obviously tell with the naked eye. As any data scientist/machine learning personel would say, training but not to the extent of overfitting is extremely crucial. 
#### Once I find a solution to these problems, I would update the respective files accordingly. 
