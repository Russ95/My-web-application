from django.shortcuts import render

# Create your views here.

# Create your views here.

# from django.shortcuts import render

from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone

from time_manage.forms import LoginForm, RegistrationForm, CreateForm, EditForm

from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar
from .models import *
from .utils import Calendar
from .forms import EventForm

from .models import *
# from .utils import Calendar
# from .forms import EventForm


@login_required
def home_page(request):
    all_items = Event.objects.filter(user=request.user)
    print (all_items)
    # print (item)

    # try:
    #     newuser=Profile.objects.get(user=request.user)
    # except:
    #     newuser=Profile(user=request.user)
    #     newuser.save()
    context={}
    context['msg']='hello world'
    context['items']=all_items

    return render(request, 'time_manage/main_page.html', context)

def index(request):
    return HttpResponse('<p>index page</p>')

class CalendarView(generic.ListView):
    model = Event
    template_name = 'time_manage/calendar.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month
@login_required
def event(request, event_id=None):
    user=request.user
    instance = Event(user=user)
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event(user=user)
    print (instance)
    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        # return HttpResponseRedirect(reverse('cal:calendar'))
        return HttpResponseRedirect(reverse('time_manage:calendar'))
        # return redirect(reverse('calendar'))
    return render(request, 'time_manage/event.html', {'form': form})




#三件套
def login_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'time_manage/login.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'time_manage/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('time_manage:home'))

def logout_action(request):
    logout(request)
    return redirect(reverse('time_manage:login'))

def register_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        # print (context)
        return render(request, 'time_manage/register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'time_manage/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('time_manage:home'))
