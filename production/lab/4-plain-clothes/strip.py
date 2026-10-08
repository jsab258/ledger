"""Join the four render views into one strip (half size) for a quick look."""
import sys
from PIL import Image
d, tag, out = sys.argv[1], sys.argv[2], sys.argv[3]
ims = [Image.open('%s/%s_%s.jpg' % (d, tag, v)) for v in ('front', 'side', 'back', 'three_quarter')]
W = sum(i.width for i in ims)
s = Image.new('RGB', (W, ims[0].height))
x = 0
for i in ims:
    s.paste(i, (x, 0)); x += i.width
s.resize((W // 2, ims[0].height // 2)).save(out, quality=85)
