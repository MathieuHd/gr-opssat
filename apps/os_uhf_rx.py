#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: OPS-SAT UHF RX
# Author: Fischer Benjamin, Mladenov Tom
# Description: UHF RX application for offset sampling and doppler compensation (GPredict)
# GNU Radio version: 3.10.8.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import analog
from gnuradio import blocks
from gnuradio import blocks, gr
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import soapy
from gnuradio import zeromq
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import gpredict
import sip



class os_uhf_rx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "OPS-SAT UHF RX", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("OPS-SAT UHF RX")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "os_uhf_rx")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.signal_freq = signal_freq = 437.2e6
        self.true_freq = true_freq = signal_freq
        self.samp_rate = samp_rate = 250e3
        self.offset_freq = offset_freq = -40e3
        self.doppler_freq = doppler_freq = true_freq - signal_freq
        self.variable_low_pass_filter_taps_0 = variable_low_pass_filter_taps_0 = firdes.low_pass(1.0, samp_rate, 25000,1000, window.WIN_HAMMING, 6.76)
        self.samp_rate_down = samp_rate_down = 57.6e3
        self.rtl_gain = rtl_gain = 20
        self.freq_tuned = freq_tuned = offset_freq - doppler_freq
        self.Squelch = Squelch = -130

        ##################################################
        # Blocks
        ##################################################

        self._rtl_gain_range = Range(0, 49.6, 1, 20, 200)
        self._rtl_gain_win = RangeWidget(self._rtl_gain_range, self.set_rtl_gain, "'rtl_gain'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._rtl_gain_win)
        self._Squelch_range = Range(-180, -0, 1, -130, 200)
        self._Squelch_win = RangeWidget(self._Squelch_range, self.set_Squelch, "'Squelch'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._Squelch_win)
        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:5555', 100, False, (-1), '', True, True)
        self.soapy_rtlsdr_source_0 = None
        dev = 'driver=rtlsdr'
        stream_args = 'bufflen=16384'
        tune_args = ['']
        settings = ['']

        def _set_soapy_rtlsdr_source_0_gain_mode(channel, agc):
            self.soapy_rtlsdr_source_0.set_gain_mode(channel, agc)
            if not agc:
                  self.soapy_rtlsdr_source_0.set_gain(channel, self._soapy_rtlsdr_source_0_gain_value)
        self.set_soapy_rtlsdr_source_0_gain_mode = _set_soapy_rtlsdr_source_0_gain_mode

        def _set_soapy_rtlsdr_source_0_gain(channel, name, gain):
            self._soapy_rtlsdr_source_0_gain_value = gain
            if not self.soapy_rtlsdr_source_0.get_gain_mode(channel):
                self.soapy_rtlsdr_source_0.set_gain(channel, gain)
        self.set_soapy_rtlsdr_source_0_gain = _set_soapy_rtlsdr_source_0_gain

        def _set_soapy_rtlsdr_source_0_bias(bias):
            if 'biastee' in self._soapy_rtlsdr_source_0_setting_keys:
                self.soapy_rtlsdr_source_0.write_setting('biastee', bias)
        self.set_soapy_rtlsdr_source_0_bias = _set_soapy_rtlsdr_source_0_bias

        self.soapy_rtlsdr_source_0 = soapy.source(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)

        self._soapy_rtlsdr_source_0_setting_keys = [a.key for a in self.soapy_rtlsdr_source_0.get_setting_info()]

        self.soapy_rtlsdr_source_0.set_sample_rate(0, samp_rate)
        self.soapy_rtlsdr_source_0.set_frequency(0, (signal_freq + offset_freq))
        self.soapy_rtlsdr_source_0.set_frequency_correction(0, 32)
        self.set_soapy_rtlsdr_source_0_bias(bool(False))
        self._soapy_rtlsdr_source_0_gain_value = rtl_gain
        self.set_soapy_rtlsdr_source_0_gain_mode(0, bool(False))
        self.set_soapy_rtlsdr_source_0_gain(0, 'TUNER', rtl_gain)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=int(samp_rate_down),
                decimation=int(samp_rate),
                taps=[],
                fractional_bw=0)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(0.1)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.gpredict_doppler_1_0 = gpredict.doppler('localhost', 4532, True)
        self.gpredict_MsgPairToVar_0 = gpredict.MsgPairToVar(self.set_true_freq)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, variable_low_pass_filter_taps_0, (-freq_tuned), samp_rate)
        self.blocks_message_debug_0 = blocks.message_debug(True, gr.log_levels.info)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, '/home/mathieu/Documents/gr-opssat/recordings/self.cf32', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.analog_simple_squelch_cc_0 = analog.simple_squelch_cc(Squelch, 1)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.gpredict_doppler_1_0, 'freq'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.gpredict_doppler_1_0, 'freq'), (self.gpredict_MsgPairToVar_0, 'inpair'))
        self.connect((self.analog_simple_squelch_cc_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.analog_simple_squelch_cc_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.zeromq_pub_sink_0, 0))
        self.connect((self.soapy_rtlsdr_source_0, 0), (self.analog_simple_squelch_cc_0, 0))
        self.connect((self.soapy_rtlsdr_source_0, 0), (self.blocks_file_sink_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "os_uhf_rx")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_signal_freq(self):
        return self.signal_freq

    def set_signal_freq(self, signal_freq):
        self.signal_freq = signal_freq
        self.set_doppler_freq(self.true_freq - self.signal_freq)
        self.set_true_freq(self.signal_freq)
        self.soapy_rtlsdr_source_0.set_frequency(0, (self.signal_freq + self.offset_freq))

    def get_true_freq(self):
        return self.true_freq

    def set_true_freq(self, true_freq):
        self.true_freq = true_freq
        self.set_doppler_freq(self.true_freq - self.signal_freq)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_variable_low_pass_filter_taps_0(firdes.low_pass(1.0, self.samp_rate, 25000, 1000, window.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.soapy_rtlsdr_source_0.set_sample_rate(0, self.samp_rate)

    def get_offset_freq(self):
        return self.offset_freq

    def set_offset_freq(self, offset_freq):
        self.offset_freq = offset_freq
        self.set_freq_tuned(self.offset_freq - self.doppler_freq)
        self.soapy_rtlsdr_source_0.set_frequency(0, (self.signal_freq + self.offset_freq))

    def get_doppler_freq(self):
        return self.doppler_freq

    def set_doppler_freq(self, doppler_freq):
        self.doppler_freq = doppler_freq
        self.set_freq_tuned(self.offset_freq - self.doppler_freq)

    def get_variable_low_pass_filter_taps_0(self):
        return self.variable_low_pass_filter_taps_0

    def set_variable_low_pass_filter_taps_0(self, variable_low_pass_filter_taps_0):
        self.variable_low_pass_filter_taps_0 = variable_low_pass_filter_taps_0
        self.freq_xlating_fir_filter_xxx_0.set_taps(self.variable_low_pass_filter_taps_0)

    def get_samp_rate_down(self):
        return self.samp_rate_down

    def set_samp_rate_down(self, samp_rate_down):
        self.samp_rate_down = samp_rate_down

    def get_rtl_gain(self):
        return self.rtl_gain

    def set_rtl_gain(self, rtl_gain):
        self.rtl_gain = rtl_gain
        self.set_soapy_rtlsdr_source_0_gain(0, 'TUNER', self.rtl_gain)

    def get_freq_tuned(self):
        return self.freq_tuned

    def set_freq_tuned(self, freq_tuned):
        self.freq_tuned = freq_tuned
        self.freq_xlating_fir_filter_xxx_0.set_center_freq((-self.freq_tuned))

    def get_Squelch(self):
        return self.Squelch

    def set_Squelch(self, Squelch):
        self.Squelch = Squelch
        self.analog_simple_squelch_cc_0.set_threshold(self.Squelch)




def main(top_block_cls=os_uhf_rx, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
