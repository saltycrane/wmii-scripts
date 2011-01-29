#!/usr/bin/env python

import os
import re
import sys


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
            total_width_px = float(sum(self.curr_colwidths))
            new_width_px = float(width_perc) / total_width_perc * total_width_px
            grow_amount_px = int(round(new_width_px - self.curr_colwidths[i]))
            self.xwrite("/tag/sel/ctl grow %d 1 right %dpx" % (i + 1, grow_amount_px))

    def read_current_col_widths(self):
        """'wmiir read /tag/sel/index' and set the attribute, self.curr_colwidths.
        self.curr_colwidths is a list of the width (ints) (in pixels) of each
        column in the view.
        """
        lines = self.read("/tag/sel/index")
        self.curr_colwidths = []
        for line in lines:
            match = re.search(r"# [^~:]+ \d+ (\d+)", line)
            if match:
                self.curr_colwidths.append(int(match.group(1)))
        print self.curr_colwidths

    def xwrite(self, path_and_value):
        """Use the xwrite form."""
        cmd = "wmiir xwrite %s" % path_and_value
        print cmd
        os.system(cmd)

    def read(self, path):
        """Return a list of the lines returned by "wmii read path" """
        return os.popen4("wmiir read " + path)[1].readlines()


if __name__ == "__main__":
    w = Wmii()
    w.set_column_widths(sys.argv[1:])
