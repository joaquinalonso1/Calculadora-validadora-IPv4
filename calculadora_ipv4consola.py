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




while True:
    entrada= input("Ingrese una dirección IP (o 'salir' para terminar): ").strip()
    if entrada.lower() == 'salir':
        break
    partes = entrada.split('/')
    if len(partes) != 2:
        print("Formato incorrecto. Acordarse de usar la barra (ej: /24).")
        continue
    ip_sola = partes[0]
    mascara_sola = partes[1]
    
    if validar_ip(ip_sola):
        if not mascara_sola.isdigit():
            print(f"{mascara_sola} no es una máscara de subred válida.")
            continue
        numero2 = int(mascara_sola)
        if not 0 <= numero2 <= 32:
            print(f"{mascara_sola} no es una máscara de subred válida.")
            continue
        print(f" Exito: IP {ip_sola} y mascara /{mascara_sola} son válidas.")
        print(f" La clase de la IP es: {calcular_clase_ip(ip_sola)}")
        mascara_decimal= calcular_mascara(numero2)
        print(f" La máscara de subred en formato decimal es: {mascara_decimal}")
        red_calculada= calcular_direccion_red(ip_sola, mascara_decimal)
        print(f" La dirección de red es: {red_calculada}")
        broadcast_calculado= calcular_broadcast(ip_sola, mascara_decimal)
        print(f" La dirección de broadcast es: {broadcast_calculado}")
        
        #separo los string de red y broadcast usando el puunto
        partes_red = red_calculada.split('.')
        partes_broadcast = broadcast_calculado.split('.')
        
        #aislo el ultimo octeto (indice 3), lo paso a entero y le aplico la matematica
        ultimo_octeto_red = int(partes_red[3])+1
        ultimo_octeto_broadcast = int(partes_broadcast[3])-1
        
        #ensamblo las ips utilizables manteniendo la base y cambiando la cola 
        primer_ip= f"{partes_red[0]}.{partes_red[1]}.{partes_red[2]}.{ultimo_octeto_red}"
        ultima_ip= f"{partes_broadcast[0]}.{partes_broadcast[1]}.{partes_broadcast[2]}.{ultimo_octeto_broadcast}"
        
        print(f"La primera IP utilizable es: {primer_ip}")
        print(f"La última IP utilizable es: {ultima_ip}")
        print(f" La cantidad de hosts posibles es: {2**(32-numero2) - 2}")
        
    else:
        print(f"{ip_sola} no es una dirección IP válida.")


