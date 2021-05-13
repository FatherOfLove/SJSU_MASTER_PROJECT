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

## Steps to run the code:  
1. Install the postgreSQL in your computer
2. Clone the github and goto the folder  
        $git clone https://github.com/FatherOfLove/SJSU_MASTER_PROJECT.git  
        $cd ./Code/Django_V1/chronus-project/  
2. create a virtual environment with python3  
	$virtualenv -p /usr/local/bin/python3 Dependencies  
3. Activate the virtual environment  
	$source Dependencies/bin/activate  
4. Install dependencies numpy, scipy, requests,tensorflow, keras  
	$pip install -r ./heroku/requirements.txt  
5. Run "python manage.py makemigrations" 
6. Run "python manage.py migrate" ---migrate the database
7. Run "python manage.py runserver" -- this starts the http server using python Django 
8. Open the port on browser and use the site.  

## Site available at:https://jjjinc.herokuapp.com/

![image] (https://github.com/FatherOfLove/SJSU_MASTER_PROJECT/blob/master/image/AI%20ENGINE%20.png)
