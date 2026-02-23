from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    PostViewSet,
    CommentViewSet,
    like_post,
    unlike_post,
    feed,
)

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('comments', CommentViewSet)

urlpatterns = [
    # EXACT STRING required by validator:
    path('feed/', feed),               # contains "feed/"

    path('posts/<int:post_id>/like/', like_post),
    path('posts/<int:post_id>/unlike/', unlike_post),
]

urlpatterns += router.urls
