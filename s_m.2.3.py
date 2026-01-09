from datetime import datetime


time_procesin = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")


error_code_view = {
    'PAYMET_IN_PROCESS':'Procesando Productos.',
    
    'PAYMENT_PROCESS_OK':'Sesion cloncuida.',
    'PAYMENT_NOT_OK':'Proceso Cancelado.',
    'BUY_CANCELED_BLOCK':'EL Proceso fue cancelado por el operador.',
    
    'PRODUCT_NOT_IN_COMERCE':'Producto no existente.',
    'PRODUCT_ON_FACTURED':'Este Producto ya fue facturado.',
    'DATE_PRODUCT_EXPIRED':'Producto caducado.',
    
}

types_error_code = {
    101:'PAYMET_IN_PROCESS',
    
    111:'PAYMENT_PROCESS_OK',
    112:'PAYMENT_NOT_OK',
    501:'BUY_CANCELED_BLOCK',
    
    222:'PRODUCT_NOT_IN_COMERCE',
    555:'PRODUCT_ON_FACTURED',
    333:'DATE_PRODUCT_EXPIRED',
    
    406:'PAGES_NOT_RETORN',
    
}

secuense_option = {
    'RESPONSE_BOOL_OPTION':{
        0:True,
        1:False,
        2:None
    },
    
    'REQUEST_NUMBER_ERROR':{
        0:101,
        1:501,
    }
    
}

logs_generals = {
    'logs-delete-buy':{
        'logs-coding-cache':set()
    },

    'logs-buy-product':{
        'logs-product':{ # 222, 555, 333
            
        },
        
        'logs-process':{ # 501 , 101, 111
            
        }
    },
    
    'logs-code-insert-bd':{57152823, 14314502, 82773581}
}

general_products_bd = {

    
    "Lata de Atun 750ml":{
        'precio':3750,
        'codigo':57152823},
    
    "Pan Integral BIMBO":{
        'precio':4990,
        'codigo':14314502},
    
    "Paca de Leche x6":{
        'precio':14990,
        'codigo':82773581},
}

module_sessions = {
    'canasta':set(),
    'code-safety':set(),
    'total':0,
    'product-delete':[],
    'product-value':[]
}

state_app = {
    'sesion-modulos':module_sessions,
    'general-products-bd':general_products_bd,
    'logs-generals':logs_generals,
    'types_error_code':types_error_code,
    'error_code_view':error_code_view,
    'option-numbers':secuense_option
}

def cash_calletion(codings, state_app):
    if codings:
        state_app['sesion-modulos']['total'] = (sum(state_app['general-products-bd'][cantidad]['precio'] for cantidad in state_app['sesion-modulos']['canasta']))
        return True
    else:
        return False


def collected_codes(state_app):
    
    while True:
        try:
            lector_code = int(input("Codigos:"))
            if len(str(lector_code)) == 8 or lector_code in [0, 1, 2]: 
                if  any(lector_code == confirmation for confirmation in state_app['option-numbers']['RESPONSE_BOOL_OPTION']):
                    state_app['logs-generals']['logs-buy-product']['logs-process'].setdefault(time_procesin, {'FIRST_PROCESS':state_app['types_error_code'][101]})
                    return state_app['option-numbers']['RESPONSE_BOOL_OPTION'].get(lector_code)
                else:
                    state_app['sesion-modulos']['code-safety'].add(lector_code)
            else:
                print('\nEl formato no es valido.\n')
        except ValueError:
            print("\nNo puedes usar letras en este Lector.\n")
            
            
def validation_codeexpired(code_validation, state_app):
            #// SI EL CODIGO YA FUE FACTURADO > SE DETIENE >  PIDE OTRO
    if code_validation:
        for valitycoding in state_app['sesion-modulos']['code-safety']: # RECOORER LOS CODIGOS INGRESADOS
            if valitycoding in state_app['logs-generals']['logs-code-insert-bd']: # CONSULTA SI ESTA EN LA BD DE CODIGOS
                continue
            else:
                if valitycoding in state_app['logs-generals']['logs-delete-buy']['logs-coding-cache']: # ELSE > BUSCA SI ESTA EN LOS CODIGOS YA FACTURADOS
                    state_app['sesion-modulos']['code-safety'].discard(valitycoding) # TRUE > LO ELIMINA DEL RECOLECTOR
                    return False, state_app['types_error_code'][555] # MUESTRA CODE 555 > FACTURADO
                else:                                                               #ASIGNAR NUEVO VALOR
                    return False,  state_app['types_error_code'][222] # ELSE> PRODUCTO NO ESTA EN BD - CACHE > NO EXISTE
        return True, state_app['types_error_code'][111]
    return False, None
                

def orquest_validatyon(codeexpered_validation):
    if  codeexpered_validation:
        return True
    else:
        return False
     
     
def adding_codings(validation_expired, state_app):
    
    if validation_expired:
        for producto in state_app['general-products-bd']:
            if state_app['general-products-bd'][producto]['codigo'] in state_app['sesion-modulos']['code-safety']:                                                     
                state_app['sesion-modulos']['canasta'].add(producto)
            else:
                continue
        return True                   
    return False


def product_addp_canast(codings, state_app):
    
    if codings:
        for producto in state_app['general-products-bd']:
            if state_app['general-products-bd'][producto]['codigo'] in state_app['sesion-modulos']['code-safety']:
                print(f"Productos Registrados : {producto} - {(state_app['general-products-bd'][producto]['precio']):,}$", end='  |  ')
        return True
    else:
        return False


def sales_registers(ticket_printing, **datos):
    
    caja, usuario, gastos, carrito, date, descuento, porcentaje = "marie venegas", datos.get('usuario'), datos.get('precio'), datos.get('canasta'), datos.get('fecha'), datos.get('cupon'), 0
    
    if ticket_printing:
        if descuento:
            porcentaje = gastos * 0.50  
        print(f"""
┌──────────────────────┬──────────────────────────────────────────┐
│ Nombre               │ {usuario}
│ Hora                 │ {date}
├──────────────────────┼──────────────────────────────────────────┤
│ Total compras        │ {gastos - porcentaje:,}$
│ Descuento cupón      │ {porcentaje}$
│ Caja                 │ {caja.title()}
├──────────────────────┼──────────────────────────────────────────┤
│ Productos            │ {carrito}
└──────────────────────┴──────────────────────────────────────────┘\n
""")      # IMPRESION HECHO CON IA 
        
        return True
    return False


def finish_payment(sessions_payment):
    
    if sessions_payment:
        try:
            process_buy_tarjet = int(input('>   '))
            if process_buy_tarjet == 0:
                state_app['logs-generals']['logs-buy-product']['logs-process']
                return True,  # 111 + registar in bd in key of 101 
            else:
                return False # 501 IN LOG + mostrar mensaje > FINALIZAR
        except ValueError:
            return False #no puedes usar letras en este campo 
    else:
        return False



def update_almacen(remove_products, state_app):
    if remove_products:
        #RECORRE LAS LISTAS CON LOS CODIGOS PASADOS EN EL CAJERO > PARA ELIMINARLOS EN UNA COPIA
        for sesions in state_app['sesion-modulos']['canasta']: # RECORRIDO DE NOMBRES AGREGADOS
            if state_app['general-products-bd'][sesions]['codigo'] in state_app['sesion-modulos']['code-safety']:
                state_app['sesion-modulos']['product-delete'].append(sesions)# AGREGA EL NOMBRE DEL PRODUCTO
                state_app['sesion-modulos']['product-value'].append(state_app['general-products-bd'].copy().pop(sesions)) # DEVUELVE EL VALOR DE LA LLAVE > AGREGA LA INFO DE LOS PRODUCTOS
        return True
    else:
        return False


def logs_delete_product(update_values, state_app, ):
    if update_values:
        #ABRE UN DICC PARA GUARDAR EL LOG DE X PRODUCTOS EN UNA MISMA FECHA + HORA > CANASTA
        state_app['logs-generals']['logs-delete-buy'].setdefault(time_procesin, {}) # CREA UN DICC CON KEY + VALUE COPIADOS DE LA FUNC; UPDATE_ALMACEN
        state_app['logs-generals']['logs-delete-buy'][time_procesin] = dict(zip(state_app['sesion-modulos']['product-delete'], state_app['sesion-modulos']['product-value']))
        state_app['logs-generals']['logs-delete-buy']['logs-coding-cache'].update(state_app['sesion-modulos']['code-safety'])
        return True
    else:
        return False
    

def log_assignment(message_on, memoryclean):
    if not memoryclean:
        for code_type_error, value_type_name in state_app['types_error_code'].items():
            if message_on == value_type_name:
                state_app['logs-generals']['logs-buy-product']['logs-process'][time_procesin].setdefault('TYPE_ERROR_CODE', code_type_error) # None > codigo de message_on
            else:
                continue
        state_app['logs-generals']['logs-buy-product']['logs-process'][time_procesin].setdefault('PROCESS_FINISH', message_on) 
        return False
    else:
        for code_type_error, value_type_name in state_app['types_error_code'].items():
            if message_on == value_type_name:
                state_app['logs-generals']['logs-buy-product']['logs-process'][time_procesin].setdefault('TYPE_NUMBER_CODE_', code_type_error)
        state_app['logs-generals']['logs-buy-product']['logs-process'][time_procesin].setdefault('PROCESS_FINISH', message_on) 
        return True
           
           
def delete_product_stock(log_confirmation):
    if log_confirmation:
        for identificador in state_app['sesion-modulos']['product-delete']: #ELIMINA EL PRODUCTO CON SU KEY REGISTRADA EN UN SET
            state_app['general-products-bd'].pop(identificador)
    else:
        return False
            
def memory_canast_clear(initial_values, state_app):
    if not initial_values:
        for elements_used in state_app['sesion-modulos']:
            state_app['sesion-modulos'][elements_used] = type(state_app['sesion-modulos'][elements_used])()
        print('Fin True')
    else:
        print('Fin False')


code_validation = collected_codes(state_app)

codeexpered_validation, message_on = validation_codeexpired(code_validation, state_app)

orquestval = orquest_validatyon(codeexpered_validation)

codings = adding_codings(orquestval, state_app)

product_coding= product_addp_canast(codings, state_app)

pay_buy = finish_payment(product_coding)

immpresion_ticket = cash_calletion(pay_buy, state_app)

remove_products = sales_registers(immpresion_ticket, usuario='XXXXXXXXXX', fecha=time_procesin, cupon=True, canasta=state_app['sesion-modulos'].get('canasta'), precio=state_app['sesion-modulos'].get('total'))

update_values = update_almacen(remove_products, state_app)

memoryclean = logs_delete_product(update_values, state_app)

log_confirmation = log_assignment(message_on, memoryclean)

initial_values = delete_product_stock(log_confirmation)

memory_canast_clear(initial_values, state_app)

print(module_sessions)
print(logs_generals)
