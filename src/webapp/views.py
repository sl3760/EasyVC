from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, render_to_response, RequestContext, HttpResponseRedirect, HttpResponse

from django.views.decorators.csrf import csrf_exempt, csrf_protect

from models import*

from pymongo import Connection

import json

def judgeNull(field):
    if not field:
        return True
    
def handle_uploaded_image(f,imageFile):
    with open(imageFile, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()

def handle_uploaded_file(f,planFile):
    with open(planFile, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        
def home(request):
    return render_to_response("home.html",
                              locals(),
                              context_instance=RequestContext(request))

def thankyou(request):
    return render_to_response("thankyou.html",
                              locals(),
                              context_instance=RequestContext(request))

def VCSignup(request):
    if request.method == 'POST':
        userName = request.POST['userName']
        if judgeNull(userName):
            return HttpResponse("Field is null!")
        user = VCUser(userName=userName)
        email = request.POST['email']
        if judgeNull(email):
            return HttpResponse("Field is null!")
        password = request.POST['password']
        if judgeNull(password):
            return HttpResponse("Field is null!")
        repassword = request.POST['repassword']
        if password != repassword:
            return HttpResponse("Passwords are inconsistent!")
        firstName = request.POST['firstName']
        if judgeNull(firstName):
            return HttpResponse("Field is null!")
        lastName = request.POST['lastName']
        if judgeNull(lastName):
            return HttpResponse("Field is null!")
        
        position = request.POST['position']
        if judgeNull(position):
            return HttpResponse("Field is null!")
        imageName = userName+'.'+request.FILES['image'].name.split('.')[-1]
        imageFile = '../static/media/images/'+imageName
        user.image = '../media/images/'+imageName
        handle_uploaded_image(request.FILES['image'],imageFile)
        location = request.POST['location']
        if judgeNull(location):
            return HttpResponse("Field is null!")
        industry = request.POST.getlist('industry')
        if judgeNull(industry):
            return HttpResponse("Field is null!")
        amount = request.POST['amount']
        if judgeNull(amount):
            return HttpResponse("Field is null!")
        introduction = request.POST['introduction']
        if judgeNull(introduction):
            return HttpResponse("Field is null!")
        
        user.role = "VC"
        user.email = email
        user.password = password
        user.firstName = firstName
        user.lastName = lastName
        user.position = position
        user.location = location
        user.industry = industry
        user.amount = amount
        user.introduction = introduction
        user.save()
        request.session['user'] = user.userName
        '''      
        subject = "Thank you for your registration"
        message = "Welcome to EasyVC!"
        from_email = settings.EMAIL_HOST_USER
        to_list = [email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        '''
        return HttpResponseRedirect('/thankyou/')
    return render_to_response("VCSignup.html",
                              locals(),
                              context_instance=RequestContext(request))

def StartupSignup(request):
    if request.method == 'POST':
        userName = request.POST['userName']
        if judgeNull(userName):
            return HttpResponse("Field is null!")
        user = StartupUser(userName=userName)
        email = request.POST['email']
        if judgeNull(email):
            return HttpResponse("Field is null!")
        password = request.POST['password']
        if judgeNull(password):
            return HttpResponse("Field is null!")
        repassword = request.POST['repassword']
        if password != repassword:
            return HttpResponse("Passwords are inconsistent!")
        firstName = request.POST['firstName']
        if judgeNull(firstName):
            return HttpResponse("Field is null!")
        lastName = request.POST['lastName']
        if judgeNull(lastName):
            return HttpResponse("Field is null!")
        
        project = request.POST['project']
        if judgeNull(project):
            return HttpResponse("Field is null!")
        imageName = userName+'.'+request.FILES['image'].name.split('.')[-1]
        imageFile = '../static/media/images/'+imageName
        user.image = '../media/images/'+imageName
        handle_uploaded_image(request.FILES['image'],imageFile)
        fileName = userName+'.'+request.FILES['file'].name.split('.')[-1]
        planFile = '../static/media/plan/'+fileName
        user.businessPlan = '../media/plan/'+fileName
        handle_uploaded_file(request.FILES['file'],planFile)
               
        location = request.POST['location']
        if judgeNull(location):
            return HttpResponse("Field is null!")
        industry = request.POST.getlist('industry')
        if judgeNull(industry):
            return HttpResponse("Field is null!")
        amount = request.POST['amount']
        if judgeNull(amount):
            return HttpResponse("Field is null!")
        introduction = request.POST['introduction']
        if judgeNull(introduction):
            return HttpResponse("Field is null!")
        
        user.role = "Startup"
        user.email = email
        user.password = password
        user.firstName = firstName
        user.lastName = lastName
        user.project = project
        user.location = location
        user.industry = industry
        user.amount = amount
        user.introduction = introduction
        user.save()
        request.session['user'] = user.userName
        '''      
        subject = "Thank you for your registration"
        message = "Welcome to EasyVC!"
        from_email = settings.EMAIL_HOST_USER
        to_list = [email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        '''
        return HttpResponseRedirect('/thankyou/')
    return render_to_response("StartupSignup.html",
                              locals(),
                              context_instance=RequestContext(request))

def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        login = False
        for user in VCUser.objects:
            if email==user.email:
                if password==user.password:
                    login = True
                    request.session['user'] = user.userName
                    return HttpResponseRedirect('/VCUI/')
                else:
                    return HttpResponse("Login unsuccessfully!")
        for user in StartupUser.objects:
            if email==user.email:
                if password==user.password:
                    login = True
                    request.session['user'] = user.userName
                    return HttpResponseRedirect('/startupUI/')
                else:
                    return HttpResponse("Login unsuccessfully!")
        if(not login):
            return HttpResponse("Login unsuccessfully!")
        
def VCUI(request):
    users = VCUser.objects
    return render_to_response("VCUI.html",
                                locals(),
                                context_instance=RequestContext(request))

@csrf_exempt
def VCUpdate(request):
    if request.is_ajax():
        industry = request.POST['industry']
        amount = request.POST['amount']
        location = request.POST['location']
        lists = getVCUsers(industry,amount,location)
        return HttpResponse(lists.to_json(), content_type="application/json")
    
@csrf_exempt
def startupUpdate(request):
    if request.is_ajax():
        industry = request.POST['industry']
        amount = request.POST['amount']
        location = request.POST['location']
        lists = getStartupUsers(industry,amount,location)
        return HttpResponse(lists.to_json(), content_type="application/json")

def startupUI(request):   
    users = StartupUser.objects
    return render_to_response("startupUI.html",
                              locals(),
                              context_instance=RequestContext(request))

def signout(request):
    try:
        del request.session['user']
    except KeyError:
        pass
    return HttpResponseRedirect("http://127.0.0.1:8000")

def editVC(request):
    userName = request.session['user']
    user = getUser('VC',userName)
    return render_to_response("editVC.html",
                                locals(),
                                context_instance=RequestContext(request))

def editStartup(request):
    userName = request.session['user']
    user = getUser('startup',userName)
    return render_to_response("editStartup.html",
                                locals(),
                                context_instance=RequestContext(request))

@csrf_exempt
def VCEditUpdate(request):
    userName = request.session['user']
    if "firstName" in request.POST:
        updateVCFirstName(userName, request.POST['firstName'])
    if "lastName" in request.POST:
        updateVCLastName(userName, request.POST['lastName'])
    return render_to_response("editVC.html",
                                locals(),
                                context_instance=RequestContext(request))

@csrf_exempt
def showVC(request, userName):
    user = getUser('VC',userName)
    return render_to_response("showVC.html",
                                locals(),
                                context_instance=RequestContext(request))

@csrf_exempt
def showStartup(request):
    user = getUser('startup',userName)
    return render_to_response("showStartup.html",
                                locals(),
                                context_instance=RequestContext(request))
