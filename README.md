## Enterprise Performance Management System(EPMS) - [official demo app link](http://www.epms.cloud/)

Installation / Setup on local machine
# Windows and Unix Like:

- Download Python from the [official Python site](https://www.python.org/downloads/release/python-361/)
- Install Python and add it to environmental variables
- On your develop directory, create a virtual environment. Can follow the this documentation / guidelines:
https://virtualenv.pypa.io/en/stable/userguide/

- Activate the environment, guidelines provided in the link above. Here is an example you would type on the command line:
```
path\to\env\Scripts\activate
```
- It's entirely up to the developer where they wish to place the virtual environment. It's recommend you create a
directory and label something like 'venvs' and create the environments there for each project. Along side the
'venv' directory, will be the project directories.
- Along side the virtual environments directory e.g' 'venvs' clone the project.
- At this step, you should have the virtual environment and it should be activated. Next to the root of the virtual
environments you will have the project you recently cloned.
```
cd enterprise_performance_management
```

# Quick way to run the application
- Run python3 -m venv env
- Run source env/bin/activate
- Run pip3 install -r requirements/base.txt
- cd to enterprise_performance_management
- Run python3 manage.py migrate
- Run python3 manage.py createsuper(follow instruction)
- Run python3 manage.py runserver or python3 manage.py runserver:port
- It will run and give you url for the app

## Application Overview

- (EPMS) is a field of business performance management which considers the visibility of operations in a closed-loop model across all facets of the enterprise. Specific to financial activities in the office of the chief financial officer, EPMS also supports financial planning and analysis (FP&A). "Corporate performance management (CPM)" is a synonym for "enterprise performance management". It increased focus on planning, and the emergence of a new category of solutions supporting the management of the financial close.

There are several modules. 
These include:

- Strategy & Planning
- Annual Perfomance Plan
- Budget
- Programme and Project Management
- Employee Perfomance Plan
- Analytics
- Reporting 

# Strategy Module
![alt text](https://github.com/kaizer88/epms/blob/master/docs/epms/AwesomeScreenshot-Employee-Performance-Management-Suite-2019-07-17-10-07-89.png)

# Annual Perfomance Plan Module
![alt text](https://github.com/kaizer88/epms/blob/master/docs/epms/AwesomeScreenshot-Employee-Performance-Management-Suite-2019-07-17-10-07-95.png)

# Budget Module
![alt text](https://github.com/kaizer88/epms/blob/master/docs/epms/AwesomeScreenshot-Employee-Performance-Management-Suite-2019-07-17-10-07-33.png)

# Programme and Project Management Module
![alt text](https://github.com/kaizer88/epms/blob/master/docs/epms/AwesomeScreenshot-Employee-Performance-Management-Suite-2019-07-17-10-07-47.png)

# Employee Perfomance Plan Module
![alt text](https://github.com/kaizer88/epms/blob/master/docs/epms/AwesomeScreenshot-Employee-Performance-Management-Suite-2019-07-17-10-07-65.png)

# Analytics Module
![alt text](https://github.com/kaizer88/epms/blob/master/docs/epms/AwesomeScreenshot-Employee-Performance-Management-Suite-2019-07-17-10-07-83.png)


