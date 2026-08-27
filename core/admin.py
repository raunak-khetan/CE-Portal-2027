from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ExportActionMixin
from .models import City, Event, Head, Team, TeamMember
from .models import CFARegistration
from .models import AboutImage

# Define resources for each model you want to export
class CityResource(resources.ModelResource):
    class Meta:
        model = City
        fields = ('id', 'name', 'venue', 'state', 'time', 'guidelines','collab')

class EventResource(resources.ModelResource):
    class Meta:
        model = Event
        fields = ('id', 'name', 'event_type', 'description', 'min_participants', 
                 'max_participants', 'deadline', 'event_date')

class HeadResource(resources.ModelResource):
    class Meta:
        model = Head
        fields = ('id', 'name', 'email', 'phone_no', 'gender', 'institute_name', 
                 'year_of_passing', 'program_enrolled', 'event__name', 'city__name', 
                 'is_disabled', 'solo')

class TeamResource(resources.ModelResource):
    class Meta:
        model = Team
        fields = ('id', 'team_name', 'head__name', 'head__email', 'created_at')

class TeamMemberResource(resources.ModelResource):
    class Meta:
        model = TeamMember
        fields = ('id', 'name', 'email', 'phone_no', 'gender', 'institute_name', 
                 'year_of_passing', 'program_enrolled', 'head__name', 'team__team_name', 
                 'is_disabled')

class CFARegistrationResource(resources.ModelResource):
    class Meta:
        model = CFARegistration
        fields = ('id', 'full_name', 'age', 'email', 'phone_number', 'alternate_phone',
                 'college_name', 'college_designation', 'fest_name', 'fest_address',
                 'fest_dates', 'number_of_days', 'expected_footfall', 'social_links',
                 'accommodation_required', 'event_preferences', 'submitted_at')

# Inline classes remain the same
class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1
    raw_id_fields = ('head',)

class EventInline(admin.TabularInline):
    model = City.events.through
    extra = 1
    autocomplete_fields = ['event']

# Updated admin classes with export functionality
@admin.register(City)
class CityAdmin(ImportExportModelAdmin):
    resource_class = CityResource
    list_display = ('name', 'venue', 'time', 'state', 'collab')
    search_fields = ('name', 'venue', 'state')
    list_filter = ('state', 'time')
    inlines = [EventInline]

    fieldsets = (
        (None, {
            'fields': ('name', 'venue', 'state', 'time', 'image','collab')
        }),
        ('Details', {
            'fields': ('guidelines',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Event)
class EventAdmin(ImportExportModelAdmin):
    resource_class = EventResource
    list_display = ('name', 'event_type', 'min_participants', 'max_participants', 'deadline', 'event_date')
    list_filter = ('event_type', 'deadline', 'event_date')
    search_fields = ('name', 'description')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'event_type', 'description')
        }),
        ('Visual Content', {
            'fields': ('image',),
            'description': 'Upload an image to represent this event'
        }),
        ('Participant Requirements', {
            'fields': ('min_participants', 'max_participants'),
            'description': 'Leave blank for solo events'
        }),
        ('Important Dates', {
            'fields': ('deadline', 'event_date')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.event_type == 'solo':
            return ['min_participants', 'max_participants']
        return []

@admin.register(Head)
class HeadAdmin(ImportExportModelAdmin):
    resource_class = HeadResource
    list_display = ('name', 'event', 'city', 'email', 'phone_no', 'institute_name', 'year_of_passing', 'solo')
    list_filter = ('gender', 'city', 'event', 'year_of_passing', 'is_disabled', 'solo')
    search_fields = ('name', 'email', 'phone_no', 'institute_name')
    raw_id_fields = ('event', 'city')
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone_no', 'gender', 'is_disabled')
        }),
        ('Academic Information', {
            'fields': ('institute_name', 'year_of_passing', 'program_enrolled')
        }),
        ('Event Information', {
            'fields': ('event', 'city', 'solo')
        }),
    )

@admin.register(Team)
class TeamAdmin(ImportExportModelAdmin):
    resource_class = TeamResource
    list_display = ('team_name', 'head', 'created_at')
    search_fields = ('team_name', 'head__name')
    list_filter = ('created_at',)
    raw_id_fields = ('head',)
    inlines = [TeamMemberInline]

@admin.register(TeamMember)
class TeamMemberAdmin(ImportExportModelAdmin):
    resource_class = TeamMemberResource
    list_display = ('name', 'head', 'team', 'phone_no', 'email', 'gender', 'institute_name', 'year_of_passing', 'program_enrolled', 'is_disabled')
    list_filter = ('gender', 'year_of_passing', 'is_disabled')
    search_fields = ('name', 'phone_no', 'email', 'head__name', 'team__team_name', 'institute_name')
    raw_id_fields = ('head', 'team')
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone_no', 'gender', 'is_disabled')
        }),
        ('Academic Information', {
            'fields': ('institute_name', 'year_of_passing', 'program_enrolled')
        }),
        ('Team Information', {
            'fields': ('head', 'team')
        }),
    )

@admin.register(CFARegistration)
class CFARegistrationAdmin(ImportExportModelAdmin):
    resource_class = CFARegistrationResource
    list_display = ('full_name', 'email', 'phone_number', 'college_name', 'fest_name', 'submitted_at')
    search_fields = ('full_name', 'email', 'college_name', 'fest_name')
    list_filter = ('college_designation', 'accommodation_required', 'submitted_at')
    readonly_fields = ('submitted_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('full_name', 'age', 'email', 'phone_number', 'alternate_phone', 'college_id_card_link')
        }),
        ('College Information', {
            'fields': ('college_name', 'college_designation')
        }),
        ('Fest Information', {
            'fields': ('fest_name', 'fest_address', 'fest_dates', 'number_of_days', 'expected_footfall', 'social_links')
        }),
        ('Additional Details', {
            'fields': ('accommodation_required', 'event_preferences')
        }),
        ('Timestamps', {
            'fields': ('submitted_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(AboutImage)
class AboutImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'image']
    ordering = ['order']