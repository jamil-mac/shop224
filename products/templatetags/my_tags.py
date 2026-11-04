from django import template

from blog.models import CommentLikeModel

register = template.Library()


@register.simple_tag
def heart_icon(user, product):
    return "fa-solid fa-heart" if user.is_authenticated and user in product.wishlist.all() else "fa-regular fa-heart"


@register.simple_tag
def comment_heart_icon(user, comment):
    like = CommentLikeModel.objects.filter(user=user, comment=comment)

    return "fa-solid fa-heart" if user.is_authenticated and like.exists() else "fa-regular fa-heart"
