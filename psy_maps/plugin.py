"""psy-simple psyplot plugin

This module defines the rcParams for the psy-simple plugin"""
import six
import yaml
from psyplot.config.rcsetup import RcParams
from matplotlib.rcsetup import validate_path_exists
from psy_simple.plugin import (
    try_and_error, validate_none, validate_str, validate_float,
    validate_nseq_float, validate_bool_maybe_none, validate_fontsize,
    validate_color, validate_dict, BoundsValidator, bound_strings,
    ValidateInStrings, validate_bool)
from psy_maps import __version__ as plugin_version


def get_versions(requirements=True):
    if requirements:
        import cartopy
        return {'version': plugin_version,
                'requirements': {'cartopy': cartopy.__version__}}
    else:
        return {'version': plugin_version}


# -----------------------------------------------------------------------------
# ------------------------- validation functions ------------------------------
# -----------------------------------------------------------------------------


def validate_grid(val):
    if isinstance(val, tuple) and len(val) in [2, 3]:
        return val
    try:
        return validate_bool_maybe_none(val)
    except ValueError:
        return BoundsValidator('grid', bound_strings, True)(val)


class ProjectionValidator(ValidateInStrings):

    def __call__(self, val):
        if isinstance(val, six.string_types):
            return ValidateInStrings.__call__(self, val)
        return val  # otherwise we skip the validation


def validate_dict_yaml(s):
    if isinstance(s, dict):
        return s
    validate_path_exists(s)
    if s is not None:
        with open(s) as f:
            return yaml.load(f)


# -----------------------------------------------------------------------------
# ------------------------------ rcParams -------------------------------------
# -----------------------------------------------------------------------------


#: the :class:`~psyplot.config.rcsetup.RcParams` for the psy-simple plugin
rcParams = RcParams(defaultParams={

    # -------------------------------------------------------------------------
    # ----------------------- Registered plotters -----------------------------
    # -------------------------------------------------------------------------

    'project.plotters': [

        {'maps': {
             'module': 'psy_maps.plotters',
             'plotter_name': 'MapPlotter',
             'plot_func': False},
         'mapplot': {
             'module': 'psy_maps.plotters',
             'plotter_name': 'FieldPlotter',
             'prefer_list': False,
             'default_slice': 0,
             'default_dims': {'x': slice(None), 'y': slice(None)},
             'summary': 'Plot a 2D scalar field on a map'},
         'mapvector': {
             'module': 'psy_maps.plotters',
             'plotter_name': 'VectorPlotter',
             'prefer_list': False,
             'default_slice': 0,
             'default_dims': {'x': slice(None), 'y': slice(None)},
             'summary': 'Plot a 2D vector field on a map',
             'example_call': "filename, name=[['u_var', 'v_var']], ..."},
         'mapcombined': {
             'module': 'psy_maps.plotters',
             'plotter_name': 'CombinedPlotter',
             'prefer_list': True,
             'default_slice': 0,
             'default_dims': {'x': slice(None), 'y': slice(None)},
             'summary': ('Plot a 2D scalar field with an overlying vector '
                         'field on a map'),
             'example_call': (
                 "filename, name=[['my_variable', ['u_var', 'v_var']]], ...")},
         }, validate_dict],

    # -------------------------------------------------------------------------
    # --------------------- Default formatoptions -----------------------------
    # -------------------------------------------------------------------------
    # MapBase
    'plotter.maps.lonlatbox': [
        None, try_and_error(validate_none, validate_str,
                            validate_nseq_float(4)),
        'fmt key to define the longitude latitude box of the data'],
    'plotter.maps.map_extent': [
        None, try_and_error(validate_none, validate_str,
                            validate_nseq_float(4)),
        'fmt key to define the extent of the map plot'],
    'plotter.maps.clon': [
        None, try_and_error(validate_none, validate_float, validate_str),
        'fmt key to specify the center longitude of the projection'],
    'plotter.maps.clat': [
        None, try_and_error(validate_none, validate_float, validate_str),
        'fmt key to specify the center latitude of the projection'],
    # TODO: Implement the drawing of shape files on a map
    # 'plotter.maps.lineshapes': [None, try_and_error(
    #     validate_none, validate_dict, validate_str, validate_stringlist)],
    'plotter.maps.grid_labels': [
        None, validate_bool_maybe_none,
        'fmt key to draw labels of the lat-lon-grid'],
    'plotter.maps.grid_labelsize': [
        12.0, validate_fontsize,
        'fmt key to modify the fontsize of the lat-lon-grid labels'],
    'plotter.maps.grid_color': [
        'k', try_and_error(validate_none, validate_color),
        'fmt key to modify the color of the lat-lon-grid'],
    'plotter.maps.grid_settings': [
        {}, validate_dict,
        'fmt key for additional line properties for the lat-lon-grid'],
    'plotter.maps.xgrid': [
        True, validate_grid, 'fmt key for drawing meridians on the map'],
    'plotter.maps.ygrid': [
        True, validate_grid, 'fmt key for drawing parallels on the map'],
    'plotter.maps.projection': [
        'cyl', ProjectionValidator(
            'projection', ['northpole', 'ortho', 'southpole', 'moll', 'geo',
                           'robin', 'cyl'], True),
        'fmt key to define the projection of the plot'],
    'plotter.maps.transform': [
        'cyl', ProjectionValidator(
            'projection', ['northpole', 'ortho', 'southpole', 'moll', 'geo',
                           'robin', 'cyl'], True),
        'fmt key to define the native projection of the data'],
    'plotter.maps.plot.min_circle_ratio': [
        0.05, validate_float,
        'fmt key to specify the min_circle_ratio that is used to mask very '
        ' flat triangles in a triangular plot'],
    'plotter.maps.lsm': [
        True, try_and_error(validate_bool, validate_float),
        'fmt key to draw a land sea mask'],

    # -------------------------------------------------------------------------
    # ---------------------------- Miscallaneous ------------------------------
    # -------------------------------------------------------------------------

    # yaml file that holds definitions of lonlatboxes
    'lonlatbox.boxes': [
        {}, validate_dict_yaml,
        'longitude-latitude boxes that shall be accessible for the lonlatbox, '
        'map_extent, etc. keywords. May be a dictionary or the path to a '
        'yaml file'],

    })

rcParams.update_from_defaultParams()
