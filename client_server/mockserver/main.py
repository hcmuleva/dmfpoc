# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
def getErrorMessage(key):
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
    
    return errors[key]
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(getErrorMessage("DeletingTenantError"))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
