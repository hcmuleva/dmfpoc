
class InternalServerError(Exception):
    pass

class SchemaValidationError(Exception):
    pass

class TenantAlreadyExistsError(Exception):
    pass

class UpdatingTenantError(Exception):
    pass

class DeletingTenantError(Exception):
    pass

class TenantNotExistsError(Exception):
    pass
class InvalidPayLoadError(Exception):
    pass
class InvalidTokenError(Exception):
    pass


errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
     "SchemaValidationError": {
         "message": "Request is missing required fields",
         "status": 400
     },
     "TenantAlreadyExistsError": {
         "message": "Tenant with given id already exists",
         "status": 400
     },
     "UpdatingTenantError": {
         "message": "Updating tenant added by other is forbidden",
         "status": 403
     },
     "DeletingTenantError": {
         "message": "Deleting tenant added by other is forbidden",
         "status": 403
     },
     "TenantNotExistsError": {
         "message": "Tenant with given id doesn't exists",
         "status": 400
     },
     "InvalidTokenError": {
         "message": "Invalid token",
         "status": 400
     },
    "InvalidPayLoadError":{
        "message": "Invalid token",
        "status": 400
    }

}