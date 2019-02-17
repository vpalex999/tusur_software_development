
from sources.gui.guimaker import GuiMaker
from sources.gui.appwindow import AppWindow


def test_init_maker_window():

    gui_maker = GuiMaker()

    assert isinstance(gui_maker, GuiMaker)
    assert gui_maker.menuBar == []
    assert gui_maker.toolBar == []
