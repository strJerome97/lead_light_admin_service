
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
            details_res = self.create_company_details()
            if not details_res["success"]:
                return {"code": details_res["code"], "success": False, "message": details_res["message"], "data": None}
            self.create_company_address(details_res["data"])
            self.create_company_bank_account(details_res["data"])

            return {"code": 201, "success": True, "message": "Company records created successfully", "data": None}
        except Exception as e:
            logger.error(f"Internal server error: {str(e)}")
            return {"code": 500, "success": False, "message": f"Internal server error: {str(e)}", "data": None}
    
    def create_company_details(self):
        try:
            """Create company details."""
            adapted_details = RecordAdapter().adapt_company_details(self.company_details)
            if not adapted_details:
                logger.error("Invalid data format for company records.")
                return {"code": 400, "success": False, "message": "Invalid data format", "data": None}
            data = CompanyDetails.objects.create(**adapted_details)
            return {"code": 201, "success": True, "message": "Company details created successfully", "data": data}
        except Exception as e:
            logger.error(f"Internal server error: {str(e)}")
            return {"code": 500, "success": False, "message": f"Internal server error: {str(e)}", "data": None}
    
    def create_company_address(self, company):
        """Create company address."""
        try:
            adapted_address = RecordAdapter().adapt_address(self.address, fkey=company)
            if not adapted_address:
                logger.error("Invalid data format for company address.")
            CompanyAddress.objects.create(**adapted_address)
        except Exception as e:
            logger.error(f"Internal server error: {str(e)}")
    
    def create_company_bank_account(self, company):
        """Create company bank account."""
        try:
            adapted_bank_account = RecordAdapter().adapt_bank_account(self.bank_account, fkey=company)
            if not adapted_bank_account:
                logger.error("Invalid data format for company bank account.")
            CompanyBankAccount.objects.create(**adapted_bank_account)
        except Exception as e:
            logger.error(f"Internal server error: {str(e)}")

class UpdateCompanyRecords:
    def __init__(self, company_id, company_details, address, bank_account):
        self.company_id = company_id
        self.company_details = company_details
        self.address = address
        self.bank_account = bank_account

    def update(self):
        """Update company records."""
        try:
            company_obj = self.update_company_details()
            if not company_obj["success"]:
                return {"code": company_obj["code"], "success": False, "message": company_obj["message"], "data": None}
            self.update_company_address(company_obj["data"])
            self.update_company_bank_account(company_obj["data"])
            return {"code": 200, "success": True, "message": "Company records updated successfully", "data": None}
        except Exception as e:
            logger.error(f"Internal server error: {str(e)}")
            return {"code": 500, "success": False, "message": f"Internal server error: {str(e)}", "data": None}
    
    def update_company_details(self):
        """Update company details."""
        try:
            adapted_details = RecordAdapter().adapt_company_details(self.company_details)
            if not adapted_details:
                logger.error("Invalid data format for company records.")
                return {"code": 400, "success": False, "message": "Invalid data format", "data": None}
            obj = CompanyDetails.objects.filter(id=self.company_id).first()
            if not obj:
                logger.error("Company details not found.")
                return {"code": 404, "success": False, "message": "Company details not found", "data": None}
            obj.update(**adapted_details)
            return {"code": 200, "success": True, "message": "Company details updated successfully", "data": obj}
        except Exception as e:
            logger.error(f"Internal server error: {str(e)}")
            return {"code": 500, "success": False, "message": f"Internal server error: {str(e)}", "data": None}

    def update_company_address(self, company):
        """Update company address."""
        try:
            adapted_address = RecordAdapter().adapt_address(self.address, fkey=company)
            if not adapted_address:
                logger.error("Invalid data format for company address.")
                return {"code": 400, "success": False, "message": "Invalid data format for address", "data": None}
            obj = CompanyAddress.objects.filter(company=company).first()
            if not obj:
                logger.error("Company address not found.")
                return {"code": 404, "success": False, "message": "Company address not found", "data": None}
            obj.update(**adapted_address)
        except Exception as e:
            logger.error(f"Internal server error: {str(e)}")
            return {"code": 500, "success": False, "message": f"Internal server error: {str(e)}", "data": None}

    def update_company_bank_account(self, company):
        """Update company bank account."""
        try:
            adapted_bank_account = RecordAdapter().adapt_bank_account(self.bank_account, fkey=company)
            if not adapted_bank_account:
                logger.error("Invalid data format for company bank account.")
                return {"code": 400, "success": False, "message": "Invalid data format for bank account", "data": None}
            obj = CompanyBankAccount.objects.filter(company=company).first()
            if not obj:
                logger.error("Company bank account not found.")
                return {"code": 404, "success": False, "message": "Company bank account not found", "data": None}
            obj.update(**adapted_bank_account)
        except Exception as e:
            logger.error(f"Internal server error: {str(e)}")
            return {"code": 500, "success": False, "message": f"Internal server error: {str(e)}", "data": None}
