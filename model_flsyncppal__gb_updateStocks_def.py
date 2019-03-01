# @class_declaration interna #
import requests
import json
from django.db import transaction
from YBLEGACY import qsatype
from YBLEGACY.constantes import *
from models.flsyncppal import flsyncppal_def as syncppal


class interna(qsatype.objetoBase):

    ctx = qsatype.Object()

    def __init__(self, context=None):
        self.ctx = context


# @class_declaration guanabana_sync #
class guanabana_sync(interna):

    @transaction.atomic
    def guanabana_sync_updateProductStock(self):
        _i = self.iface

        cdSmall = 10
        cdLarge = 120

        headers = None
        if qsatype.FLUtil.isInProd():
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Basic dGVzdDp0ZXN0"
            }
        else:
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Basic dGVzdDp0ZXN0"
            }

        try:
            body = []
            codTienda = "AL2"

            q = qsatype.FLSqlQuery()
            q.setSelect("idssw, datossincro")
            q.setFrom("mg_colasincroweb")
            q.setWhere("tipo = 'gbsyncstock' AND codalmacen = '" + codTienda + "' AND sincronizado = false ORDER BY idssw ASC LIMIT 20")

            if not q.exec_():
                qsatype.debug("Error. La consulta falló.")
                qsatype.debug(q.sql())
                syncppal.iface.log("Error. La consulta falló.", "gbsyncstock")
                return cdLarge

            ids_enviados = []
            stock = {}
            while q.next():
                stock = json.loads(q.value('datossincro'))
                if stock['error'] == "" or stock['error'] is None:
                    ids_enviados.append(str(q.value('idssw')))
                    body.append(stock)

            if not len(body):
                syncppal.iface.log("Éxito. No hay stocks que sincronizar.", "gbsyncstock")
                return cdLarge

            url = None
            if qsatype.FLUtil.isInProd():
                url = 'http://www.guanabana.store/syncapi/index.php/productupdates'
            else:
                url = 'http://local.guanabana.store/syncapi/index.php/productupdates'

            qsatype.debug(ustr("Llamando a ", url, " ", json.dumps(body)))
            response = requests.post(url, data=json.dumps(body), headers=headers)
            stCode = response.status_code
            jsonres = None
            if response and stCode == 202:
                jsonres = response.json()

                if jsonres and "request_id" in jsonres:
                    ids_enviados = ','.join(ids_enviados)
                    qsatype.FLSqlQuery().execSql("UPDATE mg_colasincroweb SET sincronizado = true WHERE idssw in (" + ids_enviados + ")")
                    syncppal.iface.log("Éxito. Stock sincronizado correctamente (id: " + str(jsonres["request_id"]) + ")", "gbsyncstock")
                    return cdSmall
                else:
                    syncppal.iface.log("Error. No se pudo actualizar el stock.", "gbsyncstock")
                    return cdSmall
            else:
                syncppal.iface.log("Error. No se pudo actualizar el stock. Código: " + str(stCode), "gbsyncstock")
                return cdSmall

        except Exception as e:
            qsatype.debug(e)
            syncppal.iface.log("Error. No se pudo establecer la conexión con el servidor.", "gbsyncstock")
            return cdSmall

        return cdSmall

    def guanabana_sync_dameSkuStock(self, referencia, talla):
        print("******referencia")
        print(referencia)
        print(talla)
        if talla == "TU":
            talla = ""
        else:
            talla = "-" + talla

        return referencia + talla

    def guanabana_sync_dameStock(self, disponible):
        if not disponible or isNaN(disponible) or disponible < 0:
            return 0
        return disponible

    def __init__(self, context=None):
        super(guanabana_sync, self).__init__(context)

    def updateProductStock(self):
        return self.ctx.guanabana_sync_updateProductStock()

    def dameSkuStock(self, referencia, talla):
        return self.ctx.guanabana_sync_dameSkuStock(referencia, talla)

    def dameStock(self, disponible):
        return self.ctx.guanabana_sync_dameStock(disponible)


# @class_declaration head #
class head(guanabana_sync):

    def __init__(self, context=None):
        super(head, self).__init__(context)


# @class_declaration ifaceCtx #
class ifaceCtx(head):

    def __init__(self, context=None):
        super(ifaceCtx, self).__init__(context)


# @class_declaration FormInternalObj #
class FormInternalObj(qsatype.FormDBWidget):
    def _class_init(self):
        self.iface = ifaceCtx(self)


form = FormInternalObj()
form._class_init()
form.iface.ctx = form.iface
form.iface.iface = form.iface
iface = form.iface
