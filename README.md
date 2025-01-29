# Don't Leak My File 🔍

Aplicación de protección contra filtraciones de documentos desarrollada en Python. Utiliza **watermarks cifrados con AES-256** y seguimiento en base de datos para detectar posibles filtraciones. ¡Protege tu propiedad intelectual con tecnología avanzada! 🛡️

---

## Características principales ✨

- **Watermark cifrado**: Incrusta metadatos cifrados con AES-256-CBC en los archivos
- **Soporte múltiple**: Funciona con archivos (PDF, DOCX, XLSX, etc.)
- **Base de datos segura**: Registra todos los documentos protegidos con UUID únicos
- **Detección de filtraciones**: Verifica si un documento aparece en registros de filtraciones
- **Interfaz amigable**: GUI intuitiva con Tkinter y ttkbootstrap
- **Protección integral**: Combina cifrado, watermarking y tracking en una solución

---

## Requisitos 📋

- Python 3.9+
- Bibliotecas requeridas:
  - `pycryptodome` (cifrado AES)
  - `pillow` (manejo de imágenes)
  - `stepic` (watermark en imágenes)
  - `ttkbootstrap` (interfaz moderna)
  - `zlib` (compresión de datos)
  - `stegano` (cifrado de datos)

---

## Instalación 🛠️

1. Clona el repositorio:

    ```bash
    git clone https://github.com/JkDevArg/dont-leak-my-file.git
    cd dont-leak-my-file
    ```

2. Instala dependencias:

    ```bash
    pip install -r requirements.txt
    ```

3. Ejecuta la aplicación:

    ```bash
    python main.py
    ```

---

## Uso 🖥️

### Proteger un documento

1. En la pestaña "Proteger Documento"
2. Ingresa el nombre completo a quien se lo compartiras
3. Selecciona el archivo a proteger
4. Guarda el archivo marcado
5. ¡Listo! El documento queda registrado con watermark cifrado

### Verificar posible filtración

1. En la pestaña "Verificar Documento"
2. Selecciona el archivo a verificar
3. La aplicación mostrará:
   - Metadatos descifrados (UUID, nombre, fecha)
   - Estado de filtración en la base de datos
   - Alerta si el documento está comprometido

---

## Estructura del proyecto 📂


dont-leak-my-file/

├── main.py

├── crypto.py # Lógica de cifrado AES

├── database.py # Manejo de base de datos SQLite

├── gui.py # Interfaz gráfica

├── watermark.py # Sistema de watermarking

└── documents.db # Base de datos de registros

---

## Mecanismo de protección 🔒

1. Genera UUID único para cada documento
2. Crea metadatos cifrados con AES-256-CBC
3. Incrusta los datos en el archivo usando:
   - Marcador binario al final del archivo
4. Registra el documento en base de datos local

---

## Notas de seguridad ⚠️

- La clave AES estática se usa solo para demostración (modifícala en producción o del uso que le des)
- Los metadatos incluyen marca temporal para tracking temporal
- El sistema detecta documentos registrados, no el contenido en sí
- Recomendado para uso interno y seguimiento de documentos confidenciales

---

## Contribuciones 🤝

¡Bienvenidas las contribuciones! Para mejorar el proyecto:

1. Haz fork del repositorio
2. Crea tu rama de features (`git checkout -b feature/awesome-feature`)
3. Haz commit de tus cambios
4. Push a la rama (`git push origin feature/awesome-feature`)
5. Abre un Pull Request

---

## Contacto 📩

**Developer**: Joaquin Centurión

GitHub: [JkDevArg](https://github.com/JkDevArg)

LinkedIn: [Joaquin Centurión](https://www.linkedin.com/in/joaquincenturion/)

¡Reporta cualquier issue en el repositorio!
