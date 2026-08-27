from django.shortcuts import render, redirect, get_object_or_404
from .models import City, Event, Head, TeamMember, Team
from .forms import RegistrationForm, TeamName, MemberForm
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from .forms import CFARegistrationStep1Form
from .models import CFARegistration
from .models import City, Event
from django.http import HttpResponse
from .models import AboutImage


def city_list(request):
    cities = City.objects.all().values('name')  # Query to get city names
    return JsonResponse(list(cities), safe=False)


def get_city_events(request, city_name):
    # Retrieve the City instance based on the slug or name
    # If using slug:
    # city = get_object_or_404(City, slug=city_name)
    # If using name:
    city = get_object_or_404(City, name=city_name)

    # Access the related events
    events = city.events.all()

    # Serialize events data
    data = {
        'time': city.time.strftime('%d %b %Y'),  # Format the date as desired
        'events': [
            {
                'name': event.name,
            }
            for event in events
        ]
    }

    return JsonResponse(data)


def prelimspage(request):
    cities = City.objects.all().prefetch_related('events')
    about_images = AboutImage.objects.all().order_by('order')

    first_reg_url = None
    for c in cities:
        first_event = c.events.first()
        if first_event:
            try:
                first_reg_url = reverse('registrationpage', args=[c.name, first_event.name])
            except Exception:
                first_reg_url = None
            break

    return render(request, 'core/home.html', {
        'cities': cities,
        'first_reg_url': first_reg_url,
        'about_images': about_images,  # ✅ Add this line
    })


def citypage(request, city_name):
    city = get_object_or_404(City, name=city_name)
    cities = City.objects.all()
    events = city.events.all()
    return render(request, 'core/compitition.html', {'events': events, 'curr_city': city, 'cities': cities})


def has_registered(email, event):
    """ Helper function to check if a user has already registered for the event. """
    return Head.objects.filter(email=email, event=event).exists()


def detailspage(request, city_name, event_name):
    city = get_object_or_404(City, name=city_name)
    event = get_object_or_404(Event, name=event_name)

    competitions = []
    cities = City.objects.prefetch_related('events').all()
    
    for city_item in cities:
        for event_item in city_item.events.all():
            # Implement the image fallback hierarchy
            image_url = ''
            if event_item.image:
                # First priority: Use the event's specific image
                image_url = event_item.image.url
            elif city_item.image:
                # Second priority: Fall back to the city's image
                image_url = city_item.image.url
            else:
                # Final fallback: Use a default static image
                # Note: We'll handle the static URL construction in the template
                image_url = 'static/core/assets/CompetitionPhoto.jpg'
            
            competitions.append({
                "city": city_item.name,
                "title": event_item.name,
                "subtitle": event_item.description,
                "date": city_item.time.strftime("%a, %d %b, %Y") if city_item.time else "No date",
                "venue": city_item.venue,
                "image": image_url,  # Now uses the fallback hierarchy
                "type": event_item.event_type.capitalize() if event_item.event_type else "N/A",
                "collab": city_item.collab
            })

    return render(request, 'core/register.html', {
        'event': event,
        'city': city,
        'competitions': competitions,  # Pass competitions for cards
        'cities': cities,
    })


def registrationpage(request, city_name, event_name):
    city = get_object_or_404(City, name=city_name)
    event = get_object_or_404(Event, name=event_name)

    # Create a formset for multiple team members
    MemberFormSet = modelformset_factory(
        TeamMember,
        form=MemberForm,
        extra=0
    )  # Use custom form to ensure radio gender without blank option

    # Always define these variables
    team_name_form = None
    team_form = None
    member_formset = None
    form = None

    if request.method == 'POST':
        if event.event_type == 'team':
            team_name_form = TeamName(request.POST)
            team_form = RegistrationForm(request.POST)
            member_formset = MemberFormSet(request.POST, prefix='members')
            print(member_formset)

            if team_name_form.is_valid() and team_form.is_valid() and member_formset.is_valid():
                # Save the team registration
                team_head = team_form.save(commit=False)
                team_head.event = event
                team_head.city = city
                team_head.save()

                team_name = team_name_form.save(commit=False)
                team_name.head = team_head
                team_name.save()

                # Save each team member
                for formset_form in member_formset:
                    if formset_form.cleaned_data:
                        member = formset_form.save(commit=False)
                        member.head = team_head
                        member.team = team_name
                        member.save()

                send_mail(
                    subject='Team Registration Successful',
                    message=f'Hello {team_head.name},\n\nYou have successfully registered your team for the event "{event.name}" in {city.name}.\n\nThank you for registering!',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[team_head.email],
                    fail_silently=False,
                )

                return render(request, 'core/thank_you.html')
        else:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                registration = form.save(commit=False)
                registration.event = event
                registration.city = city
                registration.save()

                send_mail(
                    subject='Registration Successful',
                    message=f'Hello {registration.name},\n\nYou have successfully registered for the event "{event.name}" in {city.name}.\n\nThank you for registering!',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[registration.email],
                    fail_silently=False,
                )
                return render(request, 'core/thank_you.html')
    else:
        if event.event_type == 'team':
            team_name_form = TeamName()
            team_form = RegistrationForm()
            member_formset = MemberFormSet(queryset=TeamMember.objects.none(), prefix='members')
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
            # Save the ID to session for next step
            request.session['cfa_id'] = cfa.id
            return redirect('cfa_step2')
    else:
        form = CFARegistrationStep1Form()

    return render(request, 'core/cfa_step1.html', {'form': form})


def cfa_step2_view(request):
    if request.method == 'POST':
        # Get existing CFA object
        cfa_id = request.session.get('cfa_id')
        if cfa_id:
            try:
                cfa = CFARegistration.objects.get(id=cfa_id)
                
                # Update Step 2 fields
                cfa.college_name = request.POST.get('college_name', '')
                cfa.college_designation = request.POST.get('college_designation', '')
                cfa.fest_name = request.POST.get('fest_name', '')
                cfa.fest_address = request.POST.get('fest_address', '')
                cfa.fest_dates = request.POST.get('fest_dates', '')
                cfa.number_of_days = request.POST.get('number_of_days', '')
                cfa.expected_footfall = request.POST.get('expected_footfall', '')
                cfa.social_links = request.POST.get('social_links', '')
                
                cfa.save()
                
                # Redirect to step 3
                return redirect('cfa_step3')
            except CFARegistration.DoesNotExist:
                # If CFA object doesn't exist, redirect back to step 1
                return redirect('cfa_step1')
        else:
            # If no CFA ID in session, redirect back to step 1
            return redirect('cfa_step1')

    return render(request, 'core/cfa_step2.html')


def cfa_step3(request):
    if request.method == 'POST':
        # Get existing CFA object
        cfa_id = request.session.get('cfa_id')
        if cfa_id:
            try:
                cfa = CFARegistration.objects.get(id=cfa_id)
                
                # Update Step 3 fields
                cfa.accommodation_required = request.POST.get('accommodation') == 'yes'
                cfa.event_preferences = request.POST.get('expectations', '')
                
                # Save additional fields that might be useful
                # You can add these to the model if needed
                team_size = request.POST.get('team_size', '')
                competitions = request.POST.get('competitions', '')
                
                # Combine additional info into event_preferences if needed
                additional_info = f"Team Size: {team_size}\nCompetitions: {competitions}\n\nExpectations: {request.POST.get('expectations', '')}"
                cfa.event_preferences = additional_info
                
                cfa.save()
                
                # Clear the session
                if 'cfa_id' in request.session:
                    del request.session['cfa_id']
                
                # Redirect to thank you page
                return render(request, 'core/thank_you.html')
                
            except CFARegistration.DoesNotExist:
                # If CFA object doesn't exist, redirect back to step 1
                return redirect('cfa_step1')
        else:
            # If no CFA ID in session, redirect back to step 1
            return redirect('cfa_step1')

    return render(request, 'core/cfa_step3.html')

def landing_page(request):
    return render(request, 'core/landing.html')


def test_view(request):
    return HttpResponse("Site is working!")


#bug fixes...
def home(request):
    about_images = AboutImage.objects.all().order_by('order')
    print("DEBUG: Found", about_images.count(), "AboutImage(s)")
    return render(request, 'core/home.html', {'about_images': about_images})
