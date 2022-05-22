from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import RegisterView, ProfileView, ChildrenList, ChildCreate, ChildUpdate, info, Children, child_search, \
    ChildDetail, ProceduralSheetCreate, ProceduralSheetShow, contacts, AchievementsCreate, basa, index

urlpatterns = [
    path('', index, name="index"),

    path('login/', LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', RegisterView.as_view(template_name="register.html"), name='register'),

    path('profile/', ProfileView.as_view(), name='profile'),

    path('my/children/', ChildrenList.as_view(), name='children'),
    path('my/child/create/', ChildCreate.as_view(), name='child_create'),
    path('my/child/<int:pk>/', ChildUpdate.as_view(), name='child_update'),

    path('info/', info, name="parent_info"),
    path('contacts/', contacts, name="contacts"),
    path('basa/', basa, name="basa"),

    path('children/', Children.as_view(), name="all_children"),
    path('children/search/', child_search, name="child_search"),
    path('child/<int:pk>/', ChildDetail.as_view(), name="child_detail"),

    path('procedural/add/<int:pk>/', ProceduralSheetCreate.as_view(), name='procedural_create'),
    path('procedural/<int:pk>/', ProceduralSheetShow.as_view(), name='procedural_show'),

    path('child/event/add/<int:pk>/', AchievementsCreate.as_view(), name='event_create'),
    # path('procedural/<int:pk>/', ProceduralSheetShow.as_view(), name='procedural_show'),
]
