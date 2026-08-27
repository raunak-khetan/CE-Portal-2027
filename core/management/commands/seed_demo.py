from django.core.management.base import BaseCommand
from django.utils.timezone import now

from core.models import City, Event


class Command(BaseCommand):
    help = "Seed demo cities and events for local testing"

    def handle(self, *args, **options):
        # Create events
        solo_events = [
            ("Solo Singing", "solo", None, None, "Showcase your solo vocals."),
            ("Solo Dance", "solo", None, None, "Freestyle solo dance performance."),
        ]

        team_events = [
            ("Street Dance Battle", "team", 4, 8, "Crew vs crew street battle."),
            ("Rock Band", "team", 3, 6, "Bring your band and rock the stage."),
        ]

        name_to_event = {}
        for name, etype, minp, maxp, desc in solo_events + team_events:
            event, _ = Event.objects.get_or_create(
                name=name,
                defaults={
                    "event_type": etype,
                    "min_participants": minp,
                    "max_participants": maxp,
                    "description": desc,
                },
            )
            # Update existing to ensure values are consistent for repeated runs
            if event.event_type != etype:
                event.event_type = etype
            event.min_participants = minp
            event.max_participants = maxp
            event.description = desc
            event.save()
            name_to_event[name] = event

        # Create cities and attach events
        demo_cities = [
            ("Guwahati", "Bhupen Hazarika, IIT Guwahati", now().date()),
            ("Delhi", "IIT Delhi Auditorium", now().date()),
            ("Mumbai", "IIT Bombay SAC", now().date()),
        ]

        for city_name, venue, date_val in demo_cities:
            city, _ = City.objects.get_or_create(
                name=city_name,
                defaults={
                    "venue": venue,
                    "time": date_val,
                    "guidelines": "General rules apply.",
                },
            )
            # Update venue/time for idempotency
            city.venue = venue
            city.time = date_val
            city.save()

            # Attach a mix of events
            attach_events = [
                name_to_event["Solo Singing"],
                name_to_event["Solo Dance"],
                name_to_event["Street Dance Battle"],
                name_to_event["Rock Band"],
            ]
            city.events.set(attach_events)
            city.save()

        self.stdout.write(self.style.SUCCESS("Seeded demo cities and events."))


