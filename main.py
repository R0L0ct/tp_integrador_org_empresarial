import re

# Estados posibles: 'INICIO', 'ESPERANDO_CUIT', 'ESPERANDO_RAZON_SOCIAL', 'ESPERANDO_RUBRO', 'PENDIENTE'

# Lista de diccionarios para simular una base de datos pero en memoria. 
# La inicializamos con datos pre cargados.
database_proveedores = [
    {"cuit": "20301234567", "razon_social": "Tech Solutions S.A.", "rubro": "Informática", "estado": "APROBADO"},
    {"cuit": "27459876543", "razon_social": "Logística del Norte", "rubro": "Transporte", "estado": "APROBADO"}
]

# Función generadora de sesiones: retorna una sesión limpia.
def crear_sesion() -> dict:
    return {"state": "INICIO", "temp_cuit": None, "temp_razon_social": None}

# Función chatbot: realiza todo el proceso de alta de proveedores
def procesar_mensaje_bot(mensaje: str, session: dict) -> str:
    mensaje = mensaje.strip()

    # --- ESTADO: INICIO ---
    if session["state"] == "INICIO":
        if mensaje.lower() == "/registrar":
            session["state"] = "ESPERANDO_CUIT"
            return "🏢 [Bot]: Ingrese el CUIT (11 números, sin guiones):", session
        return "❌ [Bot]: Comando no reconocido. Escriba '/registrar'.", session

    # --- ESTADO: ESPERANDO CUIT ---
    elif session["state"] == "ESPERANDO_CUIT":
        # MANEJO DEL CAMINO INFELIZ: Validación del formato del CUIT ingresado 
        # Para este caso simplemente validamos que contenga 11 caracteres empleando para ello un regex
        if not re.match(r"^\d{11}$", mensaje):
            return "⚠️ [VALOR INVÁLIDO]: El CUIT debe contener exactamente 11 caracteres numéricos y ningún guion. Intente nuevamente:", session

        # COMPUERTA LÓGICA (Gateway): Validación contra base de datos
        if any(p["cuit"] == mensaje for p in database_proveedores):
            session.update(crear_sesion())
            return "❌ [ERROR]: El CUIT ya está registrado. Proceso cancelado.", session


        # Transición de estado (Camino Feliz)
        session["temp_cuit"] = mensaje
        session["state"] = "ESPERANDO_RAZON_SOCIAL"
        return "✅ [CUIT Válido]. Ingrese la Razón Social:", session

    # --- ESTADO: ESPERANDO RAZÓN SOCIAL ---
    elif session["state"] == "ESPERANDO_RAZON_SOCIAL":
        # MANEJO DEL CAMINO INFELIZ: Validación de longitud de caracteres 
        # Simplemente verificamos que la razón social no sea menor a 3 caracteres
        if len(mensaje) < 3:
            return "⚠️ [VALOR INVÁLIDO]: La Razón Social es demasiado corta. Ingrese un nombre legal válido:", session

        session["temp_razon_social"] = mensaje
        session["state"] = "ESPERANDO_RUBRO"
        return "📝 [Guardado]. Ingrese el rubro comercial:", session

    # --- ESTADO: ESPERANDO RUBRO ---
    elif session["state"] == "ESPERANDO_RUBRO":
        if len(mensaje) < 3:
            return "⚠️ [VALOR INVÁLIDO]: Por favor, especifique un rubro comercial válido (Mínimo 3 letras):", session

        # Simulación de persistencia: Inserción del nuevo registro en la base de datos
        nuevo_proveedor = {
            "cuit": session["temp_cuit"],
            "razon_social": session["temp_razon_social"],
            "rubro": mensaje,
            "estado": "PENDIENTE" # Regla organizativa: requiere auditoría
        }
        database_proveedores.append(nuevo_proveedor)

        # Reseteo completo de la sesión tras finalizar con éxito el circuito
        session.update(crear_sesion())
        return f"🎉 [ALTA EXITOSA]: '{nuevo_proveedor['razon_social']}' registrada en estado PENDIENTE.", session
    else:
        raise ValueError(f"Estado desconocido: {session['state']}")


if __name__ == "__main__":
    print("=====================================================================")
    print("  CHATBOT: ALTA DE PROVEEDORES ")
    print("=====================================================================")
    print("Escriba '/registrar' para comenzar o 'salir' para cerrar la aplicación.\n")

    # Se crea la sesión inicial
    session = crear_sesion()
    while True:
        # El bucle mantiene al script escuchando de forma constante similar a un servidor real
        try:
            # Input para almacenar el mensaje del usuario 
            user_input = input("Tú > ")
            
            # Condición de quiebre para apagar la infraestructura del bot
            if user_input.strip().lower() == "salir":
                print("Cerrando el servicio del Bot corporativo. ¡Hasta luego!")
                break
                
            # Envío de la señal a la máquina de estados del bot
            respuesta, session = procesar_mensaje_bot(user_input, session)
            print(f"{respuesta}\n")
            
        except (KeyboardInterrupt, SystemExit):
            print("\nServicio interrumpido de forma abrupta por el sistema.")
            break