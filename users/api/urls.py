from django.urls import path,re_path, include
from rest_framework.authtoken.views import obtain_auth_token


from rest_framework import routers

from users.api.views import UserFeedbackViewSet, ExploreCoaches, ExplorePlayers, \
    FollowUser, UnFollowUser, UserFollowers, UserFollowing, ListUsersView

router = routers.DefaultRouter()
router.register(r'users', ListUsersView)
router.register(r'feedback', UserFeedbackViewSet)
# router.register(r'devices', DeviceViewSet)
# router.register(r'messagetemplate', CreateMessageTemplateViewSet)
# router.register(r'mailalerts', MailAlertsViewSet)
# router.register(r'mailsubscription', MailSubscriptionViewSet)



# app_name = "authentication"


urlpatterns = [
    # path('sign_up', SignUp, name='sign_up'),
    re_path('', include(router.urls)),
    re_path(r'^auth-token$', obtain_auth_token),
    # path("feedback/", UserFeedbackViewSet.as_view({'get': 'list'}), name="explore_coaches"),
    path("explore_coaches/", ExploreCoaches.as_view(), name="explore_coaches"),
    path("explore_players/", ExplorePlayers.as_view(), name="explore_players"),
    path("<int:user_id>/follow/", FollowUser.as_view(), name="follow_user"),
    path("<int:user_id>/unfollow/", UnFollowUser.as_view(), 
         name="unfollow_user"),
    path("<first_name>/followers", UserFollowers.as_view(), name="user_followers"),
    path("<first_name>/following", UserFollowing.as_view(), name="user_following"),
]