class PostgresRouter:
    """
    Direct all operations of the `users` app to PostgreSQL.
    """
    app_labels = {'users'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.app_labels:
            return 'default'
        return None
    
    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.app_labels:
            return 'default'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.app_labels:
            return db == 'default'
        return None