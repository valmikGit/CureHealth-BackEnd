from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def lobby(request):
    # return render(request=request, template_name='chat/lobby.html')
    return JsonResponse({
        'status' : 200,
        'message' : 'You have reached the lobby of the chat app.'
    })