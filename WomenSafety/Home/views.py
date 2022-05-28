
from django.conf import settings
from django.shortcuts import render, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from twilio.rest import Client
from twilio import twiml
account_sid = ""
auth_token = ""

# password : women123
# Create your views here.
@login_required(login_url = settings.LOGIN_URL)
def index(request):
    print(request.user)
    if request.user.is_anonymous:
        return redirect("/login") 
    return render(request, 'index.html')

def loginUser(request):
    if request.method=="POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(username, password, email)

        # check if user has entered correct credentials
        user = authenticate(username=username, email=email, password=password)

        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            return redirect("/")

        else:
            # No backend authenticated the credentials
            return render(request, 'login.html')

    return render(request, 'login.html')

@login_required(login_url = settings.LOGIN_URL)
def logoutUser(request):
    logout(request)
    return redirect("/login")

def about(request):
    return render(request,'about.html')
    #return HttpResponse("this is about page")

@login_required(login_url = settings.LOGIN_URL)
def contact(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        desc=request.POST.get('desc')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        messages.success(request, 'Your message has been sent successfully!')
    return render(request,'contact.html')
    # return HttpResponse("this is contact page")

def registerUser(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username is already taken.")
                return render(request,'register.html')
            elif User.object.filter(email=email).exists():
                messages.info(request,"Email Address is already taken.")
                return render(request,'register.html')
            else:
                user=User.objects.create_user(username=username,email=email,password=password1,first_name=first_name,last_name=last_name)
                user.save()
                messages.success(request,"Account created successfully!")
                return redirect("/login")
        else:
            messages.info(request,"Password mismatched.")
            return render(request,'register.html')
    else:
        return render(request,'register.html')

@login_required(login_url = settings.LOGIN_URL)
def sendSMS(request):
    body = request.POST["message"]
    location = request.POST["location"]
    body = "Your patient " +str(PatientUser.objects.get(user = request.user).name)+ " is currently at "+location +" and is in an emergency. He/she sends the message : "+body 
    contacts = Contact.objects.filter(user = request.user)
    
    for contact in contacts:
        client = Client(account_sid, auth_token)
        phno = "+91" + str(contact.phonenumber)
        message = client.messages \
                .create(
                     body=body,
                     from_='+14176402714',
                     to= phno
                 )
       
    messages.success(request, 'Message sent successfully.')
    return redirect("index")

@login_required(login_url = settings.LOGIN_URL)
def sendMail(request):
    if request.method=="POST":
        toemail=request.POST.get('to')
        fromemail=request.POST.get('fromemail')
        message=request.POST.get('message')
        
        send_mail(
            'Subject here',
            message,
            fromemail,
            [toemail],
            fail_silently=False,
        )
        messages.success(request,"Mail has been sent successfully!")
        return redirect("/")
    return render(request,'mail.html')

@login_required(login_url = settings.LOGIN_URL)
def fakeRingtone(request):
    pass