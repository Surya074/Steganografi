import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Program Steganografi")
        self.root.geometry("400x300")

        self.image_path = None

        self.image_path_label = tk.Label(self.root, text="Path Gambar: Tidak ada gambar dipilih")
        self.image_path_label.pack(pady=10)

        self.main_menu()
        
    # Tampilan menu utama
    def main_menu(self):
        self.clear_window()
        tk.Button(self.root, text="Sisipkan Pesan", command=self.embed_message).pack(pady=20)
        tk.Button(self.root, text="Tampilkan Pesan", command=self.extract_message).pack()
    
    # Tampilan menu sisipkan pesan
    def embed_message(self):
        self.clear_window()

        self.message_entry = tk.Entry(self.root, width=30)
        self.message_entry.pack(pady=5)

        self.image_path_label = tk.Label(self.root, text="Path Gambar: Tidak ada gambar dipilih")
        self.image_path_label.pack(pady=5)

        tk.Button(self.root, text="Pilih Gambar", command=self.choose_image).pack(pady=5)
        tk.Button(self.root, text="Konfirmasi", command=self.embed).pack(pady=5)
        tk.Button(self.root, text="Kembali", command=self.main_menu).pack(pady=5, side=tk.LEFT)

    # Tampilan menu tampilkan pesan
    def extract_message(self):
        self.clear_window()

        self.image_path_label = tk.Label(self.root, text="Path Gambar: Tidak ada gambar dipilih")
        self.image_path_label.pack(pady=5)

        tk.Button(self.root, text="Pilih Gambar", command=self.choose_image).pack(pady=5)
        tk.Button(self.root, text="Tampilkan Pesan", command=self.display_message).pack(pady=5)
        tk.Button(self.root, text="Kembali", command=self.main_menu).pack(pady=5, side=tk.LEFT)
    
    # Fungsi pemilihan gambar
    def choose_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg;*.bmp")])
        if not self.image_path:
            self.show_warning("Pilih gambar terlebih dahulu!")
            return
        
        if self.image_path:
            self.image_path_label.config(text=f"Path Gambar: {self.image_path}", wraplength=300)

    # Fungsi penyisipan pesan di GUI
    def embed(self):
        if not self.image_path:
            self.show_warning("Pilih gambar terlebih dahulu!")
            return

        message = self.message_entry.get()
        if not message:
            self.show_warning("Masukkan pesan terlebih dahulu!")
            return

        try:
            steganography = Backend(self.image_path)
            embedded_image_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if not embedded_image_path:
                return

            steganography.embed_message(message, embedded_image_path)
            messagebox.showinfo("Pesan Disisipkan", f"Pesan berhasil disisipkan!\nGambar disimpan di: {embedded_image_path}")
            self.main_menu()
        except Exception as e:
            self.show_warning(f"Error: {str(e)}")

    # Fungsi menampilkan pesan di GUI
    def display_message(self):
        if not self.image_path:
            self.show_warning("Pilih gambar terlebih dahulu.")
            return

        try:
            steganography = Backend(self.image_path)
            message = steganography.extract_message()
            messagebox.showinfo("Hasil", f"{message}")
        except Exception as e:
            self.show_warning(f"Error: {str(e)}")

    # Fungsi menampilkan peringatan
    def show_warning(self, message):
        messagebox.showwarning("Peringatan", message)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

class Backend:
    def __init__(self, image_path):
        self.image_path = image_path

    # Fungsi penyisipan pesan ke gambar
    def embed_message(self, message, output_path=None):
        image = Image.open(self.image_path)
        binary_message = self.text_to_binary(message)

        end_marker = '********'
        binary_message += ''.join(format(ord(char), '08b') for char in end_marker)  # End of message marker

        pixels = list(image.getdata())
        data_index = 0
        new_pixels = []

        for pixel in pixels:
            new_pixel = list(pixel)
            for j in range(3):  # Iterasi melalui nilai RGB
                if data_index < len(binary_message):
                    new_pixel[j] &= 0b11111110  # Set LSB ke 0
                    new_pixel[j] |= int(binary_message[data_index])
                    data_index += 1

            new_pixels.append(tuple(new_pixel))

        new_image = Image.new(image.mode, image.size)
        new_image.putdata(new_pixels)

        if output_path:
            new_image.save(output_path)

        return new_image

    # Fungsi mengambil pesan dari gambar
    def extract_message(self, output_path=None):
        image = Image.open(self.image_path)
        pixels = list(image.getdata())

        binary_message = ""
        for pixel in pixels:
            for value in pixel:  # Iterasi melalui nilai RGB
                binary_message += str(value & 1)  # Extract LSB

        end_marker = '********'
        end_marker_binary = ''.join(format(ord(char), '08b') for char in end_marker)

        end_marker_index = binary_message.find(end_marker_binary)
        if end_marker_index != -1:
            binary_message = binary_message[:end_marker_index]
            text_message = self.binary_to_text(binary_message)

            if output_path:
                new_image = Image.new(image.mode, image.size)
                new_pixels = [tuple(int(value, 2) for value in binary_message[i:i+8]) for i in range(0, len(binary_message), 8)]
                new_image.putdata(new_pixels)
                new_image.save(output_path)

            return text_message
        else:
            return "Tidak ada pesan di gambar ini."

    # Fungsi mengubah teks ke biner
    def text_to_binary(self, text):
        binary_message = ''.join(format(ord(char), '08b') for char in text)
        return binary_message

    # Fungsi mengubah biner ke teks
    def binary_to_text(self, binary):
        text = ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
        return text

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
