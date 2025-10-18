**Installation Guide - Smart School Bus System**



**Prerequisites**

\- Python 3.8 or higher

\- pip (Python package manager)

\- Git (optional)



**Step-by-Step Installation**



**1. Clone the Repository**

```bash

git clone https://github.com/yourusername/smart-school-bus-system.git

cd smart-school-bus-system



**2. Create Virtual Environment**

bash

\# Windows

python -m venv bus\_env

bus\_env\\Scripts\\activate #activating virtual enviroment



\# Mac/Linux

python3 -m venv bus\_env

source bus\_env/bin/activate #activating virtual enviroment



**3. Install Dependencies**

//bash

pip install django



**4. Database Setup**

//bash

\# Create database tables

python manage.py makemigrations

python manage.py migrate



\# Create superuser (follow prompts)

python manage.py createsuperuser



**5. Run Development Server**

bash

python manage.py runserver



**6. Access the Application**

* Main Application: http://localhost:8000
* Admin Panel: http://localhost:8000/admin



**Configuration**

**Environment Variables**

Create .env file:



env

DEBUG=True

SECRET\_KEY=your-secret-key-here

ALLOWED\_HOSTS=localhost,127.0.0.1



**Database Configuration**

Default uses SQLite. For PostgreSQL:



**python**

DATABASES = {

&nbsp;   'default': {

&nbsp;       'ENGINE': 'django.db.backends.postgresql',

&nbsp;       'NAME': 'school\_bus',

&nbsp;       'USER': 'your\_username',

&nbsp;       'PASSWORD': 'your\_password',

&nbsp;       'HOST': 'localhost',

&nbsp;       'PORT': '5432',

&nbsp;   }

}



**Testing the Installation**

**Verify Installation**

bash

\# Check Django version

python -m django --version



\# Run tests

python manage.py test



\# Check for errors

python manage.py check



**Create Test Data**



python

python manage.py shell # Run sample data creation script



**Production Deployment**



**Using Gunicorn**

bash

pip install gunicorn

gunicorn school\_bus\_system.wsgi:application



**Using Docker**

dockerfile

FROM python:3.9

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

RUN python manage.py collectstatic --noinput

CMD \["gunicorn", "school\_bus\_system.wsgi:application", "--bind", "0.0.0.0:8000"]



**Troubleshooting**

**Common Issues**

* Port already in use: Use different port python manage.py runserver 8001
* Database errors: Delete db.sqlite3 and rerun migrations
* Static files not loading: Run python manage.py collectstatic



**Getting Help**

* Check Django documentation
* Review error logs in terminal
* Verify all migration steps completed
