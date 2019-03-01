
# @class_declaration guanabana_sync_tpv_comandas #
class guanabana_sync_tpv_comandas(flfact_tpv_tpv_comandas, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    @helpers.decoradores.csr()
    def getactivity(params):
        return form.iface.getActivity(params)

    @helpers.decoradores.csr()
    def revoke(params):
        return form.iface.revoke(params)

    @helpers.decoradores.csr()
    def gbsyncorders(params):
        return form.iface.gbSyncOrders(params)

    @helpers.decoradores.csr()
    def gbsyncstock(params):
        return form.iface.gbSyncStock(params)

    @helpers.decoradores.csr()
    def gbsyncprices(params):
        return form.iface.gbSyncPrices(params)

    @helpers.decoradores.csr()
    def gbsynccust(params):
        return form.iface.gbSyncCust(params)

