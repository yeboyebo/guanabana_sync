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
    def guanabana_sync_updateProductPrice(self):
        _i = self.iface

        cdSmall = 10
        cdLarge = 180

        params_b2c = syncppal.iface.get_param_sincro('b2c')
        params_prices = syncppal.iface.get_param_sincro('b2cPricesUpload')

        headers = None
        if qsatype.FLUtil.isInProd():
            headers = {
                "Content-Type": "application/json",
                "Authorization": params_b2c['auth']
            }
        else:
            headers = {
                "Content-Type": "application/json",
                "Authorization": params_b2c['test_auth']
            }

        try:
            body = []
            codTienda = "AL2"
            now = str(qsatype.Date())
            currD = now[:10]
            currT = now[-(8):]

            fecha = qsatype.FLUtil.sqlSelect("tpv_fechasincrotienda", "fechasincro", "codtienda = '" + codTienda + "' AND esquema = 'PRICES_WEB'")
            hora = qsatype.FLUtil.sqlSelect("tpv_fechasincrotienda", "horasincro", "codtienda = '" + codTienda + "' AND esquema = 'PRICES_WEB'")

            if not fecha or fecha is None:
                fecha = "2014-08-01"
            else:
                fecha = str(fecha)[:10]

            if not hora or hora is None:
                hora = "00:00:00"
            else:
                hora = str(hora)[-(8):]

            filtroFechas = "(a.fechaalta > '" + fecha + "' OR (a.fechaalta = '" + fecha + "' AND  a.horaalta >= '" + hora + "'))"
            filtroFechas += " OR (a.fechamod > '" + fecha + "' OR (a.fechamod = '" + fecha + "' AND  a.horamod >= '" + hora + "'))"
            where = filtroFechas + " ORDER BY a.referencia"

            q = qsatype.FLSqlQuery()
            q.setSelect("a.referencia,a.pvp, a.codtarifa, st.codwebsite, st.codstoreview")
            q.setFrom("mg_websites w inner join mg_storeviews st on w.codwebsite = st.codwebsite inner join articulostarifas a on a.codtarifa = w.codtarifa")
            q.setWhere(where)

            if not q.exec_():
                qsatype.debug("Error. La consulta falló.")
                qsatype.debug(q.sql())
                syncppal.iface.log("Error. La consulta falló.", "gbsyncprices")
                return cdLarge

            while q.next():
                sku = q.value("a.referencia")
                price = parseFloat(q.value("a.pvp"))
                store_id = q.value("st.codstoreview")
                website = q.value("st.codwebsite")

                body.append({"sku": sku, "price": price, "sincroPrecios": True, "auto": True, "store_id": store_id, "website": website})

            if not len(body):
                syncppal.iface.log("Éxito. No hay precios que sincronizar.", "gbsyncprices")
                return cdLarge

            url = params_prices['url'] if qsatype.FLUtil.isInProd() else params_prices['test_url']

            qsatype.debug(ustr("Llamando a ", url, " ", json.dumps(body)))
            response = requests.post(url, data=json.dumps(body), headers=headers)
            stCode = response.status_code
            jsonres = None
            if response and stCode == int(params_prices['success_code']):
                jsonres = response.json()

                if jsonres and "request_id" in jsonres:
                    if fecha != "2014-08-01":
                        qsatype.FLSqlQuery().execSql("UPDATE tpv_fechasincrotienda SET fechasincro = '" + currD + "', horasincro = '" + currT + "' WHERE codtienda = '" + codTienda + "' AND esquema = 'PRICES_WEB'")
                    else:
                        qsatype.FLSqlQuery().execSql("INSERT INTO tpv_fechasincrotienda (codtienda, esquema, fechasincro, horasincro) VALUES ('" + codTienda + "', 'PRICES_WEB', '" + currD + "', '" + currT + "')")

                    syncppal.iface.log("Éxito. Precios sincronizados correctamente (id: " + str(jsonres["request_id"]) + ")", "gbsyncprices")
                    return cdSmall
                else:
                    syncppal.iface.log("Error. No se pudo actualizar los precios.", "gbsyncprices")
                    return cdSmall
            else:
                syncppal.iface.log("Error. No se pudo actualizar los precios. Código: " + str(stCode), "gbsyncprices")
                return cdSmall

        except Exception as e:
            qsatype.debug(e)
            syncppal.iface.log("Error. No se pudo establecer la conexión con el servidor.", "gbsyncprices")
            return cdSmall

        return cdSmall

    def __init__(self, context=None):
        super(guanabana_sync, self).__init__(context)

    def updateProductPrice(self):
        return self.ctx.guanabana_sync_updateProductPrice()


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
