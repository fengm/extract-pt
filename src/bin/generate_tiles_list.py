
def main(opts):
    import os

    _f_inp = opts.input

    for _y in range(1984, 2020):
        _cmd = 'generate_tiles_extent.py -i %(inp)s -e %(inp)s/data/h001/v001/h001v001/h001v001_tcc_%(y)s_dat.tif -o %(inp)s/list/forest_%(y)s_dat.shp' % {'inp': _f_inp, 'y': _y}
        print(_cmd)

def usage():
    _p = environ_mag.usage(False)

    _p.add_argument('-i', '--input', dest='input', required=True)
    
    return _p

if __name__ == '__main__':
    from gio import environ_mag
    environ_mag.init_path()
    environ_mag.run(main, [environ_mag.config(usage())]) 