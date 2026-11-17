import socket

# ============== CONEXION  =================

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('127.0.0.1', 5000))

#============= se selecciona el rol ===========

print("=== SISTEMA DE TIENDA (TCP) ===")
rol = input("Ingresa tu rol (CLIENTE o ADMIN): ").strip().upper()

# Enviar rol inicial al servidor
cliente.sendall(rol.encode('utf-8'))

# =========== menu ================

while (True):
    print("\n--- MENU (" + rol + ") ---")
    print("1. Consultar productos")
    if (rol == "CLIENTE"):
        print("2. Comprar producto")
    if (rol == "ADMIN"):
        print("2. Agregar producto")
    print("3. Salir")
    
    opcion = input("Elige una opcion: ")
    
    if (opcion == "1"):
        mensaje = "CONSULTAR"
    elif (opcion == "2"):
        if (rol == "CLIENTE"):
            p_id = input("ID del producto: ")
            cant = input("Cantidad: ")
            mensaje = "COMPRAR|" + p_id + "|" + cant
        else:
            nombre = input("Nombre del producto: ")
            cant = input("Stock inicial: ")
            mensaje = "AGREGAR|" + nombre + "|" + cant
    elif (opcion == "3"):
        mensaje = "SALIR"
        cliente.sendall(mensaje.encode('utf-8'))
        break
    else:
        print("Opcion invalida")
        continue
    
    # Enviar y recibir por TCP
    cliente.sendall(mensaje.encode('utf-8'))
    respuesta_bytes = cliente.recv(2048)
    print("\nRespuesta del Servidor:\n" + respuesta_bytes.decode('utf-8'))

cliente.close()