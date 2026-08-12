class Instrument:
    def play(self):
        return "Plays sound."


class Stringed(Instrument):
    def play(self):
        return super().play() + " [Strum the string]"


class Wind(Instrument):
    def play(self):
        return super().play() + " [Blow into the instrument]"


class Guitar(Stringed):
    def play(self):
        return super().play() + " [Play G major chord]"


class Trumpet(Wind):
    def play(self):
        return super().play() + " [Play a trumpet sound]"


instrument = Instrument()
stringed = Stringed()
wind = Wind()
guitar = Guitar()
trumpet = Trumpet()

instruments = [instrument, stringed, wind, guitar, trumpet]
for instr in instruments:
    print(instr.play())
