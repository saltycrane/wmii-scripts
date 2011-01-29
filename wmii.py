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
    def __init__(self):
        pass

    def set_column_widths(self, width0, width1):
        """Use the 'grow' command to set the column widths to those specified.
        Widths are specified in percentages.
        Currently only works with 2 columns.
        """
        self.determine_pixels_per_grow_horiz()
        new_width0 = sum(self.curr_colwidths) * (float(width0) /
                                                 (float(width0)+float(width1)))
        grow_amount = int(round((new_width0-self.curr_colwidths[0]) /
                                self.pixels_per_grow_increment))
        self.xwrite("/tag/sel/ctl grow 1 1 right %d" % grow_amount)

    def determine_pixels_per_grow_horiz(self):
        """Try growing by an increment of 1 and record the number of pixels changed.
        """
        self.read_current_col_widths()
        prev_colwidth0 = self.curr_colwidths[0]
        self.xwrite("/tag/sel/ctl grow 1 1 right 1")
        self.read_current_col_widths()
        self.pixels_per_grow_increment = self.curr_colwidths[0] - prev_colwidth0

    def read_current_col_widths(self):
        """'wmiir read /tag/sel/index' and set the attribute, self.curr_colwidths.
        self.curr_colwidths is a list of the width (ints) (in pixels) of each
        column in the view.
        """
        lines = self.read("/tag/sel/index")
        self.curr_colwidths = []
        for line in lines:
            match = re.search(r"# [^~]+ \d+ (\d+)", line)
            if match:
                self.curr_colwidths.append(int(match.group(1)))
        print self.curr_colwidths

    def read_current_column_number(self):
        """'wmiir read /tag/sel/ctl' and set the attribute, self.curr_col."""
        lines = self.read("/tag/sel/ctl")
        self.curr_col = re.split(" ", lines[1])[1]
        print "curr_col = %s" % self.curr_col

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
    w.set_column_widths(sys.argv[1], sys.argv[2])
