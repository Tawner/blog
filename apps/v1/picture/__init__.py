from .views import *


def add_resource(api):
    api.add_resource(PictureAlbumListView, '/picture/list')
    api.add_resource(PictureInfoView, '/picture/album/<int:album_id>')
    api.add_resource(PictureAlbumListAdminView, '/admin/picture/album/list')
    api.add_resource(AddPictureAlbumView, '/admin/picture/album')
    api.add_resource(PictureAlbumInfoView, '/admin/picture/album/<int:album_id>')
    api.add_resource(AddPictureView, '/admin/picture')
    api.add_resource(PictureInfoAdminView, '/admin/picture/<int:picture_id>')

