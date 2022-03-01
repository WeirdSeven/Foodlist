The internal management system for DeLaiQi.

## Deployment

The deployment process usually involves the following steps. Adjust based on the specific needs.

* Install packages, if you upgrade existing or include new packages.
```
pip3 install -r requirement.txt
```
* Apply migrations, if you make changes to the models.
```
python3 manage.py migrate
```
* Collect statics, if you make changes to custom-made static files, 
or include libraries that use their own static files.
``` 
python3 manager.py collectstatic
```
* Restart the app server. You most likely need this anyways.
``` 
sudo systemctl restart gunicorn
```