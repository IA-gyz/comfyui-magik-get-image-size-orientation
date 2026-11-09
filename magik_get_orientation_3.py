from comfy_api.latest import io


class MagikGetOrientation3(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="Magik.GetOrientation3",
            display_name="Magik Get Orientation 3",
            category="Magik/Image/Resolution",
            description=(
                "Inspects an image's width/height and reports a square/landscape/"
                "portrait orientation plus the corresponding target dimensions."
            ),
            inputs=[
                io.Image.Input("image", tooltip="Image to inspect."),
                io.Int.Input(
                    "narrow_side",
                    default=512,
                    min=1,
                    max=0xffffffffffffffff,
                    tooltip="Output value for the short side when the image is landscape or portrait.",
                ),
                io.Int.Input(
                    "square",
                    default=512,
                    min=1,
                    max=0xffffffffffffffff,
                    tooltip="Output value for both width and height when the image is square.",
                ),
                io.Int.Input(
                    "wide_side",
                    default=768,
                    min=1,
                    max=0xffffffffffffffff,
                    tooltip="Output value for the long side when the image is landscape or portrait.",
                ),
            ],
            outputs=[
                io.Int.Output("WIDTH", display_name="Width"),
                io.Int.Output("HEIGHT", display_name="Height"),
                io.String.Output("ORIENTATION", display_name="Orientation"),
            ],
        )

    @classmethod
    def execute(cls, image, narrow_side, square, wide_side):
        # Image tensors are [B, H, W, C]
        img_height = image.shape[1]
        img_width  = image.shape[2]

        if img_width == img_height:
            width       = square
            height      = square
            orientation = "Square"
        elif img_width > img_height:
            width       = wide_side
            height      = narrow_side
            orientation = "Landscape"
        else:
            width       = narrow_side
            height      = wide_side
            orientation = "Portrait"

        return io.NodeOutput(width, height, orientation)