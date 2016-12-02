class ManagerInstead(object):

    @staticmethod
    def initdb():
        from database import init_db
        init_db()
