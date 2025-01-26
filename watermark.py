import os
import zlib
from stepic import encode, decode  # Para imágenes
from PIL import Image

class WatermarkEngine:
    @staticmethod
    def add_watermark(file_path, data, output_path):
        try:
            compressed_data = zlib.compress(data.encode() + b':::END')

            if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Llamada CORRECTA al método interno
                WatermarkEngine._embed_in_image(file_path, compressed_data, output_path)
            else:
                WatermarkEngine._embed_in_generic(file_path, compressed_data, output_path)
            return True
        except Exception as e:
            print(f"Error al agregar watermark: {str(e)}")
            return False

    # Métodos internos deben ser estáticos y bien definidos
    @staticmethod
    def _embed_in_image(image_path, data, output_path):
        img = Image.open(image_path)

        # Convertir JPEG a PNG automáticamente
        if image_path.lower().endswith(('.jpg', '.jpeg')):
            output_path = output_path.replace('.jpg', '.png').replace('.jpeg', '.png')
            img = img.convert('RGBA')

        img_encoded = encode(img, data)
        img_encoded.save(output_path, format='PNG', compression_level=0)
        return output_path

    @staticmethod
    def _embed_in_generic(file_path, data, output_path):
        with open(file_path, 'rb') as f:
            content = f.read()

        marker = b"WTMK" + len(data).to_bytes(4, 'big') + data
        with open(output_path, 'wb') as f:
            f.write(content + marker)

    @staticmethod
    def extract_watermark(file_path):
        try:
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                img = Image.open(file_path)
                img.load()  # Forzar carga de todos los datos
                compressed_data = decode(img)

                # Buscar marcador final
                if b':::END' in compressed_data:
                    decompressed = zlib.decompress(compressed_data.split(b':::END')[0])
                    return decompressed.decode()
            else:
                with open(file_path, 'rb') as f:
                    content = f.read()

                index = content.rfind(b"WTMK")
                if index == -1:
                    return ""

                data_len = int.from_bytes(content[index+4:index+8], 'big')
                compressed_data = content[index+8:index+8+data_len]
                return zlib.decompress(compressed_data).decode()

        except Exception as e:
            print(f"Error de extracción: {str(e)}")
            return ""