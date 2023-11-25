from django.urls import path, include
from main.views import index
from .views import other_page, DeleteAppliView, register, ChangeStatusAcceptWork, ChangeStatusCompleted, request_all, \
   category_list, admin_category_add, AdminCategoryDelete
from .views import BBLoginView
from .views import BBLogoutView
from .views import profile
from .views import RegisterDoneView, RegisterUserView
from .views import profile_applic_add

app_name = 'main'


urlpatterns = [
   path('', index, name='index'),
   path('<str:page>/', other_page, name='other'),
   path('accounts/login', BBLoginView.as_view(), name='login'),
   path('accounts/logout/', BBLogoutView.as_view(), name='logout'),
   path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
   path('accounts/register/', register, name='register'),
   # path('catalog/', include('catalog.urls')),
   # path('accounts/', include('django.contrib.auth.urls')),
   path('accounts/profile/', profile, name='profile'),
   path('accounts/profile/add/', profile_applic_add, name='profile_applic_add'),
   # path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
   path('accounts/profile/delete/<int:pk>/', DeleteAppliView.as_view(), name='profile_applic_delete'),
   path('category/add/', admin_category_add, name='admin_category_add'),
   path('category/delete/<int:id>', AdminCategoryDelete.as_view(), name='admin_category_delete'),
   path('category/list/', category_list, name='category_list'),
   path('request/all/', request_all, name='request_all'),
   path('change/status/completed/<int:id>/', ChangeStatusCompleted.as_view(), name='change_status_completed'),
   path('change/status/accept/work/<int:id>/', ChangeStatusAcceptWork.as_view(), name='change_status_accept_work'),


]





