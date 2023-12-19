#!/usr/bin/env python3

import hashlib
import secrets
import os
import platform
import subprocess

# Función para ejecutar Hashcat y encontrar coincidencias
def ejecutar_hashcat(archivo_hashes, archivo_listado):
    comando_hashcat = f"hashcat -a 0 -m 0 {archivo_hashes} {archivo_listado} -o plain.txt --potfile-disable"
    os.system(comando_hashcat)

# Función para comparar hashes originales con los encontrados por Hashcat
def comparar_hashes(archivo_hashes, archivo_listado):
    # Abrir plain.txt para escritura
    with open("plain.txt", "w") as archivo_salida:
        # Llamar a ejecutar_hashcat para obtener las coincidencias
        ejecutar_hashcat(archivo_hashes, archivo_listado)

        # Abrir plain.txt para lectura
        with open("plain.txt", "r") as archivo_resultado:
            hashes_encontrados = archivo_resultado.readlines()

        # Abrir archivo_hashes para lectura
        with open(archivo_hashes, "r", encoding="latin-1") as archivo_original:
            hashes_originales = archivo_original.readlines()

        # Comparar hashes y escribir resultados en plain.txt
        for hash_original in hashes_originales:
            hash_original = hash_original.strip()
            hash_encontrado = next((h.strip() for h in hashes_encontrados if h.strip() and h.strip().startswith(hash_original)), None)

            if hash_encontrado:
                archivo_salida.write(f"{hash_original} {hash_encontrado[len(hash_original):].strip()}\n")
            else:
                archivo_salida.write(f"{hash_original}\n")

# Función para crear contraseñas con hashes SHA-256 y salt
def crear_passwords(archivo_entrada="plain.txt", archivo_salida="passwords.txt"):
    # Abrir plain.txt para lectura
    with open(archivo_entrada, "r") as archivo_entrada:
        lineas = archivo_entrada.readlines()

    # Abrir archivo_salida para escritura
    with open(archivo_salida, "w") as archivo_salida:
        # Procesar cada línea en plain.txt
        for linea in lineas:
            valores = linea.strip().split(':')
            if len(valores) >= 2:
                # Tomar el segundo valor original
                palabra_asociada = valores[1]
                
                # Generar un salt aleatorio
                salt = secrets.token_hex(8)

                # Calcular el hash SHA-256 con salt
                hash_sha256 = hashlib.sha256((palabra_asociada + salt).encode()).hexdigest()

                # Escribir el resultado en passwords.txt
                archivo_salida.write(f"{valores[1]}: {hash_sha256}\n")
            else:
                # Escribir la línea tal cual en passwords.txt si no hay segundo valor
                archivo_salida.write(f'{linea}')

# Función para verificar si Hashcat está instalado en sistemas Debian
def verificar_hashcat_instalado():
    try:
        resultado = subprocess.run(["hashcat", "--version"], capture_output=True, check=True, text=True)
        print("Hashcat está instalado. Versión:", resultado.stdout.strip())
        return True
    except FileNotFoundError:
        return False
    except subprocess.CalledProcessError:
        return False

# Función para instalar Hashcat en sistemas Debian
def instalar_hashcat():
    respuesta = input("Hashcat no está instalado. ¿Deseas instalarlo? (y/n): ")
    if respuesta.lower() == 'y':
        try:
            subprocess.run(["sudo", "apt", "install", "hashcat"], check=True)
            print("Hashcat se ha instalado correctamente.")
            return True
        except subprocess.CalledProcessError:
            print("Hubo un error al instalar Hashcat.")
            return False
    else:
        print("Hashcat no se ha instalado. Puedes instalarlo manualmente en el futuro.")
        return False

# Punto de entrada del script
if __name__ == "__main__":
    sistema_operativo = platform.system()

    if sistema_operativo == "Windows":
        print("Este script solo es funcional en sistemas Linux basados en Debian.")
    elif sistema_operativo == "Linux":
        if verificar_hashcat_instalado():
            archivo_hashes = 'pass_md5.txt'
            archivo_listado = 'rockyou.txt'
            comparar_hashes(archivo_hashes, archivo_listado)
            crear_passwords()
            print("Proceso completado.")
        else:
            instalar_hashcat()
            print("Por favor, vuelve a ejecutar el script después de instalar Hashcat.")
    else:
        print(f"Este script no ha sido probado en el sistema operativo: {sistema_operativo}.")
