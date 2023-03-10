

# UOCIS322 - Project 6 #

Joshua Muzi
CS 322
jmuzi04@gmail.com

## Project 4 Overview

Implementation of RUSA ACP controle time calculator with Flask and AJAX.
Brevet time calculator with MongoDB!

You'll add a storage to your previous project using MongoDB and docker-compose which 
makes it easier to create, manage and connect multiple container to create a single service comprised of different sub-services.

### ACP controle times

This project consists of a web application that is based on RUSA's online calculator. The algorithm for calculating controle times is described here [https://rusa.org/pages/acp-brevet-control-times-calculator](https://rusa.org/pages/acp-brevet-control-times-calculator). Additional background information is given here [https://rusa.org/pages/rulesForRiders](https://rusa.org/pages/rulesForRiders). The description is ambiguous, but the examples help. Part of finishing this project is clarifying anything that is not clear about the requirements, and documenting it clearly. 

We are essentially replacing the calculator here [https://rusa.org/octime_acp.html](https://rusa.org/octime_acp.html). Which can be used to check any answers or data.

# Understand the application

The files calc.html found in the templates folder and flask_brevets.py work together using Flask and Ajax to send data being activiely typed in the calculator. 
Flask_brevets.py then access and gathers the data needed using request.args.get in "/_calc_times". 
The calc times function will then call two acp_times.py functions those being open_time and close_time which will calculate the times per control point given the RUSA control times calc https://rusa.org/pages/acp-brevet-control-times-calculator

# How to run the application

To get started you will need to be in your computer or laptop terminal and bring yourself to the project-4 brevets directory.
This can be done using 
cd project-4
cd brevets

To start running the application you will have to build it first using Docker and the following command. This will run Dockerfile which will install locally all required resources to run your application.
This can be done by repeating the following in your brevets directory terminal:

jmuzi@DESKTOP-GDPKR20:~$ docker build -t myimage .

Then to start the webpage and calculator you will need to run the following command after.

jmuzi@DESKTOP-GDPKR20:~$ docker run -p 5001:5000 myimage


Now that the webpage is working you are given some options to choose from to customize your race.

You will be able to determine the total distance of the race in segements of 200, 300, 400, 600, 1000

You then get the oppertunity to decide the date and time for the race.

Once this is finished you can begin to fill in check points that are equal to or below your total distance, going from smallest to biggest distance, starting at 0.

#brevet calculation 


Control location (km)	Minimum Speed (km/hr)	Maximum Speed (km/hr)
0 - 200					15						34
200 - 400				15						32
400 - 600				15						30
600 - 1000				11.428					28

Calculation of open_time can be done by diving the control point location by the
maxium speed limit the control point is within. When a control point enters a 
a new table value, the control point minus the previous brevet_gap.

Calculation of close_time can be down by dividing the control points by the minimum speed limit.
This holds the same logic regarding control point but will change minimum speed limit 
when control point is greater than 600.


The ACP Brevet Control Times Calculator also has a few rules which can make things tricky,

By the rules, the overall time limit for a 200km brevet is 13H30, even though by calculation, 200/15 = 13H20

We also have another rules which became allowed use outside of France in 2018
which solves the standard problem of when a control point is too close to start 
The algorithm is as follows, when the control point is less than 60, the minimum
speed limit will be 20 in order to prevent problems

Once you have done the following calculation in order to convert the time 
to hours, minutes you can multiply the result by 60 then proceed to
set hours and minutes equal to divmod(result, 60)




#Project 5 Modifications

In project 5 we added a few additonal files being mymongo.py and test_mymongo.

These files were created to further build upon our docker application using 
docker compass and mongodb. Similar to project 4 we use calc.html to handle ajax
and json interaction using two new buttons added to the html named Submit and Display. 
Submit must store the information (brevet distance, start time, checkpoints and their opening and closing times) in the database (overwriting existing ones). 
Display will fetch the information from the database and fill in the form with them.

These buttons will then call flask_brevets.py to gather, store, and then fetch the information provided by the webpage.

Submit will store and clear the data on the webpage in mydb.lists

Mydb and many of the enviroment requirements required to run mongo/mymongo
can be found within docker-compose which acts as more advanced docker using 
the original docker as a base.


Commands:

This command will build docker-compose & Dockerfile which will
install all necessary requirments, enviroments, and files and then 
run the webpage application using the mongo and docker ports given

docker compose up


This command will close and stop the containers started

docker compose down


This command is similar and allows you to build and docker compose detached
from the terminal.

docker compose up --build -d

This command will build and run docker compose and imeditaely bring you
to mongodb shell where you can further interact with your db data


#Project 6 Modifications

Brevet time calculator with MongoDB, and a RESTful API!

Read about MongoEngine and Flask-RESTful before you start: [http://docs.mongoengine.org/](http://docs.mongoengine.org/), [https://flask-restful.readthedocs.io/en/latest/](https://flask-restful.readthedocs.io/en/latest/).



## Overview

You will reuse your code from Project 5, which already has two services:

* Brevets
	* The entire web service
* MongoDB

For this project, you re-organize `Brevets` into two separate services:

* Web (Front-end)
	* Time calculator (basically everything you had in project 4)
* API (Back-end)
	* A RESTful service to expose/store structured data in MongoDB.
	
	
	Within project 6 we inserted our brevets file from the previous project but went a step further this time.
	We went ahead and deleted config, default, mymongo in order to implement our own configurations using
	API.
	
	Until you insert your first race data the code has not changed much as the Javascript will still be calling 
	_calc_times in flask_brevets as normal and calculating in acp_times.py.
	
	Once the insert button has been clicked the javascript will once again call flask_brevets.py
	but this time calling insert_brevets which will now call a new file created called myapi.py which will handle 
	all flask_brevets requests excluding _calc_times.
	
	The myapi file brevets_insert() function will handle the data then call /api/brevets to then insert the race data
	both brevets.py and brevet.py which are api/resources will call the models.py function which will be used to 
	store, insert, delete, or update the race data given.
	
	

## Primary Tasks Completed 

* Implement a RESTful API in `api/`:
	* Write a data schema using MongoEngine for Checkpoints and Brevets:
		* `Checkpoint`:
			* `distance`: float, required, (checkpoint distance in kilometers), 
			* `location`: string, optional, (checkpoint location name), 
			* `open_time`: datetime, required, (checkpoint opening time), 
			* `close_time`: datetime, required, (checkpoint closing time).
		* `Brevet`:
			* `length`: float, required, (brevet distance in kilometers),
			* `start_time`: datetime, required, (brevet start time),
			* `checkpoints`: list of `Checkpoint`s, required, (checkpoints).
	* Using the schema, build a RESTful API with the resource `/brevets/`:
		* GET `http://API:PORT/api/brevets` should display all brevets stored in the database.
		* GET `http://API:PORT/api/brevet/ID` should display brevet with id `ID`.
		* POST `http://API:PORT/api/brevets` should insert brevet object in request into the database.
		* DELETE `http://API:PORT/api/brevet/ID` should delete brevet with id `ID`.
		* PUT `http://API:PORT/api/brevet/ID` should update brevet with id `ID` with object in request.

	* Remove `config.py` and adjust `flask_brevets.py` to use the `PORT` and `DEBUG` values specified in env variables (see `docker-compose.yml`).




## Authors

Michal Young, Ram Durairajan. Updated by Ali Hassani. Modified by Josh Muzi.
