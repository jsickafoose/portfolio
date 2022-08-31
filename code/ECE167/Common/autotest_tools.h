/* 
 * File:   tester_tools.h
 * Author: AutonomousSystemsLab
 *
 * Created on July 20, 2018, 11:37 AM
 */

#ifndef TESTER_TOOLS_H
#define	TESTER_TOOLS_H

//settings:
#define TEST_ALIGN 0 //control the left-spacing of test printout

// Macros:
#ifndef FP_DELTA
#define FP_DELTA 0.0001
#endif

#ifndef GRADER_MODE
#define g_printf(...)
#else
#define g_printf(...) printf("      >>> " __VA_ARGS__)
#endif

#define equal_within_fp_delta(a,b) ( (a-b < FP_DELTA) && (b-a) < FP_DELTA)

void printHeader(char * module_name);
void printFooter(void);

void startSubtestRun(char * test_name);
int subtestResult(int boolean, char * test_name);
double endSubtestRun(double points_for_test);
void printTotalScore(void);

void printSeedMessage(unsigned int seed);

#endif	/* TESTER_TOOLS_H */

