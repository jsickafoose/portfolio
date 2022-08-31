#include "MatrixMath.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
    
//counter for rows
int x;
//counter for columns
int y;
float counter; //just to keep track of things

//test equality of two 3 by 3 matricies
//returns 1 if true, 0 if false

void MatrixMultiply(float a[3][3], float b[3][3], float c[3][3])
{
    for (x = 0; x < 3; x++) {
        for (y = 0; y < 3; y++) {
            counter = 0; //start the counter at zero
            counter += (a[x][0] * b[0][y]);
            counter += (a[x][1] * b[1][y]);
            counter += (a[x][2] * b[2][y]);

            c[x][y] = counter;
        }

    }
}
//adds two 3 by 3 matrices together, self-explanatory

void MatrixAdd(float a[3][3], float b[3][3], float c[3][3])
{
    for (x = 0; x < 3; x++) {
        for (y = 0; y < 3; y++) {
            c[x][y] = a[x][y] + b[x][y];
        }

    }
}

//multiplies a 3 by 3 matrix by a scalar
//s is the scalar

void MatrixScalarMultiply(float s, float a[3][3], float b[3][3])
{
    for (x = 0; x < 3; x++) {
        for (y = 0; y < 3; y++) {
            b[x][y] += 0;
            b[x][y] = (s * a[x][y]);
        }

    }
}

//adds a 3 by 3 matrix with a scalar
//x is the scalar

void MatrixScalarAdd(float s, float a[3][3], float b[3][3])
{
    for (x = 0; x < 3; x++) {
        for (y = 0; y < 3; y++) {
            b[x][y] = (0.0 + s + a[x][y]);
        }

    }
}

//calculates the cross product, or determinant, of a 3 by 3 matrix
//formula for a cross product 
// a11[(a22*a33)-(a23*a32)] - a12[(a21*a33)-(a23*a31)] + a13[(a21*a32)-(a22*a31)]
// arrays start at zero so subtract 1 from every subscript

float MatrixDeterminant(float a[3][3])
{
    counter = 0.0;
    counter += ((a[1][1] * a[2][2])-(a[1][2] * a[2][1])) * a[0][0];
    counter -= ((a[1][0] * a[2][2])-(a[1][2] * a[2][0])) * a[0][1];
    counter += ((a[1][0] * a[2][1])-(a[1][1] * a[2][0])) * a[0][2];
    return counter;
}

//calculates the trace of a matrix,
//which is just the sum of the elements in a top-left to bottom-right diagonal

float MatrixTrace(float a[3][3])
{
    counter = 0;
    for (x = 0; x < 3; x++) {
        counter += a[x][x];
    }
    return counter;
}

//Transpose the matrix into the output matrix
//flip the columns and rows, is all it really does

void MatrixTranspose(float a[3][3], float b[3][3])
{
    float c[3][3];
    //setting matrix c equal to a, just in case the two arguments are the same matrix
    for (x = 0; x < 3; x++) {
        for (y = 0; y < 3; y++) {
            c[x][y] = a[x][y];
        }
    }
    //flip the rows and columns, referencing only the copied matrix, c
    for (x = 0; x < 3; x++) {
        for (y = 0; y < 3; y++) {
            b[x][y] = c[y][x]; //flip the rows and columns
        }
    }
}

//Matrix Inverse function
//returns the same matrix if determinant is zero (not invertable)

void MatrixInverse(float a[3][3], float b[3][3])
{
    float c[3][3];
    //setting matrix c equal to a, just in case the two arguments are the same matrix
    for (x = 0; x < 3; x++) {
        for (y = 0; y < 3; y++) {
            c[x][y] = a[x][y];
        }
    }

    //actual function stuff now
    float det = MatrixDeterminant(c);
    //do nothing if the determinant is zero
    if (det != 0) {
        //not very fun calculations
        b[0][0] = (c[1][1] * c[2][2]) - (c[1][2] * c[2][1]);
        b[0][1] = (c[0][2] * c[2][1]) - (c[0][1] * c[2][2]);
        b[0][2] = (c[0][1] * c[1][2]) - (c[0][2] * c[1][1]);

        b[1][0] = (c[1][2] * c[2][0]) - (c[1][0] * c[2][2]);
        b[1][1] = (c[0][0] * c[2][2]) - (c[0][2] * c[2][0]);
        b[1][2] = (c[0][2] * c[1][0]) - (c[0][0] * c[1][2]);

        b[2][0] = (c[1][0] * c[2][1]) - (c[1][1] * c[2][0]);
        b[2][1] = (c[0][1] * c[2][0]) - (c[0][0] * c[2][1]);
        b[2][2] = (c[0][0] * c[1][1]) - (c[0][1] * c[1][0]);
        
        //multiply by the determinant
        MatrixScalarMultiply(1.0 / det, b, b);
    }
}
//prints the contents of a 3 by 3 matrix into a nice little grid

void MatrixPrint(float a[3][3])
{
    for (x = 0; x < 3; x++) {
        printf("\n | ");
        for (y = 0; y < 3; y++) {
            printf("%f, ", (double) a[x][y]); //cast to double so we don't get stinky error messages
        }
        printf(" | ");
    }
    printf("\n"); //new lines to make it look nicer
}
