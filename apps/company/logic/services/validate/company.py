
class ValidateCompanyPayload:
    def __init__(self, payload):
        self.payload = payload

    def validate(self):
        """Validate the company creation payload."""
        if not isinstance(self.payload, dict):
            raise ValueError("Payload must be a dictionary.")
        
        required_fields = ["company_details", "address", "bank_account"]
        for field in required_fields:
            if field not in self.payload:
                raise ValueError(f"Missing required field: {field}")
        
        return True

class ValidateCompanyDetails:
    def __init__(self, company_details):
        self.company_details = company_details

    def validate(self):
        """Validate the company details."""
        errors = []
        
        if not self.company_details.name:
            errors.append("Company name is required.")
        
        if not self.company_details.email:
            errors.append("Email is required.")
        
        if not self.company_details.phone:
            errors.append("Phone number is required.")
        
        if errors:
            raise ValueError("Validation errors: " + ", ".join(errors))
        
        return True

class ValidateCompanyAddress:
    def __init__(self, address):
        self.address = address

    def validate(self):
        """Validate the company address."""
        errors = []
        
        if not self.address.address_line1:
            errors.append("Address line 1 is required.")
        
        if not self.address.city:
            errors.append("City is required.")
        
        if not self.address.state:
            errors.append("State is required.")
        
        if not self.address.postal_code:
            errors.append("Postal code is required.")
        
        if not self.address.country:
            errors.append("Country is required.")
        
        if errors:
            raise ValueError("Validation errors: " + ", ".join(errors))
        
        return True


class ValidateCompanyBankAccount:
    def __init__(self, bank_account):
        self.bank_account = bank_account

    def validate(self):
        """Validate the company bank account."""
        errors = []
        
        if not self.bank_account.account_number:
            errors.append("Account number is required.")
        
        if not self.bank_account.account_name:
            errors.append("Account name is required.")
        
        if not self.bank_account.bank_name:
            errors.append("Bank name is required.")
        
        if not self.bank_account.ifsc_code:
            errors.append("IFSC code is required.")
        
        if errors:
            raise ValueError("Validation errors: " + ", ".join(errors))
        
        return True