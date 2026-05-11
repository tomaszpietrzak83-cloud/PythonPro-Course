class Tv:
    def __init__(self, channel=1, volume=10, __isON=False):
        self.channel = channel
        self.volume = volume
        self.__isON = __isON

    def turn_on(self):
        self.__isON = True

    def turn_off(self):
        self.__isON = False

    def change_channel(self, number):
        if self.__isON:
            self.channel = number
        else:
            print("TV is off. Can't change channel.")

    def volume_up(self):
        if self.__isON:
            if self.volume < 100:
                self.volume += 1
            else:
                print("Volume is at maximum.")
        else:
            print("TV is off. Can't adjust volume.")

    def volume_down(self):
        if self.__isON:
            if self.volume > 0:
                self.volume -= 1
            else:
                print("Volume is at minimum.")
        else:
            print("TV is off. Can't adjust volume.")

    def info(self):
        state = "ON" if self.__isON else "OFF"
        if self.__isON:
            print(f"TV is {state}, Channel: {self.channel}, Volume: {self.volume}")
        else:
            print(f"TV is {state}.")


def repeater(times, func):
    def wrapper(*args, **kwargs):

        for _ in range(times):
            func(*args, **kwargs)

    return wrapper


tv = Tv()

tv.turn_on()
repeat_volume_up = repeater(15, tv.volume_up)
repeat_volume_up()

tv.change_channel(5)
tv.info()
