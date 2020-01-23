# MS Azure Ignite Tour in Seoul Review

1. ML DevOps in Azure

2. ML inside powerBI

![](https://github.com/rnlduaeo/alibaba/blob/master/1.JPG?raw=true)

![](https://github.com/rnlduaeo/alibaba/blob/master/2.JPG?raw=true)

![](https://github.com/rnlduaeo/alibaba/blob/master/3.JPG?raw=true)






There are several terms when we talk about ML such as datasets registered for ML process, experiments for already trained sets, pipelines for training workflows.
![](https://github.com/rnlduaeo/alibaba/blob/master/7.JPG?raw=true)

In ML DevOps session, pipelines and pipeline endpoints(for result set) were mainly presented out of several resources in machine learning development lifecycle.
![](https://github.com/rnlduaeo/alibaba/blob/master/6.JPG?raw=true)

In general ML development cycles, we followed below process.

- data preprocessing (cleansing, normalization etc.)
- training data
- model registration
- deploy to the compute resources (ACI, AKS)

With new data coming in, we follow same process with new data (we call it test dataset). Once outcome came out, model validation(with model accuracy) will be conducted and retrain the model while keeping changing the parameter set(variable) with different values until the model reach certain level of accuracy. 

![](https://github.com/rnlduaeo/alibaba/blob/master/4.JPG?raw=true)

In azure ML pipeline, we can define this ML development process with flow diagram and build a CI/CD pipeline (traditional CI/CD process likewise). In other word, the whole cycle where selecting different kinds of dataset, training code, model registration, testing the model in staging system, and final deployment to production system becomes automate which reduces huge amount of repeated tasks. 

In console, the user can see the trends of historical changes of model accuracy, rollback etc.  
![](https://github.com/rnlduaeo/alibaba/blob/master/5.JPG?raw=true)


![](https://github.com/rnlduaeo/alibaba/blob/master/8.JPG?raw=true)

![](https://github.com/rnlduaeo/alibaba/blob/master/9.JPG?raw=true)

![](https://github.com/rnlduaeo/alibaba/blob/master/10.JPG?raw=true)

![](https://github.com/rnlduaeo/alibaba/blob/master/11.JPG?raw=true)

![](https://github.com/rnlduaeo/alibaba/blob/master/12.JPG?raw=true)

![](https://github.com/rnlduaeo/alibaba/blob/master/13.JPG?raw=true)

![](https://github.com/rnlduaeo/alibaba/blob/master/14.JPG?raw=true)

![](https://github.com/rnlduaeo/alibaba/blob/master/15.JPG?raw=true)

![](https://github.com/rnlduaeo/alibaba/blob/master/16.JPG?raw=true)


<!--stackedit_data:
eyJoaXN0b3J5IjpbLTkzNTI3NjE1OCwtOTM2MzY3NzkxXX0=
-->