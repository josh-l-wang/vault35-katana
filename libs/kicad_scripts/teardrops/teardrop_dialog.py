#!/usr/bin/env python

# Teardrop for pcbnew using filled zones
# This is the plugin WX dialog
# (c) Niluje 2019 thewireddoesntexist.org
#
# Based on Teardrops for PCBNEW by svofski, 2014 http://sensi.org/~svo
# Cubic Bezier upgrade by mitxela, 2021 mitxela.com

import wx
import pcbnew
import os
import time

from .teardrop_gui import teardrop_gui
from .td import SetTeardrops, RmTeardrops, __version__

class TeardropDialog(teardrop_gui):
    """Class that gathers all the Gui control"""

    def __init__(self, board):
        """Init the brand new instance"""
        super(TeardropDialog, self).__init__(None)
        self.board = board
        self.SetTitle("Teardrops (v{0})".format(__version__))
        self.rbx_action.Bind(wx.EVT_RADIOBOX, self.onAction)
        self.Bind(wx.EVT_CLOSE, self.onCloseWindow)
        self.but_cancel.Bind(wx.EVT_BUTTON, self.onCloseWindow)
        self.but_ok.Bind(wx.EVT_BUTTON, self.onProcessAction)
        self.m_bitmap_help.SetBitmap(wx.Bitmap( os.path.join(os.path.dirname(os.path.realpath(__file__)), "rcs", "teardrops-help.png") ) )
        self.SetMinSize(self.GetSize())

    def onAction(self, e):
        """Enables or disables the parameters/options elements"""
        els = [self.st_hpercent, self.sp_hpercent, self.st_vpercent,
               self.sp_vpercent, self.st_nbseg, self.sp_nbseg,
               self.cb_include_smd_pads, self.cb_discard_in_same_zone,
               self.cb_follow_tracks, self.cb_no_bulge]
        for i, el in enumerate(els):
            if self.rbx_action.GetSelection() == 0:
                el.Enable()
            else:
                el.Disable()

    def onProcessAction(self, event):
        """Executes the requested action"""
        if self.rbx_action.GetSelection() == 0:
            start = time.time()
            count = SetTeardrops(self.sp_hpercent.GetValue(),
                                 self.sp_vpercent.GetValue(),
                                 self.sp_nbseg.GetValue(),
                                 self.board,
                                 self.cb_include_smd_pads.IsChecked(),
                                 self.cb_discard_in_same_zone.IsChecked(),
                                 self.cb_follow_tracks.IsChecked(),
                                 self.cb_no_bulge.IsChecked())
            wx.MessageBox("{} Teardrops inserted, took {:.3f} seconds".format(count, time.time()-start))
        else:
            count = RmTeardrops(pcb=self.board)
            wx.MessageBox("{0} Teardrops removed".format(count))
        pcbnew.Refresh() #Show up newly added vias
        self.EndModal(wx.ID_OK)

    def onCloseWindow(self, event):
        self.EndModal(wx.ID_OK)


def InitTeardropDialog(board):
    """Launch the dialog"""
    tg = TeardropDialog(board)
    tg.ShowModal()
    tg.Destroy()
