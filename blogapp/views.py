from django.shortcuts import render
from .models import Blog_Post
from .serializers import BlogPostSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


# Create your views here.
@api_view(['GET'])
@permission_classes([AllowAny])
def home_api(request):
     # get all the blog
     posts=Blog_Post.objects.all()[:3]
     # serialize the data
     serializer=BlogPostSerializer(posts,many=True)
     return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def author_dashboard_api(request):
     posts=Blog_Post.objects.filter(author=request.user)
     paginator=PageNumberPagination()
     # number of posts per page
     paginator.page_size=4

     paginated_posts=paginator.paginate_queryset(posts,request)

     serializer=BlogPostSerializer(paginated_posts,many=True)
     return paginator.get_paginated_response(serializer.data)


# json of pagination function
# "count": 2,
#     "next": "http://127.0.0.1:8000/blog/blog_posts/?page=2",
#     "previous": null,
#     "results": {}

# post on blog link
@api_view(['GET'])
@permission_classes([AllowAny])
def blog_posts_api(request):
     posts=Blog_Post.objects.all()
     
     paginator=PageNumberPagination()
     # number of posts per page
     paginator.page_size=4

     paginated_posts=paginator.paginate_queryset(posts,request)

     serializer=BlogPostSerializer(paginated_posts,many=True)
     return paginator.get_paginated_response(serializer.data)



# api for displaying one post by id ,anyone can access
@api_view(['GET'])
@permission_classes([AllowAny])
def post_detail_api(request,id):
     try:
          post=Blog_Post.objects.get(pk=id)
          serializer=BlogPostSerializer(post)
          return Response(serializer.data,status=status.HTTP_200_OK)
     except Blog_Post.DoesNotExist:
          return Response({'error':'page not found'},status=status.HTTP_404_NOT_FOUND)

# api for creating post by author

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def author_create_post_api(request):
    """
    API to create a new blog post.
    Only authenticated users can create posts.
    """
    serializer = BlogPostSerializer(data=request.data)
    
    if serializer.is_valid():
        # Create the instance but don't save to the database yet
        post = Blog_Post(**serializer.validated_data)
        post.author = request.user  # Set the author manually
        post.save()  # Save the instance to the database
        
        # Return a success response with the serialized data
        return Response({'message': "Post created successfully", 'data': BlogPostSerializer(post).data}, status=status.HTTP_201_CREATED)
    
    # Return an error response if the data is not valid
    return Response({'message': "Failed to create post", 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def author_edit_post_api(request, id):
    try:
        post = Blog_Post.objects.get(id=id, author=request.user)
    except Blog_Post.DoesNotExist:
        return Response({'message': 'Post not found or not authorized'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BlogPostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = BlogPostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # BlogPostSerializer()
            return Response({'message': "Edited successfully", 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'error': "Something went wrong", 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


#this is for author post detail 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def author_post_detail_api(request,id):
     try:
        post = Blog_Post.objects.get(pk=id, author=request.user)
        serializer = BlogPostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
     except Blog_Post.DoesNotExist:
        return Response({'error': 'Post not found or not authorized'}, status=status.HTTP_404_NOT_FOUND)

# api for deleting post by author
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def author_delete_post_api(request, id):
    post = get_object_or_404(Blog_Post, id=id, author=request.user)
    
    if request.method == 'DELETE':
        post.delete()
        return Response({'message': 'Post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def search_api(request):
    title = request.GET.get('title')
    
    if title:
        posts = Blog_Post.objects.filter(programming_language_tags__icontains=title)
        serializer = BlogPostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response({'error': 'Title parameter is missing'}, status=status.HTTP_400_BAD_REQUEST)


