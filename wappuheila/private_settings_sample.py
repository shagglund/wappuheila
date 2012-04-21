import os
DOC_ROOT = os.path.dirname(os.path.abspath(__file__))
DB_ENGINE ='django.db.backends.sqlite3'
DB_NAME=os.path.join(DOC_ROOT,'sqlite3.db')
DB_USER=''
DB_PASSWORD=''
DB_HOST=''
DB_PORT=''
MEDIA_ROOT=os.path.join(DOC_ROOT, "media_files")
STATIC_ROOT=os.path.join(DOC_ROOT, "static_files")

FB_API_SECRET = 'FB_APP_SECRET'
FB_API_ID = 'FB_APP_ID'
GOOGLE_OAUTH2_ID='GOOGLE_API_APP_ID'
GOOGLE_OAUTH2_SECRET='GOOGLE_API_SECRET'
ADMINS=None
SECRET_KEY='A_DJANGO_GENERATED_SECRET_KEY'