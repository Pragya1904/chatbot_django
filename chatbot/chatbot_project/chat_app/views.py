import threading

from django.shortcuts import render,redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from .models import Chat
from .utils import ask_gemini,response_queue

from django.utils import timezone

@csrf_exempt
def check_response_status(request):
    if request.method == 'GET':
        # Check if response is available in the queue
        if not response_queue.empty():
            response = response_queue.get()
            return JsonResponse({'status': 'success', 'response': response})
        else:
            return JsonResponse({'status': 'pending'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

def chatbot(request):
    chats=Chat.objects.filter(user=request.user)
    if request.method=='POST':
        message=request.POST.get('message')
        thread = threading.Thread(target=ask_gemini, args=(message,request.user.id))
        thread.start()
        response="Thinking..."
        if not response_queue.empty():
            response=response_queue.get()
        
        
        return JsonResponse({'message':message, 'response':response})
    return render(request,'chatbot.html',{'chats':chats})

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']  
        user=auth.authenticate(request,username=username,password=password)
        if user is not None:
            try:
                auth.login(request,user)
                return redirect('chatbot')
            except:
                error_message = "Error accessing account"
                return render(request,'login.html',{'error_message':error_message})
        else:
            error_message="Invalid User"
            return render(request,'login.html',{'error_message':error_message})
    return render(request,'login.html')

def register(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']

        if password1==password2:
            try:
                user=User.objects.create_user(username,email,password1)
                user.save()
                auth.login(request,user)
                return redirect('chatbot')
            except Exception as e:
                error_message = f"Error creating account {e}"
                return render(request,'register.html',{'error_message':error_message})
        else:
            error_message="Password don't match"
            return render(request,'register.html',{'error_message':error_message})
    return render(request,'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')
