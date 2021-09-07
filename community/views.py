from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse

# Create your views here.


from .models import TubeUser,Video, Contact
from django.conf import settings 
import random


from django.contrib.auth import login, authenticate

from .models import CustomUser as User
from .forms import SignUpForm, TubeUrlForm, VideoForm, ContactForm



def get_video(user):
	tube_user = TubeUser.objects.prefetch_related('viewed_users__video_set').get(user=user)
	viewed = tube_user.viewed_users.all()
	#as viewed is a queryset get the first user and videos
	if viewed.count() > 0:
		try:
			video = random.choice(viewed[0].video_set.all())
			tube_user.viewed_users.remove(viewed[0])
		except IndexError:
			video = None

		if video:
			tube_user.subscribed_users.add(viewed[0])
		
		#video[0] = new user which the viewer should subscribe
	else:
		subscribed = tube_user.subscribed_users.all()
		
		# subscribed = subscribed.union(tube_user)
		
		video = Video.objects.exclude(user__in=subscribed).exclude(user=tube_user)
		print(video)
		if video:
			video.user.viewed_users.add(tube_user)
		else:
			print('ranodm video')
			videos = Video.objects.all()
			video = random.choice(videos)
			
	return video


# def get_video_for_ajax(request):
# 	tube_user.
def test_view(request):
	print(request.GET)
	print(request.POST)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def home_view(request):
	user = request.user
	if user.is_authenticated:
		if request.session.get('unwatched'):
			video = Video.objects.get(id=request.session.get('unwatched'))

		else:
			video = get_video(request.user)
			request.session['unwatched'] = video.id
		
		context = {
			'video':video,
			}
		return render(request, 'dashboard_view.html', context)
	else:
		return render(request, 'homepage.html', {})

def dashboard_view(request):
	video_id = request.session.get('unwatched')
	video = Video.objects.get(id=video_id)
	return render(request, 'video_view.html', {'video':video})




def handle_video_ajax(request):

	if request.is_ajax():
		video = get_video(request.user)
		request.session['unwatched'] = video.id
	return render(request, 'video_view.html', {'video':video})


def notification_view(request):

	subcribed_users = TubeUser.objects.get(request.user).subscribed_users.all()
	users = User.objects.filter(tubeuser__in=subscribed_users)
	print(users)
	context = {
		'users':user
	}
	return render(request, 'notification_view.html', context)




def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.tubeuser.tube_url = form.cleaned_data.get('tube_url')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            form.cleaned_data.get('tube_url')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('community:dashboard')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def add_tube_url(request):
	if request.method == "POST":
		form = TubeUrlForm(request.POST)
		tube_url = form.cleaned_data.get('tube_url')
		t_user = tube_user.objects.create(user=request.user, tube_url=tube_url)
		return redirect('community:dashboard')
	else:
		form = TubeUrlForm()
	return render(request, 'registration/tube_url_add.html', {'form':form})


def add_video(request):
	form = VideoForm()
	if request.method == 'POST' and request.is_ajax():
		print('ok')

		form = VideoForm(request.POST)
		if form.is_valid():
			embed_script = form.cleaned_data.get('embed_script')
			url = form.cleaned_data.get('url')
			t = TubeUser.objects.get(user=request.user)
			vid = Video.objects.create(user=t, embed_script=embed_script, url=url)
			return JsonResponse({'url':url}, status=200)
		else:
			errors = form.errors.as_json()
			return JsonResponse({"errors": errors}, status=400)
	return render(request, 'video_add.html', {'form':form})


def profile_view(request):
	user = request.user
	tube_user = TubeUser.objects.get(user=user)
	videos = Video.objects.filter(user=tube_user)
	context = {
	'user':user,
	'tube_user': tube_user,
	'videos':videos
	}
	return render(request, 'profile.html', context)

def notification_view(request):
	tube_user = TubeUser.objects.get(user=request.user).subscribed_users.all()
	users = User.objects.filter(tubeuser__in=tube_user)
	context = {
	'users':users
	}
	return render(request, 'notification_view.html', context)


def contact_view(request):
	form = ContactForm()
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data.get('email')
			message = form.cleaned_data.get('message')
			Contact.objects.create(email=email, message=message)
			return redirect('index')
	return render(request, 'contact.html', {'form':form})


#https://cdn.jsdelivr.net/npm/jquery-waypoints@2.0.5/waypoints.min.js