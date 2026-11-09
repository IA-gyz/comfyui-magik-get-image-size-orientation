from comfy_api.latest import io


class MagikGetOrientation5(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="Magik.GetOrientation5",
            display_name="Magik Get Orientation 5",
            category="Magik/Image/Resolution",
            description=(
                "Picks the closest of three aspect-ratio targets (A, B, square) "
                "based on the input image's shape and returns the matching output dimensions."
            ),
            inputs=[
                io.Image.Input("image", tooltip="Image to inspect."),
                io.Int.Input(
                    "narrow_side_A",
                    default=512,
                    min=1,
                    max=0xffffffffffffffff,
                    tooltip="Short side of aspect-ratio target A.",
                ),
                io.Int.Input(
                    "wide_side_A",
                    default=768,
                    min=1,
                    max=0xffffffffffffffff,
                    tooltip="Long side of aspect-ratio target A.",
                ),
                io.Int.Input(
                    "narrow_side_B",
                    default=512,
                    min=1,
                    max=0xffffffffffffffff,
                    tooltip="Short side of aspect-ratio target B.",
                ),
                io.Int.Input(
                    "wide_side_B",
                    default=896,
                    min=1,
                    max=0xffffffffffffffff,
                    tooltip="Long side of aspect-ratio target B.",
                ),
                io.Int.Input(
                    "square",
                    default=512,
                    min=1,
                    max=0xffffffffffffffff,
                    tooltip="Side length used when the square target is chosen.",
                ),
            ],
            outputs=[
                io.Int.Output("OUTPUT_W", display_name="Width"),
                io.Int.Output("OUTPUT_H", display_name="Height"),
                io.String.Output("ORIENTATION", display_name="Orientation"),
            ],
        )

    @classmethod
    def execute(cls, image, narrow_side_A, wide_side_A, narrow_side_B, wide_side_B, square):
        # Target ratios (always >= 1 by convention: wide / narrow)
        ratio_A = wide_side_A / narrow_side_A
        ratio_B = wide_side_B / narrow_side_B

        # Image tensor shape: [B, H, W, C]
        input_height = image.shape[1]
        input_width  = image.shape[2]

        # Determine input_ratio and Orientation
        if input_width == input_height:
            input_ratio = 1.0
            orientation = "Square"
        elif input_width > input_height:
            input_ratio = input_width / input_height
            orientation = "Landscape"
        else:
            input_ratio = input_height / input_width
            orientation = "Portrait"

        # Gap between input ratio and each of the three candidates
        gap_square = abs(input_ratio - 1.0)
        gap_A      = abs(input_ratio - ratio_A)
        gap_B      = abs(input_ratio - ratio_B)

        # Pick the closest target and assign output dimensions
        if gap_square <= gap_A and gap_square <= gap_B:
            output_w = square
            output_h = square
        elif gap_A <= gap_B:
            if orientation == "Landscape":
                output_w = wide_side_A
                output_h = narrow_side_A
            else:                          # Portrait or Square (fallback)
                output_w = narrow_side_A
                output_h = wide_side_A
        else:                              # ratio_B is closest
            if orientation == "Landscape":
                output_w = wide_side_B
                output_h = narrow_side_B
            else:                          # Portrait or Square (fallback)
                output_w = narrow_side_B
                output_h = wide_side_B

        return io.NodeOutput(output_w, output_h, orientation)
