from django.urls import path
# from .views import Signup,UserList,user_login,UserDetails,TokenRefresh,logout_view,SnippetDetail,SnippetDestroyDetail,SnippetSoftDestroyDetail,UserList,list
from .views import *
urlpatterns = [
    path('signup/',Signup.as_view() ),
    # path('login/',user_login),
    # path('users/',UserList.as_view()),
    # path('users/<pk>', UserDetails.as_view()),
    # path('rtoken/',TokenRefresh.as_view()),   
    # path('users/detail/<pk>',SnippetDetail.as_view()),
    # path('users/softdelete/<pk>',SnippetSoftDestroyDetail.as_view()),
    # path('users/delete/<pk>',SnippetDestroyDetail.as_view()),
    # path('logout/',logout_view),

    path('user/',UserList.as_view()),
    path('user/<pk>',UserDetail.as_view()),
    path('user/<pk>/company',CompanyList.as_view()),
    path('user/<int:pk>/company/<int:company_id>',CompanyDetail.as_view())
]
