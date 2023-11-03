from .local import *

import warnings

# Suppress the RuntimeWarning about naive datetimes
warnings.filterwarnings(
    "ignore", category=RuntimeWarning, module="django.db.models.fields"
)
MEDIA_URL = "http://testserver/"
