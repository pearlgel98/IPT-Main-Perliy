from django.shortcuts import render
import requests
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

@api_view(['GET', 'POST']) 
@permission_classes([AllowAny])
def google_callback(request):
    # 1. Catch the code from either the URL (GET) or the Body (POST)
    code = request.GET.get('code') or request.data.get('code')
    
    if not code:
        return Response({"error": "No code provided"}, status=status.HTTP_400_BAD_REQUEST)

    # --- Prevents instant expiration in the browser ---
    if request.method == 'GET':
        return Response({
            "message": "Copy the code below and use it in a POST request in Postman.",
            "code_to_copy": code
        })

    # --- This only runs when you hit 'Send' in Postman as a POST ---
    token_endpoint = "https://oauth2.googleapis.com/token"
    data = {
        'code': code,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri': settings.GOOGLE_REDIRECT_URI, 
        'grant_type': 'authorization_code',
    }
    
    response = requests.post(token_endpoint, data=data)
    token_data = response.json()
    
    if 'error' in token_data:
        return Response(token_data, status=status.HTTP_400_BAD_REQUEST)

    # Use Access Token to get User Info
    user_info_endpoint = "https://www.googleapis.com/oauth2/v3/userinfo"
    user_info_res = requests.get(user_info_endpoint, params={'access_token': token_data['access_token']})
    user_info = user_info_res.json()

    # User Matching Logic (Security Check)
    email = user_info.get('email')
    if not email:
        return Response({"error": "Failed to retrieve email from Google"}, status=status.HTTP_400_BAD_REQUEST)

    # Automatically create user if they don't exist
    user, created = User.objects.get_or_create(
        username=email, 
        defaults={'email': email}
    )

    admin_emails = ["lr.dmsanpascual@mmdc.mcl.edu.ph"]
    if email in admin_emails and not user.is_staff:
        user.is_staff = True
        user.is_superuser = True 
        user.save()
        
    # Issue local Token for your system
    drf_token, _ = Token.objects.get_or_create(user=user)

    return Response({
        "message": "Login successful",
        "token": drf_token.key,
        "role": "Admin" if user.is_staff else "User", 
        "user_details": {
            "email": email,
            "name": user_info.get('name'),
            "picture": user_info.get('picture')
        }
    })

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def google_logout(request):

    try:
        # Check if the token exists before deleting
        if request.auth:
            request.auth.delete()
            return Response({"message": "Successfully logged out. Token deleted."}, status=status.HTTP_200_OK)
        return Response({"error": "No active token found to delete."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)