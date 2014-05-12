from mongoengine import *

connect('easyvc')

class VCUser(Document):
    userName = StringField(required = True)
    email = EmailField(required = True)
    password = StringField(required = True)
    firstName = StringField(required = True)
    lastName = StringField(required = True)
    role = StringField(required = True)
    image = StringField()
    position = StringField()
    location = StringField()
    industry = ListField()
    amount = LongField()
    introduction = StringField()
    
class StartupUser(Document):
    userName = StringField(required = True)
    email = EmailField(required = True)
    password = StringField(required = True)
    firstName = StringField(required = True)
    lastName = StringField(required = True)
    role = StringField(required = True)
    image = StringField()
    project = StringField()
    location = StringField()
    industry = ListField()
    amount = LongField()
    introduction = StringField()
    businessPlan = StringField()

def getVCUsers(industry, amount, location):
    if industry == "All" and amount == "All" and location == "All":
        return VCUser.objects
    elif industry == "All" and amount == "All":
        return VCUser.objects(location=location)
    elif industry == "All" and location == "All":
        return VCUser.objects(amount=amount)
    elif amount == "All" and location == "All":
        return VCUser.objects(industry=industry)
    elif industry == "All":
        return VCUser.objects(amount=amount,location=location)
    elif amount == "All":
        return VCUser.objects(industry=industry,location=location)
    elif location == "All":
        return VCUser.objects(industry=industry,amount=amount)
    else:
        return VCUser.objects(industry=industry,amount=amount,location=location)
    
def getStartupUsers(industry, amount, location):
    if industry == "All" and amount == "All" and location == "All":
        return StartupUser.objects
    elif industry == "All" and amount == "All":
        return StartupUser.objects(location=location)
    elif industry == "All" and location == "All":
        return StartupUser.objects(amount=amount)
    elif amount == "All" and location == "All":
        return StartupUser.objects(industry=industry)
    elif industry == "All":
        return StartupUser.objects(amount=amount,location=location)
    elif amount == "All":
        return StartupUser.objects(industry=industry,location=location)
    elif location == "All":
        return StartupUser.objects(industry=industry,amount=amount)
    else:
        return StartupUser.objects(industry=industry,amount=amount,location=location)

def getUser(role, userName):
    if role == 'VC':
        return VCUser.objects.get(userName=userName)
    elif role =='startup':
        return StartupUser.objects.get(userName=userName)

def updateVCFirstName(userName, firstName):
    VCUser.objects(userName=userName).update_one(set__firstName=firstName)
    
def updateVCLastName(userName, lastName):
    VCUser.objects(userName=userName).update_one(set__lastName=lastName)    
    