from flask import Flask
from app import app as flask_app
from werkzeug.middleware.proxy_fix import ProxyFix

# Apply ProxyFix middleware
flask_app.wsgi_app = ProxyFix(flask_app.wsgi_app, x_proto=1, x_host=1)

# Create handler for Vercel
def handler(request):
    with flask_app.request_context(request):
        try:
            return flask_app.full_dispatch_request()
        except Exception as e:
            flask_app.logger.error(f"Error handling request: {str(e)}")
            return 'Internal Server Error', 500

# This is required for Vercel serverless functions
handler = app
