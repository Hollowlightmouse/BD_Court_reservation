import mysql.connector as msql
from mysql.connector import Error
import logging


logging.basicConfig(
    filename="log_db_canchas.log",          
    level=logging.INFO,                    
    format="%(asctime)s - %(levelname)s - %(message)s",  
)

try:
    connection = msql.connect(
        host="localhost",
        port="3306",
        user="root",
        password=""
    )

    if connection.is_connected():
        cursor = connection.cursor()
        print("Conexión establecida con MySQL.\n")
        logging.info("Conexión establecida con MySQL.")

        cursor.execute("CREATE DATABASE IF NOT EXISTS Court_reservation")
        cursor.execute("USE Court_reservation")
        print("Base de datos 'Court_reservation' seleccionada o creada correctamente.\n")
        logging.info("Base de datos 'Court_reservation' seleccionada o creada correctamente.")

        # Tabla Roles
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Roles (
            idRol INT AUTO_INCREMENT PRIMARY KEY,
            nombreRol VARCHAR(45) NOT NULL,
            descripcion VARCHAR(200) NOT NULL,
            fechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            fechaActualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """)
        logging.info("Tabla 'Roles' creada/verificada correctamente.")

        # Tabla TipoDocumentos
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS TipoDocumentos (
            idTipoDocumento INT AUTO_INCREMENT PRIMARY KEY,
            nombreDocumento VARCHAR(20) NOT NULL,
            abreviatura VARCHAR(5) NOT NULL
        )
        """)
        logging.info("Tabla 'TipoDocumentos' creada/verificada correctamente.")

        # Tabla TipoCancha
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS TipoCancha (
            idTipoCancha INT AUTO_INCREMENT PRIMARY KEY,
            nombreTipo VARCHAR(60) NOT NULL
        )
        """)
        logging.info("Tabla 'TipoCancha' creada/verificada correctamente.")

        # Tabla MetodosPago
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS MetodosPago (
            idMetodoPago INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(45) NOT NULL,
            descripcion VARCHAR(100) NOT NULL,
            estado TINYINT(1) NOT NULL DEFAULT 1
        )
        """)
        logging.info("Tabla 'MetodosPago' creada/verificada correctamente.")

        # Tabla Usuarios (con anonimización)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Usuarios (
            idUsuario INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARBINARY(255) NOT NULL,
            apellido VARBINARY(255) NOT NULL,
            correo VARBINARY(255) NOT NULL UNIQUE,
            contraseña VARBINARY(255) NOT NULL,
            telefono VARBINARY(255),
            direccion VARBINARY(255),
            idRol INT NOT NULL,
            idTipoDocumento INT NOT NULL,
            estado TINYINT DEFAULT 1,
            fechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            fechaActualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (idRol) REFERENCES Roles(idRol),
            FOREIGN KEY (idTipoDocumento) REFERENCES TipoDocumentos(idTipoDocumento)
        )
        """)
        logging.info("Tabla 'Usuarios' creada/verificada correctamente.")

        # Tabla Canchas
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Canchas (
            idCancha INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(225) NOT NULL,
            ubicacion VARCHAR(45) NOT NULL,
            precio_hora DECIMAL(10,2) NOT NULL CHECK (precio_hora > 0),
            LimitePersonas VARCHAR(50) NOT NULL,
            idTipoCancha INT NOT NULL,
            Estado TINYINT NOT NULL DEFAULT 1,
            fechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            fechaActualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (idTipoCancha) REFERENCES TipoCancha(idTipoCancha)
        )
        """)
        logging.info("Tabla 'Canchas' creada/verificada correctamente.")

        # Tabla Facturas
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Facturas (
            idFactura INT AUTO_INCREMENT PRIMARY KEY,
            fecha_hora_emision DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            numero_factura VARCHAR(45) NOT NULL UNIQUE,
            subtotal DECIMAL(10,2) NOT NULL,
            impuesto DECIMAL(10,2) NOT NULL,
            total DECIMAL(10,2) NOT NULL,
            metodo_pago VARCHAR(45) NOT NULL,
            estado_factura INT(1) NOT NULL,
            detalles TEXT NOT NULL,
            metodoPago_idMetodoPago INT NOT NULL,
            FOREIGN KEY (metodoPago_idMetodoPago) REFERENCES MetodosPago(idMetodoPago)
        )
        """)
        logging.info("Tabla 'Facturas' creada/verificada correctamente.")

        # Tabla Pagos
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Pagos (
            idPago INT AUTO_INCREMENT PRIMARY KEY,
            idFactura INT NOT NULL,
            fecha_hora_pago DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            monto DECIMAL(10,2) NOT NULL CHECK (monto > 0),
            metodo_pago VARCHAR(45) NOT NULL,
            estado_pago INT(1) NOT NULL,
            referencia_pago VARCHAR(255) NOT NULL,
            metodoPago_idMetodoPago INT NOT NULL,
            FOREIGN KEY (idFactura) REFERENCES Facturas(idFactura),
            FOREIGN KEY (metodoPago_idMetodoPago) REFERENCES MetodosPago(idMetodoPago)
        )
        """)
        logging.info("Tabla 'Pagos' creada/verificada correctamente.")

        # Tabla Reservas
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Reservas (
            idReserva INT AUTO_INCREMENT PRIMARY KEY,
            idUsuario INT NOT NULL,
            idCancha INT NOT NULL,
            idPago INT NOT NULL,
            fechaInicio DATETIME NOT NULL,
            fechaFin DATETIME NOT NULL,
            estado INT(1) NULL,
            precioTotal DECIMAL(10,2) NULL,
            fechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            fechaActualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (idUsuario) REFERENCES Usuarios(idUsuario),
            FOREIGN KEY (idCancha) REFERENCES Canchas(idCancha),
            FOREIGN KEY (idPago) REFERENCES Pagos(idPago)
        )
        """)
        logging.info("Tabla 'Reservas' creada/verificada correctamente.")

        # Tabla DetalleReservas (Auditoría de reservas)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS DetalleReservas (
            idDetalleMovReserva INT AUTO_INCREMENT PRIMARY KEY,
            idReserva INT NOT NULL,
            tipoMovimiento VARCHAR(45) NOT NULL,
            descripcion VARCHAR(255),
            fechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            fechaActualizacion DATE NOT NULL,
            usuarioResponsable INT,
            FOREIGN KEY (idReserva) REFERENCES Reservas(idReserva),
            FOREIGN KEY (usuarioResponsable) REFERENCES Usuarios(idUsuario)
        )
        """)
        logging.info("Tabla 'DetalleReservas' creada/verificada correctamente.")

        # Tabla MovimientosFacturas (Auditoría de facturas)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS MovimientosFacturas (
            idMovimientosFactura INT AUTO_INCREMENT PRIMARY KEY,
            idFactura INT NOT NULL,
            tipoMovimiento VARCHAR(45) NULL,
            fechaCreacion DATE NULL,
            fechaActualizacion DATE NOT NULL,
            usuarioResponsable INT,
            FOREIGN KEY (idFactura) REFERENCES Facturas(idFactura),
            FOREIGN KEY (usuarioResponsable) REFERENCES Usuarios(idUsuario)
        )
        """)
        logging.info("Tabla 'MovimientosFacturas' creada/verificada correctamente.")

        # Tabla HistorialSesiones (con anonimización de IP)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS HistorialSesiones (
            idHistorialSesiones INT AUTO_INCREMENT PRIMARY KEY,
            idUsuario INT NOT NULL,
            fechaInicio DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            fechaFin DATETIME,
            ip VARCHAR(50) NOT NULL,
            dispositivo VARCHAR(100) NOT NULL,
            resultado ENUM('Exitoso', 'Fallido') NOT NULL,
            FOREIGN KEY (idUsuario) REFERENCES Usuarios(idUsuario)
        )
        """)
        logging.info("Tabla 'HistorialSesiones' creada/verificada correctamente.")

        # Tabla OpinionesUsuarios
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS OpinionesUsuarios (
            idOpinionesUsuarios INT AUTO_INCREMENT PRIMARY KEY,
            idUsuario INT NOT NULL,
            idReserva INT NOT NULL,
            puntuacion TINYINT(5) NOT NULL CHECK (puntuacion BETWEEN 1 AND 5),
            comentario TEXT,
            fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (idUsuario) REFERENCES Usuarios(idUsuario),
            FOREIGN KEY (idReserva) REFERENCES Reservas(idReserva)
        )
        """)
        logging.info("Tabla 'OpinionesUsuarios' creada/verificada correctamente.")

        print(" Todas las tablas fueron creadas correctamente.\n")
        logging.info("Todas las tablas creadas correctamente en la base de datos 'db_canchas'.")

        connection.commit()

except Error as e:
    print("✗ Error:", e)
    logging.error("Error en la base de datos: %s", e)

finally:
    if connection and connection.is_connected():
        cursor.close()
        connection.close()
        print("Conexión cerrada.")
        logging.info("Conexión MySQL cerrada correctamente.")