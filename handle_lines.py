class ColorButtonManager:
    def __init__(self, app):
        self.app = app
        self.UNIQUE_BUTT = 'assets/crown.png'

    def find_adjacent_lines(self, row, col):
        directions = [
            (1, 0), (0, 1), (1, 1), (1, -1),
        ]
        current_image = self.app.get_button_at(row, col).background_normal
        adjacent_lines = set()
        for direction in directions:
            line = self.find_full_line(direction, row, col, current_image)
            if len(line) >= 5:
                adjacent_lines.update(line)
        return adjacent_lines

    def find_full_line(self, direction, row, col, current_image):
        line1 = self.find_line_in_direction(direction, row, col, current_image)
        line2 = self.find_line_in_direction(
            (-direction[0], -direction[1]), row, col, current_image,
        )
        full_line = line1.union(line2)
        full_line.add((row, col))
        return full_line

    def find_line_in_direction(self, direction, row, col, current_image):
        x, y = row, col
        dir_x, dir_y = direction
        line_in_dir = set()
        while True:
            x += dir_x
            y += dir_y
            if self.app.is_within_bounds(x, y):
                adjacent_button = self.app.get_button_at(x, y)
                adjacent_image = adjacent_button.background_normal

                if adjacent_image == '' or (adjacent_image != current_image and adjacent_image != self.UNIQUE_BUTT):
                    break
                elif adjacent_image == current_image or adjacent_image == self.UNIQUE_BUTT:
                    line_in_dir.add((x, y))
            else:
                break
        return line_in_dir

    def remove_line(self, line):
        total_lines_to_remove = set()
        for x, y in line:
            lines = self.find_adjacent_lines(x, y)
            if len(lines) >= 5:
                total_lines_to_remove.update(lines)
        if len(total_lines_to_remove) >= 5:
            for x, y in total_lines_to_remove:
                if self.app.is_within_bounds(x, y):
                    self.app.clear_button(x, y)

    def remove_lines_if_unique(self, row, col):
        current_button = self.app.get_button_at(row, col)
        current_image = current_button.background_normal
        print(f'Current Image: {current_image}')
        print(row, col)
        if current_image == self.UNIQUE_BUTT:
            lines = self.find_adjacent_lines(row, col)
            print(f'Adjacent Lines: {lines}')
            # it fails to add the lines and never
            # reaches 5 or more to sent to remove_lines
            if len(lines) >= 5:
                print('Removing lines...')
                self.remove_line(lines)
            else:
                print('Not enough lines to remove.')
        else:
            print('Not a unique button.')
