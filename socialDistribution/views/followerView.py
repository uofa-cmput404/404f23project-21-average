from rest_framework.response import Response
from socialDistribution.models import Author, Follow
from socialDistribution.pagination import Pagination
from socialDistribution.serializers import AuthorSerializer, FollowSerializer, FollowRequestSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from ..util import vibely, socialSync, ctrlAltDelete, addToInbox, serializeVibelyAuthor, serializeCtrlAltDeleteAuthor, getUUID
from drf_spectacular.utils import extend_schema
from ..pagination import JsonObjectPaginator
from django.conf import settings


class FollowViewSet(generics.ListAPIView):
    queryset = Follow.objects.all()
    # serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = JsonObjectPaginator
    
    @extend_schema(
        tags=['Followers'],
        description='[local, remote] get a list of authors who are AUTHOR_ID’s followers'
    )
    def get(self, request, author_pk, format=None):
        authors = []
        try:
            author = Author.objects.get(pk=author_pk, type="author")
            followers = author.followers.filter(status="Accepted").all()
            print(followers)
            for follower in followers:
                authors.append(AuthorSerializer(Author.objects.get(pk=follower.follower.id)).data)
        except:
            # TODO: i dont think we need to get followers of remote authors on UI???
            vibelyRemoteAuthor = vibely.get(f"authors/{author_pk}")
            if vibelyRemoteAuthor.status_code == 200:
                vibelyAuthorFollowers = vibely.get(f"authors/{author_pk}/followers/")
                if vibelyAuthorFollowers.status_code == 200:
                    for follower in vibelyAuthorFollowers.json()["items"]:
                        authors.append(serializeVibelyAuthor(follower["follower"]))
            
            socialSyncRemoteAuthor = socialSync.get(f"authors/{author_pk}")
            if socialSyncRemoteAuthor.status_code == 200:
                socialSyncAuthorFollowers = socialSync.get(f"authors/{author_pk}/followers/")
                if socialSyncAuthorFollowers.status_code == 200:
                    for follower in socialSyncAuthorFollowers.json()["items"]:
                        authors.append(serializeVibelyAuthor(follower["follower"]))

            # try to find the author on ctrlAltDelete
            ctrlAltDeleteRemoteAuthor = ctrlAltDelete.get(f"authors/{author_pk}")
            if ctrlAltDeleteRemoteAuthor.status_code == 200:
                ctrlAltDeleteAuthorFollowers = ctrlAltDelete.get(f"authors/{author_pk}/followers")
                if ctrlAltDeleteAuthorFollowers.status_code == 200:
                    for follower in ctrlAltDeleteAuthorFollowers.json()["items"]:
                        authors.append(serializeCtrlAltDeleteAuthor(follower))
        
        if not authors:
            return Response({'message': 'No followers'}, status=status.HTTP_200_OK)
        page = self.paginate_queryset(authors)
        return self.get_paginated_response(page)


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
            author = Author.objects.get(pk=author_pk, type="author")
        except:
            # vibelyRemoteAuthor = vibely.get(f"authors/{author_pk}")
            # if vibelyRemoteAuthor.status_code == 200:
            #     ctrlAltDeleteAuthorFollowers = vibely.get(f"authors/{author_pk}/followers/")
            #     if ctrlAltDeleteAuthorFollowers.status_code == 200:
            #         return Response(ctrlAltDeleteAuthorFollowers.json())
            # # try to find the author on ctrlAltDelete
            # ctrlAltDeleteRemoteAuthor = ctrlAltDelete.get(f"authors/{author_pk}")
            # if ctrlAltDeleteRemoteAuthor.status_code == 200:
            #     ctrlAltDeleteAuthorFollowers = ctrlAltDelete.get(f"authors/{author_pk}/followers/")
            #     if ctrlAltDeleteAuthorFollowers.status_code == 200:
            #         return Response(ctrlAltDeleteAuthorFollowers.json())
            return Response({'message': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)
        following = author.following.filter(status="Accepted").all()
        # turn followers queryset into a list of authors
        authors = []
        for follower in following:
            authors.append(AuthorSerializer(Author.objects.get(pk=follower.following.id)).data)
        
        page = self.paginate_queryset(authors)
        return self.get_paginated_response(page)


class FollowDetailViewSet(generics.GenericAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination
    
    @extend_schema(
        tags=['Followers'],
        description='GET [local, remote] check if FOREIGN_AUTHOR_ID is a follower of AUTHOR_ID'
    )
    def get(self, request, author_pk, foreign_author_pk, format=None):
        # return true if foreign_author is a follower of author
        # TODO: check if this makes sense for cross server??
        author = Author.objects.get(pk=author_pk)
        try:
            foreign_author = Author.objects.get(pk=foreign_author_pk)
        except:
            return Response(False)
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
        author = Author.objects.get(pk=author_pk)
        print(request.data)
        try:
            foreign_author = Author.objects.get(pk=foreign_author_pk, type="author")
        except:
            # # send follow request to remote inbox
            # TODO: Implement other teams inbox
            if 'socialsync' in request.data["objectHost"]:
                remoteAuthor = socialSync.get(f"authors/{foreign_author_pk}")
                
                if remoteAuthor.status_code == 200:
                    remoteAuthor = remoteAuthor.json()
                payload = {
                    "type": "follow",
                    "summary": f"{author.username} wants to follow {remoteAuthor['displayName']}",
                    "actor": AuthorSerializer(author).data,
                    "object": remoteAuthor,
                }
                response = socialSync.post(f"authors/{getUUID(remoteAuthor['id'])}/inbox", json=payload)
                print(response.url)
                print(response, response.text)
            elif 'vibely' in request.data["objectHost"]:
                remoteAuthor = vibely.get(f"authors/{foreign_author_pk}")
                print(remoteAuthor.url, remoteAuthor.text)
                if remoteAuthor.status_code == 200:
                    remoteAuthor = remoteAuthor.json()
                payload = {
                    "type": "follow",
                    "summary": f"{author.username} wants to follow {remoteAuthor['displayName']}",
                    "actor": AuthorSerializer(author).data,
                    "object": remoteAuthor,
                }
                response = vibely.post(f"authors/{getUUID(remoteAuthor['id'])}/inbox/", json=payload)
                print(response.url)
                print(response, response.text)
            
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



# {
#   "items": {
#         "type": "Follow",      
#         "summary":"secondinstanceuser3 wants to follow user3",
#         "actor":{
#         "id": "https://socialsync-404-project-6469dd163e44.herokuapp.com/authors/7",
#         "host": "https://socialsync-404-project-6469dd163e44.herokuapp.com/",
#         "displayName": "itachi",
#         "github": null,
#         "profileImage": null,
#         "first_name": "",
#         "last_name": "",
#         "email": "",
#         "username": "itachi",
#         "type": "author"
#         },
#         "object":{
#         "id": "https://cmput-average-21-b54788720538.herokuapp.com/api/authors/db7d3968-c035-4950-a606-e690638189dd/",
#         "host": "https://cmput-average-21-b54788720538.herokuapp.com/api",
#         "displayName": "string",
#         "github": null,
#         "profileImage": null,
#         "first_name": "",
#         "last_name": "",
#         "email": "",
#         "username": "string",
#         "type": "author"
#         }
#     }
# }
