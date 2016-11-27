# cmput404-project
Project Repo for a Ualberta Cmput 404 project

Team RAPIDD:
  - [Rishi Barnwal](https://github.com/ironcupcakes)
  - [Aedan Burnett](https://github.com/SuperSheep18)
  - [Preyanshu Kumar](https://github.com/preyansh)
  - [Dayna Lacoursiere](https://github.com/DaynaLacoursiere)
  - [Daniel Sopel](https://github.com/dsopel)


Acknowledgements:

  - CSS reset from http://meyerweb.com/eric/tools/css/reset/
  - Tutorial for Django: https://tutorial.djangogirls.org/
  - Beautiful CSS: https://gist.github.com/luqmaan/044a28f52933649786b3
  
How to run:

    outside /squirespace run
        > virtualenv venv
        > source venv/bin/activate
        > pip install --upgrade pip
        > pip install Pillow
        > pip install Django==1.10
        > pip install django-friendship
        > pip install djangorestframework
        > pip install requests
        > pip install 'requests[security]'
        > pip install commonMark
    inside /squirespace run
        > python manage.py runserver
        
    then open 127.0.0.1:8000 in your browser

to run test suite:
	python manage.py test

To view our API documentation, visit our [wiki](https://github.com/DaynaLacoursiere/cmput404-project/wiki).

Team Collaboration:  
	Rishi:  
	- Friends backend  
	- Followers/Followed by backend  
	- Remote friendships  
	- Friends Tests  
	Aedan:  
	- Setup initial site skeleton  
	- Post creating/editing/deleting backend  
	- Images (server hosting, and site displaying)  
	- Setup AWS to serve site  
	- Posts/Images tests  
	- Server tests  
	Preyanshu:  
	- Authentication  
	- Registration
	- Markdown 
	- Authentication tests  
	Dayna:  
	- Registration  
	- CSS and HTML layout for all pages  
	- Browsing based on status  
	- Private/Public posting   
	- Registration tests  
	- Sorting/Filtering tests  
	Daniel:  
	- API
	- Post comments creating/editing/deleting backend  
	- Post/Comment/API tests

	  
