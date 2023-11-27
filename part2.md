## Setup
our api: `https://cmput-average-21-b54788720538.herokuapp.com/api/`

frontend: `https://frontend-21-average-f45e3b82895c.herokuapp.com`

```bash
username: string
password: string
```

curl requet to get posts of provided user credentials:
```bash
curl -X 'GET' \
  'https://cmput-average-21-b54788720538.herokuapp.com/api/authors/586539c4-b029-459b-8875-37a5f40939e4/posts/' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic c3RyaW5nOnN0cmluZw=='
```

foreign post on our app: 


![Post](remotePost.png)

connected to our own second instance
connected second instance 1: `https://second-instance-a06a2b03061a.herokuapp.com/api/`

