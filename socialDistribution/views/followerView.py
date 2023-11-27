from rest_framework.response import Response
from socialDistribution.models import Author, Follow
from socialDistribution.pagination import Pagination
from socialDistribution.serializers import AuthorSerializer, FollowSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from ..util import isFrontendRequest, team1, team2, serializeTeam1Post, serializeTeam1Author, secondInstance
from drf_spectacular.utils import extend_schema
from ..util import addToInbox


class FollowViewSet(generics.ListAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination
    
    @extend_schema(
        tags=['Followers'],
        description='[local, remote] get a list of authors who are AUTHOR_ID’s followers'
    )
    def get(self, request, author_pk, format=None):
        try:
            author = Author.objects.get(pk=author_pk)
        except:
            remote_author = team1.get(f"authors/{author_pk}")
            if remote_author.status_code == 200:
                likes = team1.get(f"authors/{author_pk}/followers/")
                if likes.status_code == 200:
                    return Response(likes.json())
            # try to find the author on team2
            remote_author = team2.get(f"authors/{author_pk}")
            if remote_author.status_code == 200:
                likes = team2.get(f"authors/{author_pk}/followers/")
                if likes.status_code == 200:
                    return Response(likes.json())
            return Response({'message': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)
        followers = author.followers.filter(status="Accepted").all()
        # turn followers queryset into a list of authors
        authors = []
        for follower in followers:
            authors.append(Author.objects.get(pk=follower.follower.id))
        
        page = self.paginate_queryset(authors)
        return self.get_paginated_response(AuthorSerializer(page, many=True).data)


class FollowingViewSet(generics.ListAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination
    
    @extend_schema(
        tags=['Followers'],
        description='[local, remote] get a list of authors who are AUTHOR_ID’s followers'
    )
    def get(self, request, author_pk, format=None):
        try:
            author = Author.objects.get(pk=author_pk)
        except:
            remote_author = team1.get(f"authors/{author_pk}")
            if remote_author.status_code == 200:
                likes = team1.get(f"authors/{author_pk}/followers/")
                if likes.status_code == 200:
                    return Response(likes.json())
            # try to find the author on team2
            remote_author = team2.get(f"authors/{author_pk}")
            if remote_author.status_code == 200:
                likes = team2.get(f"authors/{author_pk}/followers/")
                if likes.status_code == 200:
                    return Response(likes.json())
            return Response({'message': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)
        following = author.following.filter(status="Accepted").all()
        # turn followers queryset into a list of authors
        authors = []
        for follower in following:
            authors.append(Author.objects.get(pk=follower.follower.id))
        
        page = self.paginate_queryset(authors)
        return self.get_paginated_response(AuthorSerializer(page, many=True).data)


class FollowDetailViewSet(generics.GenericAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination
    
    @extend_schema(
        tags=['Followers'],
        description='GET [local, remote] check if FOREIGN_AUTHOR_ID is a follower of AUTHOR_ID'
    )
    def get(self, request, author_pk, foreign_author_pk, format=None):
        # return true if foreign_author is a follower of author
        author = Author.objects.get(pk=author_pk)
        foreign_author = Author.objects.get(pk=foreign_author_pk)
        follow = Follow.objects.filter(following=foreign_author, follower=author)
        if author and foreign_author and follow and follow[0].status == "Accepted":
            return Response(True)
        return Response(False)
    
    @extend_schema(
        tags=['Followers'],
        description='Remove FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID'
    )
    def delete(self, request, author_pk, foreign_author_pk, format=None):
        author = Author.objects.get(pk=author_pk)
        foreign_author = Author.objects.get(pk=foreign_author_pk)
        # create follow object
        follow = Follow.objects.filter(following=foreign_author, follower=author)
        
        if follow:
            follow.delete()
            return Response({'message': 'Unfollowed Successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @extend_schema(
        tags=['Followers'],
        description='Send FOREIGN_AUTHOR_ID a follow request from AUTHOR_ID (must be authenticated)'
    )
    def put(self, request, author_pk, foreign_author_pk, format=None):
        # PUT http://127.0.0.1:8000/api/authors/2c4733b5-235a-410a-975e-d8422aa19609/followers/87aac38e-48d4-489e-9da9-9f1364baa812/ 
        author = Author.objects.get(pk=author_pk)
        foreign_author = Author.objects.get(pk=foreign_author_pk)
        if not foreign_author:
            remote_author = secondInstance.get(f"authors/{foreign_author_pk}")
            if remote_author.status_code == 200:
                remoteAuthor = AuthorSerializer(remote_author).data
            # send follow request to remote inbox
            payload = {
                "type": "follow",
                "summary": f"{author.username} wants to follow {remoteAuthor['username']}",
                "actor": remoteAuthor,
                "object": AuthorSerializer(author).data,
            }
            secondInstance.post(f"author/{foreign_author_pk}/inbox/", payload)
            return Response({'message': 'Follow Request Sent Successfully'}, status=status.HTTP_201_CREATED)
        
        if author == foreign_author:
            return Response({'message': 'cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
        
        if Follow.objects.filter(following=foreign_author, follower=author):
            return Response({'message': 'already following'}, status=status.HTTP_400_BAD_REQUEST)
        
        # author is requesting to follow foreign_author
        Follow.objects.create(following=foreign_author, follower=author)

        addToInbox(foreign_author, {
                "type": "follow",
                "summary": f"{author.username} wants to follow {foreign_author.username}",
                "actor": AuthorSerializer(foreign_author).data,
                "object": AuthorSerializer(author).data,
            })

        return Response({'message': 'Follow Request Sent Successfully'}, status=status.HTTP_201_CREATED)
    
    @extend_schema(
        tags=['Followers'],
        description="Accept AUTHOR_ID follow request from FOREIGN_AUTHOR_ID (must be authenticated)"
    )
    def post(self, request, author_pk, foreign_author_pk, format=None):
        author = Author.objects.get(pk=author_pk)
        foreign_author = Author.objects.get(pk=foreign_author_pk)
        
        follow = Follow.objects.get(following=author, follower=foreign_author, status="Pending")
        if follow:
            follow.status = "Accepted"
            follow.save()
            return Response({'message': 'Follow Request Accepted Successfully'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'not found'}, status=status.HTTP_404_NOT_FOUND)
