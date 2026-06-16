from PIL import Image
img = Image.new('RGB', (240,160), (30,144,255))
img.save('test_upload.jpg', 'JPEG')
print('created test_upload.jpg')
