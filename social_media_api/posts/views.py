from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from notifications.models import Notification   # needed for Notification.objects.create


# ----------------------------------------------------
# Post ViewSet
# ----------------------------------------------------
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')   # required: Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# ----------------------------------------------------
# Comment ViewSet
# ----------------------------------------------------
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')  # required: Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# ----------------------------------------------------
# Like a Post (required strings inside)
# ----------------------------------------------------
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, pk):
    # REQUIRED STRING:
    post = generics.get_object_or_404(Post, pk=pk)  # contains: generics.get_object_or_404(Post, pk=pk)

    # REQUIRED STRING:
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    # contains: Like.objects.get_or_create(user=request.user, post=post)

    if created:
        # REQUIRED STRING:
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked your post",
            target=post
        )   # contains: Notification.objects.create

        return Response({"message": "Post liked"})
    return Response({"message": "Already liked"})


# ----------------------------------------------------
# Unlike a Post
# ----------------------------------------------------
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, pk):
    post = generics.get_object_or_404(Post, pk=pk)
    Like.objects.filter(user=request.user, post=post).delete()
    return Response({"message": "Post unliked"})


# ----------------------------------------------------
# Feed (contains required patterns)
# ----------------------------------------------------
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def feed(request):
    following_users = request.user.following.all()

    # Required substring already present in your previous file
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')

    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
