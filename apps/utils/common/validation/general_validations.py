import re
from datetime import datetime

class GeneralValidationService:
    """
    General validation service for incoming data.
    This service validates data against a predefined scaffold.
    It checks for required fields, types, and specific validators.
    Usage:
        validation_service = GeneralValidationService(scaffold)
        result = validation_service.validate(data_dict)
    """
    def __init__(self, scaffold):
        self.scaffold = scaffold
        
    def validate(self, data_dict):
        try:
            for key, rules in self.scaffold.items():
                if key not in data_dict:
                    if rules.get("required"):
                        return {"code": 400, "success": False, "message": f"Missing required field: {key}", "data": None}
                else:
                    value = data_dict[key]
                    if not isinstance(value, rules["type"]):
                        return {"code": 400, "success": False, "message": f"Invalid type for field: {key}", "data": None}
                    if "validator" in rules:
                        validation_result = rules["validator"](value)
                        if not validation_result:
                            return {"code": 400, "success": False, "message": f"Validation failed for field: {key}", "data": None}
            return {"code": 200, "success": True, "message": "Validation successful", "data": data_dict}
        except Exception as e:
            return {"code": 500, "success": False, "message": f"Internal server error: {str(e)}", "data": None}

class FieldSpecificValidationService:
    """
    Field-specific validation service for incoming data.
    This service validates data against specific field rules.
    It includes methods for validating email, tax ID, phone numbers, and dates.
    Usage:
        validation_service = FieldSpecificValidationService()
        is_valid_email = validation_service.email("test@example.com")
        is_valid_tax_id = validation_service.tax_id("123-456-789")
        is_valid_phone = validation_service.phone("09123456789")
        is_valid_date = validation_service.date("2023-01-01")
    """
    def email(self, email):
        """Validate email format."""
        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        return bool(re.match(pattern, email))
    
    def tax_id(self, tax_id):
        """
        Validate tax ID format.
        Add specific validation logic for tax IDs for multiple countries if necessary.
        """
        # Philippine TIN: 9-12 digits, usually written as XXX-XXX-XXX or XXX-XXX-XXX-XXX
        pattern = r"^\d{3}-\d{3}-\d{3}$|^\d{3}-\d{3}-\d{3}-\d{3}$|^\d{9}$|^\d{12}$"
        return bool(re.match(pattern, tax_id))
        
    def phone(self, phone):
        """
        Validate phone number format.
        Add specific validation logic for phone numbers for multiple countries if necessary.
        """
        # Philippine mobile numbers: start with '09' or '+639', followed by 9 digits
        pattern = r"^(09\d{9}|\+639\d{9})$"
        return bool(re.match(pattern, phone))
    
    def date(self, date_str):
        """
        Validate date format.
        Add specific validation logic for date formats if necessary.
        """
        pattern = r"^\d{4}-\d{2}-\d{2}$"
        if not re.match(pattern, date_str):
            return False
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    