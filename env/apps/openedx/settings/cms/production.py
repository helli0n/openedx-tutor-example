# -*- coding: utf-8 -*-
import os
from cms.envs.production import *

####### Settings common to LMS and CMS
import json
import os

from xmodule.modulestore.modulestore_settings import update_module_store_settings

# Mongodb connection parameters: simply modify `mongodb_parameters` to affect all connections to MongoDb.
mongodb_parameters = {
    "host": "mongodb",
    "port": 27017,
    
    "user": None,
    "password": None,
    
    "db": "openedx",
}
DOC_STORE_CONFIG = mongodb_parameters
CONTENTSTORE = {
    "ENGINE": "xmodule.contentstore.mongo.MongoContentStore",
    "ADDITIONAL_OPTIONS": {},
    "DOC_STORE_CONFIG": DOC_STORE_CONFIG
}
# Load module store settings from config files
update_module_store_settings(MODULESTORE, doc_store_settings=DOC_STORE_CONFIG)
DATA_DIR = "/openedx/data/modulestore"

for store in MODULESTORE["default"]["OPTIONS"]["stores"]:
   store["OPTIONS"]["fs_root"] = DATA_DIR

# Behave like memcache when it comes to connection errors
DJANGO_REDIS_IGNORE_EXCEPTIONS = True

# Elasticsearch connection parameters
ELASTIC_SEARCH_CONFIG = [{
  
  "host": "elasticsearch",
  "port": 9200,
}]

CONTACT_MAILING_ADDRESS = "My Open edX - http://local.overhang.io"

DEFAULT_FROM_EMAIL = ENV_TOKENS.get("DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
DEFAULT_FEEDBACK_EMAIL = ENV_TOKENS.get("DEFAULT_FEEDBACK_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
SERVER_EMAIL = ENV_TOKENS.get("SERVER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
TECH_SUPPORT_EMAIL = ENV_TOKENS.get("TECH_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
CONTACT_EMAIL = ENV_TOKENS.get("CONTACT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BUGS_EMAIL = ENV_TOKENS.get("BUGS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
UNIVERSITY_EMAIL = ENV_TOKENS.get("UNIVERSITY_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PRESS_EMAIL = ENV_TOKENS.get("PRESS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PAYMENT_SUPPORT_EMAIL = ENV_TOKENS.get("PAYMENT_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BULK_EMAIL_DEFAULT_FROM_EMAIL = ENV_TOKENS.get("BULK_EMAIL_DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_MANAGER_EMAIL = ENV_TOKENS.get("API_ACCESS_MANAGER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_FROM_EMAIL = ENV_TOKENS.get("API_ACCESS_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])

# Get rid completely of coursewarehistoryextended, as we do not use the CSMH database
INSTALLED_APPS.remove("lms.djangoapps.coursewarehistoryextended")
DATABASE_ROUTERS.remove(
    "openedx.core.lib.django_courseware_routers.StudentModuleHistoryExtendedRouter"
)

# Set uploaded media file path
MEDIA_ROOT = "/openedx/media/"

# Add your MFE and third-party app domains here
CORS_ORIGIN_WHITELIST = []

# Video settings
VIDEO_IMAGE_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT
VIDEO_TRANSCRIPTS_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT

GRADES_DOWNLOAD = {
    "STORAGE_TYPE": "",
    "STORAGE_KWARGS": {
        "base_url": "/media/grades/",
        "location": "/openedx/media/grades",
    },
}

ORA2_FILEUPLOAD_BACKEND = "filesystem"
ORA2_FILEUPLOAD_ROOT = "/openedx/data/ora2"
ORA2_FILEUPLOAD_CACHE_NAME = "ora2-storage"

# Change syslog-based loggers which don't work inside docker containers
LOGGING["handlers"]["local"] = {
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "all.log"),
    "formatter": "standard",
}
LOGGING["handlers"]["tracking"] = {
    "level": "DEBUG",
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "tracking.log"),
    "formatter": "standard",
}
LOGGING["loggers"]["tracking"]["handlers"] = ["console", "local", "tracking"]
# Silence some loggers (note: we must attempt to get rid of these when upgrading from one release to the next)

import warnings
from django.utils.deprecation import RemovedInDjango40Warning, RemovedInDjango41Warning
warnings.filterwarnings("ignore", category=RemovedInDjango40Warning)
warnings.filterwarnings("ignore", category=RemovedInDjango41Warning)
warnings.filterwarnings("ignore", category=DeprecationWarning, module="lms.djangoapps.course_wiki.plugins.markdownedx.wiki_plugin")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="wiki.plugins.links.wiki_plugin")

# Email
EMAIL_USE_SSL = False
# Forward all emails from edX's Automated Communication Engine (ACE) to django.
ACE_ENABLED_CHANNELS = ["django_email"]
ACE_CHANNEL_DEFAULT_EMAIL = "django_email"
ACE_CHANNEL_TRANSACTIONAL_EMAIL = "django_email"
EMAIL_FILE_PATH = "/tmp/openedx/emails"

# Language/locales
LOCALE_PATHS.append("/openedx/locale/contrib/locale")
LOCALE_PATHS.append("/openedx/locale/user/locale")
LANGUAGE_COOKIE_NAME = "openedx-language-preference"

# Allow the platform to include itself in an iframe
X_FRAME_OPTIONS = "SAMEORIGIN"


JWT_AUTH["JWT_ISSUER"] = "http://local.overhang.io/oauth2"
JWT_AUTH["JWT_AUDIENCE"] = "openedx"
JWT_AUTH["JWT_SECRET_KEY"] = "7S9loF7z1Nw9bRs0YGIPnbSy"
JWT_AUTH["JWT_PRIVATE_SIGNING_JWK"] = json.dumps(
    {
        "kid": "openedx",
        "kty": "RSA",
        "e": "AQAB",
        "d": "BEBakodZ4SdNavYqgPQ05tmmVen-eN_Hlqnfk7hZNIfLehAToW8SjoWzY0HqLs0YOdNYoqCUlVOR79JmwBeNqX7olXoawE_6xg3ulgNWuqzo_Ksz4D5IpeDauZFgc3HjW4LXQ8_bRy2KSeVPvJxw1Wr7Q_oYr9ulbnO8i3BN2Ql-OnBwmsEvAkC_DDYNdTZtg3aA8Kg1Qo0_B5FUskkohJ2H6UHQEv6GGJrb4_yI45upXRCkqiNTfgqWL17by6xZJ7pTTWOQXA9B0eGezgnX8pu7xiQfehKk_dwTgTPQirXx4czYwDmDtxOfIZApOPCWvEV9mFsBALGeAAmsMGnrdw",
        "n": "nTi4vf8k4pTS8Z1bDHQfKZxaLH3s0QQWaBMzAaaF2FKhPYvD1euhXvgEkYLFq8YsYnUHGT0cd-urdB6DxFXeG6xrb0IfHkXVMqMu6omUxIEYR61zK_Y1ndewCEv8jjGRZ4gFZBn3h7z93z8-IQJ-9NN8ZQbozui2UU4HoiFEKQhfXki5WWoLv-79awK_A2qgGTy3rUZBtH7iST45eAUWCKJAyNCt5yfdcDoNPcXB_Rdt8sk3Crgsqr9RWawHTAWkcUcVfEkDSpm8nTjJd7hmuMx9gp_P5xv1voxmYU3JCvlVH-uRF8E1VXJUvv-cAdBjhk_X0Xj4P-II4iiq0oBJcQ",
        "p": "wAtv1KF7j6NrW7OTbkqyKj2OipLckDIVPfQl7vIw8_j2lQS-LHYERvs7qVNviAA_mdsTWT4XRRkrJjlko4fUq8fAU4breW9H4enRIoB_sbtSPgRiE2JVzOZumvnKMBTZF2f1QUjxg9FqbHigzFn_Hz12s4-BE8gQ4l85QEHXhVc",
        "q": "0ZR6abXRxbJf3Ajku8weROdCKUakpLYs1psanMYJReUY4DXANtWR5A80-KGKtMEs6smhiYROO5zuZYpmR38e3e1HbvYt4Vrn109m4QOZZe554TrLjQ-H0Ud7a-1IQ1fy2C3H9UWWhYoxoAUts_pH6XdOaTWgioorbnPENxoqYnc",
    }
)
JWT_AUTH["JWT_PUBLIC_SIGNING_JWK_SET"] = json.dumps(
    {
        "keys": [
            {
                "kid": "openedx",
                "kty": "RSA",
                "e": "AQAB",
                "n": "nTi4vf8k4pTS8Z1bDHQfKZxaLH3s0QQWaBMzAaaF2FKhPYvD1euhXvgEkYLFq8YsYnUHGT0cd-urdB6DxFXeG6xrb0IfHkXVMqMu6omUxIEYR61zK_Y1ndewCEv8jjGRZ4gFZBn3h7z93z8-IQJ-9NN8ZQbozui2UU4HoiFEKQhfXki5WWoLv-79awK_A2qgGTy3rUZBtH7iST45eAUWCKJAyNCt5yfdcDoNPcXB_Rdt8sk3Crgsqr9RWawHTAWkcUcVfEkDSpm8nTjJd7hmuMx9gp_P5xv1voxmYU3JCvlVH-uRF8E1VXJUvv-cAdBjhk_X0Xj4P-II4iiq0oBJcQ",
            }
        ]
    }
)
JWT_AUTH["JWT_ISSUERS"] = [
    {
        "ISSUER": "http://local.overhang.io/oauth2",
        "AUDIENCE": "openedx",
        "SECRET_KEY": "7S9loF7z1Nw9bRs0YGIPnbSy"
    }
]

# Enable/Disable some features globally
FEATURES["ENABLE_DISCUSSION_SERVICE"] = False
FEATURES["PREVENT_CONCURRENT_LOGINS"] = False

# Disable codejail support
# explicitely configuring python is necessary to prevent unsafe calls
import codejail.jail_code
codejail.jail_code.configure("python", "nonexistingpythonbinary", user=None)
# another configuration entry is required to override prod/dev settings
CODE_JAIL = {
    "python_bin": "nonexistingpythonbinary",
    "user": None,
}


######## End of settings common to LMS and CMS

######## Common CMS settings

STUDIO_NAME = u"My Open edX - Studio"

# Authentication
SOCIAL_AUTH_EDX_OAUTH2_SECRET = "cUdmXBEXTNBTPl3iGCsYc5EC"
SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT = "http://lms:8000"
SOCIAL_AUTH_REDIRECT_IS_HTTPS = False  # scheme is correctly included in redirect_uri
SESSION_COOKIE_NAME = "studio_session_id"

MAX_ASSET_UPLOAD_FILE_SIZE_IN_MB = 100

FRONTEND_LOGIN_URL = LMS_ROOT_URL + '/login'
FRONTEND_REGISTER_URL = LMS_ROOT_URL + '/register'

# Create folders if necessary
for folder in [LOG_DIR, MEDIA_ROOT, STATIC_ROOT_BASE]:
    if not os.path.exists(folder):
        os.makedirs(folder)



######## End of common CMS settings

ALLOWED_HOSTS = [
    ENV_TOKENS.get("CMS_BASE"),
    "cms",
]

# Authentication
SOCIAL_AUTH_EDX_OAUTH2_KEY = "cms-sso"
SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = "http://local.overhang.io"

