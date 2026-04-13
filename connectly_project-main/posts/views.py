from rest_framework.decorators import permission_classes
from connectly_project.utils.task_api import get_user_tasks
from django.contrib.auth.models import User
from django.db.models import Q 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Post
from .serializers import PostSerializer, CommentSerializer 
from .services import PostFactory
from rest_framework.pagination import PageNumberPagination
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

@api_view(['GET'])
@permission_classes([AllowAny])
def google_callback(request):
    code = request.GET.get('code')
    
    if not code:
        return Response({"error": "No code provided"}, status=400)
    
    #BYPASS GOOGLE FOR TESTING
    if code == "TEST":
        user, created = User.objects.get_or_create(username="test_user")

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "message": "Test user authenticated successfully.",
            "token": token.key
        })


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

    user_info_endpoint = "https://www.googleapis.com/oauth2/v3/userinfo"
    user_info_res = requests.get(user_info_endpoint, params={'access_token': token_data['access_token']})
    user_info = user_info_res.json()

    email = user_info.get('email')
    if not email:
        return Response({"error": "Failed to retrieve email from Google"}, status=status.HTTP_400_BAD_REQUEST)

    user, created = User.objects.get_or_create(
        username=email, 
        defaults={'email': email}
    )

    admin_emails = ["lr.pgelig@mmdc.mcl.edu.ph"]
    if email in admin_emails:
        user.is_staff = True
        user.is_superuser = True
        user.save()

    token, _ = Token.objects.get_or_create(user=user)

    try:
        tasks = get_user_tasks(user.id)
    except:
        tasks = []
        
    return Response({
        "message": "login,successful",
        "token": token.key,
        "user_id": user.id
    })

@api_view(['GET'])
def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    try:
        tasks = get_user_tasks(user.id)
    except:
        tasks = []
    
    return Response({
        "username": user.username,
        "tasks": tasks
    })


@api_view(['POST'])
def share_task(request, task_id):
    import requests

    response = requests.get(f"http://127.0.0.1:8000/tasks/{task_id}/")

    if response.status_code != 200:
        return Response({"error": "task not found"}, status=404)
    
    task = response.json()

    post = Post.objects.create(
        content=f"Task: {task['title']} - {task['description']}",
        author=request.user
    )

    return Response({"message": "Task shared as post.", "post_id": post.id
    })


@cache_page(30)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated]) 
def post_list(request):
    if request.method == 'GET':
        # PRIVACY LOGIC: Only show public posts or posts I authored
        posts = Post.objects.filter(Q(privacy='public') | Q(author=request.user))
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            try:
                new_post = PostFactory.create_post(
                    user=request.user, 
                    content=serializer.validated_data['content'],
                    privacy=serializer.validated_data.get('privacy', 'public') 
                )
                
                response_serializer = PostSerializer(new_post)
                
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # PRIVACY LOGIC: If post is private and I'm not the author/admin, hide it
    if post.privacy == 'private' and post.author != request.user and not request.user.is_staff:
        return Response({'error': 'This post is private.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    if request.method == 'PUT':
        if post.author != request.user and not request.user.is_staff:
            return Response({'error': 'You cannot edit this.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        if post.author != request.user and not request.user.is_staff:
            return Response({'error': 'You cannot delete this.'}, status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# --- FEED VIEW ---
@cache_page(30)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_feed(request):
    if request.user.is_staff:
        posts = Post.objects.all()
    else:
        posts = Post.objects.filter(Q(privacy='public') | Q(author=request.user))

    posts = posts.select_related('author').prefetch_related('comments', 'likes').order_by('-created_at')

    paginator = PageNumberPagination()
    paginator.page_size = 10 
    
    result_page = paginator.paginate_queryset(posts, request)
    serializer = PostSerializer(result_page, many=True)
    
    return paginator.get_paginated_response(serializer.data)

# Like Feature
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
 
        if post.privacy == 'private' and post.author != request.user and not request.user.is_staff:
             return Response({'error': 'Cannot interact with private posts.'}, status=status.HTTP_403_FORBIDDEN)

        message = PostFactory.toggle_like(request.user, post)
        return Response({"status": message}, status=status.HTTP_200_OK)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

# Comment Feature 
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def post_comments(request, pk):
    try:
        post = Post.objects.get(pk=pk)
   
        if post.privacy == 'private' and post.author != request.user and not request.user.is_staff:
             return Response({'error': 'Cannot access comments for this post.'}, status=status.HTTP_403_FORBIDDEN)
             
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        try:
            comment_text = request.data.get('text')
            comment = PostFactory.create_comment(request.user, post, comment_text)
            return Response({"status": "Comment added", "id": comment.id}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
