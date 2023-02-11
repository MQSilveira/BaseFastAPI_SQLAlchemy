from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioSchema
from core.deps import get_session


router = APIRouter()

#POST usuario
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchema)
async def post_usuario(usuario:UsuarioSchema, db:AsyncSession=Depends(get_session)):
    
    novo_usuario = UsuarioModel(
        nome = usuario.nome,
        email = usuario.email,
    )
    
    db.add(novo_usuario)
    await db.commit()
    
    return usuario


#GET usuario
@router.get('/', response_model=List[UsuarioSchema])
async def get_usuario(db:AsyncSession=Depends(get_session)):
    async with db as session:
        
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios:List[UsuarioModel] = result.scalars().all()
        
        return usuarios


# GET usuario
@router.get('/{usuario_id}', response_model=UsuarioSchema, status_code=status.HTTP_200_OK)
async def get_usuario(usuario_id:int, db:AsyncSession=Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario = result.scalar_one_or_none()
        
        if usuario:
            return usuario
        
        raise HTTPException(
            detail='Usuario não encontrado!',
            status_code=status.HTTP_404_NOT_FOUND
            )


# PUT usuario
@router.put('/{usuario_id}', response_model=UsuarioSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_usuario(usuario_id:int, usuario:UsuarioSchema, db:AsyncSession=Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_up = result.scalar_one_or_none()
        
        if usuario_up:
            usuario_up.nome = usuario.nome
            usuario_up.email = usuario.email

            await session.commit()
            
            return usuario_up
        
        raise HTTPException(
            detail='Usuario não encontrado!',
            status_code=status.HTTP_404_NOT_FOUND
            )


# DELETE
@router.delete('/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id:int, db:AsyncSession=Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_del = result.scalar_one_or_none()
        
        if usuario_del:
            await session.delete(usuario_del)
            await session.commit()
            
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
        raise HTTPException(
            detail='Usuario não encontrado!',
            status_code=status.HTTP_404_NOT_FOUND
            )


