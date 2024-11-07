import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF
from datetime import datetime
import sys
import os
import ctypes
import subprocess
import importlib.resources

required_libraries = ['fpdf']


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()


def install_libraries():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + required_libraries)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error al intentar instalar las bibliotecas: {e}")
        sys.exit()


def check_libraries():
    try:
        import fpdf
    except ImportError:
        response = messagebox.askyesno(
            "Biblioteca faltante",
            "La biblioteca 'fpdf' no está instalada. ¿Deseas instalarla?"
        )
        if response:
            install_libraries()


def crear_pdf():
    texto = texto_entrada.get("1.0", tk.END)

    if not texto.strip():
        messagebox.showerror("Error", "Por favor, introduce algún texto")
        return

    try:
        carpeta_destino = "C:\\PDFs_Generados"
        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino)

        nombre_archivo = os.path.join(carpeta_destino,
                                      f"documento_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        texto = texto.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, txt=texto)

        pdf.output(nombre_archivo)
        messagebox.showinfo("Éxito", f"PDF creado como: {nombre_archivo}")

        os.startfile(carpeta_destino)

    except Exception as e:
        messagebox.showerror("Error", f"Error al crear el PDF: {str(e)}")


def main():
    run_as_admin()
    check_libraries()

    ventana = tk.Tk()
    ventana.title("Convertir Texto a PDF (Modo Administrador)")
    ventana.geometry("500x400")

    global texto_entrada
    texto_entrada = tk.Text(ventana, height=15, width=50)
    texto_entrada.pack(pady=20)

    boton_convertir = tk.Button(ventana, text="Convertir a PDF", command=crear_pdf)
    boton_convertir.pack(pady=10)

    admin_label = tk.Label(ventana, text="Ejecutando como Administrador", fg="red")
    admin_label.pack(pady=5)

    instrucciones = tk.Label(ventana,
                             text="Escribe o pega tu texto aquí y presiona 'Convertir a PDF'\nLos archivos se "
                                  "guardarán en C:\\PDFs_Generados")
    instrucciones.pack(pady=10)

    ventana.mainloop()


if __name__ == "__main__":
    main()
