from typing_extensions import override
from comfy_api.latest import ComfyExtension, io

from .magik_get_orientation_3 import MagikGetOrientation3
from .magik_get_orientation_5 import MagikGetOrientation5


class MagikGetOrientationExtension(ComfyExtension):
    @override
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return [MagikGetOrientation3, MagikGetOrientation5]


async def comfy_entrypoint() -> MagikGetOrientationExtension:
    return MagikGetOrientationExtension()
