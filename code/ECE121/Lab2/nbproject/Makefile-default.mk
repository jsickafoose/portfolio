#
# Generated Makefile - do not edit!
#
# Edit the Makefile in the project folder instead (../Makefile). Each target
# has a -pre and a -post target defined where you can add customized code.
#
# This makefile implements configuration specific macros and targets.


# Include project Makefile
ifeq "${IGNORE_LOCAL}" "TRUE"
# do not include local makefile. User is passing all local related variables already
else
include Makefile
# Include makefile containing local settings
ifeq "$(wildcard nbproject/Makefile-local-default.mk)" "nbproject/Makefile-local-default.mk"
include nbproject/Makefile-local-default.mk
endif
endif

# Environment
MKDIR=gnumkdir -p
RM=rm -f 
MV=mv 
CP=cp 

# Macros
CND_CONF=default
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
IMAGE_TYPE=debug
OUTPUT_SUFFIX=elf
DEBUGGABLE_SUFFIX=elf
FINAL_IMAGE=dist/${CND_CONF}/${IMAGE_TYPE}/Lab2.${IMAGE_TYPE}.${OUTPUT_SUFFIX}
else
IMAGE_TYPE=production
OUTPUT_SUFFIX=hex
DEBUGGABLE_SUFFIX=elf
FINAL_IMAGE=dist/${CND_CONF}/${IMAGE_TYPE}/Lab2.${IMAGE_TYPE}.${OUTPUT_SUFFIX}
endif

ifeq ($(COMPARE_BUILD), true)
COMPARISON_BUILD=-mafrlcsj
else
COMPARISON_BUILD=
endif

ifdef SUB_IMAGE_ADDRESS

else
SUB_IMAGE_ADDRESS_COMMAND=
endif

# Object Directory
OBJECTDIR=build/${CND_CONF}/${IMAGE_TYPE}

# Distribution Directory
DISTDIR=dist/${CND_CONF}/${IMAGE_TYPE}

# Source Files Quoted if spaced
SOURCEFILES_QUOTED_IF_SPACED=../../src/BOARD.c ../../src/CircularBuffer.c ../../src/RotaryEncoder.c ../../src/PingSensor.c ../../src/RCServo.c Lab2Application.c ../../src/FreeRunningTimer.c

# Object Files Quoted if spaced
OBJECTFILES_QUOTED_IF_SPACED=${OBJECTDIR}/_ext/1445274692/BOARD.o ${OBJECTDIR}/_ext/1445274692/CircularBuffer.o ${OBJECTDIR}/_ext/1445274692/RotaryEncoder.o ${OBJECTDIR}/_ext/1445274692/PingSensor.o ${OBJECTDIR}/_ext/1445274692/RCServo.o ${OBJECTDIR}/Lab2Application.o ${OBJECTDIR}/_ext/1445274692/FreeRunningTimer.o
POSSIBLE_DEPFILES=${OBJECTDIR}/_ext/1445274692/BOARD.o.d ${OBJECTDIR}/_ext/1445274692/CircularBuffer.o.d ${OBJECTDIR}/_ext/1445274692/RotaryEncoder.o.d ${OBJECTDIR}/_ext/1445274692/PingSensor.o.d ${OBJECTDIR}/_ext/1445274692/RCServo.o.d ${OBJECTDIR}/Lab2Application.o.d ${OBJECTDIR}/_ext/1445274692/FreeRunningTimer.o.d

# Object Files
OBJECTFILES=${OBJECTDIR}/_ext/1445274692/BOARD.o ${OBJECTDIR}/_ext/1445274692/CircularBuffer.o ${OBJECTDIR}/_ext/1445274692/RotaryEncoder.o ${OBJECTDIR}/_ext/1445274692/PingSensor.o ${OBJECTDIR}/_ext/1445274692/RCServo.o ${OBJECTDIR}/Lab2Application.o ${OBJECTDIR}/_ext/1445274692/FreeRunningTimer.o

# Source Files
SOURCEFILES=../../src/BOARD.c ../../src/CircularBuffer.c ../../src/RotaryEncoder.c ../../src/PingSensor.c ../../src/RCServo.c Lab2Application.c ../../src/FreeRunningTimer.c



CFLAGS=
ASFLAGS=
LDLIBSOPTIONS=

############# Tool locations ##########################################
# If you copy a project from one host to another, the path where the  #
# compiler is installed may be different.                             #
# If you open this project with MPLAB X in the new host, this         #
# makefile will be regenerated and the paths will be corrected.       #
#######################################################################
# fixDeps replaces a bunch of sed/cat/printf statements that slow down the build
FIXDEPS=fixDeps

.build-conf:  ${BUILD_SUBPROJECTS}
ifneq ($(INFORMATION_MESSAGE), )
	@echo $(INFORMATION_MESSAGE)
endif
	${MAKE}  -f nbproject/Makefile-default.mk dist/${CND_CONF}/${IMAGE_TYPE}/Lab2.${IMAGE_TYPE}.${OUTPUT_SUFFIX}

MP_PROCESSOR_OPTION=32MX320F128H
MP_LINKER_FILE_OPTION=
# ------------------------------------------------------------------------------------
# Rules for buildStep: assemble
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
else
endif

# ------------------------------------------------------------------------------------
# Rules for buildStep: assembleWithPreprocess
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
else
endif

# ------------------------------------------------------------------------------------
# Rules for buildStep: compile
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
${OBJECTDIR}/_ext/1445274692/BOARD.o: ../../src/BOARD.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} "${OBJECTDIR}/_ext/1445274692" 
	@${RM} ${OBJECTDIR}/_ext/1445274692/BOARD.o.d 
	@${RM} ${OBJECTDIR}/_ext/1445274692/BOARD.o 
	@${FIXDEPS} "${OBJECTDIR}/_ext/1445274692/BOARD.o.d" $(SILENT) -rsi ${MP_CC_DIR}../  -c ${MP_CC}  $(MP_EXTRA_CC_PRE) -g -D__DEBUG -D__MPLAB_DEBUGGER_PK3=1  -fframe-base-loclist  -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -I"../../src" -I"../../include" -MMD -MF "${OBJECTDIR}/_ext/1445274692/BOARD.o.d" -o ${OBJECTDIR}/_ext/1445274692/BOARD.o ../../src/BOARD.c    -DXPRJ_default=$(CND_CONF)  -legacy-libc  $(COMPARISON_BUILD)  -mdfp=${DFP_DIR}  
	
${OBJECTDIR}/_ext/1445274692/CircularBuffer.o: ../../src/CircularBuffer.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} "${OBJECTDIR}/_ext/1445274692" 
	@${RM} ${OBJECTDIR}/_ext/1445274692/CircularBuffer.o.d 
	@${RM} ${OBJECTDIR}/_ext/1445274692/CircularBuffer.o 
	@${FIXDEPS} "${OBJECTDIR}/_ext/1445274692/CircularBuffer.o.d" $(SILENT) -rsi ${MP_CC_DIR}../  -c ${MP_CC}  $(MP_EXTRA_CC_PRE) -g -D__DEBUG -D__MPLAB_DEBUGGER_PK3=1  -fframe-base-loclist  -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -I"../../src" -I"../../include" -MMD -MF "${OBJECTDIR}/_ext/1445274692/CircularBuffer.o.d" -o ${OBJECTDIR}/_ext/1445274692/CircularBuffer.o ../../src/CircularBuffer.c    -DXPRJ_default=$(CND_CONF)  -legacy-libc  $(COMPARISON_BUILD)  -mdfp=${DFP_DIR}  
	
${OBJECTDIR}/_ext/1445274692/RotaryEncoder.o: ../../src/RotaryEncoder.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} "${OBJECTDIR}/_ext/1445274692" 
	@${RM} ${OBJECTDIR}/_ext/1445274692/RotaryEncoder.o.d 
	@${RM} ${OBJECTDIR}/_ext/1445274692/RotaryEncoder.o 
	@${FIXDEPS} "${OBJECTDIR}/_ext/1445274692/RotaryEncoder.o.d" $(SILENT) -rsi ${MP_CC_DIR}../  -c ${MP_CC}  $(MP_EXTRA_CC_PRE) -g -D__DEBUG -D__MPLAB_DEBUGGER_PK3=1  -fframe-base-loclist  -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -I"../../src" -I"../../include" -MMD -MF "${OBJECTDIR}/_ext/1445274692/RotaryEncoder.o.d" -o ${OBJECTDIR}/_ext/1445274692/RotaryEncoder.o ../../src/RotaryEncoder.c    -DXPRJ_default=$(CND_CONF)  -legacy-libc  $(COMPARISON_BUILD)  -mdfp=${DFP_DIR}  
	
${OBJECTDIR}/_ext/1445274692/PingSensor.o: ../../src/PingSensor.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} "${OBJECTDIR}/_ext/1445274692" 
	@${RM} ${OBJECTDIR}/_ext/1445274692/PingSensor.o.d 
	@${RM} ${OBJECTDIR}/_ext/1445274692/PingSensor.o 
	@${FIXDEPS} "${OBJECTDIR}/_ext/1445274692/PingSensor.o.d" $(SILENT) -rsi ${MP_CC_DIR}../  -c ${MP_CC}  $(MP_EXTRA_CC_PRE) -g -D__DEBUG -D__MPLAB_DEBUGGER_PK3=1  -fframe-base-loclist  -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -I"../../src" -I"../../include" -MMD -MF "${OBJECTDIR}/_ext/1445274692/PingSensor.o.d" -o ${OBJECTDIR}/_ext/1445274692/PingSensor.o ../../src/PingSensor.c    -DXPRJ_default=$(CND_CONF)  -legacy-libc  $(COMPARISON_BUILD)  -mdfp=${DFP_DIR}  
	
${OBJECTDIR}/_ext/1445274692/RCServo.o: ../../src/RCServo.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} "${OBJECTDIR}/_ext/1445274692" 
	@${RM} ${OBJECTDIR}/_ext/1445274692/RCServo.o.d 
	@${RM} ${OBJECTDIR}/_ext/1445274692/RCServo.o 
	@${FIXDEPS} "${OBJECTDIR}/_ext/1445274692/RCServo.o.d" $(SILENT) -rsi ${MP_CC_DIR}../  -c ${MP_CC}  $(MP_EXTRA_CC_PRE) -g -D__DEBUG -D__MPLAB_DEBUGGER_PK3=1  -fframe-base-loclist  -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -I"../../src" -I"../../include" -MMD -MF "${OBJECTDIR}/_ext/1445274692/RCServo.o.d" -o ${OBJECTDIR}/_ext/1445274692/RCServo.o ../../src/RCServo.c    -DXPRJ_default=$(CND_CONF)  -legacy-libc  $(COMPARISON_BUILD)  -mdfp=${DFP_DIR}  
	
${OBJECTDIR}/Lab2Application.o: Lab2Application.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} "${OBJECTDIR}" 
	@${RM} ${OBJECTDIR}/Lab2Application.o.d 
	@${RM} ${OBJECTDIR}/Lab2Application.o 
	@${FIXDEPS} "${OBJECTDIR}/Lab2Application.o.d" $(SILENT) -rsi ${MP_CC_DIR}../  -c ${MP_CC}  $(MP_EXTRA_CC_PRE) -g -D__DEBUG -D__MPLAB_DEBUGGER_PK3=1  -fframe-base-loclist  -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -I"../../src" -I"../../include" -MMD -MF "${OBJECTDIR}/Lab2Application.o.d" -o ${OBJECTDIR}/Lab2Application.o Lab2Application.c    -DXPRJ_default=$(CND_CONF)  -legacy-libc  $(COMPARISON_BUILD)  -mdfp=${DFP_DIR}  
	
${OBJECTDIR}/_ext/1445274692/FreeRunningTimer.o: ../../src/FreeRunningTimer.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} "${OBJECTDIR}/_ext/1445274692" 
	@${RM} ${OBJECTDIR}/_ext/1445274692/FreeRunningTimer.o.d 
	@${RM} ${OBJECTDIR}/_ext/1445274692/FreeRunningTimer.o 
	@${FIXDEPS} "${OBJECTDIR}/_ext/1445274692/FreeRunningTimer.o.d" $(SILENT) -rsi ${MP_CC_DIR}../  -c ${MP_CC}  $(MP_EXTRA_CC_PRE) -g -D__DEBUG -D__MPLAB_DEBUGGER_PK3=1  -fframe-base-loclist  -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -I"../../src" -I"../../include" -MMD -MF "${OBJECTDIR}/_ext/1445274692/FreeRunningTimer.o.d" -o ${OBJECTDIR}/_ext/1445274692/FreeRunningTimer.o ../../src/FreeRunningTimer.c    -DXPRJ_default=$(CND_CONF)  -legacy-libc  $(COMPARISON_BUILD)  -mdfp=${DFP_DIR}  
	
else
${OBJECTDIR}/_ext/1445274692/BOARD.o: ../../src/BOARD.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} "${OBJECTDIR}/_ext/1445274692" 
	@${RM} ${OBJECTDIR}/_ext/1445274692/BOARD.o.d 
	@${RM} ${OBJECTDIR}/_ext/1445274692/BOARD.o 
	@${FIXDEPS} "${OBJECTDIR}/_ext/1445274692/BOARD.o.d" $(SILENT) -rsi ${MP_CC_DIR}../  -c ${MP_CC}  $(MP_EXTRA_CC_PRE)  -g -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -I"../../src" -I"../../include" -MMD -MF "${OBJECTDIR}/_ext/1445274692/BOARD.o.d" -o ${OBJECTDIR}/_ext/1445274692/BOARD.o ../../src/BOARD.c    -DXPRJ_default=$(CND_CONF)  -legacy-libc  $(COMPARISON_BUILD)  -mdfp=${DFP_DIR}  
	
${OBJECTDIR}/_ext/1445274692/CircularBuffer.o: ../../src/CircularBuffer.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} "${OBJECTDIR}/_ext/1445274692" 
	@${RM} ${OBJECTDIR}/_ext/1445274692/CircularBuffer.o.d 
	@${RM} ${OBJECTDIR}/_ext/1445274692/CircularBuffer.o 
	@${FIXDEPS} "${OBJECTDIR}/_ext/1445274692/CircularBuffer.o.d" $(SILENT) -rsi ${MP_CC_DIR}../  -c ${MP_CC}  $(MP_EXTRA_CC_PRE)  -g -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -I"../../src" -I"../../include" -MMD -MF "${OBJECTDIR}/_ext/1445274692/CircularBuffer.o.d" -o ${OBJECTDIR}/_ext/1445274692/CircularBuffer.o ../../src/CircularBuffer.c    -DXPRJ_default=$(CND_CONF)  -legacy-libc  $(COMPARISON_BUILD)  -mdfp=${DFP_DIR}  
	
${OBJECTDIR}/_ext/1445274692/RotaryEncoder.o: ../../src/RotaryEncoder.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} "${OBJECTDIR}/_ext/1445274692" 
	@${RM} ${OBJECTDIR}/_ext/1445274692/RotaryEncoder.o.d 
	@${RM} ${OBJECTDIR}/_ext/1445274692/RotaryEncoder.o 
	@${FIXDEPS} "${OBJECTDIR}/_ext/1445274692/RotaryEncoder.o.d" $(SILENT) -rsi ${MP_CC_DIR}../  -c ${MP_CC}  $(MP_EXTRA_CC_PRE)  -g -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -I"../../src" -I"../../include" -MMD -MF "${OBJECTDIR}/_ext/1445274692/RotaryEncoder.o.d" -o ${OBJECTDIR}/_ext/1445274692/RotaryEncoder.o ../../src/RotaryEncoder.c    -DXPRJ_default=$(CND_CONF)  -legacy-libc  $(COMPARISON_BUILD)  -mdfp=${DFP_DIR}  
	
${OBJECTDIR}/_ext/1445274692/PingSensor.o: ../../src/PingSensor.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} "${OBJECTDIR}/_ext/1445274692" 
	@${RM} ${OBJECTDIR}/_ext/1445274692/PingSensor.o.d 
	@${RM} ${OBJECTDIR}/_ext/1445274692/PingSensor.o 
	@${FIXDEPS} "${OBJECTDIR}/_ext/1445274692/PingSensor.o.d" $(SILENT) -rsi ${MP_CC_DIR}../  -c ${MP_CC}  $(MP_EXTRA_CC_PRE)  -g -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -I"../../src" -I"../../include" -MMD -MF "${OBJECTDIR}/_ext/1445274692/PingSensor.o.d" -o ${OBJECTDIR}/_ext/1445274692/PingSensor.o ../../src/PingSensor.c    -DXPRJ_default=$(CND_CONF)  -legacy-libc  $(COMPARISON_BUILD)  -mdfp=${DFP_DIR}  
	
${OBJECTDIR}/_ext/1445274692/RCServo.o: ../../src/RCServo.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} "${OBJECTDIR}/_ext/1445274692" 
	@${RM} ${OBJECTDIR}/_ext/1445274692/RCServo.o.d 
	@${RM} ${OBJECTDIR}/_ext/1445274692/RCServo.o 
	@${FIXDEPS} "${OBJECTDIR}/_ext/1445274692/RCServo.o.d" $(SILENT) -rsi ${MP_CC_DIR}../  -c ${MP_CC}  $(MP_EXTRA_CC_PRE)  -g -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -I"../../src" -I"../../include" -MMD -MF "${OBJECTDIR}/_ext/1445274692/RCServo.o.d" -o ${OBJECTDIR}/_ext/1445274692/RCServo.o ../../src/RCServo.c    -DXPRJ_default=$(CND_CONF)  -legacy-libc  $(COMPARISON_BUILD)  -mdfp=${DFP_DIR}  
	
${OBJECTDIR}/Lab2Application.o: Lab2Application.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} "${OBJECTDIR}" 
	@${RM} ${OBJECTDIR}/Lab2Application.o.d 
	@${RM} ${OBJECTDIR}/Lab2Application.o 
	@${FIXDEPS} "${OBJECTDIR}/Lab2Application.o.d" $(SILENT) -rsi ${MP_CC_DIR}../  -c ${MP_CC}  $(MP_EXTRA_CC_PRE)  -g -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -I"../../src" -I"../../include" -MMD -MF "${OBJECTDIR}/Lab2Application.o.d" -o ${OBJECTDIR}/Lab2Application.o Lab2Application.c    -DXPRJ_default=$(CND_CONF)  -legacy-libc  $(COMPARISON_BUILD)  -mdfp=${DFP_DIR}  
	
${OBJECTDIR}/_ext/1445274692/FreeRunningTimer.o: ../../src/FreeRunningTimer.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} "${OBJECTDIR}/_ext/1445274692" 
	@${RM} ${OBJECTDIR}/_ext/1445274692/FreeRunningTimer.o.d 
	@${RM} ${OBJECTDIR}/_ext/1445274692/FreeRunningTimer.o 
	@${FIXDEPS} "${OBJECTDIR}/_ext/1445274692/FreeRunningTimer.o.d" $(SILENT) -rsi ${MP_CC_DIR}../  -c ${MP_CC}  $(MP_EXTRA_CC_PRE)  -g -x c -c -mprocessor=$(MP_PROCESSOR_OPTION)  -I"../../src" -I"../../include" -MMD -MF "${OBJECTDIR}/_ext/1445274692/FreeRunningTimer.o.d" -o ${OBJECTDIR}/_ext/1445274692/FreeRunningTimer.o ../../src/FreeRunningTimer.c    -DXPRJ_default=$(CND_CONF)  -legacy-libc  $(COMPARISON_BUILD)  -mdfp=${DFP_DIR}  
	
endif

# ------------------------------------------------------------------------------------
# Rules for buildStep: compileCPP
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
else
endif

# ------------------------------------------------------------------------------------
# Rules for buildStep: link
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
dist/${CND_CONF}/${IMAGE_TYPE}/Lab2.${IMAGE_TYPE}.${OUTPUT_SUFFIX}: ${OBJECTFILES}  nbproject/Makefile-${CND_CONF}.mk  ../../src/Protocol.X.a  
	@${MKDIR} dist/${CND_CONF}/${IMAGE_TYPE} 
	${MP_CC} $(MP_EXTRA_LD_PRE) -g -mdebugger -D__MPLAB_DEBUGGER_PK3=1 -mprocessor=$(MP_PROCESSOR_OPTION)  -o dist/${CND_CONF}/${IMAGE_TYPE}/Lab2.${IMAGE_TYPE}.${OUTPUT_SUFFIX} ${OBJECTFILES_QUOTED_IF_SPACED}    ..\..\src\Protocol.X.a      -DXPRJ_default=$(CND_CONF)  -legacy-libc  $(COMPARISON_BUILD)   -mreserve=data@0x0:0x1FC -mreserve=boot@0x1FC02000:0x1FC02FEF -mreserve=boot@0x1FC02000:0x1FC024FF  -Wl,--defsym=__MPLAB_BUILD=1$(MP_EXTRA_LD_POST)$(MP_LINKER_FILE_OPTION),--defsym=__MPLAB_DEBUG=1,--defsym=__DEBUG=1,-D=__DEBUG_D,--defsym=__MPLAB_DEBUGGER_PK3=1,--no-code-in-dinit,--no-dinit-in-serial-mem,-Map="${DISTDIR}/${PROJECTNAME}.${IMAGE_TYPE}.map",--memorysummary,dist/${CND_CONF}/${IMAGE_TYPE}/memoryfile.xml -mdfp=${DFP_DIR}
	
else
dist/${CND_CONF}/${IMAGE_TYPE}/Lab2.${IMAGE_TYPE}.${OUTPUT_SUFFIX}: ${OBJECTFILES}  nbproject/Makefile-${CND_CONF}.mk  ../../src/Protocol.X.a 
	@${MKDIR} dist/${CND_CONF}/${IMAGE_TYPE} 
	${MP_CC} $(MP_EXTRA_LD_PRE)  -mprocessor=$(MP_PROCESSOR_OPTION)  -o dist/${CND_CONF}/${IMAGE_TYPE}/Lab2.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX} ${OBJECTFILES_QUOTED_IF_SPACED}    ..\..\src\Protocol.X.a      -DXPRJ_default=$(CND_CONF)  -legacy-libc  $(COMPARISON_BUILD)  -Wl,--defsym=__MPLAB_BUILD=1$(MP_EXTRA_LD_POST)$(MP_LINKER_FILE_OPTION),--no-code-in-dinit,--no-dinit-in-serial-mem,-Map="${DISTDIR}/${PROJECTNAME}.${IMAGE_TYPE}.map",--memorysummary,dist/${CND_CONF}/${IMAGE_TYPE}/memoryfile.xml -mdfp=${DFP_DIR}
	${MP_CC_DIR}\\xc32-bin2hex dist/${CND_CONF}/${IMAGE_TYPE}/Lab2.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX} 
endif


# Subprojects
.build-subprojects:


# Subprojects
.clean-subprojects:

# Clean Targets
.clean-conf: ${CLEAN_SUBPROJECTS}
	${RM} -r build/default
	${RM} -r dist/default

# Enable dependency checking
.dep.inc: .depcheck-impl

DEPFILES=$(shell mplabwildcard ${POSSIBLE_DEPFILES})
ifneq (${DEPFILES},)
include ${DEPFILES}
endif
