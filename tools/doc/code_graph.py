import os

import dishka.plotter

from rpgram_setup.entry.ioc import make_container


def make_graph():
    container = make_container({})
    with open(os.environ['MERMAID_FOR_WORLD'], "w+", encoding="utf-8") as f:
        f.write(dishka.plotter.render_mermaid(container))


if __name__ == "__main__":
    make_graph()
