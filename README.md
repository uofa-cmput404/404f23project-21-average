# CMPUT404-project-socialdistribution

CMPUT 404 Project: Social Distribution

[Project requirements](https://github.com/uofa-cmput404/project-socialdistribution/blob/master/project.org)

# Contributors / Licensing

Authors:

- Afaq Nabi
- Ghunaym Yahya
- Shreyank Hebbar
- Aryaman Raina
- Agrim Sood

Generally everything is LICENSE'D under the Apache-2 by the 21 Average Team

# Startup

- `git clone https://github.com/uofa-cmput404/404f23project-21-average.git`
- `cd 404f23project-21-average`
- `virtualenv venv`
- `pip install -r req.txt`
- `cd project`
- ** start local mysql server and init a DB called `socialDB` then:
- `python3 manage.py migrate`
- `python3 manage.py runserver`
- `http://127.0.0.1:8000/api/` 
