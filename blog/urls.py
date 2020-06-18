from django.urls import path
from blog import views
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('register/', views.register, name='register'),
    path('userlogin/', views.userlogin, name='userlogin'),
    path('userlogout/', views.userlogout, name='userlogout'),
    path('createpost/', views.createpost, name='createpost'),
    path('alldrafts/', views.ShowDraftsListView.as_view(), name='showdrafts'),
    path('allposts/', views.ShowPostsListView.as_view(), name='showposts'),
    #path('allposts/', views.deletepost, name='showposts'),
    #url(r'^post/(?P<pk>\d+)/$', views.PostDetailView.as_view(), name='postdetail'),
    url(r'^post/(?P<pk>\d+)/$', views.addcomment, name='postdetail'),
    #url(r'^profile/post/(?P<pk>\d+)/$', views.PostDetailView.as_view(), name = 'profile_postdetail'),
    url(r'^profile/post/(?P<pk>\d+)/$', views.addcomment, name='postdetail'),
    url(r'^alldrafts/post/(?P<pk>\d+)/$', views.addcomment, name='postdetail'),
    url(r'^allposts/post/(?P<pk>\d+)/$', views.addcomment, name='postdetail'),
    url(r'^allposts/post/update/(?P<pk>\d+)/$', views.UpdatePostView.as_view(), name='updatepost'),
    url('^alldrafts/draft/update/(?P<pk>\d+)/$', views.updatedraft, name='updatedraft'),
    url(r'^posts/delete/(?P<pk>\d+)/$', views.deletepost, name='deletepost'),
    url(r'^profile/$', views.UserProfileView.as_view(), name = 'userprofile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
