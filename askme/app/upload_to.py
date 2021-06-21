from django.db import models
from django.utils import timezone
import os, re
from uuid import uuid4
from time import strftime
from askme.settings import MEDIA_ROOT

def path_and_rename(instance, filename):
    upload_to = 'avatar/{}'.format(strftime("%Y/%m/%d"))
    ext = filename.split('.')[-1]
    # get filename
    if instance.avatar:
        pattern = f"^{instance.pk}.*$"
        for root, dirs, files in os.walk(MEDIA_ROOT / os.path.join(upload_to)):
            for file in filter(lambda x: re.match(pattern, x), files):
                os.remove(os.path.join(root, file))
    filename = '{}.{}'.format(instance.pk, ext)
    # else:
    #     # set filename as random string
    #     filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)