from colorsys import rgb_to_hls, hls_to_rgb

def _h2r(h):
    return int(h, 16) / 255

def hex_to_rgb(h):
    assert h.startswith('#') and len(h) == 7, h
    return (_h2r(h[1:3]), _h2r(h[3:5]), _h2r(h[5:7]))

def rgb_to_hex(r, g, b):
    return '#' + ''.join(hex(int(t*255))[2:] for t in (r, g, b))

def hex_to_hls(h):
    return rgb_to_hls(*hex_to_rgb(h))

def hls_to_hex(h, l, s):
    return rgb_to_hex(*hls_to_rgb(h, l, s))

