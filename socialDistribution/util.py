from .models import Inbox, Author
import json
from requests_toolbelt import sessions
import base64
from socialDistribution.serializers import AuthorSerializer

vibely = sessions.BaseUrlSession(base_url='https://vibely-23b7dc4c736d.herokuapp.com/api/')
vibely.headers['Authorization'] = f"Basic {base64.b64encode('vibely:vibely'.encode('utf - 8')).decode('utf - 8')}"

socialSync = sessions.BaseUrlSession(base_url='https://socialsync-404-project-6469dd163e44.herokuapp.com/')
socialSync.headers['Authorization'] = f"Basic {base64.b64encode('21average:bigPass'.encode('utf - 8')).decode('utf - 8')}"

ctrlAltDelete = sessions.BaseUrlSession(base_url='https://cmput404-ctrl-alt-defeat-api-12dfa609f364.herokuapp.com/api/')
ctrlAltDelete.headers['Authorization'] = f"Basic {base64.b64encode('CtrlAltDefeat:frontend'.encode('utf - 8')).decode('utf - 8')}"


def addToInbox(author, data):
    print(data)
    if author.type == "NodeAuthor": # sending posts to other people inbox
        socialSync.post(f"authors/{author.id}/inbox", json=data)
    # elif data["type"] == "like":  # sending likes to other peopel inbox
    #     socialSync.post(f"authors/{author.id}/inbox/", json=data)
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


def getUUID(url):
    components = url.split('/')
    if components[-1] == "":
        return components[-2]
    return components[-1]

def isFriend(author, foreign_author):
    if author.id == foreign_author.id:
        return True
    if author.followers.filter(follower=foreign_author).exists():
        return True
    return False


def isFrontendRequest(request):
    nodes = Author.objects.filter(type="node").all()
    for node in nodes:
        if request.user.username == node.username:
            return False
    return True


def serializeVibelyAuthor(author):
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


def serializeVibelyPost(post):
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
        "author": serializeVibelyAuthor(post["author"]),
        "categories": post["categories"],
        "image_link": None,
        "image": None,
        "imageOnlyPost": None,
        "count": post["count"],
        "comments": post["comments"]
    }


def serializeSocialSyncPost(post):
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
        "author": serializeVibelyAuthor(post["author"]),
        "categories": post["categories"],
        "comments": post["comments"],
        "image_link": None,
        "image": None,
        "imageOnlyPost": None,
        "count": 0,
    }
def serializeCtrlAltDeletePost(post):
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
        "author": serializeVibelyAuthor(post["author"]),
        "categories": post["categories"],
        "comments": post["comments"],
        "image_link": None,
        "image": None,
        "imageOnlyPost": None,
        "count": 0,
    }


def serializeCtrlAltDeleteAuthor(author):
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
