from django.db.models import Q 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .serializers import PostSerializer, CommentSerializer 
from .services import PostFactory
from rest_framework.pagination import PageNumberPagination
from django.views.decorators.cache import cache_page

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
@cache_page(60)
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