from django.apps import AppConfig


class BookstackConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bookstack'
    verbose_name = 'کتابخانه'
    
    def ready(self) -> None:
        import bookstack.signals