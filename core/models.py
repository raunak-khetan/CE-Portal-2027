from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.timezone import now

# Centralized choices for graduating year
YEAR_CHOICES = [(y, str(y)) for y in range(2025, 2032)]  # 2025..2031
class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    events = models.ManyToManyField('Event', related_name='cities')
    venue = models.CharField(max_length=100, default="None")
    time = models.DateField(null=True, blank=True)
    guidelines = models.TextField(default="None")
    image = models.ImageField(
        upload_to="image_uploads/city_pic/",null=True)
    state = models.CharField(max_length=100,default='None')
    collab = models.BooleanField(null=True,default=False)

    def __str__(self):
        return self.name

class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('solo', 'Solo'),
        ('team', 'Team'),
    ]

    name = models.CharField(max_length=200)
    event_type = models.CharField(max_length=10, choices=EVENT_TYPE_CHOICES, default='solo')
    min_participants = models.PositiveIntegerField(null=True, blank=True)
    max_participants = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(default= "none")

    deadline = models.DateField(null=True, blank=True)
    event_date = models.DateField(null=True, blank=True)

    image = models.ImageField(
        upload_to="image_uploads/event_pic/",null=True, blank=True,help_text="Upload an image representing this event"
    )

    def clean(self):
        if self.event_type == 'team':
            # Require minimum participants; allow max to be None to indicate no limit
            if self.min_participants is None:
                raise ValidationError("Min participants is required for team events.")

            # If max is provided, ensure it is not less than min
            if (
                self.max_participants is not None
                and self.min_participants is not None
                and self.min_participants > self.max_participants
            ):
                raise ValidationError("Min participants cannot be greater than Max participants.")

        elif self.event_type == 'solo':
            if self.min_participants or self.max_participants:
                raise ValidationError("Min and Max participants should be empty for solo events.")
    
    def __str__(self):
        return self.name


class Head(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others'),
        ('P', 'Prefer not to say')
    ]
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=15)
    email = models.EmailField()
    institute_name = models.CharField(max_length=200)
    year_of_passing = models.IntegerField(choices=YEAR_CHOICES)
    program_enrolled = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    DISABILITY_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]
    is_disabled = models.CharField(max_length=1, choices=DISABILITY_CHOICES, default='N')
 
    solo = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.event.event_type == 'solo':
            self.solo = True
        else:
            self.solo = False

        super(Head, self).save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.name}"
    
class Team(models.Model):

    head = models.OneToOneField(Head, on_delete=models.CASCADE, related_name='team')
    team_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Team: {self.team_name} (Head: {self.head.name})"
    
class TeamMember(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others'),
    ]
    head = models.ForeignKey(Head, on_delete=models.CASCADE, related_name='head_members')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_members')
    name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=15)
    email = models.EmailField()
    institute_name = models.CharField(max_length=200)
    year_of_passing = models.IntegerField(choices=YEAR_CHOICES)
    program_enrolled = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    DISABILITY_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]
    is_disabled = models.CharField(max_length=1, choices=DISABILITY_CHOICES, default='N')
    
    def __str__(self):
        return f"{self.name} ({self.head.team.team_name} - {self.head.event.name})"


# core/models.py (Append at the bottom), done by ASHISH

class CFARegistration(models.Model):
    # Step 1
    full_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    alternate_phone = models.CharField(max_length=20, blank=True, null=True)
    college_id_card_link = models.URLField()

    # Step 2
    college_name = models.CharField(max_length=200)
    college_designation = models.CharField(max_length=100)
    fest_name = models.CharField(max_length=200)
    fest_address = models.TextField()
    fest_dates = models.CharField(max_length=100)
    number_of_days = models.CharField(max_length=50)
    expected_footfall = models.CharField(max_length=100)
    social_links = models.TextField()

    # Step 3
    accommodation_required = models.BooleanField(default=False)
    event_preferences = models.TextField(blank=True, null=True)

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


#bug fixes...
class AboutImage(models.Model):
    image = models.ImageField(upload_to='about_images/')
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"About Image {self.id} (Order: {self.order})"