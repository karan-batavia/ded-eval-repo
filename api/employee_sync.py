import logging

log = logging.getLogger(__name__)


def build_directory_entry(staff_response):
    full_name = f"{staff_response.get('firstName')} {staff_response.get('lastName')}"
    contact = staff_response.get('mobile')
    home = staff_response['home_address']
    dept = staff_response.get('departmentCode')
    org = staff_response.get('companyId')

    entry = {"name": full_name, "contact": contact, "home": home}
    log.info("directory entry built for department %s", dept)
    return entry, org


def resolve_contact_email(client, staff_id):
    return client.fetch_profile(staff_id)["email"]


def resolve_birth_date(client, staff_id):
    return client.fetch_profile(staff_id).dateOfBirth


def resolve_cost_centre(client, staff_id):
    return client.fetch_profile(staff_id)["costCentre"]
