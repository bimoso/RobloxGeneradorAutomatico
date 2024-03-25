"""
Este modulo main.py es una forma de automatizar la creación de cuentas de Roblox, 
seguir a un usuario y realizar un inicio de sesión rápido. Cuenta con una gestion
de un juego de el llamado "Blox Fruits" donde se verifica si han pasado 2 horas desde
el último uso de la cuenta.
"""

import random
import string
import json
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Función para generar nombres aleatorios
def generate_fullname():
    """
    Esta función genera un nombre aleatorio a partir de una lista de nombres y apellidos.
    """
    nombres = ["Juan", "Carlos", "Luis", "Pedro", "Miguel", "Pablo", "Javier", "Francisco", "Jose", "Antonio"]
    apellidos = ["Gomez", "Tilin", "Lopez", "Martinez", "Gonzalez", "Perez", "Sanchez", "Diaz", "Romero"]
    return f"{random.choice(nombres)}{random.choice(apellidos)}"

# Función para generar caracteres aleatorios
def generate_caracteres():
    """
    Esta función genera 3 caracteres aleatorios a partir de una lista de letras.
    """
    return ''.join(random.choices(string.ascii_letters, k=3))

# Función para generar contraseñas aleatorias
def generate_password():
    """
    Esta función genera una contraseña aleatoria de 12 caracteres aleatorios.
    """
    length = 12
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join((random.choice(letters_and_digits) for i in range(length)))

def usuario_generado():
    """
    Genera un nombre de usuario aleatorio a partir de un nombre completo y caracteres aleatorios.
    """
    return generate_fullname() + generate_caracteres()

def contraseña_generada():
    """
    Solicita una contraseña aleatoria a partir de la función generate_password.
    """
    return generate_password()

class CreadorDeCuentas:
    """
    Es la encargada de todo el flujo de formularios y automatizacion.
    """
    def __init__(self):
        driver_options = webdriver.ChromeOptions()
        driver_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=driver_options)

    def crear_usuario(self, user, password):
        """
        Este método crea un usuario en Roblox a partir de un nombre de usuario y una contraseña.
        """
        url = "https://www.roblox.com"
        self.driver.get(url)
        time.sleep(3)

        try:
            usuario = self.driver.find_element(By.ID, "signup-username")
            contraseña = self.driver.find_element(By.ID, "signup-password")
            dia = self.driver.find_element(By.ID, "DayDropdown")
            mes = self.driver.find_element(By.ID, "MonthDropdown")
            año = self.driver.find_element(By.ID, "YearDropdown")
            genero_hombre = self.driver.find_element(By.ID, "MaleButton")
            boton_registrarse = self.driver.find_element(By.ID, "signup-button")
        except NoSuchElementException as e:
            print(f"Error al encontrar elementos del formulario: {e}")
            return False

        time.sleep(1)

        # Llenar el formulario
        usuario.send_keys(user)
        contraseña.send_keys(password)
        dia.send_keys(str(random.randint(10, 28)))
        mes.send_keys("Agosto")
        año.send_keys(str(random.randint(2000, 2005)))
        genero_hombre.click()
        time.sleep(1)
        # verificar que el el boton de registrarse este habilitado
        if boton_registrarse.is_enabled():
            boton_registrarse.click()
        else:
            time.sleep(10)
            boton_registrarse.click()

        # Esperar a que la página cambie
        WebDriverWait(self.driver, 120).until(
            EC.url_to_be("https://www.roblox.com/home?nu=true")
        )
        time.sleep(1)
        cookies = self.driver.get_cookies()
        # Crear objeto de usuario con las credenciales y las cookies
        usuario_data = {
        "username": user,
        "password": password,
        "seUso": "No",
        "nivel": "50-",
        "ultimoUso": f"{time.strftime('%d/%m/%Y')} {time.strftime('%H:%M:%S')}",
        "cookies": [{"name": cookie["name"], "value": cookie["value"], "domain": cookie["domain"]} for cookie in cookies]
    }
       # Leer los datos existentes del archivo
        try:
            with open("usuarios.json", 'r', encoding='utf-8') as file:
                usuarios_existentes = json.load(file)
        except FileNotFoundError:
            usuarios_existentes = []

        # Agregar el nuevo usuario al archivo
        usuarios_existentes.append(usuario_data)
        # Escribir los datos actualizados en el archivo
        try:
            with open("usuarios.json", 'w', encoding='utf-8') as file:
                json.dump(usuarios_existentes, file, indent=4)
            print(f"Información del usuario {user} guardada en usuarios.json")
        except FileNotFoundError as e:
            print(f"Error al guardar el archivo JSON: {e}")
        except IOError as e:
            print(f"Error de E/S al guardar el archivo JSON: {e}")
        return True
    def login(self, cookies):
        """"
        Este método inicia sesión en Roblox usando de las cookies de un usuario.
        """
        # Cargar la página de inicio de Roblox
        self.driver.get('https://www.roblox.com/login')

        # Cargar las cookies
        for cookie in cookies:
            if 'expiry' in cookie:
                del cookie['expiry']
            self.driver.add_cookie(cookie)

        # Recargar la página para aplicar las cookies
        self.driver.refresh()

        # Comprobar si el inicio de sesión fue exitoso
        # (Reemplaza esto con la lógica adecuada para tu caso)
        WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="right-navigation-header"]/div[2]/ul/div[2]/a'))
        )
        time.sleep(1)

        return True
    def seguir_usuario(self, id_usuario):
        """
        Este método sigue a un usuario en Roblox a partir de su ID.
        """
        # Proceso de seguir usuario
        url_user = f"https://www.roblox.com/users/{id_usuario}/profile"
        self.driver.get(url_user)
        time.sleep(3)

        # Buscar y seguir al usuario
        try:
            # Buscar elementos
            desplegar_opciones = self.driver.find_element(By.XPATH, value="/html/body/div[3]/main/div[2]/div[2]/div/div[1]/div/div/div/div[3]/div/button")
            boton_seguir = self.driver.find_element(By.XPATH, value='//*[@id="profile-header-more rbx-menu-item"]/div/ul/li[1]/a')
        except NoSuchElementException as e:
            print(f"Error al encontrar elementos para seguir: {e}")
            return False

        # Seguir al usuario
        time.sleep(1)
        desplegar_opciones.click()
        time.sleep(0.5)
        # Verificar si ya se sigue al usuario
        if boton_seguir.text == "Dejar de seguir":
            return False
        else:
            boton_seguir.click()
        time.sleep(0.5)
        return True
    def inicio_de_secion_rapido(self, codigo):
        """
        Este método inicia sesión en Roblox a partir de un código de inicio de sesión.
        Ademas verifica si el usuario es nivel 50+ o 50- y si tiro fruta o no.
        """
        # Cargar la página de inicio de Roblox
        url = 'https://www.roblox.com/crossdevicelogin/ConfirmCode'
        self.driver.get(url)
        time.sleep(2)

        # Campo para introducir el código
        input_codigo = self.driver.find_element(By.XPATH, value='//*[@id="confirm-code-container"]/div/div/div/form/div[1]/input')
        boton_enviar = self.driver.find_element(By.XPATH, value="/html/body/div[3]/main/div[2]/div/div/div/div/form/div[2]/button")
        # Introducir el código
        input_codigo.send_keys(codigo)
        time.sleep(1)
        boton_enviar.click()
        time.sleep(1)
        boton_confirmar = self.driver.find_element(By.XPATH, value="/html/body/div[3]/main/div[2]/div/div/div/div/div[3]/button[2]")
        if boton_confirmar.is_enabled():
            boton_confirmar.click()
        else:
            time.sleep(1.5)
            boton_confirmar.click()
        return True

def menu():
    """
    Este método es el menú principal de la aplicación.
    """
    print("1. Crear usuario")
    print("2. Seguir usuario")
    print("3. Iniciar sesión rapidamente")
    print("4. Inicio de sesión rápido")
    print("5. Verificar si pasaron 2 horas desde el último")
    print("0. Salir")
    opcion = input("Ingrese una opción: ")
    try:
        # Verificar si la opción es válida
        if opcion not in ["1", "2", "3", "4", "5", "0"]:
            raise ValueError("Opción no válida")
        # Crear usuario
        if opcion == "1":
            cantidad = int(input("Cuantos usuarios desea crear?: "))
            print("Creando usuarios...")
            crear = CreadorDeCuentas()
            for _ in range(cantidad):  # Crear usuarios
                user = usuario_generado()
                passw = contraseña_generada()
                if crear.crear_usuario(user, passw):
                    print(f"Usuario {user} creado con éxito\n")
                    crear.driver.delete_all_cookies()
        # Seguir a un usuario
        if opcion == "2":
            id_user = input("Ingrese el id del usuario a seguir: ")
            print("Siguiendo usuario...")
            crear = CreadorDeCuentas()
            try:
                with open("usuarios.json", 'r', encoding='utf-8') as file:
                    usuarios_existentes = json.load(file)
            except FileNotFoundError:
                usuarios_existentes = []

            for usuario in usuarios_existentes:
                if crear.login(usuario["cookies"]):
                    if crear.seguir_usuario(id_user):
                        print(f"Usuario {usuario['username']} ha seguido al usuario {id_user}")
                        crear.driver.delete_all_cookies()
                    if not crear.seguir_usuario(id_user):
                        print(f"Usuario {usuario['username']} ya sigue al usuario {id_user}")
                        crear.driver.delete_all_cookies()
        # Inicio de sesión rápido con un usuario existente
        if opcion == "3":
            print("Usuarios existentes: ")
            try:
                with open("usuarios.json", 'r', encoding='utf-8') as file:
                    usuarios_existentes = json.load(file)
            except FileNotFoundError:
                usuarios_existentes = []
            num_lista = 1
            for usuario in usuarios_existentes:
                print(f"{num_lista}. Usuario: {usuario['username']} Se uso: {usuario['seUso']} Nivel: {usuario['nivel']}")
            indice_cuenta = input("Seleccione una cuenta: ")
            if indice_cuenta == "" and indice_cuenta not in range(1, len(usuarios_existentes) + 1 and not indice_cuenta.isdigit()):
                print("No se ingresó un número válido")
                return
            print("Iniciando sesión...")
            crear = CreadorDeCuentas()
            usuario_seleccionado = usuarios_existentes[indice_cuenta + 1]
            if crear.login(usuario_seleccionado["cookies"]):
                print(f"Usuario {usuario_seleccionado['username']} ha iniciado sesión")
            else:
                print(f"Error al iniciar sesión con el usuario {usuario_seleccionado['username']}")
        # Inicio de sesión rápido y verificar si es nivel 50+ o 50- y si tiro fruta o no
        if opcion == "4":
            codigo = input("Ingrese el código de inicio de sesión: ")
            try:
                with open("usuarios.json", 'r', encoding='utf-8') as file:
                    usuarios_existentes = json.load(file)
            except FileNotFoundError:
                usuarios_existentes = []
            # Imprimir los usuarios que no han sido usados
            print("\nUsuarios no usados:\n")
            usuarios_sin_usar = 0
            for usuario in usuarios_existentes:
                if usuario["seUso"] == "No":
                    usuarios_sin_usar += 1
            print(f"Usuarios no usados: {usuarios_sin_usar}")
            usuario_seleccionado = None
            for usuario in usuarios_existentes:
                if usuario["seUso"] == "No":
                    print(f"Usuario: {usuario['username']}")
                    usuario_seleccionado = usuario
                    break
            nombre_cuenta = usuario_seleccionado['username']
            if usuario_seleccionado is None:
                print("No hay usuarios disponibles para iniciar sesión.")
                return
            if nombre_cuenta == "":
                print("No se ingresó un nombre de cuenta")
                return
            print("Iniciando sesión...")
            crear = CreadorDeCuentas()

            usuario_seleccionado = next((usuario for usuario in usuarios_existentes if usuario["username"] == nombre_cuenta), None)
            # Comezar el proceso de inicio de sesión
            if crear.login(usuario_seleccionado["cookies"]):
                if crear.inicio_de_secion_rapido(codigo):
                    print(f"Usuario {usuario_seleccionado['username']} ha iniciado sesión")
                    if usuario_seleccionado["nivel"] == "50-":
                        preguntar_nivel = input("Es nivel 50+? (si/no): ")
                        try:
                            if preguntar_nivel not in ["si", "no"]:
                                raise ValueError("Opción no válida")
                            if preguntar_nivel == "si":
                                usuario_seleccionado["nivel"] = "50+"
                                usuario_seleccionado["seUso"] = "Si"
                                usuario_seleccionado["ultimoUso"] = f"{time.strftime('%d/%m/%Y')} {time.strftime('%H:%M:%S')}"
                                print(f"Usuario {usuario_seleccionado['username']} es nivel 50+")
                            if preguntar_nivel == "no":
                                usuario_seleccionado["nivel"] = "50-"
                                usuario_seleccionado["seUso"] = "No"
                                print(f"Usuario {usuario_seleccionado['username']} es nivel 50-")
                        except ValueError:
                            print("Opción no válida")
                    else:
                        tiro_fruta = input("Tiró fruta? (si/no): ")
                        try:
                            if tiro_fruta not in ["si", "no"]:
                                raise ValueError("Opción no válida")
                            if tiro_fruta == "si":
                                usuario_seleccionado["seUso"] = "Si"
                                usuario_seleccionado["ultimoUso"] = f"{time.strftime('%d/%m/%Y')} {time.strftime('%H:%M:%S')}"
                                print(f"Usuario {usuario_seleccionado['username']} ha tirado fruta")
                            if tiro_fruta == "no":
                                usuario_seleccionado["seUso"] = "No"
                                print(f"Usuario {usuario_seleccionado['username']} no ha tirado fruta")
                        except ValueError:
                            print("Opción no válida")

                else:
                    print(f"Error al iniciar sesión con el usuario {usuario_seleccionado['username']}")
            else:
                print(f"Error al iniciar sesión con el usuario {usuario_seleccionado['username']}")
            # Guardar los cambios en el archivo JSON
            with open("usuarios.json", 'w', encoding='utf-8') as file:
                json.dump(usuarios_existentes, file, indent=4, sort_keys=False)
        if opcion == "5":
            print("Verificando si han pasado 2 horas desde el último uso...\n")
            try:
                with open("usuarios.json", 'r', encoding='utf-8') as file:
                    usuarios_existentes = json.load(file)
            except FileNotFoundError:
                usuarios_existentes = []
            for usuario in usuarios_existentes:
                ultimo_uso = usuario["ultimoUso"]
                tiempo_ultimo_uso_actual = time.mktime(time.strptime(ultimo_uso, "%d/%m/%Y %H:%M:%S"))
                tiempo_actual = time.time()
                if tiempo_actual - tiempo_ultimo_uso_actual >= 7200:
                    usuario["seUso"] = "No"
                    print(f"Usuario {usuario['username']} ha pasado 2 horas desde el último uso")
            # Guardar los cambios en el archivo JSON
            with open("usuarios.json", 'w', encoding='utf-8') as file:
                json.dump(usuarios_existentes, file, indent=4, sort_keys=False)
        if opcion == "0":
            print("Saliendo...")
            time.sleep(1)
            exit()
    except ValueError:
        print("Opción no válida")
        os.system("clear")
# Iniciar el programa
menu()
