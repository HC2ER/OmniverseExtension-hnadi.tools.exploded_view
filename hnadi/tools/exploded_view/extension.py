import omni.ext
import omni.usd
from .exploded_view_ui import Cretae_UI_Framework


class Main_Entrance(omni.ext.IExt):
    def on_startup(self, ext_id):
        Cretae_UI_Framework(self)

    def on_shutdown(self):
        print("[hnadi.tools.exploded_view] shutdown")
        self._window.destroy()
        self._window = None
        stage = omni.usd.get_context().get_stage()