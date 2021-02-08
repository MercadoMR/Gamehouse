from django.apps import AppConfig

#https://medium.com/codeptivesolutions/https-medium-com-codeptivesolutions-commonly-used-sql-queries-using-django-orm-e8466e8d4258
#https://stackoverflow.com/questions/43577426/appconfig-ready-is-running-twice-on-django-setup-using-heroku

class SadmConfig(AppConfig):
    name = 'gamehouse.sadm'
    #El siguiente código se ejecutara cada vez al iniciar 
    """
    def ready(self):
        from gamehouse.algorithms import updater
        updater.start_prueba() 
    """
