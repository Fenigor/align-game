class ColorButtonManager:
    def __init__(self, app):
        self.app = app
        self.UNIQUE_BUTT = 'assets/crown.png'

    def find_adjacent_lines(self, row, col):
        directions = [
            (1, 0), (0, 1), (1, 1), (1, -1),
            (-1, 0), (0, -1), (-1, -1), (-1, 1),
        ]
        current_image = self.app.get_button_at(row, col).background_normal
        adjacent_lines = set()
        for direction in directions:
            current_line = self.find_line_in_direction(
                set(), direction, row, col, current_image,
            )
            if len(current_line) >= 5:
                adjacent_lines.update(current_line)
        return adjacent_lines

    def find_line_in_direction(self, current_line, direction, row, col, current_image):
        x, y = row, col
        dir_x, dir_y = direction
        previous_image = None
        run = True
        line_in_dir = []

        while run:
            if self.app.is_within_bounds(x, y):
                adjacent_button = self.app.get_button_at(x, y)
                adjacent_image = adjacent_button.background_normal
                if adjacent_image == '':
                    break

                if not previous_image and adjacent_image != self.UNIQUE_BUTT:
                    previous_image = adjacent_image

                if previous_image and adjacent_image not in (previous_image, self.UNIQUE_BUTT):
                    break

                line_in_dir.append((x, y))

                if current_image == self.UNIQUE_BUTT:
                    if len(line_in_dir) >= 5:
                        current_line.update(line_in_dir)
                else:
                    if adjacent_image == current_image or adjacent_image == self.UNIQUE_BUTT:
                        current_line.add((x, y))
                    else:
                        if len(line_in_dir) >= 5:
                            current_line.update(line_in_dir)
                        break

                x += dir_x
                y += dir_y
            else:
                break

        if len(current_line) >= 5:
            return current_line
        else:
            return set()

    def remove_line(self, line):
        for x, y in line:
            if self.app.is_within_bounds(x, y):
                self.app.clear_button(x, y)
