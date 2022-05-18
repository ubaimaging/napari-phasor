import napari
import PhasorPy as ph
from napari.types import ImageData
from magicgui import magicgui
import tifffile


# turn the gaussian blur function into a magicgui
# - `auto_call` tells magicgui to call the function when a parameter changes
# - we use `widget_type` to override the default "float" widget on sigma,
#   and provide a maximum valid value.
# - we contstrain the possible choices for `mode`


def image_reader(path):
    return tifffile.imread(path)


@magicgui(
    auto_call=True,
    harmonic={"widget_type": "IntSlider", "max": 100},
    radius={"widget_type": "FloatSlider", "max": 1},
    layout='horizontal'
)
def phasor_plot(image=None, harmonic: int = 1, radius: float = 0.1) -> ImageData:
    if image is not None:
        dc, g, s, _, _ = ph.phasor(image, harmonic)
        return ph.interactive(dc, g, s, radius)


# create a viewer and add some images
im = image_reader('/home/bruno/Documentos/Proyectos/TESIS/TESIS/Experimentos/exp_bordes/img_1x1/lsm/exp_1x1_nevo_2.lsm')
viewer = napari.Viewer()
viewer.add_image(im, name="Raw image stack")

# Add it to the napari viewer
viewer.window.add_dock_widget(phasor_plot(im))
# update the layer dropdown menu when the layer list changes
viewer.layers.events.changed.connect(phasor_plot.reset_choices)

napari.run()
