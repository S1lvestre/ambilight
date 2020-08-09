const byte buffSize = 40;

const char startMarker = '<';
const char endMarker = '>';

byte bytesInBuffer;
byte tempBuffer[buffSize];

byte bytesStored;
char storage[buffSize];

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
            bytesStored = 0;
            for( byte n = 0; n < bytesInBuffer; n++ )
            {
                storage[n] = tempBuffer[n];
                bytesStored ++;
            }
        }
    }
}

void execute()
{
    if( allReceived )
    {
        //just replying back the received info        
        totalBytesToSend = bytesStored;
        for( byte n = 0; n < bytesStored; n++ )
        {
            tempBuffer[n] = storage[n];
        }
        
        Serial.write( startMarker );
        Serial.write( tempBuffer, totalBytesToSend );
        //Serial.write( tempBuffer[0] ); // <- used this for debugging
        Serial.write( endMarker );
        
        allReceived = false;
    }
}

