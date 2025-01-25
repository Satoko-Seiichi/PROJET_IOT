import serial

from .models import Dht11
from .serializers import DHT11serialize
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
from twilio.rest import Client
import requests
@api_view(["GET", "POST"])
def Dlist(request):
    if request.method == "GET":
        all_data = Dht11.objects.all()
        data_ser = DHT11serialize(all_data, many=True)  # Les données sont sérialisées en JSON
        return Response(data_ser.data)

    elif request.method == "POST":
        serial = DHT11serialize(data=request.data)

        if serial.is_valid():
            serial.save()
            derniere_temperature = Dht11.objects.last().temp
            print(derniere_temperature)
            if derniere_temperature > 25:

                    # Alert WhatsApp
                    account_sid = 'AC7dfbea69da07e92775b7f0b3470518b4'
                    auth_token = 'c17cc797b3d1572fba2cb9b566f6c939'
                    client = Client(account_sid, auth_token)
                    message_whatsapp = client.messages.create(
                        from_='whatsapp:+14155238886',
                        body='Il y a une alerte importante sur votre Capteur la température dépasse le seuil',
                        to='whatsapp:+212721770554'
                    )
                    # Alert Email
                    subject = 'Alerte'
                    message = 'La température dépasse le seuil de 25°C, Veuillez intervenir immédiatement pour vérifier et corriger cette situation'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = ['younesssaid27@gmail.com']
                    from django.core.mail import send_mail
                    send_mail(subject, message, email_from, recipient_list)
            return Response(serial.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)