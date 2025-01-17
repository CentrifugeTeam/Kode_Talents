from fastapi import Depends, Request, status, Response
from .crud_router import CrudRouter
from fastapi_sqlalchemy_toolkit import ModelManager
from .authenticator import BaseAuthenticator
from pydantic import BaseModel
from fastapi_users.router.common import ErrorModel
from sqlalchemy.ext.asyncio import AsyncSession
from .openapi_responses import (
    not_found_response,
    missing_token_or_inactive_user_response,
    auth_responses,
    not_a_superuser_response,

)


def get_crud_router(manager: ModelManager, get_session, read_scheme: type[BaseModel],
                    create_scheme: type[BaseModel], update_scheme: type[BaseModel],
                    authenticator: BaseAuthenticator,
                    name: str = None):
    # need a plural name
    if not name:
        name = manager.model.__tablename__
    crud = CrudRouter()
    get_current_active_user = authenticator.current_user(
        active=True
    )

    get_current_superuser = authenticator.current_user(
        active=True, superuser=True
    )

    @crud.get('/', response_model=list[read_scheme], name=f'{name}:all',
              dependencies=[Depends(get_current_active_user)],
              responses={**missing_token_or_inactive_user_response})
    async def objs(request: Request, session: AsyncSession = Depends(get_session), ):
        return await manager.list(session)

    @crud.post("/", response_model=read_scheme, responses={
        **missing_token_or_inactive_user_response,
        status.HTTP_409_CONFLICT: {
            "model": ErrorModel,
        }
    }, status_code=status.HTTP_201_CREATED, name=f"{name}:new one",
               dependencies=[Depends(get_current_active_user)],
               )
    async def obj(request: Request, objs: create_scheme, session: AsyncSession = Depends(get_session)):
        return await manager.create(session, objs)

    @crud.patch("/{id}", response_model=read_scheme, responses={
        **auth_responses,
        **not_found_response,
    }, name=f'{name}:patch one',
                dependencies=[Depends(get_current_superuser)])
    async def obj(request: Request, id: int, scheme: update_scheme, session: AsyncSession = Depends(get_session)):
        model = await manager.get_or_404(session)
        return await manager.update(session, model, scheme)

    @crud.get("/{id}",
              dependencies=[Depends(get_current_active_user)],
              response_model=read_scheme,
              responses={
                  **missing_token_or_inactive_user_response,
                  **not_found_response
              },
              name=f'{name}:one',
              )
    async def obj(request: Request, id: int, session: AsyncSession = Depends(get_session)):
        return await manager.get_or_404(session, id=id)

    @crud.delete("/{id}",
                 # dependencies=[Depends(get_current_superuser)],
                 response_class=Response,
                 responses={
                     **auth_responses,
                     **not_found_response
                 }, status_code=status.HTTP_204_NO_CONTENT, name=f'{name}:delete one')
    async def obj(request: Request, id: int, session: AsyncSession = Depends(get_session)):
        obj_in_db = await manager.get_or_404(session, id=id)
        await manager.delete(session, obj_in_db)
        return

    return crud
