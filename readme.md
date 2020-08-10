To run this project on you local follow below steps :

Make sure you have python3 and create a virtual env (Recommended, Not mandatory)

1) git pull <repo>
2) pip install -r requirements.txt
3) In "settings.py", please uncomment lines 82 to 87 and comment line 89  
4) In "static/products/app.js", please uncomment line 2 and comment line 1
5) Execute below commands :

       python manage.py migrate
       python manage.py collectstatic
       python manage.py runserver

6) Create a super user to add products and promotion rules : 
       
       python manage.py createsuperuser

    Give all required info (email will be optional)

7) Go to admin portal (http://127.0.0.1:8000/admin/) and login with the credentials you created above. There you can add products and promotion rules.

8) Go to http://127.0.0.1:8000/ to test promotion rules given on frontend.

9) To run test cases, use the below command :

       python manage.py test 

    You will see the test results.

10) Test cases for models, API and promotion logic are there in test file.
