from django.core.management.base import BaseCommand
from django.utils.timezone import now
from datetime import date, timedelta
from core.models import City, Event, Category


class Command(BaseCommand):
    help = "Seed test competitions across Drama, Dance, and Singing for testing registrations"

    def handle(self, *args, **options):
        self.stdout.write("Starting test data creation...")

        # 1. Categories
        cat_drama, _ = Category.objects.get_or_create(name="Drama")
        cat_dance, _ = Category.objects.get_or_create(name="Dance")
        cat_singing, _ = Category.objects.get_or_create(name="Singing")
        self.stdout.write(self.style.SUCCESS("Created/verified categories: Drama, Dance, Singing"))

        # 2. Events Definition
        events_spec = [
            {
                "name": "Halla Bol",
                "category": cat_drama,
                "event_type": "team",
                "min_participants": 8,
                "max_participants": 20,
                "description": "The flagship street play competition of Alcheringa. Bring issues that matter to the streets with raw energy, powerful voices, and impactful beats.",
                "days_to_deadline": 45,
                "days_to_event": 60,
                "image": "image_uploads/event_pic/Frame_6356534.png"
            },
            {
                "name": "Voice of Alcheringa",
                "category": cat_singing,
                "event_type": "solo",
                "min_participants": None,
                "max_participants": None,
                "description": "The premier solo vocal championship. Showcase your vocal range, control, and melody across Indian and Western music forms.",
                "days_to_deadline": 40,
                "days_to_event": 55,
                "image": "image_uploads/event_pic/Frame_6356534_1.png"
            },
            {
                "name": "Nataraj",
                "category": cat_dance,
                "event_type": "solo",
                "min_participants": None,
                "max_participants": None,
                "description": "Solo dance competition celebrating expressions, rhythm, and passion across classical, contemporary, and freestyle forms.",
                "days_to_deadline": 35,
                "days_to_event": 50,
                "image": "image_uploads/event_pic/Electric_heels.png"
            },
            {
                "name": "Electric Heels",
                "category": cat_dance,
                "event_type": "team",
                "min_participants": 4,
                "max_participants": 12,
                "description": "Western and street group dance showdown. Synchronized moves, high-octane choreography, and relentless energy on stage.",
                "days_to_deadline": 50,
                "days_to_event": 70,
                "image": "image_uploads/event_pic/electric-heels.png"
            },
            {
                "name": "Theatrix",
                "category": cat_drama,
                "event_type": "solo",
                "min_participants": None,
                "max_participants": None,
                "description": "Mono-acting and monologue competition. One actor, one stage, infinite expressions and emotional depth.",
                "days_to_deadline": 30,
                "days_to_event": 45,
                "image": "image_uploads/event_pic/Frame_6356534.png"
            },
            {
                "name": "Sargam",
                "category": cat_singing,
                "event_type": "team",
                "min_participants": 3,
                "max_participants": 8,
                "description": "Group singing and vocal ensemble competition. Harmonize voices with rich acoustic layers and melodic excellence.",
                "days_to_deadline": 42,
                "days_to_event": 62,
                "image": "image_uploads/event_pic/Frame_6356534_1.png"
            },
            {
                "name": "Navras",
                "category": cat_drama,
                "event_type": "team",
                "min_participants": 6,
                "max_participants": 15,
                "description": "One-act stage play competition exploring the nine human rasas with gripping narratives and theatrical brilliance.",
                "days_to_deadline": 55,
                "days_to_event": 75,
                "image": "image_uploads/event_pic/Frame_6356534.png"
            }
        ]

        created_events = {}
        for spec in events_spec:
            event, created = Event.objects.update_or_create(
                name=spec["name"],
                defaults={
                    "category": spec["category"],
                    "event_type": spec["event_type"],
                    "min_participants": spec["min_participants"],
                    "max_participants": spec["max_participants"],
                    "description": spec["description"],
                    "deadline": now().date() + timedelta(days=spec["days_to_deadline"]),
                    "event_date": now().date() + timedelta(days=spec["days_to_event"]),
                    "image": spec["image"]
                }
            )
            created_events[spec["name"]] = event
            status = "Created" if created else "Updated"
            self.stdout.write(f"{status} event: {event.name} ({event.category.name} - {event.event_type})")

        # 3. Cities & Mapping (2-3 competitions per city)
        cities_spec = [
            {
                "name": "Delhi",
                "venue": "Siri Fort Auditorium, August Kranti Marg",
                "state": "Delhi",
                "image": "image_uploads/city_pic/mumbai-mall.png",
                "events": ["Halla Bol", "Voice of Alcheringa", "Electric Heels"]
            },
            {
                "name": "Mumbai",
                "venue": "Jio World Convention Centre, BKC",
                "state": "Maharashtra",
                "image": "image_uploads/city_pic/mumbai-mall.png",
                "events": ["Voice of Alcheringa", "Nataraj", "Navras"]
            },
            {
                "name": "Bangalore",
                "venue": "Palace Grounds, Jayamahal Road",
                "state": "Karnataka",
                "image": "image_uploads/city_pic/mumbai-mall.png",
                "events": ["Electric Heels", "Sargam", "Theatrix"]
            },
            {
                "name": "Guwahati",
                "venue": "IIT Guwahati Campus, Amingaon",
                "state": "Assam",
                "image": "image_uploads/city_pic/guwahati-mall.png",
                "events": ["Halla Bol", "Voice of Alcheringa", "Nataraj"]
            },
            {
                "name": "Kolkata",
                "venue": "Science City Auditorium, J.B.S. Haldane Avenue",
                "state": "West Bengal",
                "image": "image_uploads/city_pic/mumbai-mall.png",
                "events": ["Sargam", "Navras", "Electric Heels"]
            }
        ]

        for c_spec in cities_spec:
            city, created = City.objects.update_or_create(
                name=c_spec["name"],
                defaults={
                    "venue": c_spec["venue"],
                    "state": c_spec["state"],
                    "time": now().date() + timedelta(days=60),
                    "guidelines": f"Welcome to Alcheringa prelims in {c_spec['name']}! Report to the venue 1 hour prior to event start time. Carry valid college ID cards.",
                    "image": c_spec["image"],
                    "collab": False
                }
            )
            mapped_events = [created_events[ename] for ename in c_spec["events"] if ename in created_events]
            city.events.set(mapped_events)
            self.stdout.write(f"Configured city: {city.name} with {len(mapped_events)} events: {', '.join(c_spec['events'])}")

        self.stdout.write(self.style.SUCCESS("\nAll test events and cities successfully seeded!"))
