import os
import sys
import django

# Add the api directory to Python path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# Setup Django environment - Note the settings path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nvdnew.settings.dev')
django.setup()

from nvdagen.models import Business, Listing, Sponsor, TeamMember, Program, Participant
from scripts.factories import (
    BusinessFactory,
    ListingFactory,
    SponsorFactory,
    TeamMemberFactory,
    ProgramFactory,
    ParticipantFactory
)



def print_sample_objects(objects, model_name, sample_count=3):
    """Generic function to print fields from model instances"""
    print(f"\n{'='*60}")
    print(f"Sample {model_name} objects:")
    print(f"{'='*60}")
    
    for i, obj in enumerate(objects[:sample_count], 1):
        print(f"\n{model_name} {i}:")
        # Get all field names from the model
        fields = [f.name for f in obj._meta.fields]
        
        for field_name in fields:
            value = getattr(obj, field_name)
            # Truncate long text fields
            if isinstance(value, str) and len(value) > 60:
                value = value[:60] + "..."
            print(f"  {field_name}: {value}")
    
    print(f"\nTotal {model_name} created: {len(objects)}")



def clear_existing_data():
    """Delete all existing test data"""
    # print("Clearing existing data...")
    # # Clear in reverse order of dependencies
    # Participant.objects.all().delete()
    # Program.objects.all().delete()
    # Listing.objects.all().delete()
    # TeamMember.objects.all().delete()
    # Sponsor.objects.all().delete()
    # Business.objects.all().delete()
    # print("Data cleared.")
    pass


def create_businesses(count=10):
    """Create N businesses"""
    print(f"Creating {count} businesses...")
    # businesses = BusinessFactory.create_batch(count)
    businesses = BusinessFactory.build_batch(count)
    print(f"Created {len(businesses)} businesses.")
    print_sample_objects(businesses, "Business")
    return businesses


def create_sponsors(count=5):
    """Create N sponsors"""
    print(f"Creating {count} sponsors...")
    # sponsors = SponsorFactory.create_batch(count)
    sponsors = SponsorFactory.build_batch(count)
    print(f"Created {len(sponsors)} sponsors.")
    print_sample_objects(sponsors, "Sponsor")
    return sponsors


def create_listings(count=20):
    """Create N job listings"""
    print(f"Creating {count} listings...")
    # listings = ListingFactory.create_batch(count)
    listings = ListingFactory.build_batch(count)
    print(f"Created {len(listings)} listings.")
    print_sample_objects(listings, "Listing")
    return listings

def create_team_members(count=15):
    """Create N team members"""
    print(f"Creating {count} team members...")
    # team_members = TeamMemberFactory.create_batch(count)
    team_members = TeamMemberFactory.build_batch(count)
    print(f"Created {len(team_members)} team members.")
    print_sample_objects(team_members, "TeamMember")
    return team_members


def create_programs(count=8):
    """Create N programs with varying capacities and registration status"""
    print(f"Creating {count} programs...")
    # programs = ProgramFactory.create_batch(count)
    programs = ProgramFactory.build_batch(count)
    print(f"Created {len(programs)} programs.")
    print_sample_objects(programs, "Program")
    return programs


def create_participants_for_programs():
    """Create participants for each program (some full, some with waitlist)"""
    print("Creating participants for programs...")
    # participans = ParticipantFactory.create_batch(10)
    participans = ParticipantFactory.build_batch(10)
    print(f"Created {len(participans)} participants.")
    print_sample_objects(participans, "Participant")
    return participans



def run():
    """Main function that orchestrates the data generation"""
    print("Starting test data generation...")
    
    # clear_existing_data()
    
    create_businesses()
    create_sponsors()
    create_listings()
    create_team_members()
    create_programs()
    create_participants_for_programs()
    
    print("Test data generation complete!")


if __name__ == '__main__':
    run()