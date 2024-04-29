from PIL import Image, ImageFont, ImageDraw
from pathlib import Path

class Certificate:
    FONT_COLOR = "#3E1849"
    def __init__(self, image_path, font_path, horizontal_offset=0, vertical_offset=0):
        self.font_path = Path(font_path) if isinstance(font_path, str) else font_path
        self.image_path = Path(image_path) if isinstance(image_path,str) else image_path
        self.horizontal_offset = horizontal_offset
        self.vertical_offset = vertical_offset
        self.font= None
        self.template = None
        if self.font_path.exists():
            self.font = ImageFont.truetype(self.font_path, 180)
        if self.image_path.exists():
            temp = Image.open(self.image_path)
            self.WIDTH, self.HEIGHT = temp.size
            temp.close()
        
    def __enter__(self):
        self.template = Image.open(self.image_path)
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.template.close()
        self.template = None

    def generate_certificate(self, name, out_name):
        draw = ImageDraw.Draw(self.template)
        name_width = draw.textlength(name, font=self.font)
        draw.text(((self.WIDTH - name_width) / 2 + self.horizontal_offset, self.HEIGHT/2 + self.vertical_offset),
                  name, fill=self.FONT_COLOR, font=self.font)
        # Saving the certificates in a different directory.
        save_abs = Path(f"./out/{out_name}.png")
        self.template.save(save_abs)
        print('Saving Certificate of:', name) 
        return save_abs.resolve()

if __name__ == "__main__":
    certificate = Certificate("../Templates/template-gefel.png", "../Fonts/PoetsenOne-Regular.ttf", vertical_offset=(-550)) 
    with certificate as cert:
        cert.generate_certificate("tiagof")
