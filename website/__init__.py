from flask import Flask, session, g
from supabase import create_client, Client

# Supabase Configuration
SUPABASE_URL = "https://bjbqmaxoerkggynlkruo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJqYnFtYXhvZXJrZ2d5bmxrcnVvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzcwOTcyMjksImV4cCI6MjA1MjY3MzIyOX0.M-bD_HwqpGG1A5gUTnfFVOrTX80OXt-Olj-ashHJLZo"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def create_app():
    app = Flask(__name__)
    app.secret_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJqYnFtYXhvZXJrZ2d5bmxrcnVvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczNzA5NzIyOSwiZXhwIjoyMDUyNjczMjI5fQ.MdNxfSTPD51Yc8aokEhxGiavR0HOKPrky68d-iA6l4o'

    @app.before_request
    def before_request():
        user = session.get('user')
        g.user = user  

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
