import analogio
import board

class Joystick:

    def __init__(
        self,
        pinx: analogio.AnalogIn,
        piny: analogio.AnalogIn,
        invert_x: bool = False,
        invert_y: bool = False,
        deadzone: float = 5.0,
        invertX: bool = None,
        invertY: bool = None,
    ):
        self.x_pin = pinx
        self.y_pin = piny

        self.invert_x = invert_x if invertX is None else invertX
        self.invert_y = invert_y if invertY is None else invertY

        self.deadzone = deadzone

        # Center calibration (0–100 scale)
        self.x_centre = (pinx.value / 65535) * 100.0
        self.y_centre = (piny.value / 65535) * 100.0

    # ------------------------------------------------------------ #

    def _read_axis(self, pin: analogio.AnalogIn, centre: float, invert: bool) -> float:
        raw = (pin.value / 65535) * 100.0

        # Normalize around center
        if raw < centre:
            scaled = (raw / centre) * 50.0 if centre > 0 else 0.0
        else:
            remaining = 100.0 - centre
            scaled = 50.0 + ((raw - centre) / remaining) * 50.0 if remaining > 0 else 100.0

        # Clamp
        scaled = max(0.0, min(100.0, scaled))

        # Deadzone
        if abs(scaled - 50.0) < self.deadzone:
            scaled = 50.0

        value = (100.0 - scaled) if invert else scaled
        return round(value, 2)

    # ------------------------------------------------------------ #

    def get_x(self) -> float:
        return self._read_axis(self.x_pin, self.x_centre, self.invert_x)

    def get_y(self) -> float:
        return self._read_axis(self.y_pin, self.y_centre, self.invert_y)

    def get_pos(self) -> list:
        return [self.get_x(), self.get_y()]
