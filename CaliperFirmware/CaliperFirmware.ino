const byte clockPin = 19; //second from GND on calipers
const byte dataPin = 21; //first from GND on calipers
const int buttonPin = 15; //used for pushbutton

const int cycleTime = 40; //in ms

unsigned volatile int clockFlag = 0;

long nowT = 0;
long lastInterrupt = 0;
long value = 0;

float finalValue = 0;
float previousValue = 0;

int newValue = 0;
int sign = 1;
int currentBit = 1;

int reading;       
int previous = HIGH;   

long timer = 0;
long debounce = 200; 

//Run once on startup
void setup() {
  Serial.begin(115200);
  pinMode(clockPin, INPUT);
  pinMode(dataPin, INPUT);
  pinMode(interruptPin, INPUT); 
  attachInterrupt(digitalPinToInterrupt(clockPin), clockISR, RISING);
} 

//Runs forever
void loop() {

  //Handle debounce and detect rising edge
  reading = digitalRead(buttonPin);

  if (reading == LOW && previous == HIGH && millis() - timer > debounce) {
    sendMeasurement();
    timer = millis();    
  }
  previous = reading;


  //Checks to see if the rising edge was hit
  if (clockFlag == 1){
    decode();
    clockFlag = 0;
  }
}

//Handles one bit of caliper data
void decode() {
  unsigned char dataIn;
  dataIn = digitalRead(dataPin);
  nowT = millis();
  if ((nowT - lastInterrupt) > cycleTime){
    finalValue = (value * sign);
    currentBit = 0;
    value = 0;
    sign = 1;
  }
  else if (currentBit < 24 ){
    if (dataIn == 0){
      if (currentBit < 15)/*20*/ {
        value |= 1 << currentBit;
      }
      else if (currentBit == 20) {
        sign = -1;
      }
    }
    currentBit++;
  }
  lastInterrupt = nowT;
}

//Invoked on rising edge of clock
void clockISR() {
  clockFlag = 1;
}

//Sends a measurement over serial
void sendMeasurement() {
  Serial.println(finalValue, 2);
}
