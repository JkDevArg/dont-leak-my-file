import tkinter as tk
from ttkbootstrap import Style, Frame, Notebook, Button, Entry, Label
from tkinter import filedialog, messagebox
from watermark import WatermarkEngine
from crypto import AESCipher
from database import DatabaseManager
from datetime import datetime
import uuid

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.style = Style(theme='flatly')
        self.db = DatabaseManager()
        self.cipher = AESCipher(key=b'TuClaveSecretaDe32BytesAqui12345')
        self.root.resizable(False, False)

        self._setup_ui()

        # Información :v
        self.text_copyright = tk.Text(root, height=4, width=100)
        self.text_copyright.pack()
        self.text_copyright.insert(tk.END, "Created by Joaquin Centurión\nGithub: https://github.com/JkDevArg \nLinkedin: https://www.linkedin.com/in/joaquincenturion/ \nDon't leak my file v1.0")
        self.text_copyright.config(state=tk.DISABLED)
        self.text_copyright.tag_configure("copyright", foreground="grey")
        self.text_copyright.tag_add("copyright", "1.0", "end")

    def _setup_ui(self):
        self.root.title("Don't leak my file")
        self.root.geometry("600x400")

        notebook = Notebook(self.root)

        # Pestaña de Marcado
        tab_mark = Frame(notebook)
        self._build_mark_tab(tab_mark)

        # Pestaña de Verificación
        tab_verify = Frame(notebook)
        self._build_verify_tab(tab_verify)

        notebook.add(tab_mark, text='Proteger Documento')
        notebook.add(tab_verify, text='Verificar Documento')
        notebook.pack(expand=True, fill='both')


    def _build_mark_tab(self, parent):
        Label(parent, text="Nombre completo:").pack(pady=5)
        self.name_entry = Entry(parent, width=50)
        self.name_entry.pack(pady=5)

        Button(parent, text="Seleccionar Archivo",
              command=self._select_file).pack(pady=10)

        self.file_label = Label(parent, text="Archivo seleccionado: Ninguno")
        self.file_label.pack(pady=5)

        Button(parent, text="Procesar",
              command=self._process_file,
              bootstyle="success").pack(pady=20)

    def _build_verify_tab(self, parent):
        Button(parent, text="Verificar Archivo",
              command=self._select_verify_file).pack(pady=20)

        self.verify_info = tk.Text(parent, height=10, width=60)
        self.verify_info.pack(pady=10)

    def _select_file(self):
        self.file_path = filedialog.askopenfilename()
        self.file_label.config(text=f"Archivo: {self.file_path}")

    # Función para procesar el archivo
    def _process_file(self):
        name = self.name_entry.get()
        if not name or not hasattr(self, 'file_path'):
            messagebox.showerror("Error", "Complete todos los campos")
            return

        doc_uuid = str(uuid.uuid4())
        data = f"UUID={doc_uuid}|NAME={name}|DATE={datetime.now().isoformat()}"
        encrypted_data = self.cipher.encrypt(data)

        try:
            output_path = filedialog.asksaveasfilename()
            WatermarkEngine.add_watermark(self.file_path, encrypted_data, output_path)
            self.db.insert_document(doc_uuid, name)
            messagebox.showinfo("Éxito", f"Documento protegido: {output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Función para verificar el archivo
    def _select_verify_file(self):
        file_path = filedialog.askopenfilename()
        try:
            encrypted_data = WatermarkEngine.extract_watermark(file_path)
            if not encrypted_data:
                info = "Este documento no esta protegido."
                self.verify_info.delete(1.0, tk.END)
                self.verify_info.insert(tk.END, info)
                return

            decrypted_data = self.cipher.decrypt(encrypted_data)

            # Validar formato de los datos descifrados
            if "UUID=" not in decrypted_data or "|NAME=" not in decrypted_data:
                messagebox.showerror("Error", "Marca de agua inválida")
                return

            # Extraer datos de forma segura
            uuid = decrypted_data.split("UUID=")[1].split("|")[0]  # <-- Corrección aquí
            name = decrypted_data.split("NAME=")[1].split("|")[0]
            date = decrypted_data.split("DATE=")[1]

            info = "=== Datos del archivo ===\n"
            info += f"UUID: {uuid}\nNombre: {name}\nFecha: {date}\n\n"

            if self.db.check_leak(uuid):
                info += "⚠️ ALERTA: Este documento pudo haberse filtrado, existe en la base de datos"
            else:
                info += "✅ Este documento no aparece en registros de filtraciones"

            self.verify_info.delete(1.0, tk.END)
            self.verify_info.insert(tk.END, info)

        except Exception as e:
            messagebox.showerror("Error", f"Error al verificar: {str(e)}")