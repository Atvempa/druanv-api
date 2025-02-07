from app import app

# For Vercel serverless functions
def handler(request):
    return app.wsgi_app(request.environ, lambda x, y: [])  
