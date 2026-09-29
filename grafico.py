import customtkinter as ctk

# MOTOR LÓGICO ACÁ 
def validar_ip(ip):
    #hacemos que el resultado sea una lista de strings separadas por el punto
    octetos = ip.split('.')
    #si leemos que la longitud de la lista es diferente de 4, retornamos False
    #si la longitud es 4, queda validado y pasa a la siguiente validación
    if len(octetos) != 4:
        return False
    #validamos que cada octeto sea un número entre 0 y 255
    for octeto in octetos:
        if not octeto.isdigit():
            return False
        numero = int(octeto)
        if not 0 <= numero <= 255:
            return False
    return True

def calcular_mascara(prefijo):
    #1. multiplicacion de string para armar los 32 bits de la mascara
    unos = '1' * prefijo
    ceros = '0' * (32 - prefijo)
    #junto todo en un solo string largo de 32 caracteres exactos
    binario_completo = unos + ceros
    
    
    #2. separamos el string en 4 partes de 8 bits cada una
    binario1 = binario_completo[0:8]
    binario2 = binario_completo[8:16]
    binario3 = binario_completo[16:24]
    binario4 = binario_completo[24:32]
    
    #convertimos cada parte de bloque  binario de texto a un numero entero decimal
    decimal1 = int(binario1, 2)
    decimal2 = int(binario2, 2) 
    decimal3 = int(binario3, 2)
    decimal4 = int(binario4, 2)
    
    #armo el string final de la mascara en formato decimal separado por puntos
    mascara_final= f"{decimal1}.{decimal2}.{decimal3}.{decimal4}"
    return mascara_final


def calcular_direccion_red(ip_texto, mascara_texto):
    #separo los textos de la ip y la mascaara en listas usando el punto
    partes_ip = ip_texto.split('.')
    partes_mascara = mascara_texto.split('.')
    
    #convierto los 4 fragmentos de la ip a numeros enteros
    ip1= int(partes_ip[0])
    ip2= int(partes_ip[1])
    ip3= int(partes_ip[2])
    ip4= int(partes_ip[3])
    
    #convierto los 4 fragmentos de la mascara a numeros enteros
    mascara1= int(partes_mascara[0])
    mascara2= int(partes_mascara[1])
    mascara3= int(partes_mascara[2])
    mascara4= int(partes_mascara[3])
    
    #ahora hago el cruce logico
    red1= ip1 & mascara1
    red2= ip2 & mascara2
    red3= ip3 & mascara3
    red4= ip4 & mascara4    

    direccion_red= f"{red1}.{red2}.{red3}.{red4}"   
    return direccion_red    


def calcular_broadcast(ip_texto, mascara_texto):
    #separo los textos de la ip y la mascaara en listas usando el punto
    partes_ip = ip_texto.split('.')
    partes_mascara = mascara_texto.split('.')
    
    #convierto los 4 fragmentos de la ip a numeros enteros
    red1= int(partes_ip[0])
    red2= int(partes_ip[1])
    red3= int(partes_ip[2])
    red4= int(partes_ip[3])
    
    #convierto los 4 fragmentos de la mascara a numeros enteros
    broad1= int(partes_mascara[0])
    broad2= int(partes_mascara[1])
    broad3= int(partes_mascara[2])
    broad4= int(partes_mascara[3])
    
    #ahora hago el cruce logico para calcular el broadcast
    broadcast1= red1 | (255 - broad1)
    broadcast2= red2 | (255 - broad2)
    broadcast3= red3 | (255 - broad3)
    broadcast4= red4 | (255 - broad4)    

    direccion_broadcast= f"{broadcast1}.{broadcast2}.{broadcast3}.{broadcast4}"   
    return direccion_broadcast


def calcular_clase_ip(ip):
    primer_octeto = int(ip.split('.')[0])
    if 1 <= primer_octeto <= 127:
        return "Clase A"
    elif 128 <= primer_octeto <= 191:
        return "Clase B"
    elif 192 <= primer_octeto <= 223:
        return "Clase C"
    elif 224 <= primer_octeto <= 239:
        return "Clase D (Multicast)"
    elif 240 <= primer_octeto <= 255:
        return "Clase E (Experimental)"
    else:
        return "Desconocida"




# --- 2. EL PUENTE ENTRE LA GRÁFICA Y LA LÓGICA ---
def procesar_calculo():
    # 1. Limpiamos los mensajes anteriores cada vez que se apreta el botón
    label_estado.configure(text="")
    label_red.configure(text="Red: -")
    label_broadcast.configure(text="Broadcast: -")
    label_hosts.configure(text="Hosts utilizables: -")

    # 2. Capturamos lo que el usuario escribió en la caja
    entrada = entrada_ip.get().strip()

    # 3. Primer barrera: El corte del prefijo
    partes = entrada.split('/')
    if len(partes) != 2:
        label_estado.configure(text="❌ Error: Usá la barra (ej: /24)", text_color="red")
        return # El return frena la ejecución acá mismo
        
    ip_sola = partes[0]
    mascara_sola = partes[1]

    # 4. Segunda barrera: Tu validador de IP
    if validar_ip(ip_sola):
        
        # Validamos la máscara
        if not mascara_sola.isdigit():
            label_estado.configure(text="❌ Error: La máscara debe ser un número.", text_color="red")
            return
            
        numero2 = int(mascara_sola)
        if not 0 <= numero2 <= 32:
            label_estado.configure(text="❌ Error: Máscara fuera de rango (0-32).", text_color="red")
            return
            
        # --- ZONA DE CÁLCULO ---
        # Llamá a tus funciones como hacías en el while
        clase_ip = calcular_clase_ip(ip_sola)
        
        # --- CÁLCULO DEL RANGO ---
    
        mascara_decimal = calcular_mascara(numero2)
        red_calculada = calcular_direccion_red(ip_sola, mascara_decimal)
        broadcast_calculado = calcular_broadcast(ip_sola, mascara_decimal)
        hosts = 2**(32 - numero2) - 2
        partes_red = red_calculada.split('.')
        primer_host = f"{partes_red[0]}.{partes_red[1]}.{partes_red[2]}.{int(partes_red[3]) + 1}"
        
        partes_broad = broadcast_calculado.split('.')
        ultimo_host = f"{partes_broad[0]}.{partes_broad[1]}.{partes_broad[2]}.{int(partes_broad[3]) - 1}"
        
        rango = f"{primer_host} - {ultimo_host}"
        if hosts <= 0:
            rango = "No hay hosts utilizables (/31 o /32)"
        
        # --- ACTUALIZACIÓN VISUAL ---
        # Si llegó hasta acá, todo es un éxito. Inyectamos los datos en la interfaz.
        label_estado.configure(text="✅ Cálculo exitoso", text_color="green")
        label_clase.configure(text=f"Clase: {clase_ip}")
        label_mascara.configure(text=f"Máscara: {mascara_decimal}")
        label_rango.configure(text=f"Rango de IPs: {rango}")
        label_red.configure(text=f"Red: {red_calculada}")
        label_broadcast.configure(text=f"Broadcast: {broadcast_calculado}")
        label_hosts.configure(text=f"Hosts utilizables: {hosts}")
        
    else:
        # Si validar_ip() devolvió False
        label_estado.configure(text="❌ Error: Dirección IP inválida.", text_color="red")




# --- 3. DISEÑO VISUAL DE LA VENTANA ---
# Configuración base de CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ventana = ctk.CTk()
ventana.title("Calculadora de Subredes IPv4")
ventana.geometry("700x700")

# Título principal
label_titulo = ctk.CTkLabel(ventana, text="Calculadora CIDR", font=("Roboto", 24, "bold"))
label_titulo.pack(pady=30)

# Caja de entrada
entrada_ip = ctk.CTkEntry(ventana, placeholder_text="Ej: 192.168.1.50/24", width=250)
entrada_ip.pack(pady=10)

# Botón de acción (conecta con la función procesar_calculo)
boton_calcular = ctk.CTkButton(ventana, text="Calcular Subred", command=procesar_calculo)
boton_calcular.pack(pady=20)

# Etiquetas de resultados (arrancan con guiones)
label_estado = ctk.CTkLabel(ventana, text="", text_color="yellow")
label_estado.pack(pady=5)

# Etiqueta inicial para mostrar la Clase de IP
label_clase = ctk.CTkLabel(ventana, text="Clase: -", font=("Arial", 14))
label_clase.pack(pady=5)

label_mascara = ctk.CTkLabel(ventana, text="Máscara: -", font=("Arial", 14))
label_mascara.pack(pady=5)

label_rango = ctk.CTkLabel(ventana, text="Rango de IPs: -", font=("Arial", 14))
label_rango.pack(pady=5)

label_red = ctk.CTkLabel(ventana, text="Red: -", font=("Roboto", 14))
label_red.pack(pady=5)

label_broadcast = ctk.CTkLabel(ventana, text="Broadcast: -", font=("Roboto", 14))
label_broadcast.pack(pady=5)

label_hosts = ctk.CTkLabel(ventana, text="Hosts utilizables: -", font=("Roboto", 14))
label_hosts.pack(pady=5)

# Bucle principal que mantiene la ventana abierta
ventana.mainloop()