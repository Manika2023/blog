
from django.urls import path
from accounts import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
#     path('',views.index,name="index"),
    path('register/',views.register_user,name="register_user"),
    path('login/',views.login_user,name="login_user"),
    path('profile/',views.user_profile,name="user_profile"),
    path('change_password/',views.change_password,name="change_password"),
    path('logout/',views.logout_user,name="logout")
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


