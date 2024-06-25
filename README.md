## Bank Transactions APP

Este proyecto es una aplicación Django que gestiona transacciones bancarias y proporciona funcionalidades de enriquecimiento de datos utilizando Django REST Framework y Swagger para la documentación de la API.

### Requisitos
- Python 3.11
- Django 4.x
- Django REST Framework 4.x
- MySQL

Debe tener el Engine de MySQL corriendo en la maquina donde se instale esta APP o en su defecto levantar una imagen de MySQL usando Docker

```
docker run --name bank -e MYSQL_ROOT_PASSWORD=bank123 -e MYSQL_DATABASE=bank -p 3306:3306 -d mysql:latest
```

### Configuración Inicial

1. Clonar el repostirio

```
git clone https://github.com/fenavillarroel/banktransactions.git
```

2. Instalar dependencias

```
python -m venv venv
source venv/bin/activate  # Para Linux/macOS
venv\Scripts\activate  # Para Windows
pip install -r requirements.txt
```

3. Aplicar migraciones

```
python manage.py migrate
```

4. Crear un superusuario (Opcional)

```
python manage.py createsuperuser
```

### Ejecutar la aplicación

```
python manage.py runserver
```

### Acceder a la documentación de la API (Swagger)

1. Ejecuta la aplicación localmente.
2. Accede a la URL de Swagger en tu navegador:

```
http://127.0.0.1:8000/swagger/
```

### Ejecutar Pruebas

Para ejecutar las tests unitarios:

```
python manage.py test
```