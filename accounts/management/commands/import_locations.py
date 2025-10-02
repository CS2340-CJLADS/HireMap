from django.core.management.base import BaseCommand
from accounts.models import Location

class Command(BaseCommand):
    help = 'Import comprehensive location database'

    def handle(self, *args, **options):
        self.stdout.write('Importing locations...')
        
        # Comprehensive location data - Major cities + Remote options
        locations_data = [
            # Remote Options
            {'name': 'Remote - US', 'country': 'United States', 'city': 'Remote', 'is_remote': True, 'is_major_city': True},
            {'name': 'Remote - Global', 'country': 'Global', 'city': 'Remote', 'is_remote': True, 'is_major_city': True},
            {'name': 'Remote - North America', 'country': 'North America', 'city': 'Remote', 'is_remote': True, 'is_major_city': True},
            {'name': 'Remote - Europe', 'country': 'Europe', 'city': 'Remote', 'is_remote': True, 'is_major_city': True},
            {'name': 'Remote - Asia Pacific', 'country': 'Asia Pacific', 'city': 'Remote', 'is_remote': True, 'is_major_city': True},
            {'name': 'Remote - Anywhere', 'country': 'Global', 'city': 'Remote', 'is_remote': True, 'is_major_city': True},
            
            # Major US Cities
            {'name': 'New York, NY', 'country': 'United States', 'state_province': 'NY', 'city': 'New York', 'is_major_city': True, 'population': 8336817, 'timezone': 'America/New_York'},
            {'name': 'Los Angeles, CA', 'country': 'United States', 'state_province': 'CA', 'city': 'Los Angeles', 'is_major_city': True, 'population': 3971883, 'timezone': 'America/Los_Angeles'},
            {'name': 'Chicago, IL', 'country': 'United States', 'state_province': 'IL', 'city': 'Chicago', 'is_major_city': True, 'population': 2693976, 'timezone': 'America/Chicago'},
            {'name': 'Houston, TX', 'country': 'United States', 'state_province': 'TX', 'city': 'Houston', 'is_major_city': True, 'population': 2320268, 'timezone': 'America/Chicago'},
            {'name': 'Phoenix, AZ', 'country': 'United States', 'state_province': 'AZ', 'city': 'Phoenix', 'is_major_city': True, 'population': 1608139, 'timezone': 'America/Phoenix'},
            {'name': 'Philadelphia, PA', 'country': 'United States', 'state_province': 'PA', 'city': 'Philadelphia', 'is_major_city': True, 'population': 1584064, 'timezone': 'America/New_York'},
            {'name': 'San Antonio, TX', 'country': 'United States', 'state_province': 'TX', 'city': 'San Antonio', 'is_major_city': True, 'population': 1547253, 'timezone': 'America/Chicago'},
            {'name': 'San Diego, CA', 'country': 'United States', 'state_province': 'CA', 'city': 'San Diego', 'is_major_city': True, 'population': 1423851, 'timezone': 'America/Los_Angeles'},
            {'name': 'Dallas, TX', 'country': 'United States', 'state_province': 'TX', 'city': 'Dallas', 'is_major_city': True, 'population': 1343573, 'timezone': 'America/Chicago'},
            {'name': 'San Jose, CA', 'country': 'United States', 'state_province': 'CA', 'city': 'San Jose', 'is_major_city': True, 'population': 1035317, 'timezone': 'America/Los_Angeles'},
            {'name': 'Austin, TX', 'country': 'United States', 'state_province': 'TX', 'city': 'Austin', 'is_major_city': True, 'population': 978908, 'timezone': 'America/Chicago'},
            {'name': 'Jacksonville, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Jacksonville', 'is_major_city': True, 'population': 949611, 'timezone': 'America/New_York'},
            {'name': 'Fort Worth, TX', 'country': 'United States', 'state_province': 'TX', 'city': 'Fort Worth', 'is_major_city': True, 'population': 918915, 'timezone': 'America/Chicago'},
            {'name': 'Columbus, OH', 'country': 'United States', 'state_province': 'OH', 'city': 'Columbus', 'is_major_city': True, 'population': 905748, 'timezone': 'America/New_York'},
            {'name': 'Charlotte, NC', 'country': 'United States', 'state_province': 'NC', 'city': 'Charlotte', 'is_major_city': True, 'population': 885708, 'timezone': 'America/New_York'},
            {'name': 'San Francisco, CA', 'country': 'United States', 'state_province': 'CA', 'city': 'San Francisco', 'is_major_city': True, 'population': 873965, 'timezone': 'America/Los_Angeles'},
            {'name': 'Indianapolis, IN', 'country': 'United States', 'state_province': 'IN', 'city': 'Indianapolis', 'is_major_city': True, 'population': 887642, 'timezone': 'America/New_York'},
            {'name': 'Seattle, WA', 'country': 'United States', 'state_province': 'WA', 'city': 'Seattle', 'is_major_city': True, 'population': 749256, 'timezone': 'America/Los_Angeles'},
            {'name': 'Denver, CO', 'country': 'United States', 'state_province': 'CO', 'city': 'Denver', 'is_major_city': True, 'population': 715522, 'timezone': 'America/Denver'},
            {'name': 'Washington, DC', 'country': 'United States', 'state_province': 'DC', 'city': 'Washington', 'is_major_city': True, 'population': 705749, 'timezone': 'America/New_York'},
            {'name': 'Boston, MA', 'country': 'United States', 'state_province': 'MA', 'city': 'Boston', 'is_major_city': True, 'population': 692600, 'timezone': 'America/New_York'},
            {'name': 'El Paso, TX', 'country': 'United States', 'state_province': 'TX', 'city': 'El Paso', 'is_major_city': True, 'population': 678815, 'timezone': 'America/Chicago'},
            {'name': 'Nashville, TN', 'country': 'United States', 'state_province': 'TN', 'city': 'Nashville', 'is_major_city': True, 'population': 678851, 'timezone': 'America/Chicago'},
            {'name': 'Detroit, MI', 'country': 'United States', 'state_province': 'MI', 'city': 'Detroit', 'is_major_city': True, 'population': 639111, 'timezone': 'America/New_York'},
            {'name': 'Oklahoma City, OK', 'country': 'United States', 'state_province': 'OK', 'city': 'Oklahoma City', 'is_major_city': True, 'population': 655057, 'timezone': 'America/Chicago'},
            {'name': 'Portland, OR', 'country': 'United States', 'state_province': 'OR', 'city': 'Portland', 'is_major_city': True, 'population': 652503, 'timezone': 'America/Los_Angeles'},
            {'name': 'Las Vegas, NV', 'country': 'United States', 'state_province': 'NV', 'city': 'Las Vegas', 'is_major_city': True, 'population': 641903, 'timezone': 'America/Los_Angeles'},
            {'name': 'Memphis, TN', 'country': 'United States', 'state_province': 'TN', 'city': 'Memphis', 'is_major_city': True, 'population': 633104, 'timezone': 'America/Chicago'},
            {'name': 'Louisville, KY', 'country': 'United States', 'state_province': 'KY', 'city': 'Louisville', 'is_major_city': True, 'population': 617638, 'timezone': 'America/New_York'},
            {'name': 'Baltimore, MD', 'country': 'United States', 'state_province': 'MD', 'city': 'Baltimore', 'is_major_city': True, 'population': 585708, 'timezone': 'America/New_York'},
            {'name': 'Milwaukee, WI', 'country': 'United States', 'state_province': 'WI', 'city': 'Milwaukee', 'is_major_city': True, 'population': 577222, 'timezone': 'America/Chicago'},
            {'name': 'Albuquerque, NM', 'country': 'United States', 'state_province': 'NM', 'city': 'Albuquerque', 'is_major_city': True, 'population': 564559, 'timezone': 'America/Denver'},
            {'name': 'Tucson, AZ', 'country': 'United States', 'state_province': 'AZ', 'city': 'Tucson', 'is_major_city': True, 'population': 548073, 'timezone': 'America/Phoenix'},
            {'name': 'Fresno, CA', 'country': 'United States', 'state_province': 'CA', 'city': 'Fresno', 'is_major_city': True, 'population': 542107, 'timezone': 'America/Los_Angeles'},
            {'name': 'Sacramento, CA', 'country': 'United States', 'state_province': 'CA', 'city': 'Sacramento', 'is_major_city': True, 'population': 513624, 'timezone': 'America/Los_Angeles'},
            {'name': 'Mesa, AZ', 'country': 'United States', 'state_province': 'AZ', 'city': 'Mesa', 'is_major_city': True, 'population': 504258, 'timezone': 'America/Phoenix'},
            {'name': 'Kansas City, MO', 'country': 'United States', 'state_province': 'MO', 'city': 'Kansas City', 'is_major_city': True, 'population': 508090, 'timezone': 'America/Chicago'},
            {'name': 'Atlanta, GA', 'country': 'United States', 'state_province': 'GA', 'city': 'Atlanta', 'is_major_city': True, 'population': 498715, 'timezone': 'America/New_York'},
            {'name': 'Long Beach, CA', 'country': 'United States', 'state_province': 'CA', 'city': 'Long Beach', 'is_major_city': True, 'population': 466742, 'timezone': 'America/Los_Angeles'},
            {'name': 'Colorado Springs, CO', 'country': 'United States', 'state_province': 'CO', 'city': 'Colorado Springs', 'is_major_city': True, 'population': 478961, 'timezone': 'America/Denver'},
            {'name': 'Raleigh, NC', 'country': 'United States', 'state_province': 'NC', 'city': 'Raleigh', 'is_major_city': True, 'population': 474069, 'timezone': 'America/New_York'},
            {'name': 'Miami, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Miami', 'is_major_city': True, 'population': 467963, 'timezone': 'America/New_York'},
            {'name': 'Virginia Beach, VA', 'country': 'United States', 'state_province': 'VA', 'city': 'Virginia Beach', 'is_major_city': True, 'population': 459470, 'timezone': 'America/New_York'},
            {'name': 'Omaha, NE', 'country': 'United States', 'state_province': 'NE', 'city': 'Omaha', 'is_major_city': True, 'population': 486051, 'timezone': 'America/Chicago'},
            {'name': 'Oakland, CA', 'country': 'United States', 'state_province': 'CA', 'city': 'Oakland', 'is_major_city': True, 'population': 440646, 'timezone': 'America/Los_Angeles'},
            {'name': 'Minneapolis, MN', 'country': 'United States', 'state_province': 'MN', 'city': 'Minneapolis', 'is_major_city': True, 'population': 429606, 'timezone': 'America/Chicago'},
            {'name': 'Tulsa, OK', 'country': 'United States', 'state_province': 'OK', 'city': 'Tulsa', 'is_major_city': True, 'population': 413066, 'timezone': 'America/Chicago'},
            {'name': 'Arlington, TX', 'country': 'United States', 'state_province': 'TX', 'city': 'Arlington', 'is_major_city': True, 'population': 394266, 'timezone': 'America/Chicago'},
            {'name': 'Tampa, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Tampa', 'is_major_city': True, 'population': 384959, 'timezone': 'America/New_York'},
            {'name': 'New Orleans, LA', 'country': 'United States', 'state_province': 'LA', 'city': 'New Orleans', 'is_major_city': True, 'population': 383997, 'timezone': 'America/Chicago'},
            
            # International Major Cities
            {'name': 'London, UK', 'country': 'United Kingdom', 'city': 'London', 'is_major_city': True, 'population': 8982000, 'timezone': 'Europe/London'},
            {'name': 'Toronto, ON, Canada', 'country': 'Canada', 'state_province': 'ON', 'city': 'Toronto', 'is_major_city': True, 'population': 2930000, 'timezone': 'America/Toronto'},
            {'name': 'Vancouver, BC, Canada', 'country': 'Canada', 'state_province': 'BC', 'city': 'Vancouver', 'is_major_city': True, 'population': 675218, 'timezone': 'America/Vancouver'},
            {'name': 'Montreal, QC, Canada', 'country': 'Canada', 'state_province': 'QC', 'city': 'Montreal', 'is_major_city': True, 'population': 1780000, 'timezone': 'America/Montreal'},
            {'name': 'Sydney, Australia', 'country': 'Australia', 'city': 'Sydney', 'is_major_city': True, 'population': 5312000, 'timezone': 'Australia/Sydney'},
            {'name': 'Melbourne, Australia', 'country': 'Australia', 'city': 'Melbourne', 'is_major_city': True, 'population': 5078000, 'timezone': 'Australia/Melbourne'},
            {'name': 'Berlin, Germany', 'country': 'Germany', 'city': 'Berlin', 'is_major_city': True, 'population': 3769000, 'timezone': 'Europe/Berlin'},
            {'name': 'Amsterdam, Netherlands', 'country': 'Netherlands', 'city': 'Amsterdam', 'is_major_city': True, 'population': 872680, 'timezone': 'Europe/Amsterdam'},
            {'name': 'Dublin, Ireland', 'country': 'Ireland', 'city': 'Dublin', 'is_major_city': True, 'population': 1343000, 'timezone': 'Europe/Dublin'},
            {'name': 'Zurich, Switzerland', 'country': 'Switzerland', 'city': 'Zurich', 'is_major_city': True, 'population': 415367, 'timezone': 'Europe/Zurich'},
            {'name': 'Singapore', 'country': 'Singapore', 'city': 'Singapore', 'is_major_city': True, 'population': 5454000, 'timezone': 'Asia/Singapore'},
            {'name': 'Hong Kong', 'country': 'Hong Kong', 'city': 'Hong Kong', 'is_major_city': True, 'population': 7507000, 'timezone': 'Asia/Hong_Kong'},
            {'name': 'Tokyo, Japan', 'country': 'Japan', 'city': 'Tokyo', 'is_major_city': True, 'population': 14000000, 'timezone': 'Asia/Tokyo'},
            {'name': 'Seoul, South Korea', 'country': 'South Korea', 'city': 'Seoul', 'is_major_city': True, 'population': 9720846, 'timezone': 'Asia/Seoul'},
            {'name': 'Mumbai, India', 'country': 'India', 'city': 'Mumbai', 'is_major_city': True, 'population': 12478000, 'timezone': 'Asia/Kolkata'},
            {'name': 'Bangalore, India', 'country': 'India', 'city': 'Bangalore', 'is_major_city': True, 'population': 12379000, 'timezone': 'Asia/Kolkata'},
            {'name': 'Delhi, India', 'country': 'India', 'city': 'Delhi', 'is_major_city': True, 'population': 32941000, 'timezone': 'Asia/Kolkata'},
            {'name': 'São Paulo, Brazil', 'country': 'Brazil', 'city': 'São Paulo', 'is_major_city': True, 'population': 12325000, 'timezone': 'America/Sao_Paulo'},
            {'name': 'Mexico City, Mexico', 'country': 'Mexico', 'city': 'Mexico City', 'is_major_city': True, 'population': 9209000, 'timezone': 'America/Mexico_City'},
            {'name': 'Buenos Aires, Argentina', 'country': 'Argentina', 'city': 'Buenos Aires', 'is_major_city': True, 'population': 3075000, 'timezone': 'America/Argentina/Buenos_Aires'},
            {'name': 'Cape Town, South Africa', 'country': 'South Africa', 'city': 'Cape Town', 'is_major_city': True, 'population': 4618000, 'timezone': 'Africa/Johannesburg'},
            {'name': 'Dubai, UAE', 'country': 'United Arab Emirates', 'city': 'Dubai', 'is_major_city': True, 'population': 3331000, 'timezone': 'Asia/Dubai'},
            {'name': 'Tel Aviv, Israel', 'country': 'Israel', 'city': 'Tel Aviv', 'is_major_city': True, 'population': 460613, 'timezone': 'Asia/Jerusalem'},
            
            # Additional US Cities (Smaller but still significant)
            {'name': 'Buffalo, NY', 'country': 'United States', 'state_province': 'NY', 'city': 'Buffalo', 'is_major_city': False, 'population': 278349, 'timezone': 'America/New_York'},
            {'name': 'Rochester, NY', 'country': 'United States', 'state_province': 'NY', 'city': 'Rochester', 'is_major_city': False, 'population': 211328, 'timezone': 'America/New_York'},
            {'name': 'Syracuse, NY', 'country': 'United States', 'state_province': 'NY', 'city': 'Syracuse', 'is_major_city': False, 'population': 148620, 'timezone': 'America/New_York'},
            {'name': 'Albany, NY', 'country': 'United States', 'state_province': 'NY', 'city': 'Albany', 'is_major_city': False, 'population': 99189, 'timezone': 'America/New_York'},
            {'name': 'Yonkers, NY', 'country': 'United States', 'state_province': 'NY', 'city': 'Yonkers', 'is_major_city': False, 'population': 211569, 'timezone': 'America/New_York'},
            
            # Georgia Cities
            {'name': 'Atlanta, GA', 'country': 'United States', 'state_province': 'GA', 'city': 'Atlanta', 'is_major_city': True, 'population': 498715, 'timezone': 'America/New_York'},
            {'name': 'Augusta, GA', 'country': 'United States', 'state_province': 'GA', 'city': 'Augusta', 'is_major_city': False, 'population': 202081, 'timezone': 'America/New_York'},
            {'name': 'Columbus, GA', 'country': 'United States', 'state_province': 'GA', 'city': 'Columbus', 'is_major_city': False, 'population': 206922, 'timezone': 'America/New_York'},
            {'name': 'Savannah, GA', 'country': 'United States', 'state_province': 'GA', 'city': 'Savannah', 'is_major_city': False, 'population': 147780, 'timezone': 'America/New_York'},
            {'name': 'Athens, GA', 'country': 'United States', 'state_province': 'GA', 'city': 'Athens', 'is_major_city': False, 'population': 127315, 'timezone': 'America/New_York'},
            {'name': 'Sandy Springs, GA', 'country': 'United States', 'state_province': 'GA', 'city': 'Sandy Springs', 'is_major_city': False, 'population': 108080, 'timezone': 'America/New_York'},
            {'name': 'Roswell, GA', 'country': 'United States', 'state_province': 'GA', 'city': 'Roswell', 'is_major_city': False, 'population': 94765, 'timezone': 'America/New_York'},
            {'name': 'Macon, GA', 'country': 'United States', 'state_province': 'GA', 'city': 'Macon', 'is_major_city': False, 'population': 152663, 'timezone': 'America/New_York'},
            {'name': 'Albany, GA', 'country': 'United States', 'state_province': 'GA', 'city': 'Albany', 'is_major_city': False, 'population': 69018, 'timezone': 'America/New_York'},
            {'name': 'Johns Creek, GA', 'country': 'United States', 'state_province': 'GA', 'city': 'Johns Creek', 'is_major_city': False, 'population': 82188, 'timezone': 'America/New_York'},
            {'name': 'Warner Robins, GA', 'country': 'United States', 'state_province': 'GA', 'city': 'Warner Robins', 'is_major_city': False, 'population': 80488, 'timezone': 'America/New_York'},
            {'name': 'Alpharetta, GA', 'country': 'United States', 'state_province': 'GA', 'city': 'Alpharetta', 'is_major_city': False, 'population': 67013, 'timezone': 'America/New_York'},
            {'name': 'Marietta, GA', 'country': 'United States', 'state_province': 'GA', 'city': 'Marietta', 'is_major_city': False, 'population': 60817, 'timezone': 'America/New_York'},
            {'name': 'Valdosta, GA', 'country': 'United States', 'state_province': 'GA', 'city': 'Valdosta', 'is_major_city': False, 'population': 56000, 'timezone': 'America/New_York'},
            {'name': 'Smyrna, GA', 'country': 'United States', 'state_province': 'GA', 'city': 'Smyrna', 'is_major_city': False, 'population': 56000, 'timezone': 'America/New_York'},
            {'name': 'Dunwoody, GA', 'country': 'United States', 'state_province': 'GA', 'city': 'Dunwoody', 'is_major_city': False, 'population': 50000, 'timezone': 'America/New_York'},
            {'name': 'Rome, GA', 'country': 'United States', 'state_province': 'GA', 'city': 'Rome', 'is_major_city': False, 'population': 37000, 'timezone': 'America/New_York'},
            {'name': 'East Point, GA', 'country': 'United States', 'state_province': 'GA', 'city': 'East Point', 'is_major_city': False, 'population': 35000, 'timezone': 'America/New_York'},
            {'name': 'Peachtree Corners, GA', 'country': 'United States', 'state_province': 'GA', 'city': 'Peachtree Corners', 'is_major_city': False, 'population': 42000, 'timezone': 'America/New_York'},
            {'name': 'Buford, GA', 'country': 'United States', 'state_province': 'GA', 'city': 'Buford', 'is_major_city': False, 'population': 17000, 'timezone': 'America/New_York'},
            
            # Arkansas Cities
            {'name': 'Little Rock, AR', 'country': 'United States', 'state_province': 'AR', 'city': 'Little Rock', 'is_major_city': True, 'population': 198541, 'timezone': 'America/Chicago'},
            {'name': 'Fort Smith, AR', 'country': 'United States', 'state_province': 'AR', 'city': 'Fort Smith', 'is_major_city': False, 'population': 89142, 'timezone': 'America/Chicago'},
            {'name': 'Fayetteville, AR', 'country': 'United States', 'state_province': 'AR', 'city': 'Fayetteville', 'is_major_city': False, 'population': 95015, 'timezone': 'America/Chicago'},
            {'name': 'Springdale, AR', 'country': 'United States', 'state_province': 'AR', 'city': 'Springdale', 'is_major_city': False, 'population': 84000, 'timezone': 'America/Chicago'},
            {'name': 'Jonesboro, AR', 'country': 'United States', 'state_province': 'AR', 'city': 'Jonesboro', 'is_major_city': False, 'population': 78000, 'timezone': 'America/Chicago'},
            {'name': 'North Little Rock, AR', 'country': 'United States', 'state_province': 'AR', 'city': 'North Little Rock', 'is_major_city': False, 'population': 65000, 'timezone': 'America/Chicago'},
            {'name': 'Conway, AR', 'country': 'United States', 'state_province': 'AR', 'city': 'Conway', 'is_major_city': False, 'population': 65000, 'timezone': 'America/Chicago'},
            {'name': 'Rogers, AR', 'country': 'United States', 'state_province': 'AR', 'city': 'Rogers', 'is_major_city': False, 'population': 70000, 'timezone': 'America/Chicago'},
            {'name': 'Pine Bluff, AR', 'country': 'United States', 'state_province': 'AR', 'city': 'Pine Bluff', 'is_major_city': False, 'population': 42000, 'timezone': 'America/Chicago'},
            {'name': 'Bentonville, AR', 'country': 'United States', 'state_province': 'AR', 'city': 'Bentonville', 'is_major_city': False, 'population': 55000, 'timezone': 'America/Chicago'},
            
            # Idaho Cities
            {'name': 'Boise, ID', 'country': 'United States', 'state_province': 'ID', 'city': 'Boise', 'is_major_city': True, 'population': 235684, 'timezone': 'America/Boise'},
            {'name': 'Nampa, ID', 'country': 'United States', 'state_province': 'ID', 'city': 'Nampa', 'is_major_city': False, 'population': 100000, 'timezone': 'America/Boise'},
            {'name': 'Meridian, ID', 'country': 'United States', 'state_province': 'ID', 'city': 'Meridian', 'is_major_city': False, 'population': 120000, 'timezone': 'America/Boise'},
            {'name': 'Idaho Falls, ID', 'country': 'United States', 'state_province': 'ID', 'city': 'Idaho Falls', 'is_major_city': False, 'population': 65000, 'timezone': 'America/Boise'},
            {'name': 'Pocatello, ID', 'country': 'United States', 'state_province': 'ID', 'city': 'Pocatello', 'is_major_city': False, 'population': 56000, 'timezone': 'America/Boise'},
            {'name': 'Caldwell, ID', 'country': 'United States', 'state_province': 'ID', 'city': 'Caldwell', 'is_major_city': False, 'population': 60000, 'timezone': 'America/Boise'},
            {'name': 'Coeur d\'Alene, ID', 'country': 'United States', 'state_province': 'ID', 'city': 'Coeur d\'Alene', 'is_major_city': False, 'population': 55000, 'timezone': 'America/Boise'},
            {'name': 'Twin Falls, ID', 'country': 'United States', 'state_province': 'ID', 'city': 'Twin Falls', 'is_major_city': False, 'population': 50000, 'timezone': 'America/Boise'},
            {'name': 'Lewiston, ID', 'country': 'United States', 'state_province': 'ID', 'city': 'Lewiston', 'is_major_city': False, 'population': 35000, 'timezone': 'America/Boise'},
            {'name': 'Post Falls, ID', 'country': 'United States', 'state_province': 'ID', 'city': 'Post Falls', 'is_major_city': False, 'population': 40000, 'timezone': 'America/Boise'},
            
            # Additional Major US Cities
            {'name': 'Cincinnati, OH', 'country': 'United States', 'state_province': 'OH', 'city': 'Cincinnati', 'is_major_city': True, 'population': 309317, 'timezone': 'America/New_York'},
            {'name': 'Cleveland, OH', 'country': 'United States', 'state_province': 'OH', 'city': 'Cleveland', 'is_major_city': True, 'population': 383793, 'timezone': 'America/New_York'},
            {'name': 'Toledo, OH', 'country': 'United States', 'state_province': 'OH', 'city': 'Toledo', 'is_major_city': False, 'population': 270871, 'timezone': 'America/New_York'},
            {'name': 'Akron, OH', 'country': 'United States', 'state_province': 'OH', 'city': 'Akron', 'is_major_city': False, 'population': 197597, 'timezone': 'America/New_York'},
            {'name': 'Dayton, OH', 'country': 'United States', 'state_province': 'OH', 'city': 'Dayton', 'is_major_city': False, 'population': 140407, 'timezone': 'America/New_York'},
            {'name': 'Parma, OH', 'country': 'United States', 'state_province': 'OH', 'city': 'Parma', 'is_major_city': False, 'population': 81000, 'timezone': 'America/New_York'},
            {'name': 'Canton, OH', 'country': 'United States', 'state_province': 'OH', 'city': 'Canton', 'is_major_city': False, 'population': 70000, 'timezone': 'America/New_York'},
            {'name': 'Youngstown, OH', 'country': 'United States', 'state_province': 'OH', 'city': 'Youngstown', 'is_major_city': False, 'population': 60000, 'timezone': 'America/New_York'},
            {'name': 'Lorain, OH', 'country': 'United States', 'state_province': 'OH', 'city': 'Lorain', 'is_major_city': False, 'population': 60000, 'timezone': 'America/New_York'},
            {'name': 'Hamilton, OH', 'country': 'United States', 'state_province': 'OH', 'city': 'Hamilton', 'is_major_city': False, 'population': 63000, 'timezone': 'America/New_York'},
            
            # Florida Cities
            {'name': 'Jacksonville, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Jacksonville', 'is_major_city': True, 'population': 949611, 'timezone': 'America/New_York'},
            {'name': 'Miami, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Miami', 'is_major_city': True, 'population': 467963, 'timezone': 'America/New_York'},
            {'name': 'Tampa, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Tampa', 'is_major_city': True, 'population': 384959, 'timezone': 'America/New_York'},
            {'name': 'Orlando, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Orlando', 'is_major_city': True, 'population': 307573, 'timezone': 'America/New_York'},
            {'name': 'St. Petersburg, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'St. Petersburg', 'is_major_city': False, 'population': 258308, 'timezone': 'America/New_York'},
            {'name': 'Hialeah, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Hialeah', 'is_major_city': False, 'population': 223109, 'timezone': 'America/New_York'},
            {'name': 'Tallahassee, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Tallahassee', 'is_major_city': False, 'population': 196169, 'timezone': 'America/New_York'},
            {'name': 'Fort Lauderdale, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Fort Lauderdale', 'is_major_city': False, 'population': 182437, 'timezone': 'America/New_York'},
            {'name': 'Port St. Lucie, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Port St. Lucie', 'is_major_city': False, 'population': 204851, 'timezone': 'America/New_York'},
            {'name': 'Cape Coral, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Cape Coral', 'is_major_city': False, 'population': 194016, 'timezone': 'America/New_York'},
            {'name': 'Pembroke Pines, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Pembroke Pines', 'is_major_city': False, 'population': 171178, 'timezone': 'America/New_York'},
            {'name': 'Hollywood, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Hollywood', 'is_major_city': False, 'population': 153067, 'timezone': 'America/New_York'},
            {'name': 'Miramar, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Miramar', 'is_major_city': False, 'population': 140328, 'timezone': 'America/New_York'},
            {'name': 'Gainesville, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Gainesville', 'is_major_city': False, 'population': 141085, 'timezone': 'America/New_York'},
            {'name': 'Coral Springs, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Coral Springs', 'is_major_city': False, 'population': 134394, 'timezone': 'America/New_York'},
            {'name': 'Miami Gardens, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Miami Gardens', 'is_major_city': False, 'population': 113187, 'timezone': 'America/New_York'},
            {'name': 'Clearwater, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Clearwater', 'is_major_city': False, 'population': 117292, 'timezone': 'America/New_York'},
            {'name': 'Palm Bay, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Palm Bay', 'is_major_city': False, 'population': 119760, 'timezone': 'America/New_York'},
            {'name': 'West Palm Beach, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'West Palm Beach', 'is_major_city': False, 'population': 117415, 'timezone': 'America/New_York'},
            {'name': 'Pompano Beach, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Pompano Beach', 'is_major_city': False, 'population': 112046, 'timezone': 'America/New_York'},
            {'name': 'Lakeland, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Lakeland', 'is_major_city': False, 'population': 112641, 'timezone': 'America/New_York'},
            {'name': 'Davie, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Davie', 'is_major_city': False, 'population': 105691, 'timezone': 'America/New_York'},
            {'name': 'Miami Beach, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Miami Beach', 'is_major_city': False, 'population': 92000, 'timezone': 'America/New_York'},
            {'name': 'Sunrise, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Sunrise', 'is_major_city': False, 'population': 97000, 'timezone': 'America/New_York'},
            {'name': 'Plantation, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Plantation', 'is_major_city': False, 'population': 95000, 'timezone': 'America/New_York'},
            {'name': 'Boca Raton, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Boca Raton', 'is_major_city': False, 'population': 98000, 'timezone': 'America/New_York'},
            {'name': 'Deltona, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Deltona', 'is_major_city': False, 'population': 95000, 'timezone': 'America/New_York'},
            {'name': 'Largo, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Largo', 'is_major_city': False, 'population': 85000, 'timezone': 'America/New_York'},
            {'name': 'Deerfield Beach, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Deerfield Beach', 'is_major_city': False, 'population': 85000, 'timezone': 'America/New_York'},
            {'name': 'Boynton Beach, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Boynton Beach', 'is_major_city': False, 'population': 80000, 'timezone': 'America/New_York'},
            {'name': 'Lauderhill, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Lauderhill', 'is_major_city': False, 'population': 75000, 'timezone': 'America/New_York'},
            {'name': 'Weston, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Weston', 'is_major_city': False, 'population': 70000, 'timezone': 'America/New_York'},
            {'name': 'Homestead, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Homestead', 'is_major_city': False, 'population': 80000, 'timezone': 'America/New_York'},
            {'name': 'Tamarac, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Tamarac', 'is_major_city': False, 'population': 70000, 'timezone': 'America/New_York'},
            {'name': 'Delray Beach, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Delray Beach', 'is_major_city': False, 'population': 70000, 'timezone': 'America/New_York'},
            {'name': 'Kissimmee, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Kissimmee', 'is_major_city': False, 'population': 75000, 'timezone': 'America/New_York'},
            {'name': 'North Miami, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'North Miami', 'is_major_city': False, 'population': 65000, 'timezone': 'America/New_York'},
            {'name': 'Wellington, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Wellington', 'is_major_city': False, 'population': 65000, 'timezone': 'America/New_York'},
            {'name': 'Jupiter, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Jupiter', 'is_major_city': False, 'population': 65000, 'timezone': 'America/New_York'},
            {'name': 'Ocala, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Ocala', 'is_major_city': False, 'population': 65000, 'timezone': 'America/New_York'},
            {'name': 'Palm Coast, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Palm Coast', 'is_major_city': False, 'population': 95000, 'timezone': 'America/New_York'},
            {'name': 'Pensacola, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Pensacola', 'is_major_city': False, 'population': 55000, 'timezone': 'America/Chicago'},
            {'name': 'Sarasota, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Sarasota', 'is_major_city': False, 'population': 60000, 'timezone': 'America/New_York'},
            {'name': 'Naples, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Naples', 'is_major_city': False, 'population': 25000, 'timezone': 'America/New_York'},
            {'name': 'Key West, FL', 'country': 'United States', 'state_province': 'FL', 'city': 'Key West', 'is_major_city': False, 'population': 25000, 'timezone': 'America/New_York'},
        ]
        
        created_count = 0
        updated_count = 0
        
        for location_data in locations_data:
            location, created = Location.objects.get_or_create(
                name=location_data['name'],
                defaults=location_data
            )
            if created:
                created_count += 1
            else:
                # Update existing location with new data
                for key, value in location_data.items():
                    setattr(location, key, value)
                location.save()
                updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully imported {created_count} new locations and updated {updated_count} existing locations'
            )
        )
