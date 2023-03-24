from django.shortcuts import render, redirect, get_object_or_404
from expenditure.forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse_lazy
from expenditure.models.user import *
from expenditure.helpers import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from expenditure.email_manager import EmailSender


@login_prohibited
def sign_up(request):
    if request.method == 'POST':
        # request.POST contains dictionary with all of the data
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            user.points += 10
            user.save()
            EmailSender().send_welcome_email(user)
            create_default_categories(user)
            return redirect('feed')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})


@login_prohibited
def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        next = request.POST.get('next') or ''
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                point, created = DailyPoint.objects.get_or_create(
                    user=user, date=date.today())  # point not in use?
                if created:
                    user.add_login_points()
                    check_league(request)
                    messages.success(
                        request, 'Thank you for logging in today. You have earned 1 point!')
                redirect_url = next or 'feed'
                return redirect(redirect_url)
        # Add error message here
        messages.add_message(request, messages.ERROR,
                             "The credentials provided were invalid!")
    else:
        next = request.GET.get('next') or ''
    form = LogInForm()

    context = {
        'form': form,
        'next': next,
        'messages': messages.get_messages(request),
    }
    return render(request, 'log_in.html', context)


def log_out(request):
    logout(request)
    return redirect('home')


@login_required
def leaderboard(request):
    check_league(request)
    num_top_users = 10

    users = User.objects
    user_overall_place = users.filter(
        points__gt=request.user.points).count() + 1

    users = users.filter(
        league_status=request.user.league_status).order_by('-points')
    user_place = users.filter(points__gt=request.user.points).count() + 1

    # if (users.filter(points__gte=request.user.points).last().points == request.user.points):
    #     user_overall_place += 1
    #     user_place += 1

    pedestal = []
    for i in range(3):
        try:
            pedestal.append(users[i])
        except IndexError:
            pedestal.append('None')

    context = {
        'num_top_users': num_top_users,
        'users': users[:num_top_users],
        'user_place': user_place,
        'user_overall_place': user_overall_place,
        'pedestal': pedestal,
        'first_place': pedestal[0],
        'second_place': pedestal[1],
        'third_place': pedestal[2],
        'messages': messages.get_messages(request),
    }
    return render(request, 'leaderboard.html', context=context)


# global variable
search = ''

# from django.shortcuts import render, redirect
# from .models import ListItem
#
# def list_view(request):
#    items = ListItem.objects.all()
#    if request.method == 'POST':
#        item_id = request.POST.get('item_id')
#        item = ListItem.objects.get(pk=item_id)
#        item.status = not item.status
#        item.save()
#        return redirect('list_view')
#

# <ul>
# {% for item in items %}
#    <li>{{ item.name }} <form method="post">
#        {% csrf_token %}
#        <button type="submit" name="item_id" value="{{ item.id }}">
#        {% if item.status %}Mark as incomplete{% else %}Mark as complete{% endif %}
#        </button>
#    </form></li>
# {% endfor %}
# </ul>


@login_required
def search_friends(request):
    global search
    current_user = request.user
    if request.method == "POST":
        form = FriendSearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data.get('search')
    else:
        form = FriendSearchForm()
    results = []
    if search != '':
        results = User.objects.filter(first_name__contains=search).exclude(
            id=current_user.id) | User.objects.filter(last_name__contains=search).exclude(id=current_user.id)

    context = {
        'form': form,
        'search_results': results,
    }
    return render(request, 'search_friends.html', context)


@login_required
def show_friends_profile(request, id):
    results = User.objects.get(id=id)
    template = loader.get_template('friends_profile.html')
    context = {
        'results': results,
    }
    return HttpResponse(template.render(context, request))


@login_required
def follow_toggle(request):
    current_user = request.user
    print(f'===========')
    results = search_friends(request)
    print(f'====={results}======')
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        searched_user = User.objects.get(pk=item_id)
        current_user.toggle_follow(searched_user)
        print(f'====={searched_user.first_name}======')
        print(f'== ==={current_user.first_name} - -{searched_user.first_name} - ->{current_user.is_following(searched_user)} == == ==')

        request.session['is_following'] = current_user.is_following(
            searched_user)
        return redirect('search_friends')
    return render(request, 'search_friends.html', {'search_results': results})
#    current_user = request.user
#    searched_user = get_object_or_404(User, id=request_id)
#    current_user.toggle_follow(searched_user)
#    print(f'{current_user.is_following(searched_user)}=============')
#    if not current_user.is_following(searched_user):
#        current_user.points += 1
#        current_user.save()
#    request.session['is_following'] = current_user.is_following(searched_user)
#    return redirect('search_friends')


@login_required
def toggle_privacy(request):
    current_user = request.user
    if current_user.toggle_privacy == 'ON':
        current_user.is_private = False
        current_user.toggle_privacy = 'OFF'
        current_user.save()
    else:
        current_user.toggle_privacy = 'ON'
        current_user.is_private = True
        current_user.save()
    return redirect('settings')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('user_profile')

    else:
        user_form = UpdateUserForm(instance=request.user)

    return render(request, 'profile.html', {'user_form': user_form})


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_message = 'Successfully changed password'
    success_url = reverse_lazy("user_profile")


@login_prohibited
def forgot_password(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
    else:
        form = EmailForm()
    return render(request, 'forgot_password.html', {'form': form})


@login_required
def delete_account(request):
    user_pk = request.user.pk
    logout(request)
    User = get_user_model()
    User.objects.filter(pk=user_pk).delete()
    return redirect('home')


class PasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'


class PasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_sent.html'


class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_form.html'


class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'
