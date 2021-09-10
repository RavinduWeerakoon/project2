from django.urls import path

app_name = 'community'
from .views import (test_view, 
					 
					handle_video_ajax, 
					add_video, 
					profile_view, 
					dashboard_view,
					notification_view,
					getting_started)

urlpatterns = [
	
	path('test/', test_view, name="test-view"),
	
	path('dashboard-video-ajax/,', handle_video_ajax, name='handle-video-ajax'),
	path('video-add/', add_video, name="add-video"),
	path('profile/', profile_view, name='profile-view'),
	path('notifications/', notification_view, name='notifications'),
	path('dashboard-view/', dashboard_view, name='dashboard'),
	path('getting-started/', getting_started, name='getting-started')]