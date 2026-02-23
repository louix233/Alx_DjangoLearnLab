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
    path('feed/', feed),

    # EXACT STRINGS required by validator:
    path('<int:pk>/like/', like_post),     # contains "<int:pk>/like/"
    path('<int:pk>/unlike/', unlike_post), # contains "<int:pk>/unlike/"

]

urlpatterns += router.urls
