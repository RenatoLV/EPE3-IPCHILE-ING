from pathlib import Path
import pypdfium2 as pdfium
from PIL import Image,ImageOps,ImageDraw
root=Path(__file__).resolve().parents[1]
out=root/'build/report_render';out.mkdir(exist_ok=True)
pdf=pdfium.PdfDocument(str(root/'entregables/Maqueta_Informe_EPE3.pdf'))
thumbs=[]
for i,page in enumerate(pdf):
    img=page.render(scale=1.4).to_pil().convert('RGB')
    img.save(out/f'page-{i+1}.png')
    thumb=ImageOps.contain(img,(300,420))
    tile=Image.new('RGB',(320,455),'#dce2e7');tile.paste(thumb,((320-thumb.width)//2,5))
    ImageDraw.Draw(tile).text((12,433),str(i+1),fill='black')
    thumbs.append(tile)
for start in range(0,len(thumbs),7):
    sheet=Image.new('RGB',(320*len(thumbs[start:start+7]),455),'white')
    for j,t in enumerate(thumbs[start:start+7]):sheet.paste(t,(320*j,0))
    sheet.save(out/f'contact-{start}.png')
