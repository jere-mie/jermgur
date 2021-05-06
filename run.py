from website import app, db
import os

# initializing db if it doesn't exist yet
if not os.path.exists("website/site.db"):
    db.create_all()

if __name__=='__main__':
    app.run(debug=True)