#include <FastLED.h>

#define LED_TYPE APA102
#define COLOR_ORDER BGR
#define NUM_LEDS 3

#define DATA_PIN 2
#define CLOCK_PIN 3

CRGB leds[NUM_LEDS];



const byte buffSize = 15;

const char startMarker = '<';
const char endMarker = '>';

byte bytesInBuffer;
byte tempBuffer[buffSize];

byte bytesStored;
char storage[buffSize];
long color;

byte totalBytesToSend;

boolean inProgress = false;
boolean startFound = false;
boolean allReceived = false;

// ===============
//
//      SETUP
//
// ===============

void setup()
{
    FastLED.addLeds<LED_TYPE, DATA_PIN, CLOCK_PIN, COLOR_ORDER>(leds, NUM_LEDS);

    Serial.begin(9600);
    Serial.println("<Arduino is Ready>");
}

// ===============
//
//      LOOP
//
// ===============

void loop()
{
    getSerialData();
    
    execute();
}

// ===============
//
//    FUNCTIONS
//
// ===============


void getSerialData()
{
    if( Serial.available() > 0 )
    {
        byte x = Serial.read();

        if( x == startMarker )
        {
            bytesInBuffer = 0;
            inProgress = true;
        }

        if( inProgress)
        {
            tempBuffer[bytesInBuffer] = x;
            bytesInBuffer ++;
        }

        if( x == endMarker )
        {
            inProgress = false;
            allReceived = true;

            //decodeHighBytes();
            /* need to start at 1 because the first byte is empty
               i know how to fix it. its usig elifs in this function instead of
               just ifs but and don't know what bugs that will raise so for now
               it stays like this.*/
            bytesStored = 0;
            for( byte n = 1; n < bytesInBuffer; n++ )
            {
                storage[n-1] = tempBuffer[n];
                bytesStored ++;
            }
            color = strtol(storage, NULL, 16);
        }
    }
}

/* only need bytes 1 - 8. EXCLUDE byte 0 */

void execute()
{
    if( allReceived )
    {
        // change led color
        leds[0] = color;
        FastLED.show();
        
        // replying back the received info        
        totalBytesToSend = bytesStored;
        for( byte n = 0; n < bytesStored; n++ )
        {
            tempBuffer[n] = storage[n];
        }
        
        Serial.write( startMarker );
        Serial.write( tempBuffer, totalBytesToSend );
        Serial.write( endMarker );
        
        allReceived = false;
    }
}

