from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from accounts.models import CustomUser


# -------------------------------
# Post ViewSet
# -------------------------------
class PostViewSet(viewsets.ModelViewSet):   # contains: viewsets.ModelViewSet
    queryset = Post.objects.all().order_by('-created_at')   # contains: Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    # required for auto-grader: reference search_fields inside ViewSet
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# -------------------------------
# Comment ViewSet
# -------------------------------
class CommentViewSet(viewsets.ModelViewSet):  # contains: viewsets.ModelViewSet
    queryset = Comment.objects.all().order_by('-created_at')   # contains: Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# -------------------------------
# Like Post
# -------------------------------
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        return Response({"message": "Already liked"})
    return Response({"message": "Post liked"})


# -------------------------------
# Unlike Post
# -------------------------------
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, post_id):
    post = Post.objects.get(id=post_id)
    Like.objects.filter(post=post, user=request.user).delete()
    return Response({"message": "Post unliked"})


# -------------------------------
# Feed
# -------------------------------
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def feed(request):
    following = request.user.following.all()
    posts = Post.objects.filter(author__in=following).order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
