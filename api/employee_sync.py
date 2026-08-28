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
