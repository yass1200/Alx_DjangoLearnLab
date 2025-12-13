# Social Media API (Django + DRF)

**Repo:** Alx_DjangoLearnLab  
**Directory:** social_media_api

## Setup (local)
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Auth (Token)
- `POST /api/accounts/register/`  -> returns token
- `POST /api/accounts/login/`     -> returns token

## Profile
- `GET /api/accounts/profile/`
- `PUT /api/accounts/profile/`

## Posts & Comments (CRUD)
- Posts: `/api/posts/posts/`
- Comments: `/api/posts/comments/`
- Feed: `GET /api/posts/posts/feed/`

## Follow / Unfollow
- `POST /api/accounts/follow/<user_id>/`
- `POST /api/accounts/unfollow/<user_id>/`

## Likes
- `POST /api/posts/posts/<id>/like/`
- `POST /api/posts/posts/<id>/unlike/`

## Notifications
- `GET /api/notifications/`
- `POST /api/notifications/<id>/mark-read/`

## IMPORTANT
Do **NOT** upload your `venv/` or `.venv/` folder to GitHub.
