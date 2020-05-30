"""
File: extract_tcc_records.py
Author: Min Feng
Version:  0.1
Create: 2020-05-15 21:54:57
Description: 
"""

def extract_tcc_tile(f, pt):
    from gio import geo_raster_ex as gx

    _bnd = gx.load(f)
    if _bnd is None:
        return None

    _vv = _bnd.read(pt)

    if _vv is None:
        return None

    if _vv > 100:
        return None

    return _vv

def extract_tcc_bnd(f, pt):
    from gio import geo_raster as ge

    _bnd = ge.open(f).get_band()
    if _bnd is None:
        return None

    _vv = _bnd.read_location(pt.x, pt.y)
    if _vv is None:
        return None

    if _vv > 100:
        return None

    return _vv

def extract_tcc_records(d_inp, y, x):
    from gio import geo_raster as ge
    from gio import geo_base as gb
    import os
    import re

    _vs = {}
    _pt = gb.geo_point(x, y, gb.proj_from_epsg())

    for _root, _dirs, _files in os.walk(d_inp):
        for _file in _files:
            _vv = None
            if _file.endswith('_dat.tif'):
                _vv = extract_tcc_bnd(os.path.join(_root, _file), _pt)

            if _file.endswith('_dat.shp'):
                _vv = extract_tcc_tile(os.path.join(_root, _file), _pt)

            if _vv is None:
                continue

            if _vv > 100:
                continue

            _mm = re.search('_(\d{4})_dat', _file)
            if not _mm:
                continue

            _y = _mm.group(1)

            print('+', _y, _vv)
            _vs[_y] = _vv
    
    _xs = sorted(_vs.keys())
    _ys = [_vs[_k] for _k in _xs]

    return _xs, _ys

def extract_pt_ndvi(y, x):
    _url = 'https://tpts01.terrapulse.com:8090/_gee_ndvi?format=png&x=%f&y=%f&w=1040&h=220&agg=month' % (x, y)
    print(_url)
    return _url

def generate_list(d):
    import os

    _f_inp = os.path.abspath(d)
    for _y in range(1984, 2020):
        print('indexing', _y)

        _cmd = 'generate_tiles_extent.py -i %(inp)s -e %(inp)s/data/h001/v001/h001v001/h001v001_tcc_%(y)s_dat.tif -o %(inp)s/list/forest_%(y)s_dat.shp' % {'inp': _f_inp, 'y': _y}
        if os.path.exists('generate_tiles_extent.py'):
            _cmd = 'python ' + _cmd

        os.system(_cmd.replace('/', os.path.sep))

def extract_pt_tcc(d_inp, y, x, f_out):
    import os
    import pandas as pd
    import matplotlib.pyplot as plt

    _d_inp = os.path.join(d_inp, 'data')
    if not os.path.exists(_d_inp):
        print('* the input folder is wrong, please check and try again')
        return

    _d_inp = os.path.join(d_inp, 'list')
    if not os.path.exists(_d_inp):
        generate_list(d_inp)

    fig = plt.figure(figsize=(15, 3), dpi=80, facecolor='w', edgecolor='k')
    axes = fig.add_subplot(111)

    _xs, _ys = extract_tcc_records(_d_inp, y, x)

    axes.grid()
    axes.plot(_xs, _ys, 'go--', markersize=8)
    fig.autofmt_xdate()

    import os
    (lambda x: os.path.exists(x) or os.makedirs(x))(os.path.dirname(os.path.abspath(f_out)))
    plt.savefig(f_out)

def main(opts):
    extract_pt_tcc(opts.input, opts.coordinate[0], opts.coordinate[1], opts.output)

def usage():
    _p = environ_mag.usage(False)
    
    _p.add_argument('-i', '--input', dest='input', required=True)
    _p.add_argument('-c', '--coordinate', dest='coordinate', required=True, type=float, nargs=2)
    _p.add_argument('-o', '--output', dest='output', required=True)

    return _p

if __name__ == '__main__':
    from gio import environ_mag
    environ_mag.init_path()
    environ_mag.run(main, [environ_mag.config(usage())]) 
