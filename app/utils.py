# -*- coding: utf-8 -*-

import fractions

import numpy
import scipy.signal


class FilterFunction(object):
    def __init__(self, b, a, wp, btype, shift):
        self._b = b
        self._a = a
        wp = numpy.atleast_1d(wp)
        if len(wp) > 1 and btype.lower() not in {'bs', 'bandstop', 'bands', 'stop', 'bandstop'}:
            shiftfreq = numpy.average(wp)
        else:
            shiftfreq = 0.0

        if shift:
            self._shift = int(numpy.round(scipy.signal.group_delay((b, a), [shiftfreq], fs=2.0)[1]))
        else:
            self._shift = 0

        self.phase_shift = (numpy.angle(
            scipy.signal.freqz(b, a, worN=[shiftfreq], fs=2.0)[1][0]) + self._shift * numpy.pi * shiftfreq) % (
                                   2.0 * numpy.pi)

    def __call__(self, x):
        if self._shift == 0:
            return scipy.signal.lfilter(self._b, self._a, x)
        elif self._shift > 0:
            return scipy.signal.lfilter(self._b, self._a, numpy.concatenate((x, x[-1] * numpy.ones(self._shift))))[
                   self._shift:]
        else:
            return scipy.signal.lfilter(self._b, self._a, numpy.concatenate((x[0] * numpy.ones(-self._shift), x)))[
                   :self._shift]


def iirfilter(N, Wn, rp=None, rs=None, btype='band', ftype='butter', shift=True):
    b, a = scipy.signal.iirfilter(N, Wn, rp, rs, btype, ftype=ftype)
    return FilterFunction(b, a, Wn, btype, shift)


def iirdesign(wp, ws, gpass, gstop, ftype='butter', shift=True):
    smallest = numpy.nextafter(0.0, 1.0)
    largest = numpy.nextafter(1.0, 0.0)
    b, a = scipy.signal.iirdesign(numpy.maximum(wp, smallest), numpy.minimum(ws, largest), gpass, gstop, ftype=ftype)
    btype = 'band'
    if len(numpy.atleast_1d(wp)) > 1 and len(numpy.atleast_1d(ws)) > 1 and ws[0] > wp[0]:
        btype = 'bandstop'
    return FilterFunction(b, a, wp, btype, shift)


def iirdesign_wc(wc, wp, ws, gpass, gstop, ftype='butter', shift=True):
    return iirdesign([wc - wp, wc + wp], [wc - ws, wc + ws], gpass, gstop, ftype, shift)


def iirsplitter(wc, wp, ws, gpass, gstop, ftype='butter', shift=True):
    def invert_db(db):
        return -(20.0 * numpy.log10(1.0 - 10.0 ** (-db / 20.0)))

    bpass = iirdesign_wc(wc, wp, ws, gpass, gstop, ftype, shift)
    bstop = iirdesign_wc(wc, ws, wp, invert_db(gstop), invert_db(gpass), ftype, shift)
    return bpass, bstop

def start_phase(frame, line, fsc):
    reference_line = min(21, 283)
    frame %= fractions.Fraction(fsc / (30000.0 / 1001.0)).limit_denominator().denominator
    frame_shift = (frame * (2.0 * numpy.pi * ((fsc / (30000.0 / 1001.0)) % 1.0))) % (2.0 * numpy.pi)
    line_shift = 2.0 * numpy.pi * ((fsc / ((30000.0 / 1001.0) * 525)) % 1.0)

    line_shift = ((analog_line(line) - reference_line) * line_shift) % (2.0 * numpy.pi)
    return (frame_shift + line_shift) % (2.0 * numpy.pi)

def analog_line(digital_line):
    adjusted = digital_line
    if adjusted % 2 == 0:
        return 283 + adjusted // 2
    else:
        return 21 + adjusted // 2