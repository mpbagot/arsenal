from PIL import Image

import random
import hashlib

cachepath = ''

def build_cat(user_id, seed=''):
	if seed:
		hasher = hashlib.md5()
		hasher.update(seed.encode())
		seed = int(hasher.hexdigest()[:6], 16)
		random.seed(seed)

	parts = {'body' : random.randint(1, 15),
		'fur' : random.randint(1, 10),
		'eyes' : random.randint(1, 15),
		'mouth' : random.randint(1, 10),
		'accessorie' : random.randint(1, 20)
		}
	parts_order = ['body', 'fur', 'eyes', 'mouth', 'accessorie']

	random.seed()

	cat = Image.new('RGBA', (70, 70))
	for part in parts_order:
		filename = 'avatars/{}_{}.png'.format(part, parts[part])
		image = Image.open(filename).convert('RGBA')
		cat = Image.alpha_composite(cat, image)	
	cat.save('../static/img/user_img/'+str(user_id)+'.png', 'PNG')
