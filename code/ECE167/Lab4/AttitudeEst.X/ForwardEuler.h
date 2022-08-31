/* 
 * File:   ForwardEuler.h
 * Author: kyleg
 *
 * Created on May 23, 2022, 2:53 PM
 */

#ifndef FORWARDEULER_H
#define	FORWARDEULER_H

// Computes new DCM using forward integration, stores into Rnew
void ForwardEuler(float Rnew[3][3], float R[3][3], float dT,float p, float q, float r);

//Computes new DCM using matrix exponential, stores into Rnew
void MatrixExponential(float Rnew[3][3], float R[3][3], float dT,float p, float q, float r);

#endif