// ForwardEuler.c
// Performs forward integration using 1) simple forward integration, 
// 2) matrix exponential form
// Lab 4
#include "MatrixMath.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include "BOARD.h"

//Cutoff in rad/s for rate when calculating matrix exponential
#define CUTOFF 0.2
// identity matrix

void ForwardEuler(float Rnew[3][3], float R[3][3], float dT, float p, float q, float r){
    float Rdot[3][3]; // Derivative of DCM
    float RT[3][3]; // For storing the matrix from multiplying Rdot by dT
    
    // Initialize skew symmetric matrix with given rotation rates p,q,r
    float wx[3][3] = {{0, -r, q},
                      {r, 0, -p},
                      {-q, p, 0}};
    
    // Differential equation for propagating DCM
    MatrixMultiply(wx,R,Rdot); 
    // Turn Rdot negative
    MatrixScalarMultiply(-1, Rdot, Rdot); 
    
    // Multiply dT and Rdot together
    MatrixScalarMultiply(dT, Rdot, RT);
    
    // Add the result with the Rk to get Rk+1
    MatrixAdd(R,RT,Rnew);
    
}

void MatrixExponential(float Rnew[3][3], float R[3][3], float dT,float p, float q, float r){
    // Declare identity matrix
    float I[3][3] = {{1, 0, 0},
                     {0, 1, 0},
                     {0, 0, 1}};
    
    float wx2[3][3]; // Declare Squared skew symmetrix matrix
    
    float Mexp[3][3]; //Declare matrix exponential
    float Mterm1[3][3]; // First matrix term for calculating matrix exponential
    float Mterm2[3][3]; // second matrix term for calculating matrix exponential
    float Mterm3[3][3]; // Third matrix term for calculating matrix exponential
    
    float sinterm = 0;
    float costerm = 0;
    
    // Initialize skew symmetric matrix with given rotation rates p,q,r
    float wx[3][3] = {{0, -r, q},
                      {r, 0, -p},
                      {-q, p, 0}};
    // Create squared skew symmetric matrix
    MatrixMultiply(wx,wx,wx2);  
    
    float w2norm = sqrt(p*p + q*q + r*r);
    
    // Use MacLauren series expansion when less than cutoff (0.2) rotation
    if(w2norm <= CUTOFF){
        sinterm = dT - ((dT*dT*dT)*(w2norm*w2norm)/6) + ((dT*dT*dT*dT*dT)*(w2norm*w2norm*w2norm*w2norm)/120);
        costerm = (dT*dT)/2 - ((dT*dT*dT*dT)*(w2norm*w2norm)/24) + ((dT*dT*dT*dT*dT*dT)*(w2norm*w2norm*w2norm*w2norm)/720);
    }
    // Else calculate terms as normal
    else{
        sinterm = sin(w2norm * dT)/w2norm;    
        costerm = (1-cos(w2norm*dT))/(w2norm*w2norm);             
    }
    // Multiply these terms by the skew symmetric matrix
    MatrixScalarMultiply(sinterm, wx, Mterm1);
    MatrixScalarMultiply(costerm, wx2, Mterm2);
    
    // Add sin and cosine term together into new matrix
    MatrixAdd(Mterm1, Mterm2, Mterm3);
    // Convert new matrix negative to add to identity matrix
    MatrixScalarMultiply(-1, Mterm3, Mterm3); 
    // Subtract from identity matrix to produce matrix exponential
    MatrixAdd(I, Mterm3, Mexp);
    // Multiply matrix exponential and DCM to produce new DCM
    MatrixMultiply(Mexp, R, Rnew);
}