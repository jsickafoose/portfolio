

#ifndef FEEDBACKCONTROL_H
#define	FEEDBACKCONTROL_H

/*******************************************************************************
 * PUBLIC #DEFINES                                                            *
 ******************************************************************************/
#define FEEDBACK_MAXOUTPUT_POWER 27

/*******************************************************************************
 * PUBLIC DATATYPES
 ******************************************************************************/



/*******************************************************************************
 * PUBLIC FUNCTIONS                                                           *
 ******************************************************************************/

/**
 * @Function FeedbackControl_Init(void)
 * @param None
 * @return SUCCESS or ERROR
 * @brief initializes the controller to the default values and (P,I,D)->(1, 0, 0)*/
int FeedbackControl_Init(void);

/**
 * @Function FeedbackControl_SetProportionalGain(int newGain);
 * @param newGain, integer proportional gain
 * @return SUCCESS or ERROR
 * @brief sets the new P gain for controller */
int FeedbackControl_SetProportionalGain(int newGain);

/**
 * @Function FeedbackControl_SetIntegralGain(int newGain);
 * @param newGain, integer integral gain
 * @return SUCCESS or ERROR
 * @brief sets the new I gain for controller */
int FeedbackControl_SetIntegralGain(int newGain);

/**
 * @Function FeedbackControl_SetDerivativeGain(int newGain);
 * @param newGain, integer derivative gain
 * @return SUCCESS or ERROR
 * @brief sets the new D gain for controller */
int FeedbackControl_SetDerivativeGain(int newGain);

/**
 * @Function FeedbackControl_GetPorportionalGain(void)
 * @param None
 * @return Proportional Gain
 * @brief retrieves requested gain */
int FeedbackControl_GetProportionalGain(void);

/**
 * @Function FeedbackControl_GetIntegralGain(void)
 * @param None
 * @return Integral Gain
 * @brief retrieves requested gain */
int FeedbackControl_GetIntegralGain(void);

/**
 * @Function FeedbackControl_GetDerivativeGain(void)
 * @param None
 * @return Derivative Gain
 * @brief retrieves requested gain */
int FeedbackControl_GetDerivativeGain(void);

/**
 * @Function FeedbackControl_Update(int referenceValue, int sensorValue)
 * @param referenceValue, wanted reference
 * @param sensorValue, current sensor value
 * @brief performs feedback step according to algorithm in lab manual */
int FeedbackControl_Update(int referenceValue, int sensorValue);

/**
 * @Function FeedbackControl_ResetController(void)
 * @param None
 * @return SUCCESS or ERROR
 * @brief resets integrator and last sensor value to zero */
int FeedbackControl_ResetController(void);


#endif	/* FEEDBACKCONTROL_H */

