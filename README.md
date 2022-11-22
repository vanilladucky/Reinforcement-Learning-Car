# Self learning car using NeuroEvolution of Augmenting Topologies

# Table of Content
* Project
* Algorithm used 
* Files 

# Project 
### This is a project that is centered around the idea of [Reinforcement Learning](https://en.wikipedia.org/wiki/Reinforcement_learning) (RL). It is a machine learning approach where there is no need for a huge dataset and specific instructions, but just neural networks that will learn the optimal solution through achieving rewards. 
### This idea has been one of the three most fundemental approaches of machine learning, beside supervised and unsupervised learning. It is a intuitive idea as we all can believe how the machine would likely learn the optimal solution, by trying to maximize its reward, like how a puppy learns to sit in order to reeive that treat or in this case, like how a car learns how to drive around a track to maximize its reward. 
### This project uses an approach similar to that of RL which is another field called [Genetic Algorithms](https://medium.com/xrpractices/reinforcement-learning-vs-genetic-algorithm-ai-for-simulations-f1f484969c56) (GA). GAs are heavily influenced by Charles Darwin's theory of natural evolution and if one has a simple knowledge of the theory, it won't be hard to see how GAs function. 

# Algorithm used
### The specific GA used in this project is called NeuroEvolution of Augmenting Topologies or NEAT. It was proposed in 2002 by Kenneth O. Stanley and Risto Miikkulainen. I admit it is not the state of the art but as of then, as you can see from the [paper](https://nn.cs.utexas.edu/downloads/papers/stanley.cec02.pdf), its performance is unparalled to other similar models. It introduces some new and interesting concepts such as Historical Markings, which reduces the computation needed to analysis every single genomes and makes traversing through topologies unnecessary. It also mentions Speciation, the introduction of species, and this greatly improves the performance of the algorithm as it allows genomes of its own species to compete with their own, leading to less 'accidental' removal of those genomes with great potential. 
### The idea is truly fascinating and this paper is only 6 pages long so if you do have an hour to spare, please give it a go and try reading the paper. It is explained in a way that makes this frightening sounding algorithm feel like a run of the mill algorithm.

# Files
