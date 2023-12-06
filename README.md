# Social Distrubution
## Our App
`UI: https://frontend-21-average-f45e3b82895c.herokuapp.com/`

`API: https://cmput-average-21-b54788720538.herokuapp.com/api/`

`Admin: https://cmput-average-21-b54788720538.herokuapp.com/admin/`

### Our Users
```bash
ADMIN:
    username: admin
    password: admin

REGULAR USERS:
    username: itachi
    password: string

    username: string
    password: string
```

### Connected Teams
- SocialSync 
    - https://socialsync-404-project-6469dd163e44.herokuapp.com/login/
    - `username: username password: pass`
- Vibely
    - https://656d595c9cf6c70641d9d342--chic-mochi-59bc3d.netlify.app/signin
    - `username: user password: pass`
- CTRLALTDELETE
    - https://cmput404-ctrl-alt-defeat-react-574ccb97869b.herokuapp.com/
    - `username: user password: pass`


## User Stories
   
   - [x] As an author I want to make public posts.
   - [x] As an author I want to edit public posts.
   - [ ] As an author, posts I create can link to images.
   - [x] As an author, posts I create can be images.
   - [x] As a server admin, images can be hosted on my server.
   - [ ] As an author, posts I create can be private to another author
   - [x] As an author, posts I create can be private to my friends
   - [x] As an author, I can share other author's public posts
   - [x] As an author, I can re-share other author's friend posts to my friends
   - [x] As an author, posts I make can be in simple plain text
   - [x] As an author, posts I make can be in CommonMark
   - [x] As an author, I want a consistent identity per server
   - [x] As a server admin, I want to host multiple authors on my server
   - [x] As a server admin, I want to share public images with users
     on other servers.
   - [x] As an author, I want to pull in my github activity to my "stream"
   - [x] As an author, I want to post posts to my "stream"
   - [x] As an author, I want to delete my own public posts.
   - [x] As an author, I want to befriend local authors
   - [x] As an author, I want to befriend remote authors
   - [x] As an author, I want to feel safe about sharing images and posts
     with my friends -- images shared to friends should only be
     visible to friends. [public images are public]
   - [x] As an author, when someone sends me a friends only-post I want to
     see the likes.
   - [x] As an author, comments on friend posts are private only to me the
     original author.
   - [x] As an author, I want un-befriend local and remote authors
   - [x] As an author, I want to be able to use my web-browser to manage
     my profile
   - [x] As an author, I want to be able to use my web-browser to manage/author
     my posts
   - [x] As a server admin, I want to be able add, modify, and remove
     authors.
   - [x] As a server admin, I want to OPTIONALLY be able allow users to sign up but
     require my OK to finally be on my server
   - [x] As a server admin, I don't want to do heavy setup to get the
     posts of my author's friends.
   - [x] As a server admin, I want a restful interface for most operations
   - [x] As an author, other authors cannot modify my public post
   - [x] As an author, other authors cannot modify my shared to friends post.
   - [x] As an author, I want to comment on posts that I can access
   - [x] As an author, I want to like posts that I can access
   - [x] As an author, my server will know about my friends
   - [x] As an author, When I befriend someone (they accept my friend request) I follow them, only when
     the other author befriends me do I count as a real friend -- a bi-directional follow is a true friend.
   - [x] As an author, I want to know if I have friend requests.
   - [x] As an author I should be able to browse the public posts of everyone
   - [x] As a server admin, I want to be able to add nodes to share with
   - [x] As a server admin, I want to be able to remove nodes and stop
     sharing with them.
   - [x] As a server admin, I can limit nodes connecting to me via
     authentication.
   - [x] As a server admin, node to node connections can be authenticated
     with HTTP Basic Auth
   - [x] As a server admin, I can disable the node to node interfaces for
     connections that are not authenticated!
   - [x] As an author, I want to be able to make posts that are unlisted,
     that are publicly shareable by URI alone (or for embedding images)