/* 
 * File:   tester_tools.c
 * Author: AutonomousSystemsLab
 *
 * Created on July 20, 2018, 11:36 AM
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "_cruzID.h"
#include <GenericTypeDefs.h>

#ifndef CRUZID
#define CRUZID "STAFF TEST"
#endif

#include "autotest_tools.h"

int subtestsPassed;
int totalSubtests;

double scoreAwarded = 0;
double totalScore = 0;

static char module_name_static[100];
static char subtest_name_static[100];

void printHeader(char * module_name)
{
    printf("\n\n### %s Results ####\n", module_name);
    printf("Testing:    %s\n", CRUZID);
    strcpy(module_name_static, module_name);
#ifdef AUTOGRADER
    printf("This output was auto-compiled and auto-run.\n");
#endif
}

void printFooter(void)
{
    printf("\n completed autotesting for %s, %s\n", CRUZID,module_name_static);
    printf("DONE\n");
}

void printSeedMessage(unsigned int randSeed)
{
    printf("This test used a random seed = %d\n", randSeed);
    srand(randSeed);
}

void startSubtestRun(char * subtest_name)
{
    printf("\nBEGINNING %s:\n", subtest_name);
    subtestsPassed = 0;
    totalSubtests = 0;
    strcpy(subtest_name_static, subtest_name);
}

int subtestResult(int boolean, char * subtest_name)
{
    char * result = "FAILED";
    int pass = FALSE;
    if (boolean) {
        result = "passed";
        subtestsPassed++;
        pass = TRUE;
    }
    printf("   %s : %s\n", subtest_name, result);
    totalSubtests++;
    return pass;
}

double endSubtestRun(double points_for_test)
{
    printf("Total passed:  %d / %d\n", subtestsPassed, totalSubtests);
    
    double points_awarded = (double) subtestsPassed / totalSubtests;
    //we want them to reach for full completion, so we square the result:
    points_awarded = points_awarded * points_awarded * points_for_test;

    printf("SUBSCORE: %s > %4.2f / %4.2f\n",
            subtest_name_static,
            points_awarded, 
            points_for_test);
    totalScore += points_for_test;
    scoreAwarded += points_awarded;

    return points_awarded;
}

void printTotalScore(void)
{
    printf("\n\nTOTAL for %s: %4.2f / %4.2f\n", module_name_static, scoreAwarded, totalScore);
}

