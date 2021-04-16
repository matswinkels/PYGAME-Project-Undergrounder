from load_map import load_map
import numpy

CHUNKS = []
cmap1 = load_map('maps/cmap1')
n_chunks = len(numpy.ravel(cmap1)) - 1 # liczba chunków

for n in range(n_chunks):
    CHUNKS.append(
        {
            'bmap': load_map('maps/bmap' + str(n)),
            'emap': load_map('maps/emap' + str(n)),
            'umap': load_map('maps/umap' + str(n))
        }
    )


'''
bmap1 = load_map('maps/bmap1')
emap1 = load_map('maps/emap1')
umap1 = load_map('maps/umap1')
bmap2 = load_map('maps/bmap2')
emap2 = load_map('maps/emap2')
umap2 = load_map('maps/umap2')
bmap3 = load_map('maps/bmap3')
emap3 = load_map('maps/emap3')
umap3 = load_map('maps/umap3')
bmap4 = load_map('maps/bmap4')
emap4 = load_map('maps/emap4')
umap4 = load_map('maps/umap4')
'''