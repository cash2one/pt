# -*- coding: utf-8 -*-


class AuthRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        if model._meta.app_label in ('auth','sessions'):
            return 'auth_db'
        # if model._meta.app_label in ('online'):
        #     return 'online'
        if model._meta.app_label in ('open'):
            return 'open'
        if model._meta.app_label in ('activity'):
            return 'activity'
        if model._meta.app_label in ('auth_db','man'):
            return 'auth_db'
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        if model._meta.app_label in ('auth', 'sessions'):
            return 'auth_db'
        # if model._meta.app_label in ('online'):
        #     return 'online'
        if model._meta.app_label in ('open'):
            return 'open'
        if model._meta.app_label in ('activity'):
            return 'activity'
        if model._meta.app_label in ('auth_db','man'):
            return 'auth_db'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label in ('auth','sessions','online','open','activity','auth_db','man') or \
           obj2._meta.app_label in ('auth','sessions','online','open','activity','auth_db','man'):
           return True
        return True

    def allow_migrate(self, db, app_label, model=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if app_label in ('auth','sessions'):
            return db == 'auth_db'
        # if model._meta.app_label in ('online'):
        #     return 'online'
        if model._meta.app_label in ('open'):
            return 'open'
        if model._meta.app_label in ('auth_db','man'):
            return 'auth_db'
        if model._meta.app_label in ('activity'):
            return 'activity'
        return 'default'