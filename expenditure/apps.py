from django.apps import AppConfig


class ExpenditureConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'expenditure'

    def ready(self):
        from . import signals
        from expenditure.scheduler import scheduler
        """ uncomment the code below to start scheduler upon running server
            NB: comment out before running initial migration
        """
<<<<<<< HEAD
        #scheduler.start()
=======
        # scheduler.start()
>>>>>>> forms
