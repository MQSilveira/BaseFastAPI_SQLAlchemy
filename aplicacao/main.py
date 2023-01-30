from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from models import Aluno


app = FastAPI()

@app.get('/')
async def raiz():
    return {'mensagem': 'Seja bem vindo ao MoreDevs2Blu'}


alunos = {
    1 : {'Nome': 'marcos', 'Idade': 32, 'E-mail': 'marcos@gmail.com'},
    2 : {'Nome': 'amanda', 'Idade': 30, 'E-mail': 'amanda@gmail.com'},
    3 : {'Nome': 'ana', 'Idade': 12, 'E-mail': 'ana@gmail.com'},
    4 : {'Nome': 'joão', 'Idade': 26, 'E-mail': 'joao@gmail.com'}
}


#GET
@app.get('/alunos')
async def get_alunos():
    return alunos


@app.get('/alunos/{id_aluno}')
async def get_aluno(id_aluno:int):

    try :
        aluno = alunos[id_aluno]
        alunos.update({'id':id_aluno})
        return aluno
    
    except KeyError:
    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Aluno não encontrado')

# POST
@app.post('/alunos')
async def post_alunos(aluno: Aluno):
    
    next_id : int = len(alunos)+1
    
    alunos[next_id] = aluno
    
    return alunos



if __name__ == '__main__':
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host = "127.0.0.1",
        port = 8000,
        log_level = "info",
        reload = True
    )