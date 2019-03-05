# @class_declaration interna_mg_colasincroweb #
import importlib

from YBUTILS.viewREST import helpers

from models.flfactalma import models as modelos


class interna_mg_colasincroweb(modelos.mtd_mg_colasincroweb, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration guanabana_sync_mg_colasincroweb #
class guanabana_sync_mg_colasincroweb(interna_mg_colasincroweb, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True


# @class_declaration mg_colasincroweb #
class mg_colasincroweb(guanabana_sync_mg_colasincroweb, helpers.MixinConAcciones):
    pass

    class Meta:
        proxy = True

    def getIface(self=None):
        return form.iface


definitions = importlib.import_module("models.flfactalma.mg_colasincroweb_def")
form = definitions.FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
