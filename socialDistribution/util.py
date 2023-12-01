from .models import Inbox, Author
import json
from requests_toolbelt import sessions
from requests.auth import HTTPBasicAuth
import base64
import uuid

CONNECTED = ["vibely", "CtrlAltDefeat"]
team1 = sessions.BaseUrlSession(base_url='https://vibely-23b7dc4c736d.herokuapp.com/api/')
team1.headers['Authorization'] = f"Basic {base64.b64encode('vibely:vibely'.encode('utf - 8')).decode('utf - 8')}"

team2 = sessions.BaseUrlSession(base_url='https://socialsync-404-project-6469dd163e44.herokuapp.com/')
team2.headers['Authorization'] = f"Basic {base64.b64encode('21average:bigPass'.encode('utf - 8')).decode('utf - 8')}"

team3 = sessions.BaseUrlSession(base_url='https://cmput404-ctrl-alt-defeat-api-12dfa609f364.herokuapp.com/api/')
team3.headers['Authorization'] = 'Basic MjFBdmVyYWdlOnBhc3N3b3Jk'

def addToInbox(author, data):
    if author.type == "NodeAuthor":
        team1.post(f"authors/{author.id}/inbox/", json={"items":data})
    else:
        inbox = Inbox.objects.get(author=author)
        items = json.loads(inbox.items)
        items.append(json.dumps(data, default=str))
        inbox.items = json.dumps(items)
        inbox.save()


def sendToEveryonesInbox(data):
    # send to all authors
    authors = Author.objects.all()
    for author in authors:
        addToInbox(author, data)


def sendToFriendsInbox(author, data):
    # send to all friends that have status accepted
    followers = author.followers.filter(status="Accepted").all()
    # following = author.following.filter(status="Accepted").all()
    # print(following)
    result = []
    for follower in followers:
        result.append(Author.objects.get(id=follower.follower.id))
    # for friend in following:
    #     result.append(Author.objects.get(id=friend.following.id))
    
    # remover duplicate authors
    # TODO: check if this works
    # result = list(dict.fromkeys(result))
    # Convert the follow object to author object
    print(result)
    for friend in result:
        addToInbox(friend, data)


def isFriend(author, foreign_author):
    if author.id == foreign_author.id:
        return True
    if author.followers.filter(follower=foreign_author).exists():
        return True
    return False


def isFrontendRequest(request):
    # return False
    if request.user.username in CONNECTED:
        return False
    return True


def serializeTeam1Author(author):
    return {
        "id": author["id"],
        "host": author["host"],
        "displayName": author["displayName"],
        "github": author["github"],
        "profileImage": author["profileImage"],
        "first_name": "",
        "last_name": "",
        "email": "",
        "username": author["displayName"],
        "type": "author"
    }


def serializeTeam1Post(post):
    return {
        "id": post["id"],
        "title": post["title"],
        "type": "post",
        "source": post["source"],
        "origin": post["origin"],
        "description": post["description"],
        "contentType": post["contentType"],
        "visibility": post["visibility"],
        "unlisted": post["unlisted"],
        "content": post["content"],
        "published": post["published"],
        "author": serializeTeam1Author(post["author"]),
        "categories": post["categories"],
        "image_link": None,
        "image": None,
        "imageOnlyPost": None,
        "count": post["count"],
        "comments": post["comments"]
    }


def serializeTeam2Post(post):
    return {
        "id": post["id"],
        "title": "",
        "type": "post",
        "source": post["source"],
        "origin": post["origin"],
        "description": post["description"],
        "contentType": post["contentType"],
        "visibility": post["visibility"],
        "unlisted": post["unlisted"],
        "content": post["content"],
        "published": post["published"],
        "author": serializeTeam1Author(post["author"]),
        "categories": post["categories"],
        "comments": post["comments"],
        "image_link": None,
        "image": None,
        "imageOnlyPost": None,
        "count": 0,
    }
def serializeTeam3Post(post):
    return {
        "id": post["id"],
        "title": "",
        "type": "post",
        "source": post["source"],
        "origin": post["origin"],
        "description": post["description"],
        "contentType": post["contentType"],
        "visibility": post["visibility"],
        "unlisted": post["unlisted"],
        "content": post["content"],
        "published": post["published"],
        "author": serializeTeam1Author(post["author"]),
        "categories": post["categories"],
        "comments": post["comments"],
        "image_link": None,
        "image": None,
        "imageOnlyPost": None,
        "count": 0,
    }


def serializeTeam3Author(author):
    return {
        "id": author["url"],
        "host": author["host"],
        "displayName": author["displayName"],
        "github": author["github"],
        # "profileImage": author["profileImage"],
        "first_name": "",
        "last_name": "",
        "email": "",
        "username": author["displayName"],
        "type": "author"
    }
