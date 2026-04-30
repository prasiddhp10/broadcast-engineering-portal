# broadcast-engineering-portal
5COSC021W Software Development Group Project – Broadcast Engineering Teams Portal | Django | SQLite | Bootstrap 5 | Team BP | 

# Prerequisites
- Python
- GIT

# Setup Instructions
- Step 1: Clone the github repository: 
    https://github.com/prasiddhp10/broadcast-engineering-portal.git
- Step 2: Go into the project folder
    cd broadcast-engineering-portal/broadcast_portal
- Step 3: Create a virtual environment and activate environment
    Mac/Linux: 
        python3 -m venv venv
        source venv/bin/activate
    Windows: 
        python -m venv venv
        venv\Scripts\activate
    After the virtual environment is activated, it will show venv before each line of terminal. 
- Step 5: Install dependencies
    pip install -r requirements.txt
- Step 6: Apply database migrations
    python manage.py migrate
- Step 7: Create a superuser (Admin Account)
    python manage.py createsuperuser
- Step 8: Run the  server
    python manage.py runserver
- Step 9: Open the link through browser
    Main Site: http://127.0.0.1:8000
    Admin Panel: http://127.0.0.1:8000/admin
    Dashboard: http://127.0.0.1:8000/dashboard
    Teams: http://127.0.0.1:8000/teams
    Organization: http://127.0.0.1:8000/organization
    Messages: http://127.0.0.1:8000/messages
    Schedule: http://127.0.0.1:8000/schedule
    
