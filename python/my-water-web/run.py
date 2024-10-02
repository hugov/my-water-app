from app import create_app
from datetime import datetime, timedelta


app = create_app()
app.permanent_session_lifetime = timedelta(minutes=30)

if __name__ == '__main__':
    #app.run(host="0.0.0.0", port=5000, debug=True)
    app.run(debug=True)