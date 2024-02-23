# Algumas informações uteis

Endpoints da API
- http://localhost:8000/api/token/ | Autenticar na API com usuario e senha. (djangorestframework-simplejwt)

- http://localhost:8000/api/token/ | Autenticar na API com usuario e senha. (djangorestframework-simplejwt)

- http://localhost:8000/api/my-planted-trees/ | Árvores plantadas pelo usuário. (Precisa do token Beare gerado no endpoint acima)



# Para rodar a aplicação você vai precisar do seguinte 

Você precisa ter instalado em sua maquina apenas docker e docker compose.

mude o nome do arquvio <b>.envsample</b> para <b>.env</b>

Rode os seguintes comandos.

- Vocẽ pode rodar a aplicação usando Make ou apenas Docker e Docker compose.

## Usando o programa make
    make up
    
Isso já deve subir a aplicação.

A aplicação já estará rodando no seguinte endereço <a href="http://localhost:8000/"> http://localhost:8000/ </a>

### Criando o usuario admin.
Use o comando.

    make admin

### Para rodar todos os testes 

Para rodar os testes , use o comando.

    make tests

### Alguns utilitarios de comandos podem ser encontrados dentro do arquivo Make


## Usando apenas docker
```bash
docker compose up -d
```

Ao rodar este comando já ira fazer o build das imagens necessarias

Para criar usuario admin

    
```bash
docker exec -it youshop_djangoapp python manage.py createsuperuser
```

Para rodar os testes use o comando.
    
```bash
docker exec -it youshop_djangoapp python manage.py test
```

