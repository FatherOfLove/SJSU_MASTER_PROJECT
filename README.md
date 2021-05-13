# AI for Healthcare: A Deep Learning Platform for Clinical Time- Series Data
SJSU CMPE 295 Master Project

Team Members: 
- Jerry Huang
- Jacky Chow
- Jumana Nadir


![alt text](https://github.com/FatherOfLove/SJSU_MASTER_PROJECT/blob/master/S10_Poster.png)

## Learn about the product at: https://drive.google.com/file/d/1RKQxNFQ0adXA2M2gAJ8WDBY_HF2PGnoE/view


## Technologies used:

- Python for backend  
- Django framework for integration of frontend and backend  
- JavaScript frame work with CSS and HTML for front end  
- PostgreSQL for database
- Django ORM for database management 
![Alt text](image/Stacks.jpg?raw=true)

### ORM for Database
![Alt text](image/ORM.png?raw=true)

## Steps to run the code: 
### run locally
1. Install the postgreSQL in your computer
2. Clone the github and goto the folder  
        $git clone https://github.com/FatherOfLove/SJSU_MASTER_PROJECT.git  
        $cd ./Code/Django_V1/chronus-project/  
3. edit the settings.py in the "./Code/Django_V1/chronus-project/chronus/" folder
	To fit your database setting(database,user name, password and so on.
4. create a virtual environment with python3  
	$virtualenv -p /usr/local/bin/python3 Dependencies  
5. Activate the virtual environment  
	$source Dependencies/bin/activate  
6. Install dependencies numpy, scipy, requests,tensorflow, keras  
	$pip install -r ./heroku/requirements.txt  
7. Run "python manage.py makemigrations" 
8. Run "python manage.py migrate" ---migrate the database
9. Run "python manage.py runserver" -- this starts the http server using python Django 
10. Open the "http://127.0.0.1:8000/" on browser and use the site.  

### run in the cloud
- Please follow the README in heroku folder using your setting
  https://github.com/FatherOfLove/SJSU_MASTER_PROJECT/blob/master/heroku/README.md
- Or use any other cloud server you like

## Site available at:https://jjjinc.herokuapp.com/
![Alt text](image/index.jpg?raw=true) 


## Our AI Engine:
![alt text](https://github.com/FatherOfLove/SJSU_MASTER_PROJECT/blob/master/image/AI%20ENGINE%20.png)

### Dataset Distribution
![Alt text](image/dataset_distribution.png?raw=true)

#### Part of our data 
![Alt text](image/wav_plot.png?raw=true) 


### One of our model
![Alt text](image/model.png?raw=true) 

### Results 
![Alt text](image/results.jpg?raw=true)

