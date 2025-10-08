import factory
from factory.django import DjangoModelFactory
from faker import Faker
from nvdagen.models import (
    Business, 
    Listing, 
    Sponsor, 
    TeamMember, 
    Form, 
    Participant,
    Program,
    # Import the choice constants
    LISTINGTYPECHOICE,
    # SUMMER_INTERNSHIP,
    # FULL_TIME,
    # OTHER_POSITION,
    LEVELTYPECHOICE,
    # GOLD,
    # SILVER,
    # BRONZE,
    DAYSCHOICE,
    # DAY1,
    # DAY2,
    # BOTH,
    # DAYS_NONE,
)

LOCALE = 'no_NO' # For Norwegian data
EXAMPLE_URL = 'http://example.com'

fake = Faker(LOCALE) # For Norwegian data
factory.Faker.override_default_locale(LOCALE)

class BusinessFactory(DjangoModelFactory):
    class Meta:
        model = Business
    
    name = factory.Faker('company')
    logo_uri = EXAMPLE_URL
    website_url = EXAMPLE_URL
    text = factory.Faker('paragraph')
    level = factory.Iterator(LEVELTYPECHOICE)
    days = factory.Iterator(DAYSCHOICE)
    standnumber = factory.Sequence(lambda n: n + 1)


class ListingFactory(DjangoModelFactory):
    class Meta:
        model = Listing
    
    name = factory.Faker('name')
    company_name = factory.Faker('company')
    logo_uri = EXAMPLE_URL
    type = factory.Iterator(LISTINGTYPECHOICE)
    listing_url = EXAMPLE_URL
    city = factory.Faker('city')
    content = factory.Faker('paragraph')
    # internal_url
    # deadline


class SponsorFactory(DjangoModelFactory):
    class Meta:
        model = Sponsor
    name = factory.Faker('company')
    logo_uri = EXAMPLE_URL
    website_url = EXAMPLE_URL


class TeamMemberFactory(DjangoModelFactory):
    class Meta:
        model = TeamMember
    name = factory.Faker('name')
    email = factory.Faker('email')
    photo_uri = EXAMPLE_URL
    team = factory.Faker('word')
    position = factory.Faker('job')


class FormFactory(DjangoModelFactory):
    class Meta:
        model = Form


class ProgramFactory(DjangoModelFactory):
    class Meta:
        model = Program
    
    header = factory.Faker('sentence', nb_words=4)
    place = factory.Faker('city')
    timeStart = factory.Faker('future_datetime', end_date='+60d')
    timeEnd = factory.LazyAttribute(lambda obj: obj.timeStart)  # Same as start or later
    paragraph = factory.Faker('paragraph')
    registration = factory.Faker('random_element', elements = [True, False])
    maxRegistered = factory.Faker('random_int', min=10, max=100)
    registrationStart = factory.Faker('past_datetime', start_date='-30d')
    registrationEnd = factory.Faker('future_datetime', end_date='+30d')

class ParticipantFactory(DjangoModelFactory):
    class Meta:
        model = Participant
    
    event = factory.SubFactory(ProgramFactory)  # Creates a Program if needed
    email = factory.Faker('email')
    name = factory.Faker('name')
    year = factory.Faker('random_element', elements=['1', '2', '3', '4', '5'])
    study = factory.Faker('random_element', elements=['Kybernetikk og robotikk', 'Datateknologi', 'Elsys'])
    code = factory.Faker('uuid4')  # Random unique code
    allergies = factory.Faker('random_element', elements=['', 'Nøtter', 'Laktose', 'Gluten', ''])
    
