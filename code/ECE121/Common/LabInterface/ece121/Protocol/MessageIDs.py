import enum


class MessageIDs(enum.Enum):
	ID_INVALID = 0
	ID_DEBUG = 128
	ID_LEDS_SET = enum.auto()
	ID_LEDS_STATE = enum.auto()
	ID_LEDS_GET = enum.auto()
	ID_PING = enum.auto()
	ID_PONG = enum.auto()
	ID_ROTARY_ANGLE = enum.auto()
	ID_PING_DISTANCE = enum.auto()
	ID_COMMAND_SERVO_PULSE = enum.auto()
	ID_SERVO_RESPONSE = enum.auto()
	ID_LAB2_ANGLE_REPORT = enum.auto()
	ID_LAB2_INPUT_SELECT = enum.auto()
	ID_LOG_INT_ONE = enum.auto()
	ID_LOG_INT_TWO = enum.auto()
	ID_LOG_INT_THREE = enum.auto()
	ID_LOG_INT_FOUR = enum.auto()
	ID_LOG_INT_FIVE = enum.auto()
	ID_ADC_SELECT_CHANNEL = enum.auto()
	ID_ADC_SELECT_CHANNEL_RESP = enum.auto()
	ID_ADC_READING = enum.auto()
	ID_ADC_FILTER_VALUES = enum.auto()
	ID_ADC_FILTER_VALUES_RESP = enum.auto()
	ID_NVM_READ_BYTE = enum.auto()
	ID_NVM_READ_BYTE_RESP = enum.auto()
	ID_NVM_WRITE_BYTE = enum.auto()
	ID_NVM_WRITE_BYTE_ACK = enum.auto()
	ID_NVM_READ_PAGE = enum.auto()
	ID_NVM_READ_PAGE_RESP = enum.auto()
	ID_NVM_WRITE_PAGE = enum.auto()
	ID_NVM_WRITE_PAGE_ACK = enum.auto()
	ID_LAB3_CHANNEL_FILTER = enum.auto()
	ID_LAB3_SET_FREQUENCY = enum.auto()
	ID_LAB3_FREQUENCY_ONOFF =enum.auto()
	ID_COMMAND_OPEN_MOTOR_SPEED = enum.auto()
	ID_COMMAND_OPEN_MOTOR_SPEED_RESP = enum.auto()
	ID_REPORT_RATE = enum.auto()
	ID_FEEDBACK_SET_GAINS = enum.auto()
	ID_FEEDBACK_SET_GAINS_RESP = enum.auto()
	ID_FEEDBACK_REQ_GAINS = enum.auto()
	ID_FEEDBACK_CUR_GAINS =enum.auto()
	ID_FEEDBACK_RESET_CONTROLLER = enum.auto()
	ID_FEEDBACK_RESET_CONTROLLER_RESP = enum.auto()
	ID_FEEDBACK_UPDATE = enum.auto()
	ID_FEEDBACK_UPDATE_OUTPUT = enum.auto()
	ID_COMMANDED_RATE = enum.auto()
	ID_REPORT_FEEDBACK = enum.auto()
	ID_COMMANDED_POSITION = enum.auto()
	ID_ENCODER_ABS = enum.auto()
	ID_LAB5_REPORT = enum.auto()
	ID_LAB5_ADC = enum.auto()
	ID_LAB5_SET_MODE = enum.auto()
	ID_LAB5_REQ_MODE = enum.auto()
	ID_LAB5_CUR_MODE = enum.auto()







# adding documentation is straight forward but a few steps must be followed
# add a new message to the enum
# create a dictionary entry for it appending to the list below
# Each entry value will be surrounded by parentheses
# this allows for multi line strings
# each one will have double quotes
# xml formatting is preserved so use it for emphasis
# <br> will generate a break in the doxygen popup but not the file itself
# adding \n will split the comment into multiple lines

packetDocumentation = dict()

packetDocumentation[MessageIDs.ID_INVALID] = ("Invalid Packet, used as an error return from functions")
packetDocumentation[MessageIDs.ID_DEBUG] = (" Array of chars displayed as a string<br>"
											"\nThis string is <b>NOT</b> NULL terminated.")
packetDocumentation[MessageIDs.ID_LEDS_SET] = ("A single char whose bits represent each of the LEDs "
											   "\nrespectively, to be set on the uc32 IO-Shield.")
packetDocumentation[MessageIDs.ID_LEDS_STATE] = (" The ID for the response to ID_LEDS_GET. Corresponding "
												 "\npayload is a single char (byte). Ex: If LED1 is on, and "
												 "\nall others are off, respond with 0x01, ")
packetDocumentation[MessageIDs.ID_LEDS_GET] = (" A request for the current states of each of the LEDS. The "
											   "\npayload is of length one (just the ID). The response "
											   "\npacket to a packet with this ID should have an ID of "
											   "\nID_LEDS_STATE.")
packetDocumentation[MessageIDs.ID_PING] = ("Packet with this ID has payload of an unsigned int (4 bytes).")
packetDocumentation[MessageIDs.ID_PONG] = ("Payload should be an unsigned int (4 bytes). This ID is used in "
										   "\n response to an ID_PING packet.")
packetDocumentation[MessageIDs.ID_ROTARY_ANGLE] = (" Raw angle from an encoder as an unsigned 14-bit short.")
packetDocumentation[MessageIDs.ID_LAB2_ANGLE_REPORT] = (" int of degrees*1000 followed by status char.")
packetDocumentation[MessageIDs.ID_PING_DISTANCE] = (" unsigned int of distance in millimeters.")
packetDocumentation[MessageIDs.ID_COMMAND_SERVO_PULSE] = ("Number of servo ticks represented by an "
														  "\nunsigned int interpreted as microseconds.")
packetDocumentation[MessageIDs.ID_SERVO_RESPONSE] = ("Unsigned int interpreted as microseconds requested")
packetDocumentation[MessageIDs.ID_LAB2_INPUT_SELECT] = ("Designates which input to use in Lab2 Application: 0 PING SENSOR, 1 ENCODER")
packetDocumentation[MessageIDs.ID_LOG_INT_ONE] = ("Log a single integers to a .csv file.")
packetDocumentation[MessageIDs.ID_LOG_INT_TWO] = ("Log two integers to a .csv file.")
packetDocumentation[MessageIDs.ID_LOG_INT_THREE] = ("Log three integers to a .csv file.")
packetDocumentation[MessageIDs.ID_LOG_INT_FOUR] = ("Log four integers to a .csv file.")
packetDocumentation[MessageIDs.ID_LOG_INT_FIVE] = ("Log five integers to a .csv file.")
packetDocumentation[MessageIDs.ID_ADC_SELECT_CHANNEL] = ("Char between 0-3 to select a channel to work with")
packetDocumentation[MessageIDs.ID_ADC_SELECT_CHANNEL_RESP] = ("Echo of channel set to to confirm channel change")
packetDocumentation[MessageIDs.ID_ADC_READING] = (
	" Two shorts holding the filtered and unfiltered values of a single channel")
packetDocumentation[MessageIDs.ID_ADC_FILTER_VALUES] = ("Filter values consisting of an array of 32 shorts")
packetDocumentation[MessageIDs.ID_ADC_FILTER_VALUES_RESP] = ("Char of channel filter values were applied to")
packetDocumentation[MessageIDs.ID_NVM_READ_BYTE] = ("Integer address to read from")
packetDocumentation[MessageIDs.ID_NVM_READ_BYTE_RESP] = ("Unsigned char value holding value stored in address")
packetDocumentation[MessageIDs.ID_NVM_WRITE_BYTE] = ("Integer address and char value to store")
packetDocumentation[MessageIDs.ID_NVM_WRITE_BYTE_ACK] = ("No payload but indicating that value was written.")
packetDocumentation[MessageIDs.ID_NVM_READ_PAGE] = ("Integer page to read from.")
packetDocumentation[MessageIDs.ID_NVM_READ_PAGE_RESP] = ("The 64 bytes of the requested page")
packetDocumentation[MessageIDs.ID_NVM_WRITE_PAGE] = ("Integer address followed by 64 bytes of data to write")
packetDocumentation[MessageIDs.ID_NVM_WRITE_PAGE_ACK] = ("No payload but indication that page was written")
packetDocumentation[MessageIDs.ID_LAB3_CHANNEL_FILTER] = ("Byte with upper four bytes being channel and bottom 4 being filter, sent when there is a system change")
packetDocumentation[MessageIDs.ID_LAB3_SET_FREQUENCY] = ("Unsigned short representing a new frequency in the valid range")
packetDocumentation[MessageIDs.ID_LAB3_FREQUENCY_ONOFF] = ("Controls Frequency output: 0 Off, 1 ON")
packetDocumentation[MessageIDs.ID_COMMAND_OPEN_MOTOR_SPEED] = ("Integer representing Motor speed in units of <b>Duty Cycle</b> (+/- 1000) for open loop control.")
packetDocumentation[MessageIDs.ID_COMMAND_OPEN_MOTOR_SPEED_RESP] = ("No payload but indicating command was accepted")
packetDocumentation[MessageIDs.ID_REPORT_RATE] = ("Signed integer representing the raw rate")
packetDocumentation[MessageIDs.ID_FEEDBACK_SET_GAINS] = ("Trio of integers representing Porportional, Integral, and Derivative Gain")
packetDocumentation[MessageIDs.ID_FEEDBACK_SET_GAINS_RESP] = ("No Payload indicating new gains were set")
packetDocumentation[MessageIDs.ID_FEEDBACK_RESET_CONTROLLER] = ("Reset the integrated value back to zero")
packetDocumentation[MessageIDs.ID_FEEDBACK_RESET_CONTROLLER_RESP] = ("Integrated value has been clear response")
packetDocumentation[MessageIDs.ID_FEEDBACK_UPDATE] = ("int reference followed by int sensorValue")
packetDocumentation[MessageIDs.ID_FEEDBACK_UPDATE_OUTPUT] = ("int control output")
packetDocumentation[MessageIDs.ID_COMMANDED_RATE] = ("integer commanded rate in raw ticks/count")
packetDocumentation[MessageIDs.ID_REPORT_FEEDBACK] = ("Trio of integers representing error, current rate, and PWM"
													  "\n<b> error = Commanded Rate - Current Rate")
packetDocumentation[MessageIDs.ID_FEEDBACK_REQ_GAINS] = ("no payload but requesting current gains")
packetDocumentation[MessageIDs.ID_FEEDBACK_CUR_GAINS] = ("Trio of integers representing Porportional, Integral, and Derivative Gain")
packetDocumentation[MessageIDs.ID_COMMANDED_POSITION] = ("signed integer represented commanded position in raw ticks")
packetDocumentation[MessageIDs.ID_ENCODER_ABS] = ("signed integer representing absolute positon of motor accounting for rollovers")
packetDocumentation[MessageIDs.ID_LAB5_REPORT] = ("Four signed integers with the following information"
													"\n<b>current error"
													"\n<b>Reference signal"
													"\n<b>Sensor signal"
													"\n<b>commanded position, yes there will be a duplicate value in command mode")
packetDocumentation[MessageIDs.ID_LAB5_ADC] = ("two signed shorts of the filtered readings for both IR sensors")
packetDocumentation[MessageIDs.ID_LAB5_CUR_MODE] = ("one unsigned char representing the current mode of the lab 5 application"
													"\n<b>0: commanded position mode"
													"\n<b>1: sensor input mode")
packetDocumentation[MessageIDs.ID_LAB5_SET_MODE] = ("one unsigned char representing the new mode required")
packetDocumentation[MessageIDs.ID_LAB5_REQ_MODE] = ("no payload but micro must respond with current mode")
# packetDocumentation[MessageIDs.ID_INVALID] = ("")



if __name__ == "__main__":
	# from . import MessageIDs

	for id in MessageIDs:
		print(id, id.value)
# print(IDs.ID_DEBUG.value)
