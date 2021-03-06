import json

import django.contrib.auth as auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.humanize.templatetags.humanize import ordinal
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone

# Create your views here.
from pluto import models
from pluto.forms import SignUpForm, LogInForm, PasswordForm, PersonalInfoForm, PersonalImageForm, HeroSkinForm
from pluto.models import mate_change


def test(request):
    '''
    messages.info(request, "Some brand new info.")
    messages.success(request, "It's already a success.")
    messages.warning(request, "But be warned.")
    messages.error(request, "Errors everywhere.")
    '''

    level_id = 1
    current_level = models.Level.objects.get(id=level_id)
    context = {'tiles': json.loads(current_level.tilemap),
               'hero': {'direction': current_level.hero_dir, 'x': current_level.hero_x, 'y': current_level.hero_y,
                        'type': request.user.skin if request.user.is_authenticated() else 'polo'},
               'count': {'forward': current_level.command_forward,
                         'backward': current_level.command_backward,
                         'left': current_level.command_left,
                         'right': current_level.command_right,
                         'lo': current_level.command_lo,
                         'op': current_level.command_op}, 'id': current_level.id,
               'name': current_level.name, 'by': current_level.by.username}
    return render(request, 'test.html', context)


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
    return render(request, 'login.html', context)


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
        context['records'] = models.Record.objects.filter(by=profile_id)
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
def me(request):
    return profile(request)


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

    skin = HeroSkinForm()
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
        if 'skin_btn' in request.POST:
            skin = HeroSkinForm(request.POST)
            if not skin.is_valid():
                [messages.error(request, str(x)) for y in list(skin.errors.values()) for x in y]
                skin = HeroSkinForm()
            else:
                request.user.skin = skin.cleaned_data['skin']
                request.user.save()
                messages.success(request, "Skin successfully changed. Have Fun.")

    context = {'info_form': info, 'image_form': image, 'password_form': password, 'skin_form': skin}
    return render(request, 'settings.html', context)


def levels(request):
    context = {'levels': models.Level.objects.all().order_by('-date')}
    return render(request, 'levels.html', context)


def level(request, level_id=None):
    context = {'level': models.Level.objects.get(id=level_id),
               'records': models.Record.objects.filter(to=level_id)}
    return render(request, 'level.html', context)


def play(request, level_id=None):
    if level_id:
        current_level = models.Level.objects.get(id=level_id)
        context = {'tiles': json.loads(current_level.tilemap),
                   'hero': {'direction': current_level.hero_dir, 'x': current_level.hero_x, 'y': current_level.hero_y,
                            'type': request.user.skin if request.user.is_authenticated() else 'polo'},
                   'count': {'forward': current_level.command_forward,
                             'backward': current_level.command_backward,
                             'left': current_level.command_left,
                             'right': current_level.command_right,
                             'lo': current_level.command_lo,
                             'op': current_level.command_op}, 'id': current_level.id,
                   'name': current_level.name, 'by': current_level.by.username}
    else:
        messages.error(request, "Hm. Something went wrong. Try not to do this again.")
        return levels(request)
    # TODO pass pluto skin ;0
    return render(request, 'play.html', context)


@login_required(login_url='/login')
def creator(request, level_id=None):
    if request.method == 'POST':
        creation = json.loads(request.POST['level'])
        created_level = models.Level()
        if level_id:
            created_level = models.Level.objects.get(id=level_id)
        created_level.name = request.POST['name']
        created_level.tilemap = creation['tilemap']
        created_level.command_forward = creation['commands']['forward']
        created_level.command_backward = creation['commands']['backward']
        created_level.command_left = creation['commands']['left']
        created_level.command_right = creation['commands']['right']
        created_level.command_lo = creation['commands']['lo']
        created_level.command_op = creation['commands']['op']
        created_level.hero_x = creation['hero']['x']
        created_level.hero_y = creation['hero']['y']
        created_level.hero_dir = creation['hero']['direction']
        created_level.by = request.user
        created_level.save()
        if level_id:
            messages.success(request, 'Success. Level has been edited.')
        else:
            messages.success(request, 'Success. Level has been created.')
        return level(request, created_level.id)
    else:
        if level_id:
            try:
                current_level = models.Level.objects.get(id=level_id)
            except ObjectDoesNotExist:
                messages.error(request, "No such level in database.")
                return levels(request)

            if current_level.by.id != request.user.id:
                messages.error(request, "You have no permission to edit this.")
                return levels(request)

            context = {'tiles': json.loads(current_level.tilemap),
                       'hero': {'direction': current_level.hero_dir, 'x': current_level.hero_x,
                                'y': current_level.hero_y,
                                'type': request.user.skin if request.user.is_authenticated() else 'polo'},
                       'count': {'forward': current_level.command_forward,
                                 'backward': current_level.command_backward,
                                 'left': current_level.command_left,
                                 'right': current_level.command_right,
                                 'lo': current_level.command_lo,
                                 'op': current_level.command_op}, 'id': current_level.id,
                       'name': current_level.name, 'by': current_level.by.username}
        else:
            context = {'tiles': [
                {"type": "tile_default", "x": 1, "y": 1},
                {"type": "tile_finish", "x": 2, "y": 1}
                ],
                'hero': {'direction': 1, 'x': 1,
                         'y': 1,
                         'type': request.user.skin if request.user.is_authenticated() else 'polo'},
                'count': {'forward': 0,
                          'backward': 0,
                          'left': 0,
                          'right': 0,
                          'lo': 0,
                          'op': 0}, 'id': '-1',
                'name': 'new level', 'by': request.user.username}

    return render(request, 'creator.html', context)


@login_required(login_url='/login')
def record(request, level_id=None, by_id=None):
    # Fix all this shit
    if request.method == 'POST':
        by_id = request.user.id

    if level_id and by_id:
        try:
            current_level = models.Level.objects.get(id=level_id)
        except ObjectDoesNotExist:
            messages.error(request, "No such level.")
            return levels(request)

        if request.method == 'POST':
            try:
                current = models.Record.objects.get(by=by_id, to=level_id)
            except ObjectDoesNotExist:
                current = models.Record()
                current.by = request.user
                current.to = current_level
                current.attempts = 0

            current.attempts += int(request.POST['attempts'])
            current.date = timezone.localtime(timezone.now())
            program = json.loads(request.POST['program'])
            score = 0
            for i in program:
                if i == 'forward' or i == 'backward':
                    score += models.move_value
                elif i == 'left' or i == 'right':
                    score += models.turn_value
                elif i == 'lo' or i == 'op':
                    score += models.loop_value

            max_score = (current_level.command_forward + current_level.command_backward) * models.move_value
            max_score += (current_level.command_right + current_level.command_left) * models.turn_value
            max_score += (current_level.command_lo + current_level.command_op) * models.loop_value

            score = max_score * 2 - score

            if not current.score or score > current.score:
                current.score = score
                current.program = program
                # TODO Maybe check if level wasn't hacked
            current.save()

            messages.success(request, "Good job! Now you are " + ordinal(
                current.ranking()) + " in " + current_level.name + " level rating.")
        else:
            try:
                current = models.Record.objects.get(to=level_id, by=by_id)
            except ObjectDoesNotExist:
                messages.error(request, "No records like this.")
                return record(request, current_level)

        return render(request, 'result.html', {'result': current})
    else:
        context = {}
        if level_id:
            try:
                current_level = models.Level.objects.get(id=level_id)
            except ObjectDoesNotExist:
                messages.error(request, "No such level yet.")
                return record(request)

            try:
                results = models.Record.objects.filter(to=current_level).order_by('score')
            except ObjectDoesNotExist:
                messages.warning(request, "None passed this level yet.")
                return level(request, current_level)

            context['level'] = current_level
        elif by_id:
            try:
                current_profile = models.User.objects.get(id=by_id)
            except ObjectDoesNotExist:
                messages.error(request, "No such user yet.")
                return record(request)

            try:
                results = models.Record.objects.filter(by=current_profile).order_by('-date')
            except ObjectDoesNotExist:
                messages.warning(request, "This user haven't passes any level yet.")
                return profile(request, by_id)

            context['profile'] = current_profile
        else:
            results = models.Record.objects.all().order_by('-date')

        context['records'] = results
        return render(request, 'results.html', context)
