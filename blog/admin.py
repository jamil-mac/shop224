from django.contrib import admin

from blog.models import BannerModel, PostModel, CommentModel, CommentLikeModel

admin.site.register(BannerModel)
admin.site.register(PostModel)
admin.site.register(CommentModel)
admin.site.register(CommentLikeModel)
