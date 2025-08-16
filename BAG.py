import customtkinter as ctk
import random
import string
import json
import pyperclip
import os
from tkinter import filedialog


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(BASE_DIR, "icono.ICO")

ESCRITORIO = os.path.join(os.path.expanduser("~"), "Desktop")
CARPETA_DATOS = os.path.join(ESCRITORIO, "BAG DATA")
os.makedirs(CARPETA_DATOS, exist_ok=True)

DATA_FILE = os.path.join(CARPETA_DATOS, "data.json")


def mensaje_info(ventana, texto, x, y):
    label = ctk.CTkLabel(ventana, text=texto, font=("arial", 20), text_color="green")
    label.place(x=x, y=y)
    ventana.after(3000, label.destroy)


def centrar_ventana(ventana, ancho, alto):
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    x = (ancho_pantalla // 2) - (ancho // 2)
    y = (alto_pantalla // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")


def crear_pass():
    try:
        entero = int(entrada_longitud.get())
        palabras = f"{string.ascii_letters}{string.ascii_lowercase}{string.ascii_uppercase}{string.digits}{string.punctuation}"
        azar = random.choices(palabras, k=entero)
        convert = ""
        salida_contraseña.delete(0, ctk.END)
        salida_contraseña.insert(0, convert.join(azar))
        mensaje_info(ventana=app, texto="Contraseña generada", x=300, y=190)
    except ValueError:
        salida_contraseña.delete(0, ctk.END)
        salida_contraseña.insert(0, "ingresar un numero")
        salida_contraseña.after(4000, lambda: salida_contraseña.delete(0, ctk.END))


def create_json():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as archivo:
            json.dump({}, archivo)


def copair_portapapeles():
    salida = salida_contraseña.get()
    if salida:
        pyperclip.copy(salida)


def pegar_portapapeles():
    contenido = pyperclip.paste()
    if contenido:
        entrada_pass.delete(0, ctk.END)
        entrada_pass.insert(0, contenido)


def leer_json():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as archivo:
            try:
                return json.load(archivo)
            except json.JSONDecodeError:
                return {}
    return {}


def data_json():
    correo = entrada_correo.get()
    contraseña = entrada_pass.get()
    nuevo_dato = {correo: contraseña}

    datos = leer_json()
    datos.update(nuevo_dato)

    with open(DATA_FILE, "w") as archivo:
        json.dump(datos, archivo, indent=4)

    entrada_correo.delete(0, ctk.END)
    entrada_pass.delete(0, ctk.END)
    mensaje_info(ventana=app, texto="Contraseña Guardada", x=300, y=490)


def menu_hacer(seleccion):
    if seleccion == "cargar informacion":
        win = ctk.CTk()
        win.title("Tus datos")
        win.iconbitmap(ICON_PATH)
        win._state_before_windows_set_titlebar_color = "zoomed"

        scroll = ctk.CTkScrollableFrame(win, width=680, height=400)
        scroll.pack(pady=10, padx=10, fill="both", expand=True)

        data = leer_json()

        header = ctk.CTkFrame(scroll)
        header.pack(fill="x", pady=(0, 5))
        ctk.CTkLabel(header, text="Correo / Usuario", font=("Arial", 15, "bold"), anchor="w", width=250).pack(side="left", padx=5)
        ctk.CTkLabel(header, text="Contraseña", font=("Arial", 15, "bold"), anchor="w", width=150).pack(side="left", padx=5)
        ctk.CTkLabel(header, text="Acciones", font=("Arial", 15, "bold"), anchor="center", width=100).pack(side="left", padx=5)

        if not data:
            ctk.CTkLabel(scroll, text="No hay datos guardados").pack(pady=5)
        else:
            for i, (correo, contraseña) in enumerate(data.items()):
                fila = ctk.CTkFrame(scroll, fg_color="#f0f0f0" if i % 2 == 0 else "#e0e0e0")
                fila.pack(fill="x", pady=2)

                ctk.CTkLabel(fila, text=correo, font=("Arial", 14), anchor="w", width=250).pack(side="left", padx=5, pady=5)
                ctk.CTkLabel(fila, text=contraseña, font=("Arial", 14), anchor="w", width=150).pack(side="left", padx=5, pady=5)

                frame_acciones = ctk.CTkFrame(fila, fg_color="transparent", width=100)
                frame_acciones.pack(side="left", padx=5, pady=5)

                def copiar(texto=contraseña):
                    pyperclip.copy(texto)

                def eliminar(correo_eliminar=correo):
                    datos = leer_json()
                    if correo_eliminar in datos:
                        del datos[correo_eliminar]
                        with open(DATA_FILE, "w") as f:
                            json.dump(datos, f, indent=4)
                        win.destroy()
                        menu_hacer("cargar informacion")

                ctk.CTkButton(frame_acciones, text="Copiar", width=45, command=copiar).pack(side="left", padx=2)
                ctk.CTkButton(frame_acciones, text="Eliminar", width=55, command=eliminar).pack(side="left", padx=2)

        win.mainloop()

    elif seleccion == "exportar informacion":
        def export_data():
            file_name = entrada_exportar.get().strip()
            if not file_name:
                mensaje_info(ventana=win, texto="Por favor ingresa un nombre de archivo", x=50, y=140)
                return

            data = leer_json()
            export_format = menu_jsontotxt.get()
            try:
                if export_format == "Exportar a Json":
                    with open(os.path.join(CARPETA_DATOS, f"{file_name}.json"), "w") as archivo:
                        json.dump(data, archivo, indent=4)
                elif export_format == "Exportar a Txt":
                    with open(os.path.join(CARPETA_DATOS, f"{file_name}.txt"), "w") as archivo:
                        for correo, contraseña in data.items():
                            archivo.write(f"{correo}: {contraseña}\n")
                mensaje_info(ventana=win, texto="Datos Exportados Exitosamente", x=50, y=140)
            except Exception as e:
                mensaje_info(ventana=win, texto=f"Error al exportar: {str(e)}", x=50, y=140)

        win = ctk.CTk()
        win.title("Exportar datos")
        centrar_ventana(win, 400, 200)
        win.resizable(False, False)
        win.iconbitmap(ICON_PATH)

        exportar_label = ctk.CTkLabel(win, text="Ingresa el nombre para el archivo:", font=("arial", 17))
        exportar_label.place(x=10, y=10)

        entrada_exportar = ctk.CTkEntry(win, placeholder_text="Nombre del archivo", width=250, font=("arial", 20))
        entrada_exportar.place(x=10, y=50)

        opciones_jsontotxt = ["Exportar a Json", "Exportar a Txt"]
        menu_jsontotxt = ctk.CTkOptionMenu(master=win, values=opciones_jsontotxt)
        menu_jsontotxt.set("Exportar a Txt")
        menu_jsontotxt.place(x=160, y=100)

        guardar_button = ctk.CTkButton(win, text="Guardar", font=("arial", 20), command=export_data)
        guardar_button.place(x=10, y=100)

        win.mainloop()

    elif seleccion == "importar informacion":
        def importar_json():
            archivo_json = filedialog.askopenfilename(filetypes=[("Archivos JSON", "*.json")])
            win.lift()
            win.focus_force()
            if archivo_json:
                try:
                    with open(archivo_json, "r") as archivo:
                        contenido = archivo.read().strip()
                        if not contenido:
                            mensaje_info(ventana=win, texto="El archivo está vacío", x=118, y=140)
                            return
                        datos_importar = json.loads(contenido)

                    data = leer_json()
                    data.update(datos_importar)
                    with open(DATA_FILE, "w") as archivo:
                        json.dump(data, archivo, indent=4)

                    mensaje_info(ventana=win, texto="Datos Importados", x=118, y=140)
                except json.JSONDecodeError:
                    mensaje_info(ventana=win, texto="El archivo esta dañado", x=115, y=140)

        win = ctk.CTk()
        win.title("Importar datos")
        centrar_ventana(win, 400, 200)
        win.resizable(False, False)
        win.iconbitmap(ICON_PATH)

        importar_label = ctk.CTkLabel(win, text="Carga el archivo json:", font=("Arial", 20))
        importar_label.pack(pady=10)

        boton_importar = ctk.CTkButton(win, text="Importar", font=("Arial", 20), command=importar_json)
        boton_importar.pack(pady=20)

        win.mainloop()

app = ctk.CTk()
app._state_before_windows_set_titlebar_color = "zoomed"
app.state("zoomed")
app.title("Generador de claves")
app.iconbitmap(ICON_PATH)

label_texto = ctk.CTkLabel(app, text="Ingresa la longitud de tu contraseña:", font=("arial", 20))
label_texto.place(x=200, y=50)

entrada_longitud = ctk.CTkEntry(app, placeholder_text="Ingrese un número", text_color="blue", font=("Times", 20), width=250)
entrada_longitud.place(x=200, y=90)

salida_contraseña = ctk.CTkEntry(app, placeholder_text="Esperando...", width=250, text_color="red", font=("Times", 20))
salida_contraseña.place(x=200, y=140)

accion = ctk.CTkButton(app, text="Generar", font=("Times", 20), command=crear_pass)
accion.place(x=480, y=90)

copiar_portapapeles_but = ctk.CTkButton(app, text="Copiar", font=("Times", 20), command=copair_portapapeles)
copiar_portapapeles_but.place(x=480, y=140)

guardar_info = ctk.CTkLabel(app, text="Guarda tu correo o usuarios aquí:", font=("arial", 20))
guardar_info.place(x=200, y=250)

entrada_correo = ctk.CTkEntry(app, placeholder_text="Ingresalo aquí..", width=400, font=("Times", 20))
entrada_correo.place(x=200, y=290)

poner_pass = ctk.CTkLabel(app, text="Introduce la contraseña generada:", font=("arial", 20))
poner_pass.place(x=200, y=330)

entrada_pass = ctk.CTkEntry(app, placeholder_text="Usa Ctrl+V para pegar", width=400, font=("Times", 20))
entrada_pass.place(x=200, y=370)

boton_pegar = ctk.CTkButton(app, text="Pegar", font=("Times", 20), command=pegar_portapapeles)
boton_pegar.place(x=470, y=430)

boton_guardar = ctk.CTkButton(app, text="Guardar", font=("Times", 20), command=data_json)
boton_guardar.place(x=200, y=430)

menu_label = ctk.CTkLabel(app, text="Menú de opciones", font=("arial", 20))
menu_label.place(x=900, y=50)

opciones = ["cargar informacion", "exportar informacion", "importar informacion"]
menu = ctk.CTkOptionMenu(master=app, values=opciones, command=menu_hacer)
menu.place(x=900, y=90)

create_json()
app.mainloop()
