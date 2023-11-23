from .models import Inbox, Author
from .serializers import InboxSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import json


def addToInbox(author, data):
    inbox = Inbox.objects.get(author=author)
    items = json.loads(inbox.items)
    items.append(json.dumps(data, default=str))
    inbox.items = json.dumps(items)
    inbox.save()


def sendToFriendsInbox(author, data):
    # send to all friends that have status accepted
    followers = author.followers.filter(status="Accepted").all()
    following = author.following.filter(status="Accepted").all()
    print(followers)
    print(following)
    result = []
    for follower in followers:
        result.append(Author.objects.get(id=follower.follower.id))
    for friend in following:
        result.append(Author.objects.get(id=friend.following.id))
    
    # remover duplicate authors
    result = list(dict.fromkeys(result))
    # Convert the follow object to author object
    print(result)
    for friend in result:
        addToInbox(friend, data)


def isFriend(author, foreign_author):
    if author.followers.filter(follower=foreign_author).exists():
        return True
    return False
