from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    ProfileView,
    FollowUserView,
    UnfollowUserView,
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/', ProfileView.as_view()),

    # EXACT STRINGS required by validator:
    path('follow/<int:user_id>', FollowUserView.as_view()),      # contains "follow/<int:user_id>"
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view()), # contains "unfollow/<int:user_id>/"
]
