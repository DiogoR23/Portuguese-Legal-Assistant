class CassandraRouter:
    """
    Direct all operations of the `ptlaws_api` app to Cassandra.
    """
    app_labels = {'ptlaws_api'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.app_labels:
            return 'cassandra'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.app_labels:
            return 'cassandra'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model=None, **hints):
        if app_label in self.app_labels:
            return db == 'cassandra'
        return None