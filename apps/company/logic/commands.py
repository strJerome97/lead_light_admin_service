
import json
from apps.company.logic.services.crud.company import CreateCompanyRecords
from apps.utils.common.abstract.create_interface import CreateCommand
from apps.company.logic.services.validate import company as validate_company

# ADD verification layer to every command to check the validity of action
class CompanyCreateCommand(CreateCommand):
    def __init__(self, request):
        self.request = request
        self.body = json.loads(request.body)
    
    def create(self):
        pass  # This method is abstract and will be implemented in the execute method
    
    def validate(self):
        pass
        # Validate the request body
        
        # Validate company details
        
        # Validate company address
        
        # Validate company bank account

    def execute(self):
        # Logic to create a new company
        company_records = CreateCompanyRecords(
            company_details=self.company_details,
            address=self.address,
            bank_account=self.bank_account
        )
        company_records.create()

class CompanyUpdateCommand:
    def __init__(self, company_id, updated_details):
        self.company_id = company_id
        self.updated_details = updated_details

    def execute(self):
        # Logic to update an existing company
        pass

class CompanyArchiveCommand:
    def __init__(self, company_id):
        self.company_id = company_id

    def execute(self):
        # Logic to archive a company
        pass

class CompanyRestoreCommand:
    def __init__(self, company_id):
        self.company_id = company_id

    def execute(self):
        # Logic to restore an archived company
        pass

class CompanyDeleteCommand:
    def __init__(self, company_id):
        self.company_id = company_id

    def execute(self):
        # Logic to delete a company
        pass

class CompanyRetrieveCommand:
    def __init__(self, company_id):
        self.company_id = company_id

    def execute(self):
        # Logic to retrieve a company's details
        pass