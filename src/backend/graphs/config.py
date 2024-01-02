from pyvis.network import Network


class NetworkConstants:
    HEIGHT = "750px"
    WIDTH = "750px"
    DIRECTED = False
    NOTEBOOK = False
    BACKGROUND_COLOUR = "#0E1117"
    FONT_COLOUR = "white"

    PAPER_SIZE = 20
    REF_SIZE = 10

    _HEIGHT_INT = int(HEIGHT.split("px")[0])
    _WIDTH_INT = int(WIDTH.split("px")[0])


def get_default_network(
    _network_constants: NetworkConstants = NetworkConstants(),
) -> Network:
    return Network(
        height=_network_constants.HEIGHT,
        width=_network_constants.WIDTH,
        directed=_network_constants.DIRECTED,
        notebook=_network_constants.NOTEBOOK,
        bgcolor=_network_constants.BACKGROUND_COLOUR,
        font_color=_network_constants.FONT_COLOUR,
    )
