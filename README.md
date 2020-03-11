# stylestore
mega project  

### Steps to initialise database
```python manage.py makemigrations```  
```python manage.py migrate```  
```python manage.py shell```  
```
from main import models as main_models
from django.contrib.auth.models import User
User.objects.create_superuser(username='abcdef', email='email@email.com', password='abcdef')
main_models.Address.objects.create(**{"line_1": "Line 1 of address", "line_2": "Line 2 of address", "city": "Delhi", "state": "Delhi", "country": "India", "pin_code": "123456"})
main_models.CustomUser.objects.create(**{"username": "abcdef", "firstname": "ABC", "lastname": "DEF", "phone_number": "9876543210", "address_id": 1, "gender": 'm'})

main_models.Styles.objects.create(**{"name": "Bricks", "image": "styles/bricks.jpeg", "image_model": "bricks.h5"})
main_models.Styles.objects.create(**{"name": "Music", "image": "styles/music.jpg", "image_model": "music2epoch.h5"})
main_models.Styles.objects.create(**{"name": "Rain Princess", "image": "styles/rain_princess.jpg", "image_model": "rain_princess.h5"})
main_models.Styles.objects.create(**{"name": "Starry Night", "image": "styles/starry_night.jpeg", "image_model": "starry_night.h5"})
main_models.Styles.objects.create(**{"name": "Udnie", "image": "styles/udnie.jpg", "image_model": "udnie2epoch.h5"})

main_models.Templates.objects.create(**{"name": "T-Shirt", "image": "static/templates/tshirt.png", "unit_price": "450"})
main_models.Templates.objects.create(**{"name": "Shirt", "image": "static/templates/shirt.png", "unit_price": "500"})
main_models.Templates.objects.create(**{"name": "Mug", "image": "static/templates/mug.png", "unit_price": "200"})
main_models.Templates.objects.create(**{"name": "Pillow", "image": "static/templates/pillow.png", "unit_price": "300"})
main_models.Templates.objects.create(**{"name": "Phone Cover", "image": "static/templates/phonecover.png", "unit_price": "110"})
quit()
```

### Steps to start app
```python manage.py collectstatic --no-input```  
```python manage.py runserver```  

