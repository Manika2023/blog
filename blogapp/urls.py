
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
   path('home/',views.home_api,name="home"),
   path('author_dashboard/',views.author_dashboard_api,name="auther_dashboard"),
   path('blog_posts/',views.blog_posts_api,name="blog_posts"),
   path('blog_posts/<int:id>/',views.post_detail_api,name="post_detail"),
   path('author_create_post/',views.author_create_post_api,name="author_create_post"),
   path('author_edit_post/<int:id>/',views.author_edit_post_api,name="author_edit_post"),
   path('author_post_detail/<int:id>/',views.author_post_detail_api,name="author_post_detail"),
   path('delete_post_author/<int:id>/',views.author_delete_post_api,name="edit_post_author"),
   path('search/',views.search_api,name="search")

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
