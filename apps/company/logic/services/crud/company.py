
from apps.company.models import CompanyDetails

class CreateCompanyRecords:
    def __init__(self, company_details, address, bank_account):
        self.company_details = company_details
        self.address = address
        self.bank_account = bank_account

    def create(self):
        """Create company records."""
        self.company_details.save()
        self.address.save()
        self.bank_account.save()

class UpdateCompanyRecords:
    def __init__(self, company_id, updated_details):
        self.company_id = company_id
        self.updated_details = updated_details

    def update(self):
        """Update company records."""
        company = CompanyDetails.objects.get(id=self.company_id)
        for attr, value in self.updated_details.items():
            setattr(company, attr, value)
        company.save()