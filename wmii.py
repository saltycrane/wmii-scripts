#!/usr/bin/env python


import os
import re
import sys


def main():
    w = Wmii()
    cmd = sys.argv[1]
    args = sys.argv[2:]
    if cmd == 'scw':
        w.set_column_widths(args)
    elif cmd == 'makw':
        w.move_and_keep_width(args[0])


class Wmii:
    """
    wmiir xwrite /tag/sel/ctl grow col row side increment
    col: column number of the window to grow
    row: row number of the window to grow
    side: the side to grow. one of left, right, up, or down
    increment: the number of pixels to grow. use a positive number to grow larger
    and a negative number to grow smaller
    """
    def set_column_widths(self, width_list):
        """Use the 'grow' command to set the column widths to those specified.
        Widths are specified in percentages.
        Works with any number of columns.
        """
        total_width_perc = sum([float(width) for width in width_list])
        for i, width_perc in enumerate(width_list[:-1]):
            self.read_current_col_widths()
            total_width_px = float(sum(self.curr_colwidths_px))
            new_width_px = float(width_perc) / total_width_perc * total_width_px
            grow_amount_px = int(round(new_width_px - self.curr_colwidths_px[i]))
            self.xwrite("/tag/sel/ctl grow %d 1 right %dpx" % (i + 1, grow_amount_px))

    def move_and_keep_width(self, direction):
        """Move the selected window and make the new column the width of the
        old column.

        direction: either "left" or "right"
        """
        print direction
        self.read_current_col_widths()
        self.read_column_number_of_selected_client()
        if direction == 'left':
            colwidths_px = self.swap_with_previous(self.curr_colwidths_px,
                                                   self.curr_col_index)
        elif direction == 'right':
            colwidths_px = self.swap_with_next(self.curr_colwidths_px,
                                               self.curr_col_index)
        colwidths_perc = self.convert_px_to_percent(colwidths_px)
        print colwidths_perc
        self.set_column_widths(colwidths_perc)
        self.xwrite("/tag/sel/ctl send sel %s" % direction)

    def read_current_col_widths(self):
        """'wmiir read /tag/sel/index' and set the attribute, self.curr_colwidths_px.
        self.curr_colwidths_px is a list of the width (ints) (in pixels) of each
        column in the view.
        """
        lines = self.read("/tag/sel/index")
        self.curr_colwidths_px = []
        for line in lines:
            match = re.search(r"# [^~:]+ \d+ (\d+)", line)
            if match:
                self.curr_colwidths_px.append(int(match.group(1)))
        print self.curr_colwidths_px

    def read_column_number_of_selected_client(self):
        """Determine the column number (0-based) of the selected client
        """
        lines = self.read("/client/sel/ctl")
        client_id = lines[0].strip()
        print client_id
        lines = self.read("/tag/sel/index")
        for line in lines:
            if client_id in line:
                column = line.split()[0]
                break
        self.curr_col_index = int(column) - 1

    def convert_px_to_percent(self, colwidths):
        """Given a list of column widths in pixels, convert to a list
        of column widths in percents.
        """
        total = sum(colwidths)
        return [float(width) / float(total) for width in self.curr_colwidths_px]

    def xwrite(self, path_and_value):
        """Use the xwrite form."""
        cmd = "wmiir xwrite %s" % path_and_value
        print cmd
        os.system(cmd)

    def read(self, path):
        """Return a list of the lines returned by "wmii read path" """
        return os.popen4("wmiir read " + path)[1].readlines()

    def swap_with_previous(self, alist, index):
        alist[index], alist[index - 1] = alist[index - 1], alist[index]
        return alist

    def swap_with_next(self, alist, index):
        alist[index], alist[index + 1] = alist[index + 1], alist[index]
        return alist


if __name__ == "__main__":
    main()
