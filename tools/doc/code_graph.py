import dishka.plotter

from rpgram_setup.infrastructure.ioc import make_container


def make_graph():
    container = make_container({})
    # d2
    with open("../../docs/code.d2", "w+", encoding="utf-8") as f:
        f.write(dishka.plotter.render_d2(container))
    # mermaid
    with open("../../docs/code.html", "w+", encoding="utf-8") as f:
        f.write(dishka.plotter.render_mermaid(container))


if __name__ == "__main__":
    make_graph()
