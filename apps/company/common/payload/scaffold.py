
from apps.utils.common.validation.general_validations import FieldSpecificValidationService as field_validation_service

COMPANY_SCAFFOLD = {
    "details": {
        "companyName": {"type": str, "required": True, "validator": field_validation_service().email},
        "phone": {"type": str, "required": True, "validator": field_validation_service().phone},
        "email": {"type": str, "required": True, "validator": field_validation_service().email},
        "affiliatedPartner": {"type": int, "required": False},
        "website": {"type": str, "required": False},
        "taxId": {"type": str, "required": True, "validator": field_validation_service().tax_id},
        "establishedDate": {"type": str, "required": False, "validator": field_validation_service().date},
        "description": {"type": str, "required": False}
    },
    "address": {
        "addressLine1": {"type": str, "required": True},
        "addressLine2": {"type": str, "required": False},
        "city": {"type": str, "required": True},
        "state": {"type": str, "required": True},
        "postalCode": {"type": str, "required": True},
        "country": {"type": str, "required": True}
    },
    "bankAccount": {
        "accountNumber": {"type": str, "required": True},
        "accountName": {"type": str, "required": True},
        "bankName": {"type": str, "required": True},
        "ifscCode": {"type": str, "required": False}
    }
}