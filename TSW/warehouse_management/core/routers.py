class SecondDBRouter:
    """
    Роутер для работы с таблицей eclient в базе second_db.
    """

    def db_for_read(self, model, **hints):
        if model._meta.db_table == 'eclient':
            print("ЧТЕНИЕ из second_db")
            return 'second_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.db_table == 'eclient':
            print("Пишем в second_db!")  # Логируем
            return 'second_db'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'second_db':
            print("Миграции запрещены в second_db")
            return False
        return None