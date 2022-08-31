/* 
 * File:   MatrixMath.h
 * Author: kyleg
 *
 * Created on May 22, 2022, 6:42 PM
 */

#ifndef MATRIXMATH_H
#define	MATRIXMATH_H

// Multiples matrices together
void MatrixMultiply(float a[3][3], float b[3][3], float c[3][3]);

//adds two 3 by 3 matrices together, self-explanatory

void MatrixAdd(float a[3][3], float b[3][3], float c[3][3]);

//multiplies a 3 by 3 matrix by a scalar
//s is the scalar

void MatrixScalarMultiply(float s, float a[3][3], float b[3][3]);

//adds a 3 by 3 matrix with a scalar
//x is the scalar

void MatrixScalarAdd(float s, float a[3][3], float b[3][3]);

//calculates the cross product, or determinant, of a 3 by 3 matrix
//formula for a cross product 
// a11[(a22*a33)-(a23*a32)] - a12[(a21*a33)-(a23*a31)] + a13[(a21*a32)-(a22*a31)]
// arrays start at zero so subtract 1 from every subscript

float MatrixDeterminant(float a[3][3]);


//calculates the trace of a matrix,
//which is just the sum of the elements in a top-left to bottom-right diagonal

float MatrixTrace(float a[3][3]);


//Transpose the matrix into the output matrix
//flip the columns and rows, is all it really does

void MatrixTranspose(float a[3][3], float b[3][3]);

//Matrix Inverse function
//returns the same matrix if determinant is zero (not invertable)

void MatrixInverse(float a[3][3], float b[3][3]);


   
//prints the contents of a 3 by 3 matrix into a nice little grid

void MatrixPrint(float a[3][3]);

#endif
