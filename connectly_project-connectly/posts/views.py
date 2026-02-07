from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .serializers import PostSerializer
from .services import PostFactory

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    # CREATE
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            # 2. REPLACE serializer.save() with the Factory call
            # This uses the Factory Pattern to handle the creation logic
            try:
                PostFactory.create_post(
                    user=request.user, 
                    content=serializer.validated_data['content']
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                # This catches errors from your APISettings Singleton (e.g., max length)
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    # CREATE
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # READ
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    # UPDATE
    if request.method == 'PUT':
        # Security: Only allow author to edit their own post
        if post.author != request.user:
            return Response({'error': 'You cannot edit this.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    if request.method == 'DELETE':
        if post.author != request.user:
            return Response({'error': 'You cannot delete this.'}, status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)