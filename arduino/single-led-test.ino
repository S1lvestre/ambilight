const int redpin = 11;
const int greenpin = 9;
const int bluepin = 10;

void setup() {
  // put your setup code here, to run once:
  pinMode(redpin, OUTPUT);
  pinMode(greenpin, OUTPUT);
  pinMode(bluepin, OUTPUT);

  Serial.begin(9600);
}

void loop() {

  if (Serial.available() > 0) {
    // look for the next valid integer in the incoming serial stream:
    int red = Serial.parseInt();
    // do it again:
    int green = Serial.parseInt();
    // do it again:
    int blue = Serial.parseInt();

    if (Serial.read() == '\n') {
      analogWrite(redpin,red);
      analogWrite(greenpin, green);
      analogWrite(bluepin, blue);
      
      // print the three numbers in one string as hexadecimal:
      Serial.print(red, HEX);
      Serial.print(green, HEX);
      Serial.println(blue, HEX);
    }
  }
}
