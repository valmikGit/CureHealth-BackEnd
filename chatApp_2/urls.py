from django.urls import path
from chatApp_2 import views

urlpatterns = [
    path('', view=views.chat_2_Home),
    path('send-messages/', view=views.SendMessages.as_view()),
    path('my-messages/', view=views.MyInbox.as_view()),
    path('get-messages/', view=views.GetMessages.as_view()),
    path('search-user/', view=views.SearchUser.as_view())
    # path('my-mesages/<str:user_id>', view=views.MyInbox.as_view()),
    # path('get-messages/<str:sender-id>/<str:receiver-id>', view=views.GetMessages.as_view()),
]
