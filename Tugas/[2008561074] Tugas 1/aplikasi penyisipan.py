from PIL import Image

def Encode(path_gambar, teks, path_output):
    gambar_asli = Image.open(path_gambar)
    gambar_terencode = gambar_asli.copy()
    teks_biner = ''.join(format(ord(char), '08b') for char in teks) + '1111111111111110'
    if len(teks_biner) > (gambar_asli.width * gambar_asli.height * 3):
        raise ValueError("Pesan terlalu panjang!")
    
    index = 0
    for x in range(gambar_asli.width):
        for y in range(gambar_asli.height):
            pixel = list(gambar_asli.getpixel((x, y)))
            for color_channel in range(3):
                if index < len(teks_biner):
                    pixel[color_channel] = int(format(pixel[color_channel], '08b')[:-1] + teks_biner[index], 2)
                    index += 1
            gambar_terencode.putpixel((x, y), tuple(pixel))

    nama_output = path_output + '\output.bmp'
    gambar_terencode.save(nama_output)
    

def Decode(path_gambar):
    gambar_terencode = Image.open(path_gambar)
    teks_biner = ''

    for x in range(gambar_terencode.width):
        for y in range(gambar_terencode.height):
            pixel = list(gambar_terencode.getpixel((x, y)))
            for color_channel in range(3):
                teks_biner += format(pixel[color_channel], '08b')[-1]

    delimiter_index = teks_biner.find('1111111111111110')
    if delimiter_index != -1:
        teks_biner = teks_biner[:delimiter_index]

    try:
        text = ''.join(chr(int(teks_biner[i:i+8], 2)) for i in range(0, len(teks_biner), 8))
        return text
    except ValueError:
        return "Pesan tidak ditemukan!"
    
def main():
    while True:
        print("\n##Aplikasi Penyisip Teks Ke Gambar##")
        print("Opsi :")
        print("1. Encode teks ke dalam gambar")
        print("2. Decode teks dari gambar")
        print("3. Keluar")
        pil = input("Masukan Opsi: ")

        if pil == "1":
            path_gambar = input("Masukkan path gambar dengan nama dan formatnya: ")
            teks = input("Masukkan teks yang ingin disisipkan: ")
            path_output = input("Masukkan path output gambar: ")
            Encode(path_gambar, teks, path_output)
            print("Teks berhasil disisipkan ke dalam gambar!")
        elif pil == "2":
            path_gambar = input("Masukkan path gambar yang ingin didecode: ")
            decoded_teks = Decode(path_gambar)
            print("Hasil decode:", decoded_teks)
        elif pil == "3":
            break
        else:
            print("Inputan tidak valid, mohon ulangi lagi")
            input("Tekan Enter untuk melanjutkan...")

if __name__ == '__main__':
    main()