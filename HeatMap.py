from PIL import Image, ImageDraw, ImageFont


class HeatMap:
    def __init__(self, directory='images/'):
        # keyboard.png is the base image
        self.image = Image.open('keyboard.png').convert('RGBA')
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.truetype("arial.ttf", 20)

        self.key_map = {}
        self.same = {}
        self.directory = directory

        # stored location of the keys are in this file
        file = open('keys.txt')
        for line in file:
            args = line.split(' ')
            if len(args) == 5:
                self.key_map[args[0]] = tuple([int(i) for i in args[1:]])
            else:
                self.same[args[0]] = args[1].strip()  # for characters that share a key
        file.close()
        self.same['\n'] = 'enter'

    def reset(self):
        # give ourselves a blank image again
        self.image = Image.open('keyboard.png').convert('RGBA')
        self.draw = ImageDraw.Draw(self.image)

    # Draws the appropriate colors and letters on the keyboard and saves the image, returning the path to the image
    def get_heat_map(self, comment, title='keys'):
        self.draw_heat(comment)
        self.draw_text()
        try:
            self.save_image(title)
        except OSError:  # some names like https:// will give an OSError
            title = 'keys'
            self.save_image(title)
        return self.directory + title + '.png'

    # This will use the data given from _rank() to draw the appropriate color on the key of the keyboard. Keys
    # more frequently pressed will show more red, keys less frequently pressed will show more yellow.
    def draw_heat(self, comment):
        rankings = self._rank(comment)
        # we need a highest count so we color the map based on the amount of keys pressed relative to one another
        highest = max(rankings.values())
        for key, value in rankings.items():
            try:
                intensity = int(255 * (value / highest))
            except ZeroDivisionError:
                print('ERROR ERROR ERROR')
                print('\t' + comment)
                print('\t' + str(rankings))
            x, y, width, height = self.key_map[key]
            self.draw.rectangle(((x, y), (x + width, y + height)),
                                (255, int(255 - intensity), int(intensity / 4),
                                 255))  # this gives us a nice Red -> Yellow scale

    # _rank will take the comment given and give a "rank" to each letter in the comment depending on how frequent
    # the letter was pressed.
    def _rank(self, comment):
        rankings = {}
        for letter in comment:
            # check if it was key that needed shift to be pressed
            if letter in self.same.keys() or letter.isupper():
                letter = self.same[letter] if not letter.isalpha() else letter.lower()
                # we assume they used the far-side shift
                if self.key_map[letter][0] < 268:
                    rankings['R-shift'] = 0 if 'R-shift' not in rankings else rankings['R-shift'] + 1
                else:
                    rankings['L-shift'] = 0 if 'L-shift' not in rankings else rankings['L-shift'] + 1
            letter = letter.lower()
            if letter in self.key_map:
                rankings[letter] = 0 if letter not in rankings else rankings[letter] + 1
        return rankings

    def draw_text(self):
        for key, value in self.key_map.items():
            x, y, width, height = value
            self.draw.text((x + (width / 4), y + (height / 4)), key, (0, 0, 0, 255), self.font)

    def save_image(self, name='keys'):
        self.image.save(self.directory + name + '.png')
