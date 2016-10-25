import numpy as np
import os
import sys

import pydefs

sys.path.append('../build/src/nav_core/.libs/')
sys.path.append('../build/src/nav_openloop/.libs/')
import libnav_core
import libnav_openloop

class filter():
    def __init__(self):
        self.ekf = libnav_openloop.OpenLoop()
        self.name = 'Open Loop'
        self.filter_sync = 0.0

    def python2c(self, imu, gps):
        cimu = libnav_core.IMUdata()
        cimu.time = imu.time
        cimu.p = imu.p
        cimu.q = imu.q
        cimu.r = imu.r
        cimu.ax = imu.ax
        cimu.ay = imu.ay
        cimu.az = imu.az
        cimu.hx = imu.hx
        cimu.hy = imu.hy
        cimu.hz = imu.hz
        
        cgps = libnav_core.GPSdata()
        cgps.time = gps.time
        cgps.tow = gps.tow
        cgps.newData = gps.newData
        cgps.vn = gps.vn
        cgps.ve = gps.ve
        cgps.vd = gps.vd
        cgps.lat = gps.lat
        cgps.lon = gps.lon
        cgps.alt = gps.alt

        return cimu, cgps

    def c2python(self, cnav):
        P = np.diag([cnav.Pp0, cnav.Pp1, cnav.Pp2,
                     cnav.Pv0, cnav.Pv1, cnav.Pv2,
                     cnav.Pa0, cnav.Pa1, cnav.Pa2,
                     cnav.Pabx, cnav.Paby, cnav.Pabz,
                     cnav.Pgbx, cnav.Pgby, cnav.Pgbz])
        stateInnov = np.nan*np.ones(6)
        insgps = pydefs.INSGPS(1, # fixme: valid/init
                               cnav.time,
                               [cnav.lat, cnav.lon, cnav.alt],
                               [cnav.vn, cnav.ve, cnav.vd],
                               [cnav.psi, cnav.the, cnav.phi],
                               [cnav.abx, cnav.aby, cnav.abz],
                               [cnav.gbx, cnav.gby, cnav.gbz],
                               P,
                               stateInnov)
        return insgps
    
    def init(self, imu, gps, filt):
        self.ekf.init(filt.lat, filt.lon, filt.alt,
                      filt.vn, filt.ve, filt.vd,
                      filt.phi, filt.the, filt.psi)
        cimu, cgps = self.python2c(imu, gps)
        cnav = self.ekf.update(cimu)
        return self.c2python(cnav)

    def update(self, imu, gps, filt):
        cimu, cgps = self.python2c(imu, gps)
        if filt.time > self.filter_sync + 300:
            print 'resync:', filt.time
            self.filter_sync = filt.time
            return self.init(imu, gps, filt)
        else:
            cnav = self.ekf.update(cimu)
        return self.c2python(cnav)

    def close(self):
        pass