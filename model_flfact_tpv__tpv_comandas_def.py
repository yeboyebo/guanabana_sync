
# @class_declaration guanabana_sync #
from sync import tasks


class guanabana_sync(flfact_tpv):

    def guanabana_sync_getActivity(self, params):
        return tasks.getActivity()

    def guanabana_sync_revoke(self, params):
        return tasks.revoke(params["id"])

    def guanabana_sync_gbSyncOrders(self, params):
        if "passwd" in params and params['passwd'] == "bUqfqBMnoH":
            tasks.getUnsynchronizedOrders.delay(params['fakeRequest'])
            return True
        else:
            print("no tengo contraseña")

        return False

    def guanabana_sync_gbSyncStock(self, params):
        if "passwd" in params and params['passwd'] == "bUqfqBMnoH":
            tasks.updateProductStock.delay(params['fakeRequest'])
            return True
        else:
            print("no tengo contraseña")

        return False

    def guanabana_sync_gbSyncPrices(self, params):
        if "passwd" in params and params['passwd'] == "bUqfqBMnoH":
            tasks.updateProductPrice.delay(params['fakeRequest'])
            return True
        else:
            print("no tengo contraseña")

        return False

    def guanabana_sync_gbSyncCust(self, params):
        if "passwd" in params and params['passwd'] == "bUqfqBMnoH":
            tasks.getUnsynchronizedCustomers.delay(params['fakeRequest'])
            return True
        else:
            print("no tengo contraseña")

        return False

    def __init__(self, context=None):
        super().__init__(context)

    def getActivity(self, params):
        return self.ctx.guanabana_sync_getActivity(params)

    def revoke(self, params):
        return self.ctx.guanabana_sync_revoke(params)

    def gbSyncOrders(self, params):
        return self.ctx.guanabana_sync_gbSyncOrders(params)

    def gbSyncStock(self, params):
        return self.ctx.guanabana_sync_gbSyncStock(params)

    def gbSyncPrices(self, params):
        return self.ctx.guanabana_sync_gbSyncPrices(params)

    def gbSyncCust(self, params):
        return self.ctx.guanabana_sync_gbSyncCust(params)

