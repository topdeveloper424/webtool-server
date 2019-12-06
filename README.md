# Online Editor For Music List


[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](http://192.236.179.241:8000/)

This editor is a cloud-enabled, offline-storage powered HTML5 Markdown editor.

  - User Authentication
  - Automatic Crawling
  - Monitoring Logs and view
  - Editing lists
  - Integrations with API

# New Features!

  - Extracting data from source websites
  - Scheduling crawler job
  - Save, Delete records

### Dependencies

This web tool uses a number of open source projects to work properly:
* [Python 3.6.5] - python programming language!
* [Django 2.2.3] - python Back-end framework 
* [Javascript] - front-end programming language.
* [jQuery] - javascript

### Installation

This editor requires [python 3.6.5](https://www.python.org/downloads/release/python-365/) + to run.

Install the dependencies and devDependencies and start the server.

-- running development mode on window OS 
```sh
$ cd webtool
$ venv\Scripts\activate
$ pip install -r requirements.txt
$ python manage.py runserver
```
-- running development mode on linux 
```sh
$ cd webtool
$ source mypython/bin/activate
$ pip install -r requirements.txt
$ python manage.py runserver
```

For production environments...
https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html


Verify the deployment by navigating to your server address in your preferred browser.

```sh
127.0.0.1:8000
```

### Instructions

-- running crawler

![image](https://user-images.githubusercontent.com/40516126/67326838-0def8580-f4e5-11e9-9e30-61837ba1aa4c.png)

-- Summary job and logs

![image](https://user-images.githubusercontent.com/40516126/67327068-5a3ac580-f4e5-11e9-99cd-b5fb0d01f7c0.png)

-- view logs detail

![image](https://user-images.githubusercontent.com/40516126/67327176-82c2bf80-f4e5-11e9-9c60-8343c6a7324a.png)
![image](https://user-images.githubusercontent.com/40516126/67327226-98d08000-f4e5-11e9-92f5-a94c9f4c6435.png)

-- Editing
there are  5 status.  pending, approved, import sent, deleted, canceled.
![image](https://user-images.githubusercontent.com/40516126/67327528-13999b00-f4e6-11e9-86e9-244a8027f793.png)

-- modifying script (not recommend)
![image](https://user-images.githubusercontent.com/40516126/67327686-4e033800-f4e6-11e9-97be-8993cd148504.png)


