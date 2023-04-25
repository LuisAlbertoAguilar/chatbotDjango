## Prerequisites
Before installing a Django project from a repository, make sure you have the following:

- Python 3.x installed on your system.
- Pip package manager for Python installed on your system.
- Git installed on your system.

## Installation

1. Clone the repository: 
git clone https://github.com/LuisAlbertoAguilar/chatbotDjango

2. Navigate to the project directory:
cd <project-directory>

3. Create a virtual environment:
python3 -m venv <virtual-environment-name>
  
4. Activate the virtual environment:
source <virtual-environment-name>/bin/activate
 
5. Install the project dependencies:
pip install -r requirements.txt

6. Create a `.env` file for storing environment variables:
cp example.env .env

7. Set up the database by running the following commands:
python manage.py makemigrations
python manage.py migrate

8. Run the development server:
python manage.py runserver
  
9. Open your web browser and navigate to `http://127.0.0.1:8000/` to view the project.

