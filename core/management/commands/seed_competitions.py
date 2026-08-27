from django.core.management.base import BaseCommand
from django.utils.timezone import now
from datetime import date, timedelta
import random

from core.models import City, Event


class Command(BaseCommand):
    help = "Seed diverse competitions with different venues, types, and dates"

    def handle(self, *args, **options):
        # Clear existing data
        Event.objects.all().delete()
        City.objects.all().delete()
        
        self.stdout.write("Cleared existing data...")

        # Create diverse events
        events_data = [
            # Solo Events
            ("Classical Vocal", "solo", None, None, "Traditional Indian classical vocal performance showcasing ragas and talas."),
            ("Contemporary Dance", "solo", None, None, "Modern dance forms including contemporary, jazz, and lyrical styles."),
            ("Poetry Slam", "solo", None, None, "Spoken word poetry performance with original compositions."),
            ("Instrumental Solo", "solo", None, None, "Solo instrumental performance on any classical or western instrument."),
            ("Stand-up Comedy", "solo", None, None, "Original stand-up comedy routine with clean humor."),
            
            # Team Events
            ("Fusion Band", "team", 4, 8, "Multi-genre fusion band combining classical and contemporary music."),
            ("Dance Crew", "team", 6, 12, "Group dance performance with synchronized choreography."),
            ("Theatre Ensemble", "team", 8, 15, "Dramatic performance with acting, dialogue, and stage presence."),
            ("Acapella Group", "team", 6, 10, "Vocal harmony group performing without instrumental accompaniment."),
            ("Street Art Collective", "team", 3, 6, "Collaborative street art and graffiti creation."),
        ]

        # Create events
        name_to_event = {}
        for name, etype, minp, maxp, desc in events_data:
            event = Event.objects.create(
                name=name,
                event_type=etype,
                min_participants=minp,
                max_participants=maxp,
                description=desc,
                deadline=now().date() + timedelta(days=random.randint(30, 90)),
                event_date=now().date() + timedelta(days=random.randint(60, 120))
            )
            name_to_event[name] = event
            self.stdout.write(f"Created event: {name}")

        # Create diverse cities with different venues and dates
        cities_data = [
            ("Mumbai", "Jio World Convention Centre, BKC", "Maharashtra", "2025-03-15"),
            ("Delhi", "Siri Fort Auditorium, South Delhi", "Delhi", "2025-03-22"),
            ("Bangalore", "Palace Grounds, Race Course Road", "Karnataka", "2025-04-05"),
            ("Chennai", "Chennai Trade Centre, Nandambakkam", "Tamil Nadu", "2025-04-12"),
            ("Kolkata", "Science City Auditorium, Salt Lake", "West Bengal", "2025-04-19"),
            ("Hyderabad", "HICC, HITEC City", "Telangana", "2025-04-26"),
            ("Pune", "Balmohan Vidyamandir, Shivajinagar", "Maharashtra", "2025-05-03"),
            ("Ahmedabad", "Gujarat High Court Auditorium", "Gujarat", "2025-05-10"),
            ("Jaipur", "Birla Auditorium, Statue Circle", "Rajasthan", "2025-05-17"),
            ("Lucknow", "Gomti Nagar Convention Centre", "Uttar Pradesh", "2025-05-24"),
        ]

        # Create cities
        for city_name, venue, state, date_str in cities_data:
            event_date = date.fromisoformat(date_str)
            city = City.objects.create(
                name=city_name,
                venue=venue,
                time=event_date,
                state=state,
                guidelines=f"General competition rules apply for {city_name}. Please check individual event guidelines.",
                image="image_uploads/city_pic/Frame.png"  # Default image
            )
            
            # Assign 3-4 random events to each city
            num_events = random.randint(3, 4)
            selected_events = random.sample(list(name_to_event.values()), num_events)
            city.events.set(selected_events)
            
            self.stdout.write(f"Created city: {city_name} with {num_events} events")

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully seeded {len(events_data)} events across {len(cities_data)} cities!"
            )
        )
        
        # Display summary
        self.stdout.write("\nCompetition Summary:")
        self.stdout.write("=" * 50)
        
        for city in City.objects.all():
            self.stdout.write(f"\n{city.name}, {city.state}")
            self.stdout.write(f"Venue: {city.venue}")
            self.stdout.write(f"Date: {city.time.strftime('%B %d, %Y')}")
            self.stdout.write("Events:")
            for event in city.events.all():
                event_type = "Team" if event.event_type == "team" else "Solo"
                participants = f"({event.min_participants}-{event.max_participants} members)" if event.event_type == "team" else ""
                self.stdout.write(f"  • {event.name} - {event_type} {participants}")
