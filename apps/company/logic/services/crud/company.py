
from apps.utils.common.logger.logger import PortalLogger
from apps.company.models import CompanyDetails, CompanyAddress, CompanyBankAccount

logger = PortalLogger(__name__)

class RecordAdapter:
    def adapt_company_details(self, record):
        try:
            params = {
                "name": record.get("companyName", None),
                "email": record.get("email", None),
                "phone": record.get("phone", None),
                "affiliated_partner": record.get("affiliatedPartner", None),
                "website": record.get("website", None),
                "tax_id": record.get("taxId", None),
                "established_date": record.get("establishedDate", None),
                "description": record.get("description", None),
            }
            return params
        except Exception as e:
            logger.error(f"Internal server error: {str(e)}")
            return False

    def adapt_address(self, record, fkey=None):
        try:
            params = {
                "company": fkey,
                "address_line1": record.get("addressLine1", None),
                "address_line2": record.get("addressLine2", None),
                "city": record.get("city", None),
                "state": record.get("state", None),
                "postal_code": record.get("postalCode", None),
                "country": record.get("country", None),
            }
            return params
        except Exception as e:
            logger.error(f"Internal server error: {str(e)}")
            return False

    def adapt_bank_account(self, record, fkey=None):
        try:
            params = {
                "company": fkey,
                "account_number": record.get("accountNumber", None),
                "account_name": record.get("accountName", None),
                "bank_name": record.get("bankName", None),
                "ifsc_code": record.get("ifscCode", None),
            }
            return params
        except Exception as e:
            logger.error(f"Internal server error: {str(e)}")
            return False
        
class CreateCompanyRecords:
    def __init__(self, company_details, address, bank_account):
        self.company_details = company_details
        self.address = address
        self.bank_account = bank_account

    def create(self):
        """Create company records."""
        try:
            adapted_details = RecordAdapter().adapt_company_details(self.company_details)
            
            if not adapted_details:
                logger.error("Invalid data format for company records.")
                return {"code": 400, "success": False, "message": "Invalid data format", "data": None}
            
            details_res = CompanyDetails.objects.create(**adapted_details)
            if not details_res:
                logger.error("Failed to create company details.")
                return {"code": 500, "success": False, "message": "Failed to create company details", "data": None}
            
            adapted_address = RecordAdapter().adapt_address(self.address, fkey=details_res)
            if not adapted_address:
                logger.error("Invalid data format for company address.")
                return {"code": 400, "success": False, "message": "Invalid data format for address", "data": None}
            CompanyAddress.objects.create(**adapted_address)
            
            adapted_bank_account = RecordAdapter().adapt_bank_account(self.bank_account, fkey=details_res)
            if not adapted_bank_account:
                logger.error("Invalid data format for company bank account.")
                return {"code": 400, "success": False, "message": "Invalid data format for bank account", "data": None}
            CompanyBankAccount.objects.create(**adapted_bank_account)

            return {"code": 201, "success": True, "message": "Company records created successfully", "data": None}
        except Exception as e:
            logger.error(f"Internal server error: {str(e)}")
            return {"code": 500, "success": False, "message": f"Internal server error: {str(e)}", "data": None}
    
    def create_company_details(self):
        try:
            """Create company details."""
            adapted_details = RecordAdapter().adapt_company_details(self.company_details)
            return CompanyDetails.objects.create(**adapted_details)
        except Exception as e:
            logger.error(f"Internal server error: {str(e)}")
            return {"code": 500, "success": False, "message": f"Internal server error: {str(e)}", "data": None}
    
    def create_company_address(self, company):
        """Create company address."""
        adapted_address = RecordAdapter().adapt_address(self.address, fkey=company)
        return CompanyAddress.objects.create(**adapted_address)
    
    def create_company_bank_account(self, company):
        """Create company bank account."""
        adapted_bank_account = RecordAdapter().adapt_bank_account(self.bank_account, fkey=company)
        return CompanyBankAccount.objects.create(**adapted_bank_account)

class UpdateCompanyRecords:
    def __init__(self, company_id, updated_details):
        self.company_id = company_id
        self.updated_details = updated_details

    def update(self):
        """Update company records."""
        pass
    
    def update_company_details(self):
        """Update company details."""
        pass
    
    def update_company_address(self, company):
        """Update company address."""
        pass

    def update_company_bank_account(self, company):
        """Update company bank account."""
        pass
