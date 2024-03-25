import random
import string
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import os


def generate_fullname():
    nombres = ["Juan", "Carlos", "Luis", "Pedro", "Miguel", "Pablo", "Javier", "Francisco", "Jose", "Antonio"]
    apellidos = ["Gomez", "Tilin", "Lopez", "Martinez", "Gonzalez", "Perez", "Sanchez", "Diaz", "Romero"]
    return f"{random.choice(nombres)}{random.choice(apellidos)}"

# Función para generar caracteres aleatorios
def generate_caracteres():
    return ''.join(random.choices(string.ascii_letters, k=3))

# Función para generar contraseñas aleatorias
def generate_password():
    length = 12
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join((random.choice(letters_and_digits) for i in range(length)))

def usuarioGenerado():    
    return generate_fullname() + generate_caracteres()

def contraseñaGenerada(): 
    return generate_password()

class CreadorDeCuentas:
    def __init__(self):
        driver_options = webdriver.ChromeOptions()
        driver_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=driver_options)

    def crear_usuario(self, user, password):
        url = "https://www.roblox.com"
        self.driver.get(url)
        time.sleep(3)

        try:
            usuario = self.driver.find_element(By.ID, "signup-username")
            contraseña = self.driver.find_element(By.ID, "signup-password")
            dia = self.driver.find_element(By.ID, "DayDropdown")
            mes = self.driver.find_element(By.ID, "MonthDropdown")
            año = self.driver.find_element(By.ID, "YearDropdown")
            generoHombre = self.driver.find_element(By.ID, "MaleButton")
            botonRegistrarse = self.driver.find_element(By.ID, "signup-button")
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
        generoHombre.click()
        time.sleep(1)
        # verificar que el el boton de registrarse este habilitado
        if botonRegistrarse.is_enabled():
            botonRegistrarse.click()
        else:
            time.sleep(10)
            botonRegistrarse.click()

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
            with open("usuarios.json", 'r') as file:
                usuarios_existentes = json.load(file)
        except FileNotFoundError:
            usuarios_existentes = []
            
        # Agregar el nuevo usuario al archivo
        usuarios_existentes.append(usuario_data)
        
        # Escribir los datos actualizados en el archivo
        try:
            with open("usuarios.json", 'w') as file:
                json.dump(usuarios_existentes, file, indent=4)
            print(f"Información del usuario {user} guardada en usuarios.json")
        except Exception as e:
            print(f"Error al guardar el archivo JSON: {e}")
        
        
        return True
    
    def login(self, user, password, cookies):
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
    
    def seguirUsuario(self, idUsuario):
        # Proceso de seguir usuario
        urlUser = f"https://www.roblox.com/users/{idUsuario}/profile"
        self.driver.get(urlUser)
        time.sleep(3)

        # Buscar y seguir al usuario
        try:
            # Buscar elementos
            desplegarOpciones = self.driver.find_element(By.XPATH, value="/html/body/div[3]/main/div[2]/div[2]/div/div[1]/div/div/div/div[3]/div/button")
            botonSeguir = self.driver.find_element(By.XPATH, value='//*[@id="profile-header-more rbx-menu-item"]/div/ul/li[1]/a')
        except NoSuchElementException as e:
            print(f"Error al encontrar elementos para seguir: {e}")
            return False

        # Seguir al usuario
        time.sleep(1)
        desplegarOpciones.click()
        time.sleep(0.5)
        # Verificar si ya se sigue al usuario
        if botonSeguir.text == "Dejar de seguir":
            return False
        else:
            botonSeguir.click()
        time.sleep(0.5)
        return True
    
    def inicioSecionRapido(self, codigo):
        # Cargar la página de inicio de Roblox
        url = 'https://www.roblox.com/crossdevicelogin/ConfirmCode'
        self.driver.get(url)
        time.sleep(2)

        # Campo para introducir el código
        inputCodigo = self.driver.find_element(By.XPATH, value='//*[@id="confirm-code-container"]/div/div/div/form/div[1]/input')
        botonEnviar = self.driver.find_element(By.XPATH, value="/html/body/div[3]/main/div[2]/div/div/div/div/form/div[2]/button") 
               
        
        # Introducir el código
        inputCodigo.send_keys(codigo)
        time.sleep(1)
        botonEnviar.click()
        time.sleep(1)
        botonConfirmar = self.driver.find_element(By.XPATH, value="/html/body/div[3]/main/div[2]/div/div/div/div/div[3]/button[2]")
        if botonConfirmar.is_enabled():
            botonConfirmar.click()
        else:
            time.sleep(1.5)
            botonConfirmar.click()
        
        return True

def menu():    
    print("1. Crear usuario")
    print("2. Seguir usuario")
    print("3. Iniciar sesión rapidamente")
    print("4. Inicio de sesión rápido")
    print("5. Verificar si pasaron 2 horas desde el último")
    print("0. Salir")
    
    opcion = input("Ingrese una opción: ")
    
    try:
        if opcion not in ["1", "2", "3", "4", "5", "0"]:
            raise ValueError("Opción no válida")
        
        if opcion == "1":
            cantidad = int(input("Cuantos usuarios desea crear?: "))
            print("Creando usuarios...")
            crear = CreadorDeCuentas()
            
            for _ in range(cantidad):  # Crear usuarios
                user = usuarioGenerado()
                passw = contraseñaGenerada()
                if crear.crear_usuario(user, passw):
                    print(f"Usuario {user} creado con éxito\n")
                    crear.driver.delete_all_cookies()
                    
        if opcion == "2":            
            idUsuario = input("Ingrese el id del usuario a seguir: ")
            print("Siguiendo usuario...")
            crear = CreadorDeCuentas()
            
            try:
                with open("usuarios.json", 'r') as file:
                    usuarios_existentes = json.load(file)
            except FileNotFoundError:
                usuarios_existentes = []
            
            
            for usuario in usuarios_existentes:
                if crear.login(usuario["username"], usuario["password"], usuario["cookies"]):
                    if crear.seguirUsuario(idUsuario):
                        print(f"Usuario {usuario['username']} ha seguido al usuario {idUsuario}")
                        crear.driver.delete_all_cookies()
                    if not crear.seguirUsuario(idUsuario):
                        print(f"Usuario {usuario['username']} ya sigue al usuario {idUsuario}")
                        crear.driver.delete_all_cookies()
        
        if opcion == "3":            
            nombreCuenta = input("Ingrese el nombre de la cuenta: ")
            if nombreCuenta == "":
                print("No se ingresó un nombre de cuenta")
                return 
            print("Iniciando sesión...")
            crear = CreadorDeCuentas()
        
            try:
                with open("usuarios.json", 'r') as file:
                    usuarios_existentes = json.load(file)
            except FileNotFoundError:
                usuarios_existentes = []
        
            usuarioSeleccionado = next((usuario for usuario in usuarios_existentes if usuario["username"] == nombreCuenta), None)
        
            if crear.login(usuarioSeleccionado["username"], usuarioSeleccionado["password"], usuarioSeleccionado["cookies"]):
                print(f"Usuario {usuarioSeleccionado['username']} ha iniciado sesión")
            else:
                print(f"Error al iniciar sesión con el usuario {usuarioSeleccionado['username']}")     
        

        if opcion == "4":            
            codigo = input("Ingrese el código de inicio de sesión: ")
            
            try:
                with open("usuarios.json", 'r') as file:
                    usuarios_existentes = json.load(file)
            except FileNotFoundError:
                usuarios_existentes = []
                
            # Imprimir los usuarios que no han sido usados
            print("\nUsuarios no usados:\n")
            usuariosSinUsar = 0
            for usuario in usuarios_existentes:
                if usuario["seUso"] == "No":
                    usuariosSinUsar += 1
                
            print(f"Usuarios no usados: {usuariosSinUsar}")
            usuarioSeleccionado = None
            for usuario in usuarios_existentes:                
                if usuario["seUso"] == "No":
                    print(f"Usuario: {usuario['username']}") 
                    usuarioSeleccionado = usuario
                    break
            
            nombreCuenta = usuarioSeleccionado['username']
            
            if usuarioSeleccionado is None:
                print("No hay usuarios disponibles para iniciar sesión.")
                return
            
            if nombreCuenta == "":
                print("No se ingresó un nombre de cuenta")
                return 
            print("Iniciando sesión...")
            crear = CreadorDeCuentas()

            usuarioSeleccionado = next((usuario for usuario in usuarios_existentes if usuario["username"] == nombreCuenta), None)

            if crear.login(usuarioSeleccionado["username"], usuarioSeleccionado["password"], usuarioSeleccionado["cookies"]):
                if crear.inicioSecionRapido(codigo):
                    print(f"Usuario {usuarioSeleccionado['username']} ha iniciado sesión")
                    if usuarioSeleccionado["nivel"] == "50-":
                        preguntaNivel = input("Es nivel 50+? (si/no): ")
                        try:
                            if preguntaNivel not in ["si", "no"]:
                                raise ValueError("Opción no válida")
                            if preguntaNivel == "si":
                                usuarioSeleccionado["nivel"] = "50+"  
                                usuarioSeleccionado["seUso"] = "Si"
                                usuarioSeleccionado["ultimoUso"] = f"{time.strftime('%d/%m/%Y')} {time.strftime('%H:%M:%S')}"
                                print(f"Usuario {usuarioSeleccionado['username']} es nivel 50+")
                            if preguntaNivel == "no":
                                usuarioSeleccionado["nivel"] = "50-"
                                usuarioSeleccionado["seUso"] = "No"
                                print(f"Usuario {usuarioSeleccionado['username']} es nivel 50-")
                        except ValueError:
                            print("Opción no válida")
                    else:
                        tiroFruta = input("Tiró fruta? (si/no): ")
                        try:
                            if tiroFruta not in ["si", "no"]:
                                raise ValueError("Opción no válida")
                            if tiroFruta == "si":
                                usuarioSeleccionado["seUso"] = "Si"
                                usuarioSeleccionado["ultimoUso"] = f"{time.strftime('%d/%m/%Y')} {time.strftime('%H:%M:%S')}"
                                print(f"Usuario {usuarioSeleccionado['username']} ha tirado fruta")
                            if tiroFruta == "no":
                                usuarioSeleccionado["seUso"] = "No"
                                print(f"Usuario {usuarioSeleccionado['username']} no ha tirado fruta")
                        except ValueError:
                            print("Opción no válida")

                else:
                    print(f"Error al iniciar sesión con el usuario {usuarioSeleccionado['username']}")
            else:
                print(f"Error al iniciar sesión con el usuario {usuarioSeleccionado['username']}")
            
            # Guardar los cambios en el archivo JSON
            with open("usuarios.json", 'w') as file:
                json.dump(usuarios_existentes, file, indent=4, sort_keys=False)         
    
        if opcion == "5":
            print("Verificando si han pasado 2 horas desde el último uso...\n")
            try:
                with open("usuarios.json", 'r') as file:
                    usuarios_existentes = json.load(file)
            except FileNotFoundError:
                usuarios_existentes = []
                
            for usuario in usuarios_existentes:
                ultimoUso = usuario["ultimoUso"]
                tiempoUltimoUso = time.mktime(time.strptime(ultimoUso, "%d/%m/%Y %H:%M:%S"))
                tiempoActual = time.time()
                if tiempoActual - tiempoUltimoUso >= 7200:
                    usuario["seUso"] = "No"
                    print(f"Usuario {usuario['username']} ha pasado 2 horas desde el último uso")
            
            # Guardar los cambios en el archivo JSON
            with open("usuarios.json", 'w') as file:
                json.dump(usuarios_existentes, file, indent=4, sort_keys=False)
                 
            
        if opcion == "0":
            print("Saliendo...")
            time.sleep(1)
            exit()
    except ValueError:
        print("Opción no válida")
        os.system("clear")        
        

menu()