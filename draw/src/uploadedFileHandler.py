import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from ..models import FileOwl
from .utils import BUFF_SIZE
from .utils import md5_uploaded_file
from .utils import sha1_uploaded_file


def handle_uploaded_file(f, user):
    old_name = f._name
    #+- get sha1 of input file
    sha1 = sha1_uploaded_file(f)
    new_name = "".join((sha1, "_", old_name))
    path = "".join((settings.OWLS_DIR, new_name))
    
    #+- save file to settings.OWLS_DIR
    with open(path, 'wb+') as destination:
        for chunk in f.chunks(chunk_size=BUFF_SIZE):
            destination.write(chunk)
    
    #+- set-get information about file in db in FileOwl model
    try:
        db_file_owl = FileOwl.objects.get(sha1=sha1)
    except ObjectDoesNotExist:
        file_name_physical = path
        db_file_owl = FileOwl(old_name=old_name, new_name=new_name, path_name=path, sha1=sha1, pub_date=datetime.datetime.now(), owner=user)
        db_file_owl.save()
    
    return(db_file_owl)
