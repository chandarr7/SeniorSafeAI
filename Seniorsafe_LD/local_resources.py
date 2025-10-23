"""
Local Resources Lookup System for SeniorSafe AI
Provides ZIP code-based lookup for local law enforcement, consumer protection, and cybercrime reporting resources.
"""

import re
from typing import Dict, List, Optional
from dataclasses import dataclass
import requests

@dataclass
class LocalResource:
    """Represents a local resource for reporting cybercrimes"""
    name: str
    type: str
    phone: str
    website: str
    address: Optional[str] = None
    hours: Optional[str] = None
    description: Optional[str] = None


class ZIPCodeValidator:
    """Validates and processes ZIP codes"""

    @staticmethod
    def validate(zip_code: str) -> bool:
        """Validate ZIP code format (5 digits or 5+4 format)"""
        pattern = r'^\d{5}(-\d{4})?$'
        return bool(re.match(pattern, zip_code.strip()))

    @staticmethod
    def extract_zip5(zip_code: str) -> str:
        """Extract 5-digit ZIP code"""
        return zip_code.strip()[:5]


class ZIPToStateMapper:
    """Maps ZIP codes to states"""

    # ZIP code ranges to state mapping
    ZIP_RANGES = {
        range(500, 599): 'NY',
        range(600, 699): 'PA',
        range(700, 729): 'DC',
        range(730, 799): 'VA',
        range(800, 899): 'NC',
        range(900, 999): 'SC',
        range(1000, 2799): 'MA',
        range(2800, 2999): 'RI',
        range(3000, 3899): 'NH',
        range(3900, 4999): 'ME',
        range(5000, 5999): 'VT',
        range(6000, 6999): 'CT',
        range(7000, 8999): 'NJ',
        range(10000, 14999): 'NY',
        range(15000, 19699): 'PA',
        range(19700, 19999): 'DE',
        range(20000, 20599): 'DC',
        range(20600, 21999): 'MD',
        range(22000, 24699): 'VA',
        range(24700, 26999): 'WV',
        range(27000, 28999): 'NC',
        range(29000, 29999): 'SC',
        range(30000, 31999): 'GA',
        range(32000, 34999): 'FL',
        range(35000, 36999): 'AL',
        range(37000, 38599): 'TN',
        range(38600, 39799): 'MS',
        range(39800, 39999): 'GA',
        range(40000, 42799): 'KY',
        range(43000, 45999): 'OH',
        range(46000, 47999): 'IN',
        range(48000, 49999): 'MI',
        range(50000, 52999): 'IA',
        range(53000, 54999): 'WI',
        range(55000, 56799): 'MN',
        range(57000, 57999): 'SD',
        range(58000, 58999): 'ND',
        range(59000, 59999): 'MT',
        range(60000, 62999): 'IL',
        range(63000, 65999): 'MO',
        range(66000, 67999): 'KS',
        range(68000, 69999): 'NE',
        range(70000, 71599): 'LA',
        range(71600, 72999): 'AR',
        range(73000, 74999): 'OK',
        range(75000, 79999): 'TX',
        range(80000, 81699): 'CO',
        range(82000, 83199): 'WY',
        range(83200, 83999): 'ID',
        range(84000, 84999): 'UT',
        range(85000, 86599): 'AZ',
        range(87000, 88499): 'NM',
        range(88500, 89999): 'NV',
        range(90000, 96199): 'CA',
        range(96700, 96899): 'HI',
        range(97000, 97999): 'OR',
        range(98000, 99499): 'WA',
        range(99500, 99999): 'AK',
    }

    @classmethod
    def get_state(cls, zip_code: str) -> Optional[str]:
        """Get state abbreviation from ZIP code"""
        zip5 = ZIPCodeValidator.extract_zip5(zip_code)
        try:
            zip_int = int(zip5)
            for zip_range, state in cls.ZIP_RANGES.items():
                if zip_int in zip_range:
                    return state
        except ValueError:
            return None
        return None


class LocalResourceDatabase:
    """Database of local resources by state"""

    # State consumer protection offices
    STATE_CONSUMER_OFFICES = {
        'AL': {
            'name': 'Alabama Attorney General Consumer Protection Division',
            'phone': '1-800-392-5658',
            'website': 'https://www.alabamaag.gov/consumers',
            'description': 'State consumer protection and fraud reporting'
        },
        'AK': {
            'name': 'Alaska Attorney General Consumer Protection Unit',
            'phone': '907-269-5200',
            'website': 'https://law.alaska.gov/department/civil/consumer.html',
            'description': 'State consumer protection and fraud reporting'
        },
        'AZ': {
            'name': 'Arizona Attorney General Consumer Protection Division',
            'phone': '602-542-5763',
            'website': 'https://www.azag.gov/consumer',
            'description': 'State consumer protection and fraud reporting'
        },
        'AR': {
            'name': 'Arkansas Attorney General Consumer Protection Division',
            'phone': '1-800-482-8982',
            'website': 'https://arkansasag.gov/consumer-protection',
            'description': 'State consumer protection and fraud reporting'
        },
        'CA': {
            'name': 'California Attorney General Public Inquiry Unit',
            'phone': '1-800-952-5225',
            'website': 'https://oag.ca.gov/contact/consumer-complaint-against-business-or-company',
            'description': 'State consumer protection and fraud reporting'
        },
        'CO': {
            'name': 'Colorado Attorney General Consumer Protection Section',
            'phone': '1-800-222-4444',
            'website': 'https://coag.gov/office-sections/consumer-protection',
            'description': 'State consumer protection and fraud reporting'
        },
        'CT': {
            'name': 'Connecticut Attorney General Consumer Protection',
            'phone': '860-808-5318',
            'website': 'https://portal.ct.gov/AG/Consumer-Protection',
            'description': 'State consumer protection and fraud reporting'
        },
        'DE': {
            'name': 'Delaware Attorney General Fraud & Consumer Protection Division',
            'phone': '1-800-220-5424',
            'website': 'https://attorney.general.delaware.gov/fraud/',
            'description': 'State consumer protection and fraud reporting'
        },
        'FL': {
            'name': 'Florida Attorney General Consumer Protection Division',
            'phone': '1-866-966-7226',
            'website': 'https://www.myfloridalegal.com/consumer-protection',
            'description': 'State consumer protection and fraud reporting'
        },
        'GA': {
            'name': 'Georgia Governor\'s Office of Consumer Protection',
            'phone': '404-651-8600',
            'website': 'https://consumer.georgia.gov',
            'description': 'State consumer protection and fraud reporting'
        },
        'HI': {
            'name': 'Hawaii Office of Consumer Protection',
            'phone': '808-586-2636',
            'website': 'https://cca.hawaii.gov/ocp/',
            'description': 'State consumer protection and fraud reporting'
        },
        'ID': {
            'name': 'Idaho Attorney General Consumer Protection',
            'phone': '208-334-2424',
            'website': 'https://www.ag.idaho.gov/consumer-protection',
            'description': 'State consumer protection and fraud reporting'
        },
        'IL': {
            'name': 'Illinois Attorney General Consumer Fraud Bureau',
            'phone': '1-800-386-5438',
            'website': 'https://illinoisattorneygeneral.gov/consumers',
            'description': 'State consumer protection and fraud reporting'
        },
        'IN': {
            'name': 'Indiana Attorney General Consumer Protection Division',
            'phone': '1-800-382-5516',
            'website': 'https://www.in.gov/attorneygeneral/consumer-protection',
            'description': 'State consumer protection and fraud reporting'
        },
        'IA': {
            'name': 'Iowa Attorney General Consumer Protection Division',
            'phone': '515-281-5926',
            'website': 'https://www.iowaattorneygeneral.gov/for-consumers',
            'description': 'State consumer protection and fraud reporting'
        },
        'KS': {
            'name': 'Kansas Attorney General Consumer Protection',
            'phone': '1-800-432-2310',
            'website': 'https://www.ag.ks.gov/consumer-protection',
            'description': 'State consumer protection and fraud reporting'
        },
        'KY': {
            'name': 'Kentucky Attorney General Consumer Protection',
            'phone': '1-888-432-9257',
            'website': 'https://ag.ky.gov/consumer-protection',
            'description': 'State consumer protection and fraud reporting'
        },
        'LA': {
            'name': 'Louisiana Attorney General Consumer Protection Section',
            'phone': '1-800-351-4889',
            'website': 'https://www.ag.state.la.us/ConsumerProtection',
            'description': 'State consumer protection and fraud reporting'
        },
        'ME': {
            'name': 'Maine Attorney General Consumer Protection Division',
            'phone': '1-800-436-2131',
            'website': 'https://www.maine.gov/ag/consumer',
            'description': 'State consumer protection and fraud reporting'
        },
        'MD': {
            'name': 'Maryland Attorney General Consumer Protection Division',
            'phone': '410-528-8662',
            'website': 'https://www.marylandattorneygeneral.gov/Pages/CPD/default.aspx',
            'description': 'State consumer protection and fraud reporting'
        },
        'MA': {
            'name': 'Massachusetts Attorney General Consumer Advocacy & Response Division',
            'phone': '617-727-8400',
            'website': 'https://www.mass.gov/consumer-protection',
            'description': 'State consumer protection and fraud reporting'
        },
        'MI': {
            'name': 'Michigan Attorney General Consumer Protection',
            'phone': '517-335-7599',
            'website': 'https://www.michigan.gov/ag/consumer-protection',
            'description': 'State consumer protection and fraud reporting'
        },
        'MN': {
            'name': 'Minnesota Attorney General Consumer Protection',
            'phone': '651-296-3353',
            'website': 'https://www.ag.state.mn.us/consumer',
            'description': 'State consumer protection and fraud reporting'
        },
        'MS': {
            'name': 'Mississippi Attorney General Consumer Protection',
            'phone': '1-800-281-4418',
            'website': 'https://www.ago.state.ms.us/divisions/consumer-protection',
            'description': 'State consumer protection and fraud reporting'
        },
        'MO': {
            'name': 'Missouri Attorney General Consumer Protection',
            'phone': '1-800-392-8222',
            'website': 'https://ago.mo.gov/home/consumer',
            'description': 'State consumer protection and fraud reporting'
        },
        'MT': {
            'name': 'Montana Department of Justice Office of Consumer Protection',
            'phone': '1-800-481-6896',
            'website': 'https://dojmt.gov/consumer',
            'description': 'State consumer protection and fraud reporting'
        },
        'NE': {
            'name': 'Nebraska Attorney General Consumer Protection',
            'phone': '402-471-2682',
            'website': 'https://ago.nebraska.gov/consumer-protection',
            'description': 'State consumer protection and fraud reporting'
        },
        'NV': {
            'name': 'Nevada Attorney General Bureau of Consumer Protection',
            'phone': '702-486-3132',
            'website': 'https://ag.nv.gov/Hot_Topics/Consumer_Protection',
            'description': 'State consumer protection and fraud reporting'
        },
        'NH': {
            'name': 'New Hampshire Attorney General Consumer Protection Bureau',
            'phone': '603-271-3641',
            'website': 'https://www.doj.nh.gov/consumer',
            'description': 'State consumer protection and fraud reporting'
        },
        'NJ': {
            'name': 'New Jersey Division of Consumer Affairs',
            'phone': '1-800-242-5846',
            'website': 'https://www.njconsumeraffairs.gov',
            'description': 'State consumer protection and fraud reporting'
        },
        'NM': {
            'name': 'New Mexico Attorney General Consumer Protection',
            'phone': '1-844-255-9210',
            'website': 'https://www.nmag.gov/consumer-environmental-protection',
            'description': 'State consumer protection and fraud reporting'
        },
        'NY': {
            'name': 'New York Attorney General Bureau of Consumer Frauds',
            'phone': '1-800-771-7755',
            'website': 'https://ag.ny.gov/bureau/consumer-frauds-bureau',
            'description': 'State consumer protection and fraud reporting'
        },
        'NC': {
            'name': 'North Carolina Attorney General Consumer Protection Division',
            'phone': '1-877-566-7226',
            'website': 'https://ncdoj.gov/protecting-consumers',
            'description': 'State consumer protection and fraud reporting'
        },
        'ND': {
            'name': 'North Dakota Attorney General Consumer Protection',
            'phone': '1-800-472-2600',
            'website': 'https://attorneygeneral.nd.gov/consumer-protection',
            'description': 'State consumer protection and fraud reporting'
        },
        'OH': {
            'name': 'Ohio Attorney General Consumer Protection Section',
            'phone': '1-800-282-0515',
            'website': 'https://www.ohioattorneygeneral.gov/Individuals-and-Families/Consumers',
            'description': 'State consumer protection and fraud reporting'
        },
        'OK': {
            'name': 'Oklahoma Attorney General Consumer Protection Unit',
            'phone': '405-521-2029',
            'website': 'https://www.oag.ok.gov/consumer-protection',
            'description': 'State consumer protection and fraud reporting'
        },
        'OR': {
            'name': 'Oregon Department of Justice Consumer Protection',
            'phone': '1-877-877-9392',
            'website': 'https://www.doj.state.or.us/consumer-protection',
            'description': 'State consumer protection and fraud reporting'
        },
        'PA': {
            'name': 'Pennsylvania Attorney General Bureau of Consumer Protection',
            'phone': '1-800-441-2555',
            'website': 'https://www.attorneygeneral.gov/protect-yourself/consumer-protection',
            'description': 'State consumer protection and fraud reporting'
        },
        'RI': {
            'name': 'Rhode Island Attorney General Consumer Protection Unit',
            'phone': '401-274-4400',
            'website': 'https://riag.ri.gov/divisions/consumer-protection',
            'description': 'State consumer protection and fraud reporting'
        },
        'SC': {
            'name': 'South Carolina Department of Consumer Affairs',
            'phone': '1-800-922-1594',
            'website': 'https://consumer.sc.gov',
            'description': 'State consumer protection and fraud reporting'
        },
        'SD': {
            'name': 'South Dakota Attorney General Consumer Protection',
            'phone': '1-800-300-1986',
            'website': 'https://atg.sd.gov/Consumers/default.aspx',
            'description': 'State consumer protection and fraud reporting'
        },
        'TN': {
            'name': 'Tennessee Division of Consumer Affairs',
            'phone': '1-800-342-8385',
            'website': 'https://www.tn.gov/consumer',
            'description': 'State consumer protection and fraud reporting'
        },
        'TX': {
            'name': 'Texas Attorney General Consumer Protection Division',
            'phone': '1-800-621-0508',
            'website': 'https://www.texasattorneygeneral.gov/consumer-protection',
            'description': 'State consumer protection and fraud reporting'
        },
        'UT': {
            'name': 'Utah Division of Consumer Protection',
            'phone': '801-530-6601',
            'website': 'https://consumerprotection.utah.gov',
            'description': 'State consumer protection and fraud reporting'
        },
        'VT': {
            'name': 'Vermont Attorney General Consumer Assistance Program',
            'phone': '1-800-649-2424',
            'website': 'https://ago.vermont.gov/cap',
            'description': 'State consumer protection and fraud reporting'
        },
        'VA': {
            'name': 'Virginia Attorney General Consumer Protection Section',
            'phone': '1-800-552-9963',
            'website': 'https://www.oag.state.va.us/consumer-protection',
            'description': 'State consumer protection and fraud reporting'
        },
        'WA': {
            'name': 'Washington Attorney General Consumer Protection Division',
            'phone': '1-800-551-4636',
            'website': 'https://www.atg.wa.gov/consumer-protection',
            'description': 'State consumer protection and fraud reporting'
        },
        'WV': {
            'name': 'West Virginia Attorney General Consumer Protection Division',
            'phone': '1-800-368-8808',
            'website': 'https://ago.wv.gov/consumerprotection',
            'description': 'State consumer protection and fraud reporting'
        },
        'WI': {
            'name': 'Wisconsin Department of Agriculture Trade & Consumer Protection',
            'phone': '1-800-422-7128',
            'website': 'https://datcp.wi.gov/Pages/Programs_Services/ConsumerProtection.aspx',
            'description': 'State consumer protection and fraud reporting'
        },
        'WY': {
            'name': 'Wyoming Attorney General Consumer Protection Unit',
            'phone': '307-777-7841',
            'website': 'https://ag.wyo.gov/divisions/consumer-protection',
            'description': 'State consumer protection and fraud reporting'
        },
        'DC': {
            'name': 'DC Office of the Attorney General Consumer Protection',
            'phone': '202-442-9828',
            'website': 'https://oag.dc.gov/consumer-protection',
            'description': 'District consumer protection and fraud reporting'
        },
    }

    # Federal resources (available to all states)
    FEDERAL_RESOURCES = {
        'ftc': {
            'name': 'Federal Trade Commission (FTC)',
            'phone': '1-877-382-4357',
            'website': 'https://reportfraud.ftc.gov',
            'description': 'Report identity theft and fraud to the FTC'
        },
        'ic3': {
            'name': 'FBI Internet Crime Complaint Center (IC3)',
            'phone': 'N/A - Online reporting only',
            'website': 'https://www.ic3.gov/Home/FileComplaint',
            'description': 'Report internet crimes to the FBI'
        },
        'identitytheft': {
            'name': 'IdentityTheft.gov',
            'phone': '1-877-438-4338',
            'website': 'https://identitytheft.gov',
            'description': 'Report and recover from identity theft'
        },
        'usps': {
            'name': 'U.S. Postal Inspection Service',
            'phone': '1-877-876-2455',
            'website': 'https://www.uspis.gov/report',
            'description': 'Report mail fraud and scams'
        },
        'irs': {
            'name': 'IRS Identity Protection Specialized Unit',
            'phone': '1-800-908-4490',
            'website': 'https://www.irs.gov/identity-theft-fraud-scams',
            'description': 'Report tax-related identity theft'
        },
        'ssa': {
            'name': 'Social Security Administration Fraud Hotline',
            'phone': '1-800-269-0271',
            'website': 'https://oig.ssa.gov/report',
            'description': 'Report Social Security fraud'
        },
    }

    @classmethod
    def get_resources_by_state(cls, state: str) -> List[LocalResource]:
        """Get all resources for a given state"""
        resources = []

        # Add state consumer office
        if state in cls.STATE_CONSUMER_OFFICES:
            office = cls.STATE_CONSUMER_OFFICES[state]
            resources.append(LocalResource(
                name=office['name'],
                type='State Consumer Protection',
                phone=office['phone'],
                website=office['website'],
                description=office['description']
            ))

        # Add federal resources
        for key, fed_resource in cls.FEDERAL_RESOURCES.items():
            resources.append(LocalResource(
                name=fed_resource['name'],
                type='Federal Agency',
                phone=fed_resource['phone'],
                website=fed_resource['website'],
                description=fed_resource['description']
            ))

        # Add general emergency services
        resources.append(LocalResource(
            name='Local Police Department (Non-Emergency)',
            type='Local Law Enforcement',
            phone='Find your local number at https://www.usa.gov/local-governments',
            website='https://www.usa.gov/local-governments',
            description='Your local police can take reports of cybercrimes'
        ))

        return resources

    @classmethod
    def get_resources_by_zip(cls, zip_code: str) -> Optional[List[LocalResource]]:
        """Get resources by ZIP code"""
        if not ZIPCodeValidator.validate(zip_code):
            return None

        state = ZIPToStateMapper.get_state(zip_code)
        if not state:
            return None

        return cls.get_resources_by_state(state)


class LocalResourceFormatter:
    """Formats local resources for display"""

    @staticmethod
    def format_resources(resources: List[LocalResource], state: str, zip_code: str) -> str:
        """Format resources as a readable message"""
        if not resources:
            return "Sorry, I couldn't find local resources for that ZIP code."

        message = f"## Local Resources for ZIP Code {zip_code} ({state})\n\n"
        message += "Here are the agencies and organizations you can contact to report cybercrimes and get help:\n\n"

        # Group by type
        state_resources = [r for r in resources if r.type == 'State Consumer Protection']
        federal_resources = [r for r in resources if r.type == 'Federal Agency']
        local_resources = [r for r in resources if r.type == 'Local Law Enforcement']

        # State resources
        if state_resources:
            message += "### State Resources\n\n"
            for resource in state_resources:
                message += f"**{resource.name}**\n"
                message += f"- **Phone:** {resource.phone}\n"
                message += f"- **Website:** {resource.website}\n"
                message += f"- **Description:** {resource.description}\n\n"

        # Federal resources
        if federal_resources:
            message += "### Federal Resources\n\n"
            for resource in federal_resources:
                message += f"**{resource.name}**\n"
                message += f"- **Phone:** {resource.phone}\n"
                message += f"- **Website:** {resource.website}\n"
                message += f"- **Description:** {resource.description}\n\n"

        # Local resources
        if local_resources:
            message += "### Local Law Enforcement\n\n"
            for resource in local_resources:
                message += f"**{resource.name}**\n"
                message += f"- **Phone:** {resource.phone}\n"
                message += f"- **Website:** {resource.website}\n"
                message += f"- **Description:** {resource.description}\n\n"

        message += "\n### What to Do Next:\n\n"
        message += "1. **Start with your state consumer protection office** - They handle most scam reports\n"
        message += "2. **File a report with the FTC** at reportfraud.ftc.gov\n"
        message += "3. **Report to IC3** if it involves internet crime\n"
        message += "4. **Contact local police** for serious crimes or threats\n"
        message += "5. **Keep records** of all reports and case numbers\n\n"
        message += "Would you like help with anything else, such as steps to protect your accounts or identity?"

        return message


def get_local_resources(zip_code: str) -> str:
    """Main function to get formatted local resources by ZIP code"""
    if not ZIPCodeValidator.validate(zip_code):
        return ("I need a valid 5-digit ZIP code to find your local resources. "
                "Please provide your ZIP code (for example: 10001 or 90210).")

    resources = LocalResourceDatabase.get_resources_by_zip(zip_code)
    if not resources:
        return ("I couldn't find resources for that ZIP code. "
                "Please make sure you entered a valid US ZIP code.")

    state = ZIPToStateMapper.get_state(zip_code)
    return LocalResourceFormatter.format_resources(resources, state, zip_code)


# Example usage
if __name__ == "__main__":
    # Test with different ZIP codes
    test_zips = ['10001', '90210', '60601', '33101', '02101']

    for zip_code in test_zips:
        print(f"\n{'='*80}")
        print(get_local_resources(zip_code))
        print(f"{'='*80}\n")
