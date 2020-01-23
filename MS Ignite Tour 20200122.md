# MS Azure Ignite Tour in Seoul Review

## ML DevOps in Azure
There are several terms when we talk about ML. Datasets registered for ML process, experiments for already trained sets, pipelines for training workflows etc. 
![](https://github.com/rnlduaeo/alibaba/blob/master/7.JPG?raw=true)

In ML DevOps session, pipelines and pipeline endpoints(for result set) were mainly delivered out of several terms in machine learning development lifecycle.
![](https://github.com/rnlduaeo/alibaba/blob/master/6.JPG?raw=true)

In general ML development cycles, the process may be as follows.

- data preprocessing (cleansing, normalization etc.)
- training data
- model registration
- deploy to the compute resources (ACI, AKS)

With new data coming in, we follow same process with new data (we call it test dataset). Once outcome came out, model validation(with model accuracy) will be conducted and retrain the model while keeping changing the parameter set(variable) with different values until the model reach certain level of accuracy. 

![](https://github.com/rnlduaeo/alibaba/blob/master/4.JPG?raw=true)

In azure ML pipeline, we can define this ML development process with flow diagram and build a CI/CD pipeline (traditional CI/CD process likewise). In other word, the whole cycle where selecting different kinds of dataset, training code, model registration, testing the model in staging system, and final deployment to production system becomes automate which allows us to reduce huge amount of repeated tasks. 

In console, the user can see the historically changed trend in model accuracy, do the rollback by simply clicking etc.  
![](https://github.com/rnlduaeo/alibaba/blob/master/5.JPG?raw=true)

Can be leveraged in different scenarios either model embedded in application or development with azure cognitive service API(e.g image, voice recognition prebuilt API) 
![](https://github.com/rnlduaeo/alibaba/blob/master/3.JPG?raw=true)

General comment on this session: 
Their user-friendly console UI was interesting. was easy to understand due to similarity with traditional CI/CD pipeline concept. 


![](https://github.com/rnlduaeo/alibaba/blob/master/8.JPG?raw=true)

## ML in PowerBI

General introduction of Azure ML services
![](https://github.com/rnlduaeo/alibaba/blob/master/2.JPG?raw=true)

![](https://github.com/rnlduaeo/alibaba/blob/master/1.JPG?raw=true)

Power BI can be easily integrated with ML ecosystem in Azure. 
![](https://github.com/rnlduaeo/alibaba/blob/master/9.JPG?raw=true)

The title was ML in Power BI, however the presenter mainly talked about general development methodology with Power BI using embedded analytics, Rest API, custom visuals.
![](https://github.com/rnlduaeo/alibaba/blob/master/10.JPG?raw=true)

When I proposed Oracle BI product which called as OAC(similar visualization tool with Power BI), I saw many customers wanted to use it as an single application by integrating it with existing IAMs and applications rather than using OAC standalone.

From my perspective,  Power BI has market value in that it has a variety of features that facilitate integration with existing applications.

![](https://github.com/rnlduaeo/alibaba/blob/master/11.JPG?raw=true)

Datasets in PowerBI can be not only shared by itself but also bound with dynamic values from application side. 
![](https://github.com/rnlduaeo/alibaba/blob/master/12.JPG?raw=true)

API has different kinds of operations with certain privilege. We can simply select them. 
![](https://github.com/rnlduaeo/alibaba/blob/master/13.JPG?raw=true)

![](https://github.com/rnlduaeo/alibaba/blob/master/14.JPG?raw=true)

The presenter showed us one of power BI dashboards embedded in his own application. emphasized simplicity too much.. 
![](https://github.com/rnlduaeo/alibaba/blob/master/15.JPG?raw=true)

Resources info. If you are interested in, plz refer to it. 
![](https://github.com/rnlduaeo/alibaba/blob/master/16.JPG?raw=true)


<!--stackedit_data:
eyJoaXN0b3J5IjpbMTIxNTgzMzczOSwxNTY4MzA3MjQ3LC00OT
k0MzI4MTAsMTU3OTQ4OTcyOCwtODUxMDExMjE5LC03NTIzMDY3
OTMsLTE1Mzc4MjY5MDUsLTM0MDIwNDU3NSwtOTM2MzY3NzkxXX
0=
-->