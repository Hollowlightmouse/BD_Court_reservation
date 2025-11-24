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

        cursor.execute("CREATE DATABASE IF NOT EXISTS db_canchas")
        cursor.execute("USE db_canchas")
        print("Base de datos 'db_canchas' seleccionada o creada correctamente.\n")
        logging.info("Base de datos 'db_canchas' seleccionada o creada correctamente.")


        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Roles (
            idRol INT AUTO_INCREMENT PRIMARY KEY,
            nombreRol VARCHAR(45) NOT NULL,
            descripcion VARCHAR(200),
            fechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            fechaActualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """)
        logging.info("Tabla 'Roles' creada/verificada correctamente.")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS TipoDocumentos (
            idTipoDocumento INT AUTO_INCREMENT PRIMARY KEY,
            nombreDocumento VARCHAR(45) NOT NULL,
            abreviatura VARCHAR(10) NOT NULL
        )
        """)
        logging.info("Tabla 'TipoDocumentos' creada/verificada correctamente.")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS TipoCancha (
            idTipoCancha INT AUTO_INCREMENT PRIMARY KEY,
            nombreTipo VARCHAR(45) NOT NULL
        )
        """)
        logging.info("Tabla 'TipoCancha' creada/verificada correctamente.")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS MetodosPago (
            idMetodoPago INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(45) NOT NULL,
            descripcion VARCHAR(200),
            estado TINYINT DEFAULT 1
        )
        """)
        logging.info("Tabla 'MetodosPago' creada/verificada correctamente.")


        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Usuarios (
            idUsuario INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARBINARY(255) NOT NULL,
            apellido VARBINARY(255) NOT NULL,
            correo VARBINARY(255) NOT NULL UNIQUE,
            contrasena VARBINARY(255) NOT NULL,
            telefono VARBINARY(255),
            direccion VARBINARY(255),
            idRol INT,
            idTipoDocumento INT,
            estado TINYINT DEFAULT 1,
            fechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            fechaActualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (idRol) REFERENCES Roles(idRol),
            FOREIGN KEY (idTipoDocumento) REFERENCES TipoDocumentos(idTipoDocumento)
        )
        """)
        logging.info("Tabla 'Usuarios' creada/verificada correctamente.")


        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Canchas (
            idCancha INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            ubicacion VARCHAR(100) NOT NULL,
            precio_hora DECIMAL(10,2) NOT NULL CHECK (precio_hora > 0),
            limite_personas INT CHECK (limite_personas > 0),
            idTipoCancha INT,
            estado TINYINT DEFAULT 1,
            fechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            fechaActualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (idTipoCancha) REFERENCES TipoCancha(idTipoCancha)
        )
        """)
        logging.info("Tabla 'Canchas' creada/verificada correctamente.")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Facturas (
            idFactura INT AUTO_INCREMENT PRIMARY KEY,
            fechaEmision DATETIME DEFAULT CURRENT_TIMESTAMP,
            numeroFactura VARCHAR(50) UNIQUE,
            subtotal DECIMAL(10,2) NOT NULL,
            impuesto DECIMAL(10,2) NOT NULL,
            total DECIMAL(10,2) NOT NULL,
            metodoPago INT,
            estadoFactura TINYINT DEFAULT 0,
            detalles VARCHAR(255),
            FOREIGN KEY (metodoPago) REFERENCES MetodosPago(idMetodoPago)
        )
        """)
        logging.info("Tabla 'Facturas' creada/verificada correctamente.")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Pagos (
            idPago INT AUTO_INCREMENT PRIMARY KEY,
            idFactura INT NOT NULL,
            fechaPago DATETIME DEFAULT CURRENT_TIMESTAMP,
            monto DECIMAL(10,2) NOT NULL CHECK (monto > 0),
            metodoPago INT,
            estadoPago TINYINT DEFAULT 1,
            referencia VARCHAR(100),
            FOREIGN KEY (idFactura) REFERENCES Facturas(idFactura),
            FOREIGN KEY (metodoPago) REFERENCES MetodosPago(idMetodoPago)
        )
        """)
        logging.info("Tabla 'Pagos' creada/verificada correctamente.")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Reservas (
            idReserva INT AUTO_INCREMENT PRIMARY KEY,
            idUsuario INT NOT NULL,
            idCancha INT NOT NULL,
            idFactura INT,
            fechaInicio DATETIME NOT NULL,
            fechaFin DATETIME NOT NULL,
            estado TINYINT DEFAULT 1,
            precioTotal DECIMAL(10,2) NOT NULL,
            fechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            fechaActualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (idUsuario) REFERENCES Usuarios(idUsuario),
            FOREIGN KEY (idCancha) REFERENCES Canchas(idCancha),
            FOREIGN KEY (idFactura) REFERENCES Facturas(idFactura)
        )
        """)
        logging.info("Tabla 'Reservas' creada/verificada correctamente.")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS DetalleReservas (
            idDetalle INT AUTO_INCREMENT PRIMARY KEY,
            idReserva INT NOT NULL,
            tipoMovimiento VARCHAR(45) NOT NULL,
            descripcion VARCHAR(255),
            usuarioResponsable INT,
            fechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (idReserva) REFERENCES Reservas(idReserva),
            FOREIGN KEY (usuarioResponsable) REFERENCES Usuarios(idUsuario)
        )
        """)
        logging.info("Tabla 'DetalleReservas' creada/verificada correctamente.")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS MovimientosFacturas (
            idMovimiento INT AUTO_INCREMENT PRIMARY KEY,
            idFactura INT NOT NULL,
            tipoMovimiento VARCHAR(45) NOT NULL,
            descripcion VARCHAR(255),
            usuarioResponsable INT,
            fechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (idFactura) REFERENCES Facturas(idFactura),
            FOREIGN KEY (usuarioResponsable) REFERENCES Usuarios(idUsuario)
        )
        """)
        logging.info("Tabla 'MovimientosFacturas' creada/verificada correctamente.")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS HistorialSesiones (
            idSesion INT AUTO_INCREMENT PRIMARY KEY,
            idUsuario INT,
            fechaInicio DATETIME DEFAULT CURRENT_TIMESTAMP,
            fechaFin DATETIME,
            ip VARCHAR(50),
            dispositivo VARCHAR(100),
            resultado ENUM('Exitoso','Fallido') DEFAULT 'Exitoso',
            FOREIGN KEY (idUsuario) REFERENCES Usuarios(idUsuario)
        )
        """)
        logging.info("Tabla 'HistorialSesiones' creada/verificada correctamente.")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS OpinionesUsuarios (
            idOpinion INT AUTO_INCREMENT PRIMARY KEY,
            idUsuario INT,
            idReserva INT,
            puntuacion TINYINT CHECK (puntuacion BETWEEN 1 AND 5),
            comentario TEXT,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (idUsuario) REFERENCES Usuarios(idUsuario),
            FOREIGN KEY (idReserva) REFERENCES Reservas(idReserva)
        )
        """)
        logging.info("Tabla 'OpinionesUsuarios' creada/verificada correctamente.")

        print(" Todas las tablas fueron creadas.\n")
        logging.info("Todas las tablas creadas correctamente en la base de datos 'db_canchas'.")


except Error as e:
    print(" Error:", e)
    logging.error("Error en la base de datos: %s", e)


finally:
    if connection and connection.is_connected():
        cursor.close()
        connection.close()
        print("Conexión cerrada.")
        logging.info("Conexión MySQL cerrada correctamente.")
