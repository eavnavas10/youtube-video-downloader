#LINK DEL VIDEO: https://youtu.be/kH95f_yxQ1I?si=42IETlhfREtBbs4H
import re
import tkinter
import customtkinter
from yt_dlp import YoutubeDL

# Función para manejar el progreso
def on_progress(d):
    if d['status'] == 'downloading':
        try:
            # Obtener porcentaje de progreso desde '_percent_str'
            percentage_str = d.get('_percent_str', '0.00%').strip()
            
            # Eliminar caracteres ANSI y extraer el número
            percentage_str = re.sub(r'\x1b\[[0-9;]*m', '', percentage_str)  # Remover colores
            percentage_of_completion = float(percentage_str.replace('%', '').strip())  # Convertir a float

            # Actualizar barra de progreso
            progressBar.set(percentage_of_completion / 100)
            pPercentage.configure(text=f"{percentage_of_completion:.2f}%")
            app.update_idletasks()  # Forzar actualización de la interfaz
        except (ValueError, KeyError) as e:
            print(f"Error al procesar el progreso: {e}")

# Función para manejar la descarga
def startDownload():
    url = url_var.get()  # Obtener el valor de la entrada como texto
    if not url.strip():  # Validar que no esté vacío
        finishLabel.configure(text="Por favor, ingresa un enlace válido.")
        return

    try:
        # Actualizar opciones con el hook de progreso
        ydl_opts['progress_hooks'] = [on_progress]

        with YoutubeDL(ydl_opts) as ydl:
            # Obtener información del video
            info = ydl.extract_info(url, download=False)
            video_title = info.get("title", "Título no encontrado")
            title.configure(text=f"Título: {video_title}")

            # Descargar el video
            ydl.download([url])
            finishLabel.configure(text="Video descargado!", text_color="green")
    except Exception as e:
        finishLabel.configure(text=f"Error al descargar el video: {e}", text_color="red")

# Configuración para obtener la calidad más alta del video y el nombre del archivo
ydl_opts = {
    'format': 'bestvideo+bestaudio/best',  # Selecciona la mejor combinación de video y audio
    'outtmpl': '%(title)s.%(ext)s',       # Formato de salida del archivo
    'merge_output_format': 'mp4',         # Combina video y audio en MP4
}

# Configuración del sistema
customtkinter.set_appearance_mode("Light")
customtkinter.set_default_color_theme("blue")

# Marco de nuestra app
app = customtkinter.CTk()
app.geometry("720x480")
app.title("Youtube Downloader")

# Añadiendo elementos de la interfaz
title = customtkinter.CTkLabel(app, text="Ingrese un link de Youtube")
title.pack(padx=10, pady=10)

url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack()

download = customtkinter.CTkButton(app, text="Download", command=startDownload)
download.pack(padx=10, pady=10)

progressBar = customtkinter.CTkProgressBar(app, width=300)
progressBar.set(0)  # Inicializar en 0%
progressBar.pack(pady=10)

pPercentage = customtkinter.CTkLabel(app, text="0%")
pPercentage.pack()

finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack()

# Run app
app.mainloop()
