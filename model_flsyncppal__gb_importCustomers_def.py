# @class_declaration interna #
import requests
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
    def guanabana_sync_getUnsynchronizedCustomers(self):
        _i = self.iface

        cdSmall = 10
        cdLarge = 180

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
            url = None
            if qsatype.FLUtil.isInProd():
                url = 'http://www.guanabana.store/syncapi/index.php/customers/unsynchronized'
            else:
                url = 'http://local.guanabana.store/syncapi/index.php/customers/unsynchronized'

            print("Llamando a", url)
            response = requests.get(url, headers=headers)
            stCode = response.status_code
            json = None
            if response and stCode == 200:
                json = response.json()
            else:
                raise Exception("Mala respuesta")

        except Exception as e:
            print(e)
            syncppal.iface.log("Error. No se pudo establecer la conexión con el servidor.", 'gbsynccust')
            return cdLarge

        if json and len(json):
            try:
                aCustomers = _i.processCustomers(json)

                if not aCustomers and not isinstance(aCustomers, (list, tuple)):
                    syncppal.iface.log("Error. Ocurrió un error al sincronizar los clientes.", 'gbsynccust')
                    return cdSmall
            except Exception as e:
                print(e)
                return cdSmall

            if aCustomers and len(aCustomers):
                syncppal.iface.log(ustr("Éxito. Los siguientes clientes se han sincronizado correctamente: ", ustr(aCustomers)), 'gbsynccust')
                for customer in aCustomers:
                    try:
                        url = None
                        if qsatype.FLUtil.isInProd():
                            url = 'http://www.guanabana.store/syncapi/index.php/customers/' + str(customer) + '/synchronized'
                        else:
                            url = 'http://local.guanabana.store/syncapi/index.php/customers/' + str(customer) + '/synchronized'

                        print("Llamando a", url)
                        response = requests.put(url, headers=headers)
                        print("Correcto")
                    except Exception:
                        syncppal.iface.log(ustr("Error. El cliente ", customer, " no ha podido marcarse como sincronizado."), 'gbsynccust')
            elif aCustomers == []:
                syncppal.iface.log("Éxito. No hay clientes que sincronizar.", 'gbsynccust')
                return cdLarge
        else:
            syncppal.iface.log("Éxito. No hay clientes que sincronizar.", 'gbsynccust')
            return cdLarge

        return cdSmall

    def guanabana_sync_processCustomers(self, customers):
        try:
            aCustomers = []
            for customer in customers:
                email = customer["email"]

                curTab = qsatype.FLSqlCursor("mg_customers")
                curTab.select("email = '" + email + "'")

                if curTab.first():
                    curTab.setModeAccess(curTab.Edit)
                    curTab.refreshBuffer()
                else:
                    curTab.setModeAccess(curTab.Insert)
                    curTab.refreshBuffer()
                    curTab.setValueBuffer("email", email[:255])

                sexo = "Masculino" if customer["gender"] == 1 else "Femenino" if customer["gender"] == 2 else None
                if customer["dob"] and customer["dob"] != "" and customer["dob"] is not None:
                    fnac = str(customer["dob"])[:10]
                else:
                    fnac = None
                now = str(qsatype.Date())
                currD = now[:10]
                currT = now[-(8):]

                cifnif = syncppal.iface.replace(customer["taxvat"])
                nombre = syncppal.iface.replace(customer["firstname"])
                apellidos = syncppal.iface.replace(customer["lastname"])
                website = str(customer["website_id"])

                curTab.setValueBuffer("sexo", sexo[:255] if sexo else sexo)
                curTab.setValueBuffer("fechanacimiento", fnac)
                curTab.setValueBuffer("cifnif", cifnif[:255] if cifnif else cifnif)
                curTab.setValueBuffer("idusuariomod", "sincro")
                curTab.setValueBuffer("fechamod", currD)
                curTab.setValueBuffer("horamod", currT)
                curTab.setValueBuffer("nombre", nombre[:255] if nombre else nombre)
                curTab.setValueBuffer("apellidos", apellidos[:255] if apellidos else apellidos)
                curTab.setValueBuffer("suscrito", customer["suscribed"])
                curTab.setValueBuffer("codwebsite", website[:255] if website else website)

                if customer["billing_address"]:
                    nombrefac = syncppal.iface.replace(customer["billing_address"]["firstname"])
                    apellidosfac = syncppal.iface.replace(customer["billing_address"]["lastname"])
                    telefonofac = syncppal.iface.replace(customer["billing_address"]["telephone"])
                    direccionfac = syncppal.iface.replace(customer["billing_address"]["street"])
                    codpostalfac = syncppal.iface.replace(customer["billing_address"]["postcode"])
                    ciudadfac = syncppal.iface.replace(customer["billing_address"]["city"])
                    provinciafac = syncppal.iface.replace(customer["billing_address"]["region"])
                    paisfac = syncppal.iface.replace(customer["billing_address"]["country_id"])

                    curTab.setValueBuffer("nombrefac", nombrefac[:255] if nombrefac else nombrefac)
                    curTab.setValueBuffer("apellidosfac", apellidosfac[:255] if apellidosfac else apellidosfac)
                    curTab.setValueBuffer("telefonofac", telefonofac[:255] if telefonofac else telefonofac)
                    curTab.setValueBuffer("direccionfac", direccionfac[:255] if direccionfac else direccionfac)
                    curTab.setValueBuffer("codpostalfac", codpostalfac[:255] if codpostalfac else codpostalfac)
                    curTab.setValueBuffer("ciudadfac", ciudadfac[:255] if ciudadfac else ciudadfac)
                    curTab.setValueBuffer("provinciafac", provinciafac[:255] if provinciafac else provinciafac)
                    curTab.setValueBuffer("paisfac", paisfac[:255] if paisfac else paisfac)

                if customer["shipping_address"]:
                    nombreenv = syncppal.iface.replace(customer["shipping_address"]["firstname"])
                    apellidosenv = syncppal.iface.replace(customer["shipping_address"]["lastname"])
                    telefonoenv = syncppal.iface.replace(customer["shipping_address"]["telephone"])
                    direccionenv = syncppal.iface.replace(customer["shipping_address"]["street"])
                    codpostalenv = syncppal.iface.replace(customer["shipping_address"]["postcode"])
                    ciudadenv = syncppal.iface.replace(customer["shipping_address"]["city"])
                    provinciaenv = syncppal.iface.replace(customer["shipping_address"]["region"])
                    paisenv = syncppal.iface.replace(customer["shipping_address"]["country_id"])

                    curTab.setValueBuffer("nombreenv", nombreenv[:255] if nombreenv else nombreenv)
                    curTab.setValueBuffer("apellidosenv", apellidosenv[:255] if apellidosenv else apellidosenv)
                    curTab.setValueBuffer("telefonoenv", telefonoenv[:255] if telefonoenv else telefonoenv)
                    curTab.setValueBuffer("direccionenv", direccionenv[:255] if direccionenv else direccionenv)
                    curTab.setValueBuffer("codpostalenv", codpostalenv[:255] if codpostalenv else codpostalenv)
                    curTab.setValueBuffer("ciudadenv", ciudadenv[:255] if ciudadenv else ciudadenv)
                    curTab.setValueBuffer("provinciaenv", provinciaenv[:255] if provinciaenv else provinciaenv)
                    curTab.setValueBuffer("paisenv", paisenv[:255] if paisenv else paisenv)

                if curTab.modeAccess() == curTab.Insert:
                    curTab.setValueBuffer("idusuarioalta", "sincro")
                    curTab.setValueBuffer("fechaalta", currD)
                    curTab.setValueBuffer("horaalta", currT)

                if not curTab.commitBuffer():
                    syncppal.iface.log(ustr("Error. No se pudo guardar el cliente ", str(email)), 'gbsynccust')
                    return False

                aCustomers.append(customer["entity_id"])

            return aCustomers

        except Exception as e:
            qsatype.debug(e)
            return False

    def __init__(self, context=None):
        super(guanabana_sync, self).__init__(context)

    def getUnsynchronizedCustomers(self):
        return self.ctx.guanabana_sync_getUnsynchronizedCustomers()

    def processCustomers(self, customers):
        return self.ctx.guanabana_sync_processCustomers(customers)


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
