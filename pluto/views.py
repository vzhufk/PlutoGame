import json

import django.contrib.auth as auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from pluto import models
from pluto.forms import SignUpForm, LogInForm, PasswordForm, PersonalInfoForm, PersonalImageForm, LevelCreationForm
from pluto.models import mate_change


def test(request):
    messages.info(request, "Some brand new info.")
    messages.success(request, "It's already a success.")
    messages.warning(request, "But be warned.")
    messages.error(request, "Errors everywhere.")
    return render(request, 'base.html')


def index(request):
    context = {'content': []}
    article = models.Article.objects.all().order_by('-date')
    messages.info(request, "Developer build.")
    context['title'] = 'Pluto'
    context['content'] += article
    return render(request, 'base.html', context)


def signup(request):
    context = {'title': 'SignUp', 'form': SignUpForm()}
    if request.method == 'POST':
        form = context['form'] = SignUpForm(request.POST)
        if not form.is_valid():
            [messages.error(request, str(x)) for y in list(form.errors.values()) for x in y]
        else:
            user = models.User()
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Success. User has been registered.')
    return render(request, 'form.html', context)


def login(request):
    context = {'title': 'Login', 'form': LogInForm()}

    if request.method == 'POST':
        form = context['form'] = LogInForm(request.POST)
        if not form.is_valid():
            [messages.error(request, str(x)) for y in list(form.errors.values()) for x in y]
        else:
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(request=request, username=username, password=password)
            if user is None:
                messages.error(request, 'Email or password is incorrect.')
            else:
                auth.login(request, user)
                return index(request)
    return render(request, 'form.html', context)


def logout(request):
    auth.logout(request)
    messages.success(request, 'Logout proceed successfully.')
    return index(request)


def profile(request, profile_id=None):
    context = {}
    if not profile_id:
        profile_id = request.user.id
    try:
        context['profile'] = models.User.objects.get(id=profile_id)
        context['levels'] = models.Level.objects.filter(by=profile_id)
        try:
            mate = models.Mate.objects.filter(Q(a=request.user.id, b=profile_id) | Q(a=profile_id, b=request.user.id))[
                0]
        except IndexError:
            mate = None
        except ObjectDoesNotExist:
            mate = None

        if mate:
            relation = {mate.a.id: mate.a_confirmation, mate.b.id: mate.b_confirmation}
        else:
            relation = {request.user.id: False, int(profile_id): False}
        context['mate'] = {}
        context['mate']['me'] = relation[request.user.id]
        context['mate']['you'] = relation[int(profile_id)]
    except ObjectDoesNotExist:
        messages.error(request, 'Profile with this ID doesnt exist.')
    return render(request, 'profile.html', context)


@login_required(login_url='/login')
def mate_it(request, profile_id):
    try:
        profile_id = models.User.objects.get(id=profile_id)
    except ObjectDoesNotExist:
        messages.error(request, 'User does not exist.')
        return mates(request)
    mate_change(request.user.id, profile_id.id)
    messages.success(request, 'Request to ' + str(profile_id.username) + ' successfully proceed.')
    return mates(request)


@login_required(login_url='/login')
def mates(request):
    context = {}
    income = models.Mate.objects.filter(
        Q(a=request.user.id, a_confirmation=False, b_confirmation=True)
        | Q(b=request.user.id, a_confirmation=True, b_confirmation=False))

    outcome = models.Mate.objects.filter(
        Q(a=request.user.id, a_confirmation=True, b_confirmation=False)
        | Q(b=request.user.id, a_confirmation=False, b_confirmation=True))

    mate = models.Mate.objects.filter(Q(a=request.user.id, a_confirmation=True, b_confirmation=True)
                                      | Q(b=request.user.id, a_confirmation=True, b_confirmation=True))

    context['mates'] = []
    context['income'] = []
    context['outcome'] = []
    for i in mate:
        if i.a != request.user:
            context['mates'].append(i.a)
        else:
            context['mates'].append(i.b)

    for i in income:
        if i.a != request.user:
            context['income'].append(i.a)
        else:
            context['income'].append(i.b)

    for i in outcome:
        if i.a != request.user:
            context['outcome'].append(i.a)
        else:
            context['outcome'].append(i.b)

    return render(request, 'mates.html', context)


@login_required(login_url='/login')
def settings(request):
    # Initial
    info = PersonalInfoForm()
    info.fields['first_name'].initial = request.user.first_name
    info.fields['last_name'].initial = request.user.last_name

    image = PersonalImageForm()
    image.fields['image'].initial = request.user.image

    password = PasswordForm()
    if request.method == 'POST':
        if 'info_btn' in request.POST:
            info = PersonalInfoForm(request.POST)
            if not info.is_valid():
                [messages.error(request, str(x)) for y in list(info.errors.values()) for x in y]
                info = PersonalInfoForm()
            else:
                request.user.first_name = info.cleaned_data['first_name']
                request.user.last_name = info.cleaned_data['last_name']
                request.user.save()
                messages.success(request, "Personal info successfully changed.")
        if 'image_btn' in request.POST:
            image = PersonalImageForm(request.POST, request.FILES)
            if not image.is_valid():
                [messages.error(request, str(x)) for y in list(image.errors.values()) for x in y]
                image = PersonalImageForm()
            else:
                request.user.image = image.cleaned_data['image']
                request.user.save()
                messages.success(request, "Personal image successfully changed.")
        if 'password_btn' in request.POST:
            password = PasswordForm(request.POST)
            if not password.is_valid():
                [messages.error(request, str(x)) for y in list(password.errors.values()) for x in y]
                password = PasswordForm()
            else:
                request.user.set_password(password.cleaned_data['password'])
                request.user.save()
                messages.success(request, "Password successfully changed.")

    context = {'info_form': info, 'image_form': image, 'password_form': password}
    return render(request, 'settings.html', context)


def levels(request):
    context = {'levels': models.Level.objects.all().order_by('-date')}
    return render(request, 'levels.html', context)


def level(request, level_id=None):
    context = {'level': models.Level.objects.get(id=level_id)}
    return render(request, 'level.html', context)


def play(request, level_id=None):
    if level_id:
        current_level = models.Level.objects.get(id=level_id)
        context = json.loads(current_level.json)
        context['name'] = current_level.name
        context['by'] = current_level.by.username
    else:
        messages.error(request, "Hm. Something went wrong. Try not to do this again.")
        return levels(request)
    # TODO pass pluto skin ;0
    return render(request, 'play.html', context)


@login_required(login_url='/login')
def creator(request, level_id=None):
    creation = LevelCreationForm()

    if level_id:
        try:
            current = models.Level.objects.get(id=level_id)
        except ObjectDoesNotExist:
            messages.error(request, "No such level in database.")
            return levels(request)

        if current.by.id != request.user.id:
            messages.error(request, "You have no permission to edit this.")
            return levels(request)

        creation.fields['name'].initial = current.name
        creation.fields['json'].initial = current.json

    if request.method == 'POST':
        creation = LevelCreationForm(request.POST)
        if not creation.is_valid():
            [messages.error(request, str(x)) for y in list(creation.errors.values()) for x in y]
        else:
            created_level = models.Level()
            if level_id:
                created_level = models.Level.objects.get(id=level_id)

            created_level.name = creation.cleaned_data['name']
            created_level.json = creation.cleaned_data['json']
            created_level.by = request.user
            created_level.save()
            if level_id:
                messages.success(request, 'Success. Level has been edited.')
            else:
                messages.success(request, 'Success. Level has been created.')

    context = {'form': creation}
    return render(request, 'creator.html', context)


@login_required(login_url='/login')
def result(request, level_id):
    if request.method == 'POST':
        current = models.Result()
        current.by = request.user
        current.to = models.Level.objects.get(id=level_id)
        current.attempts = request.POST['attempts']
        current.program = request.POST['program']
