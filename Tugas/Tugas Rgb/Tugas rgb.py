from PIL import Image

# Memasukkan gambar
nama_gambar = input('Masukkan gambar dengan ekstensinya : ')
data_gambar = Image.open(nama_gambar)

# Memasukkan koordinat X dan Y
print('\nMasukan koordinat gambar yang ingin dibaca')
x_gambar = int(input('Masukkan koordinat X : '))
y_gambar = int(input('Masukkan koordinat Y : '))

# Membaca warna RGB gambar
warna_gambar = data_gambar.getpixel((x_gambar, y_gambar))
print('\nWarna RGB gambar pada titik ({}, {}) : {}'.format(x_gambar, y_gambar, warna_gambar))

# Memasukkan cover image
nama_cover = input('\nMasukkan cover image dengan ekstensinya : ')
data_cover = Image.open(nama_cover)

# Memasukkan koordinat X dan Y cover
print('\nMasukan koordinat cover image yang ingin diubah sesuai warna rgb gambar tadi')
x_cover = int(input('Masukkan koordinat X : '))
y_cover = int(input('Masukkan koordinat Y : '))

# Membaca warna RGB cover
warna_cover = data_cover.getpixel((x_cover, y_cover))
print('\nWarna RGB cover pada titik ({}, {}) sebelum diubah: {}'.format(x_cover,y_cover, warna_cover))

# Mengubah warna RGB di titik yang ditentukan
data_cover.putpixel((x_cover,y_cover), warna_gambar)
warna_cover = warna_gambar
print('Warna RGB cover pada titik ({}, {}) setelah diubah: {}'.format(x_cover,y_cover, warna_cover))

# Menyimpan gambar yang telah diubah
data_cover.save('hasil.bmp')