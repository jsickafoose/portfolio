#include "CircularBuffer.h"
#include "Uart1.h"

//CSE13E Support Library
#include "BOARD.h"

#include <xc.h>
#include <sys/attribs.h>

static CircularBuffer uart1RxBuffer;
static uint8_t u1RxBuf[1024];
static CircularBuffer uart1TxBuffer;
static uint8_t u1TxBuf[1024];

/*
 * Private functions.
 */
void Uart1StartTransmission(void);

/**
 * Initialization function for the UART_USED peripheral.
 * Should be called in initialization code for the
 * model. This function configures the UART
 * for whatever baud rate is specified. It also configures two circular buffers
 * for transmission and reception.
 */
void Uart1Init(uint32_t baudRate)
{
    // First initialize the necessary circular buffers.
    CB_Init(&uart1RxBuffer, u1RxBuf, sizeof (u1RxBuf));
    CB_Init(&uart1TxBuffer, u1TxBuf, sizeof (u1TxBuf));

#ifdef PIC32MX
    //the next few lines below are redundant with actions performed in BOARD_Init():
    U1MODEbits.ON = 1; //turn on UART
    U1STAbits.UTXEN = 1; //enable TX pin
    U1STAbits.URXEN = 1; //enable RX oun

    // The FIFO mode here for transmission is not set to `*_TX_BUFFER_EMPTY` as that seems to fail
    // with some characters dropped. This method, waiting until transmission is finished, is
    // technically slower, but works quite nicely.
    
    U1STAbits.UTXISEL = 0b01; //interrupt when transmission is complete
    U1STAbits.URXISEL = 0b00; //interrupt when RX is not empty (has at least 1 character)


    // Configure UART interrupt for both RX and TX
    IEC0bits.U1RXIE = 1; //enable RX interrupt
    IEC0bits.U1TXIE = 1; //enable TX interrupt
    IPC6bits.U1IP = 6; //set UART interrupt priority to 6
    IPC6bits.U1IS = 0; //set interrupt subpriority to 0
#endif
}

void Uart1ChangeBaudRate(uint16_t brgRegister)
{
    uint8_t utxen = U1STAbits.UTXEN;

    // Disable the port;
    U1MODEbits.UARTEN = 0;

    // Change the BRG register to set the new baud rate
    U1BRG = brgRegister;

    // Enable the port restoring the previous transmission settings
    U1MODEbits.UARTEN = 1;
    U1STAbits.UTXEN = utxen;
}

uint8_t Uart1HasData(void)
{
    return (uart1RxBuffer.dataSize > 0);
}

/**
 * This function actually initiates transmission. It
 * attempts to start transmission with the first element
 * in the queue if transmission isn't already proceeding.
 * Once transmission starts the interrupt handler will
 * keep things moving from there. The buffer is checked
 * for new data and the transmission buffer is checked that
 * it has room for new data before attempting to transmit.
 */
void Uart1StartTransmission(void)
{
    while (uart1TxBuffer.dataSize > 0 && !U1STAbits.UTXBF) {
        // A temporary variable is used here because writing directly into U1TXREG causes some weird issues.
        uint8_t c;
        CB_ReadByte(&uart1TxBuffer, &c);
        U1TXREG = c;
    }
}

int Uart1ReadByte(uint8_t *datum)
{
    return CB_ReadByte(&uart1RxBuffer, datum);
}

/**
 * This function supplements the uart1EnqueueData() function by also
 * providing an interface that only enqueues a single byte.
 */
void Uart1WriteByte(uint8_t datum)
{
    CB_WriteByte(&uart1TxBuffer, datum);
    Uart1StartTransmission();
}

/**
 * This function enqueues all bytes in the passed data character array according to the passed
 * length.
 */
int Uart1WriteData(const void *data, size_t length)
{
    int success = CB_WriteMany(&uart1TxBuffer, data, length, FALSE);

    Uart1StartTransmission();

    return success;
}

#ifdef PIC32MX

void __ISR(_UART_1_VECTOR, ipl6auto) Uart1Interrupt(void)
{
    // if receive flag is set, handle received character input
    if (IFS0bits.U1RXIF) {
        // Keep receiving new bytes while the buffer has data.
        while (U1STAbits.URXDA == 1) {
            CB_WriteByte(&uart1RxBuffer, (uint8_t) U1RXREG);
        }

        // Clear buffer overflow bit if triggered
        if (U1STAbits.OERR == 1) {
            U1STAbits.OERR = 0;
        }

        // Clear the interrupt flag
        IFS0bits.U1RXIF = 0;
    }

    // Handle transmission interrupt
    if (IFS0bits.U1TXIF) {
        Uart1StartTransmission();

        // Clear the interrupt flag
        IFS0bits.U1TXIF = 0;
    }
}
#endif
