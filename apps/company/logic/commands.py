
import json
import traceback
import sys
from apps.utils.common.logger.logger import PortalLogger
from apps.company.logic.services.crud.company import ArchiveCompany, CreateCompanyRecords, RestoreCompany, UpdateCompanyRecords, DeleteCompany
from apps.utils.common.abstract.create_interface import CreateCommand
from apps.company.logic.services.validate import company as validate_company

logger = PortalLogger(__name__)

# ADD verification layer to every command to check the validity of action
class CompanyCreateCommand(CreateCommand):
    def __init__(self, request):
        self.request = request
        self.body = json.loads(request.body)
    
    def create(self):
        try:
            result = CreateCompanyRecords(
                company_details=self.body.get("details"),
                address=self.body.get("address"),
                bank_account=self.body.get("bankAccount")
            ).create()
            if not result["success"]:
                return {"code": result["code"], "success": False, "message": result["message"], "data": None}
            return {"code": 201, "success": True, "message": "Company created successfully", "data": None}
        except KeyError as e:
            logger.error(f"KeyError: {str(e)} - {traceback.format_exc()}")
            return {"code": 400, "success": False, "message": f"Missing key in request body: {str(e)}", "data": None}
        except json.JSONDecodeError:
            logger.error("Invalid JSON format in request body")
            return {"code": 400, "success": False, "message": "Invalid JSON format", "data": None}
        except Exception as e:
            logger.error(f"Internal server error: {str(e)}")
            return {"code": 500, "success": False, "message": f"Internal server error: {str(e)}", "data": None}
    
    def validate(self):
        try:
            # Validate the request body
            payload_validate = validate_company.ValidateCompanyPayload(self.body).validate()
            if not payload_validate["success"]:
                return {"code": 400, "success": False, "message": payload_validate["message"], "data": None}
            
            # Validate company details
            details_validate = validate_company.ValidateCompanyDetails(self.body.get("company_details")).validate()
            if not details_validate["success"]:
                return {"code": 400, "success": False, "message": details_validate["message"], "data": None}

            # Validate company address
            address_validate = validate_company.ValidateCompanyAddress(self.body.get("address")).validate()
            if not address_validate["success"]:
                return {"code": 400, "success": False, "message": address_validate["message"], "data": None}

            # Validate company bank account
            bank_account_validate = validate_company.ValidateCompanyBankAccount(self.body.get("bank_account")).validate()
            if not bank_account_validate["success"]:
                return {"code": 400, "success": False, "message": bank_account_validate["message"], "data": None}

            return {"code": 200, "success": True, "message": "Validation successful", "data": None}
        except json.JSONDecodeError:
            logger.error("Invalid JSON format in request body")
            return {"code": 400, "success": False, "message": "Invalid JSON format", "data": None}
        except Exception as e:
            logger.error(f"Internal server error: {str(e)}")
            return {"code": 500, "success": False, "message": f"Internal server error: {str(e)}", "data": None}

    def execute(self):
        validation_result = self.validate()
        if not validation_result["success"]:
            return {"code": validation_result["code"], "status": "error", "message": validation_result["message"], "data": None}
        
        # Create company records
        result = self.create()
        if not result.get("success", True):
            return {"code": 500, "status": "error", "message": "Failed to create company records", "data": None}
        
        return {"code": 201, "status": "success", "message": "Company created successfully", "data": None}

class CompanyUpdateCommand:
    def __init__(self, request):
        self.request = request
        self.body = json.loads(request.body)
    
    def update(self):
        try:
            result = UpdateCompanyRecords(
                company_id=self.body.get("id"),
                company_details=self.body.get("details"),
                address=self.body.get("address"),
                bank_account=self.body.get("bankAccount")
            ).update()
            if not result["success"]:
                return {"code": result["code"], "success": False, "message": result["message"], "data": None}
            return {"code": 200, "success": True, "message": "Company updated successfully", "data": None}
        except KeyError as e:
            logger.error(f"KeyError: {str(e)} - {traceback.format_exc()}")
            return {"code": 400, "success": False, "message": f"Missing key in request body: {str(e)}", "data": None}
        except json.JSONDecodeError:
            logger.error("Invalid JSON format in request body")
            return {"code": 400, "success": False, "message": "Invalid JSON format", "data": None}
        except Exception as e:
            logger.error(f"Internal server error: {str(e)}")
            return {"code": 500, "success": False, "message": f"Internal server error: {str(e)}", "data": None}
    
    def validate(self):
        # Logic to validate the updated company details
        try:
            # Validate the request body
            payload_validate = validate_company.ValidateCompanyPayload(self.body).validate()
            if not payload_validate["success"]:
                return {"code": 400, "success": False, "message": payload_validate["message"], "data": None}
            
            # Validate company details
            details_validate = validate_company.ValidateCompanyDetails(self.body.get("company_details")).validate()
            if not details_validate["success"]:
                return {"code": 400, "success": False, "message": details_validate["message"], "data": None}

            # Validate company address
            address_validate = validate_company.ValidateCompanyAddress(self.body.get("address")).validate()
            if not address_validate["success"]:
                return {"code": 400, "success": False, "message": address_validate["message"], "data": None}

            # Validate company bank account
            bank_account_validate = validate_company.ValidateCompanyBankAccount(self.body.get("bank_account")).validate()
            if not bank_account_validate["success"]:
                return {"code": 400, "success": False, "message": bank_account_validate["message"], "data": None}

            return {"code": 200, "success": True, "message": "Validation successful", "data": None}
        except json.JSONDecodeError:
            logger.error("Invalid JSON format in request body")
            return {"code": 400, "success": False, "message": "Invalid JSON format", "data": None}
        except Exception as e:
            logger.error(f"Internal server error: {str(e)}")
            return {"code": 500, "success": False, "message": f"Internal server error: {str(e)}", "data": None}

    def execute(self):
        # Logic to update an existing company
        validation_result = self.validate()
        if not validation_result["success"]:
            return {"code": validation_result["code"], "status": "error", "message": validation_result["message"], "data": None}

        # Update company records
        # result = self.update()
        # if not result.get("success", True):
        #     return {"code": 500, "status": "error", "message": "Failed to update company records", "data": None}

        return {"code": 200, "status": "success", "message": "Company updated successfully", "data": None}

class CompanyArchiveCommand:
    def __init__(self, request):
        self.company_id = request.get("id")

    def execute(self):
        # Logic to archive a company
        archive_service = ArchiveCompany(self.company_id)
        return archive_service.archive()

class CompanyRestoreCommand:
    def __init__(self, request):
        self.company_id = request.get("id")

    def execute(self):
        # Logic to restore an archived company
        restore_service = RestoreCompany(self.company_id)
        return restore_service.restore()

class CompanyDeleteCommand:
    def __init__(self, request):
        self.company_id = request.get("id")

    def execute(self):
        # Logic to delete a company
        delete_service = DeleteCompany(self.company_id)
        return delete_service.delete()

class CompanyRetrieveCommand:
    def __init__(self, company_id):
        self.company_id = company_id

    def execute(self):
        # Logic to retrieve a company's details
        pass
    