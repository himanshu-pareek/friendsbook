from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout

urlpatterns = [
    url (r'^$', views.home),
    url (r'^login/$', login, {'template_name': 'accounts/login.html'}),
    url (r'^logout/$', logout, {'template_name': 'accounts/logout.html'}),
    url (r'^register/$', views.register, name='register'),
    url (r'^profile/$', views.view_profile, name = 'profile'),
    url (r'^profile/edit/$', views.edit_profile, name = 'edit_profile'),
    # url (r'^change-password/$', views.change_password, name = 'change_password')
    url (r'^search_results/$', views.search_results, name = 'search_results'),
    url (r'^public_profile/$', views.public_profile, name = 'public_profile'),
    url (r'^add_friend/$', views.add_friend, name = 'add_friend'),
    url (r'^confirm_request/$', views.confirm_request, name = 'confirm_request'),
    url (r'^chat/$', views.chat, name = 'chat'),
    url (r'^chat_box/$', views.chat_box, name = 'chat_box'),
    url (r'^save_message/$', views.save_message, name = 'save_message')
]
