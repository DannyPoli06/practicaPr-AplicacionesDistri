import socket
import threading

# ==========================================
# 1. CONFIGURACIÓN DE LA CONEXIÓN PRIMERO
# ==========================================
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(('127.0.0.1', 5000))
servidor.listen(5)

# Base de datos en memoria y variables globales
productos = {1: "Laptop", 2: "Mouse", 3: "Teclado"}
stock = {1: 5, 2: 12, 3: 0}
id_siguiente = 4

print("Servidor TCP iniciado en el puerto 5000...")

# ==========================================
# 2. FUNCIONES DE LÓGICA Y MANEJO DE CLIENTES
# ==========================================
def manejar_cliente(conn, addr):
    global id_siguiente
    print("Nuevo cliente conectado desde:", addr)
    
    # Recibir el rol al iniciar
    rol_bytes = conn.recv(1024)
    rol = rol_bytes.decode('utf-8')
    
    while (True):
        mensaje_bytes = conn.recv(1024)
        if (not mensaje_bytes):
            break
            
        mensaje = mensaje_bytes.decode('utf-8')
        partes = mensaje.split('|')
        accion = partes[0]
        respuesta = ""
        
        if (accion == "SALIR"):
            respuesta = "Sesion cerrada."
            conn.sendall(respuesta.encode('utf-8'))
            break
            
        # 1. CONSULTAR (Stock >= 1)
        if (accion == "CONSULTAR"):
            resultado = "--- LISTA DE PRODUCTOS ---\n"
            for id_p in productos:
                cant = stock[id_p]
                if (cant >= 1):
                    resultado = resultado + "ID: " + str(id_p) + " | " + productos[id_p] + " | Stock: " + str(cant) + "\n"
            respuesta = resultado
            
        # 2. COMPRAR (Solo Clientes)
        elif (accion == "COMPRAR"):
            if (rol != "CLIENTE"):
                respuesta = "ERROR: Solo los clientes pueden comprar."
            else:
                p_id = int(partes[1])
                cantidad = int(partes[2])
                if (p_id in productos):
                    if (stock[p_id] >= cantidad):
                        stock[p_id] = stock[p_id] - cantidad
                        respuesta = "Compra exitosa. Stock restante: " + str(stock[p_id])
                    else:
                        respuesta = "ERROR: Stock insuficiente."
                else:
                    respuesta = "ERROR: El ID del producto no existe."
                    
        # 3. AGREGAR (Solo Administradores)
        elif (accion == "AGREGAR"):
            if (rol != "ADMIN"):
                respuesta = "ERROR: Solo los administradores pueden agregar productos."
            else:
                nombre = partes[1]
                cantidad_ini = int(partes[2])
                productos[id_siguiente] = nombre
                stock[id_siguiente] = cantidad_ini
                respuesta = "Producto agregado con ID: " + str(id_siguiente)
                id_siguiente = id_siguiente + 1
                
        conn.sendall(respuesta.encode('utf-8'))
        
    conn.close()
    print("Cliente desconectado:", addr)

# ==========================================
# 3. BUCLE PRINCIPAL (Aceptar conexiones e hilos)
# ==========================================
while (True):
    conn, addr = servidor.accept()
    hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
    hilo.start()