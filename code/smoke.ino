int inputPin = 1; // select the input pin for the interrupter
int val = 0; // variable to store the value coming from the sensor

void setup()
{
    Serial.begin(9600);
}

void loop()
{
    val = analogRead(inputPin); // read the value from the sensor
    Serial.println(val); // print the sensor value to the serial monitor
    delay(50);
}
