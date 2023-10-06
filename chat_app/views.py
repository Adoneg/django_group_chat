from django.shortcuts import render, redirect
from .models import Room, Message
from django.http import HttpResponse, JsonResponse
from django.contrib import messages

# Create your views here.
def home(request):
    rooms = Room.objects.all()
    return render(request, 'home.html', {'rooms': rooms})

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room) #filter a room corresponding to the name the user entered

    return render(request, 'room.html', {
                                         "username": username, 
                                         "room": room,
                                         "room_details": room_details 
                                         }
                                         )

def check_room(request):
    room = request.POST["room_name"]
    username = request.POST["username"]

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        messages.info(request, "This room did not match any of the above, please try again")
        return redirect('home')
        
def send(request):
    message = request.POST["message"]
    username = request.POST["username"]
    room_id = request.POST["room_id"]
    room_name = request.POST["room_name"]

    new_message = Message.objects.create(value=message,
                                         user=username,
                                         room=room_name)
    new_message.save()

    return HttpResponse("Message sent successfully")

def getMessages(request, room):
     room_details = Room.objects.get(name=room)

     messages = Message.objects.filter(room=room_details.name) #filter all message of thesame id
     return JsonResponse({"messages":list(messages.values())})

    

# def ajax(request):
#     return HttpResponse("Name registered successfully")

# def getAjax(request, jax):
#     room_details = Room.objects.get(name=jax)
#     messages = Message.objects.filter(room=room_details.id)
#     return JsonResponse({"messages":list(messages.values())})