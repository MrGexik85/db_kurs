from fastapi import HTTPException, Request, status
from v1.user.schema import UserSession


def get_auth_user_from_session(req: Request):
    if 'user' not in req.session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='This method needs to authorize')
    user = req.session['user']
    return UserSession(id=user['id'], username=user['username'], isAdmin=user['is_admin'])


def get_admin_user_from_session(req: Request):
    user = get_auth_user_from_session(req)
    if not user.isAdmin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You dont have admin rights')
    return user