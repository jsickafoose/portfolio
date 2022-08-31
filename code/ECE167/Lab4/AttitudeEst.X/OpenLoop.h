/* 
 * File:   OpenLoop.h
 * Author: kyleg
 *
 * Created on May 24, 2022, 1:51 PM
 */

#ifndef OPENLOOP_H
#define	OPENLOOP_H

//Inputs: Previous attitute DCM (R)
//         Body Fixed Rotation rates gyros ([p;q;r]) in rad/s
//         Time between samples (dT) in seconds

// Outputs: New DCM (Rnew)
void IntegrateOpenLoop(float R[2][2],float gyros,float dT);