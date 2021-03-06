/*! \file EKF_15state.c
 *	\brief 15 state EKF navigation filter
 *
 *	\details  15 state EKF navigation filter using loosely integrated INS/GPS architecture.
 * 	Time update is done after every IMU data acquisition and GPS measurement
 * 	update is done every time the new data flag in the GPS data packet is set. Designed by Adhika Lie.
 *	Attitude is parameterized using quaternions.
 *	Estimates IMU bias errors.
 *	\ingroup nav_fcns
 *
 * \author University of Minnesota
 * \author Aerospace Engineering and Mechanics
 * \copyright Copyright 2011 Regents of the University of Minnesota. All rights reserved.
 *
 */

#ifndef NAV_15STATE_MAG_HXX
#define NAV_15STATE_MAG_HXX


#include <math.h>
#include <eigen3/Eigen/Core>
#include <eigen3/Eigen/Geometry>
#include <eigen3/Eigen/LU>
using namespace Eigen;

#include "../core/structs.hxx"

// usefule constants
const double g = 9.814;
const double D2R = M_PI / 180.0;

// define some types for notational convenience and consistency
typedef Matrix<double,9,9>   Matrix9d;
typedef Matrix<double,12,12> Matrix12d;
typedef Matrix<double,15,15> Matrix15d;
typedef Matrix<double,9,15>  Matrix9x15d;
typedef Matrix<double,15,9>  Matrix15x9d;
typedef Matrix<double,15,12> Matrix15x12d;
typedef Matrix<double,9,1>   Vector9d;
typedef Matrix<double,15,1>  Vector15d;

class EKF15mag {

public:

    EKF15mag() {
	default_config();
    }
    ~EKF15mag() {}

    // set/get error characteristics of navigation sensors
    void set_config(NAVconfig config);
    NAVconfig get_config();
    void default_config();

    // main interface
    NAVdata init(IMUdata imu, GPSdata gps);
    NAVdata update(IMUdata imu, GPSdata gps);
    
private:

    Matrix15d F, PHI, P, Qw, Q, ImKH, KRKt, I15 /* identity */;
    Matrix15x12d G;
    Matrix15x9d K;
    Vector15d x;
    Matrix12d Rw;
    Matrix9x15d H;
    Matrix9d R;
    Vector9d y;
    Matrix3d C_N2B, C_B2N, I3 /* identity */, temp33;
    Vector3d grav, f_b, om_ib, nr, pos_ins_ecef, pos_ins_ned, pos_gps, pos_gps_ecef, pos_gps_ned, dx, mag_ned;

    Quaterniond quat;
    double denom, Re, Rn;
    double tprev;

    NAVconfig config;
    NAVdata nav;
};


#endif // NAV_15STATE_MAG_HXX
