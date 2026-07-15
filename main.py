from database import create_database
from login import LoginWindow
from ui import BillingSystem

# Create database automatically if it doesn't exist
create_database()

login = LoginWindow()
login.run()

if login.login_success:
    app = BillingSystem()
    app.run()