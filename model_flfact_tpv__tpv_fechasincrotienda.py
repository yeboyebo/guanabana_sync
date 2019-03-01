# @class_declaration interna_tpv_fechasincrotienda #
import importlib

from YBUTILS.viewREST import helpers

from models.flfact_tpv import models as modelos


class interna_tpv_fechasincrotienda(modelos.mtd_tpv_fechasincrotienda, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration guanabana_sync_tpv_fechasincrotienda #
class guanabana_sync_tpv_fechasincrotienda(interna_tpv_fechasincrotienda, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration tpv_fechasincrotienda #
class tpv_fechasincrotienda(guanabana_sync_tpv_fechasincrotienda, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfact_tpv.tpv_fechasincrotienda_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
