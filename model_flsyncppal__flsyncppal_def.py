
# @class_declaration guanabana_sync #
class guanabana_sync(flsyncppal):

    def guanabana_sync_get_customer(self):
        return "guanabana"

    def __init__(self, context=None):
        super().__init__(context)

    def get_customer(self):
        return self.ctx.guanabana_sync_get_customer()

