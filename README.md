# twitter

RESTful API endpoint to provide data from Twitter by scraping in real-time. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

github link for get clone or download repository (public repository)

```
github link: https://github.com/jimy1824/twitter.git

```

### Installing

1. Install python, project require python 3.6/3.7 install python
2. Create virtual environment
    1. Install pip first
        ```
        sudo apt-get install python3-pip
        ```
    2. Then install virtualenv using pip3
        ```
       sudo pip3 install virtualenv
        ```
    3. create a virtual environment
        ```
         virtualenv venv
        ```
        for specific Python interpreter  choice
        ```
          virtualenv -p /usr/bin/python3.6 venv
        ```
    4. Activate virtual environment
        ``` 
        source venv/bin/activate
        ```
3. Install requirements
```
command pip install -r requirements.txt
```

## Run Server
Run the server
```
python manage.py runserver
```

## Running the tests

Run test cases 
```
python manage.py test
```

## Usage

API based project for api call use postman or any other source

Get the list of tweets of a user, e.g:
```
http://127.0.0.1:8000/users/ImranKhanPTI?limit=30
```
     
   Expected arguments
   1. User twitter name e.g ImranKhanPTI  
   2. Limit of tweets e.g limit=30 (its optional argument default is 30 and max_limit=50)
        
        APIs return json response
        
       ![Alt text](static/ge_list_of_tweets.png?raw=true "Title")



Get the list of tweets with the given hashtag, e.g:
```
http://127.0.0.1:8000/hashtags/hashtag?limit=30
```
Expected arguments
   1. hashtag e.g pakistan  
   2. Limit of tweets limit=30 (its optional argument default is 30 and max_limit=50)
   
        APIs return json response
   
         ![Alt text](static/get_list_of_hashtag_tweets.png?raw=true "Title")       

## Built With

* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - For Scraping
* [Selenium](https://www.seleniumhq.org/) - Web Automation
* [REST](https://www.django-rest-framework.org/) - Used to generate RESTFul APIs



## Authors

* **Jamshaid Iqbal** - *Initial work* - [jimy1824](https://github.com/jimy1824)

