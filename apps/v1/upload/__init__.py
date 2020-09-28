from .views import *


def add_resource(api):
    api.add_resource(UploadView, '/upload')

