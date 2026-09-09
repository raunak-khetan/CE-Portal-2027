import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import transaction
from django.forms import modelformset_factory
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import CFARegistrationStep1Form, MemberForm, RegistrationForm, TeamName
from .models import (
    AboutImage,
    CFARegistration,
    Category,
    City,
    Event,
    Head,
    Team,
    TeamMember,
)

logger = logging.getLogger(__name__)


def city_list(request):
    cities = City.objects.all().values('name')  # Query to get city names
    return JsonResponse(list(cities), safe=False)


def get_city_events(request, city_name):
    city = get_object_or_404(City, name=city_name)
    events = city.events.all()

    data = {
        'time': city.time.strftime('%d %b %Y') if city.time else None,
        'events': [{'name': event.name} for event in events],
    }

    return JsonResponse(data)


def prelimspage(request):
    cities = City.objects.all().prefetch_related('events')
    about_images = AboutImage.objects.all().order_by('order')
    categories = Category.objects.all()

    first_reg_url = None
    for c in cities:
        first_event = c.events.first()
        if first_event:
            try:
                first_reg_url = reverse('registrationpage', args=[c.name, first_event.name])
            except Exception:
                logger.exception("Could not reverse registrationpage for %s / %s", c.name, first_event.name)
                first_reg_url = None
            break

    return render(request, 'core/home.html', {
        'cities': cities,
        'first_reg_url': first_reg_url,
        'about_images': about_images,
        'categories': categories,
    })


def citypage(request, city_name):
    city = get_object_or_404(City, name=city_name)
    cities = City.objects.all()
    events = city.events.all()
    return render(request, 'core/compitition.html', {
        'events': events,
        'curr_city': city,
        'cities': cities,
    })


def has_registered(email, event):
    """Check whether this email has already registered (as a team head or solo entrant) for this event."""
    if not email:
        return False
    return Head.objects.filter(email__iexact=email, event=event).exists()


def detailspage(request, city_name, event_name):
    city = get_object_or_404(City, name=city_name)
    event = get_object_or_404(Event, name=event_name)

    competitions = []
    cities = City.objects.prefetch_related('events').all()

    for city_item in cities:
        for event_item in city_item.events.all():
            if event_item.image:
                image_url = event_item.image.url
            elif city_item.image:
                image_url = city_item.image.url
            else:
                image_url = 'static/core/assets/CompetitionPhoto.jpg'

            competitions.append({
                "city": city_item.name,
                "title": event_item.name,
                "subtitle": event_item.description,
                "date": city_item.time.strftime("%a, %d %b, %Y") if city_item.time else "No date",
                "venue": city_item.venue,
                "image": image_url,
                "type": event_item.event_type.capitalize() if event_item.event_type else "N/A",
                "collab": city_item.collab,
            })

    return render(request, 'core/register.html', {
        'event': event,
        'city': city,
        'competitions': competitions,
        'cities': cities,
    })

def _build_member_formset(event, data=None):
    min_members = max(0, (event.min_participants or 1) - 1)
    max_members = (event.max_participants - 1) if event.max_participants else None

    MemberFormSet = modelformset_factory(
        TeamMember,
        form=MemberForm,
        extra=0,
        min_num=min_members,
        max_num=max_members,
        validate_min=True,
        validate_max=True,
    )

    kwargs = {'prefix': 'members', 'queryset': TeamMember.objects.none()}
    if data is not None:
        return MemberFormSet(data, **kwargs)
    return MemberFormSet(**kwargs)


def _send_confirmation_email(name, email, event, city, is_team=False):
    """
    Send the registration confirmation email. Returns True if it sent
    successfully, False otherwise. The caller decides what to do with
    that — currently, a failed send blocks the registration from being
    saved at all.
    """
    subject = 'Team Registration Successful' if is_team else 'Registration Successful'
    verb = 'registered your team' if is_team else 'registered'

    message = (
        f'Hello {name},\n\n'
        f'You have successfully {verb} for the event "{event.name}" in {city.name}.\n\n'
        'Thank you for registering!'
    )

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
        return True
    except Exception:
        logger.exception(
            "Confirmation email failed to send (email=%s, event=%s, city=%s)",
            email, event.name, city.name,
        )
        return False


@transaction.atomic
def _save_team_registration(team_form, team_name_form, member_formset, event, city):
    """All-or-nothing save of the team head, team name, and every member."""
    team_head = team_form.save(commit=False)
    team_head.event = event
    team_head.city = city
    team_head.save()

    team = team_name_form.save(commit=False)
    team.head = team_head
    team.save()

    for member_form in member_formset:
        if member_form.cleaned_data:
            member = member_form.save(commit=False)
            member.head = team_head
            member.team = team
            member.save()

    return team_head


def registrationpage(request, city_name, event_name):
    city = get_object_or_404(City, name=city_name)
    event = get_object_or_404(Event, name=event_name)

    team_name_form = None
    team_form = None
    member_formset = None
    form = None

    if request.method == 'POST':

        if event.event_type == 'team':
            team_name_form = TeamName(request.POST)
            team_form = RegistrationForm(request.POST)
            member_formset = _build_member_formset(event, data=request.POST)

            if (
                team_name_form.is_valid()
                and team_form.is_valid()
                and member_formset.is_valid()
            ):
                email = team_form.cleaned_data.get('email')
                name = team_form.cleaned_data.get('name')

                if has_registered(email, event):
                    team_form.add_error('email', 'This email has already registered for this event.')
                elif not _send_confirmation_email(name, email, event, city, is_team=True):
                    team_form.add_error(
                        None,
                        'We could not send a confirmation email right now, so your registration '
                        'was not saved. Please try again in a few minutes.'
                    )
                else:
                    _save_team_registration(team_form, team_name_form, member_formset, event, city)
                    return render(request, 'core/thank_you.html')

        else:
            form = RegistrationForm(request.POST)

            if form.is_valid():
                email = form.cleaned_data.get('email')
                name = form.cleaned_data.get('name')

                if has_registered(email, event):
                    form.add_error('email', 'This email has already registered for this event.')
                elif not _send_confirmation_email(name, email, event, city, is_team=False):
                    form.add_error(
                        None,
                        'We could not send a confirmation email right now, so your registration '
                        'was not saved. Please try again in a few minutes.'
                    )
                else:
                    registration = form.save(commit=False)
                    registration.event = event
                    registration.city = city
                    registration.save()
                    return render(request, 'core/thank_you.html')

    else:
        if event.event_type == 'team':
            team_name_form = TeamName()
            team_form = RegistrationForm()
            member_formset = _build_member_formset(event)
        else:
            form = RegistrationForm()

    return render(request, 'core/register_form.html', {
        'form': form,
        'team_form': team_form,
        'team_name_form': team_name_form,
        'event': event,
        'city': city,
        'member_formset': member_formset,
        'min_participants': event.min_participants,
        'max_participants': event.max_participants,
    })

def cfa_register_step1(request):
    if request.method == 'POST':
        form = CFARegistrationStep1Form(request.POST)
        if form.is_valid():
            cfa = form.save(commit=False)
            cfa.save()
            request.session['cfa_id'] = cfa.id
            return redirect('cfa_step2')
    else:
        form = CFARegistrationStep1Form()

    return render(request, 'core/cfa_step1.html', {'form': form})


def cfa_step2_view(request):
    if request.method == 'POST':
        cfa_id = request.session.get('cfa_id')
        if not cfa_id:
            return redirect('cfa_step1')

        try:
            cfa = CFARegistration.objects.get(id=cfa_id)
        except CFARegistration.DoesNotExist:
            return redirect('cfa_step1')

        cfa.college_name = request.POST.get('college_name', '')
        cfa.college_designation = request.POST.get('college_designation', '')
        cfa.fest_name = request.POST.get('fest_name', '')
        cfa.fest_address = request.POST.get('fest_address', '')
        cfa.fest_dates = request.POST.get('fest_dates', '')
        cfa.number_of_days = request.POST.get('number_of_days', '')
        cfa.expected_footfall = request.POST.get('expected_footfall', '')
        cfa.social_links = request.POST.get('social_links', '')
        cfa.save()

        return redirect('cfa_step3')

    return render(request, 'core/cfa_step2.html')


def cfa_step3(request):
    if request.method == 'POST':
        cfa_id = request.session.get('cfa_id')
        if not cfa_id:
            return redirect('cfa_step1')

        try:
            cfa = CFARegistration.objects.get(id=cfa_id)
        except CFARegistration.DoesNotExist:
            return redirect('cfa_step1')

        cfa.accommodation_required = request.POST.get('accommodation') == 'yes'

        team_size = request.POST.get('team_size', '')
        competitions = request.POST.get('competitions', '')
        expectations = request.POST.get('expectations', '')

        cfa.event_preferences = (
            f"Team Size: {team_size}\n"
            f"Competitions: {competitions}\n\n"
            f"Expectations: {expectations}"
        )
        cfa.save()

        request.session.pop('cfa_id', None)

        return render(request, 'core/thank_you.html')

    return render(request, 'core/cfa_step3.html')


def landing_page(request):
    return render(request, 'core/landing.html')


def test_view(request):
    return HttpResponse("Site is working!")


def home(request):
    about_images = AboutImage.objects.all().order_by('order')
    return render(request, 'core/home.html', {'about_images': about_images})