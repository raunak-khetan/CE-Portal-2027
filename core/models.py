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
    deadline = models.DateField(null=True, blank=True, verbose_name="Registration Deadline")

    @property
    def registration_deadline(self):
        return self.deadline

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('solo', 'Solo'),
        ('team', 'Team'),
    ]

    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events'
    )
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
    
    @property
    def registration_deadline(self):
        return self.deadline

    def __str__(self):
        return self.name


class CityEventConfig(models.Model):
    """
    Controls per-city-per-event registration status AND dates.
    Create one record for each (city, event) pair where you want to
    override the defaults. If no record exists the registration
    is treated as open and the global Event date is used.
    """
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='event_configs')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='city_configs')
    is_registration_open = models.BooleanField(
        default=True,
        verbose_name="Registration Open",
        help_text="Uncheck to close registration for this event in this city only. Other cities are not affected."
    )
    event_date = models.DateField(
        null=True, blank=True,
        verbose_name="City-Specific Event Date",
        help_text="Override the global event date for this competition in this city only. Leave blank to use the event's default date."
    )
    deadline = models.DateField(
        null=True, blank=True,
        verbose_name="City-Specific Registration Deadline",
        help_text="Override the global registration deadline for this competition in this city only. Leave blank to use the event's default deadline."
    )

    class Meta:
        unique_together = ('city', 'event')
        verbose_name = "City-Event Registration Config"
        verbose_name_plural = "City-Event Registration Configs"

    def get_event_date(self):
        """Returns city-specific date if set, otherwise falls back to the global Event date."""
        return self.event_date or self.event.event_date

    def get_deadline(self):
        """Returns city-specific deadline if set, otherwise falls back to the global Event deadline."""
        return self.deadline or self.event.deadline

    def __str__(self):
        status = "Open" if self.is_registration_open else "Closed"
        date_str = f" | Date: {self.event_date}" if self.event_date else ""
        return f"{self.event.name} in {self.city.name} — {status}{date_str}"


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
        ('P', 'Prefer not to say'),
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