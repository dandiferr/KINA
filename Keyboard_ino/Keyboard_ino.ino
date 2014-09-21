void setup() {
	Serial.begin(9600); // use the same baud-rate as the python side

}
void loop() {
      if(digitalRead(4) == 1)
      {
        Serial.println("1");
        Serial.write("1");
        while(digitalRead(4) == 1)
        {
           delay(10);
        }
	  }
      else if(digitalRead(3) == 1)
      {
        Serial.println("2");
        Serial.write("2");
        while(digitalRead(3) == 1)
        {
           delay(10);
        }
      }
      else if(digitalRead(2) == 1)
      {
        Serial.println("3");
        Serial.write("3");
        while(digitalRead(2) == 1)
        {
           delay(10);
        }
      }
      else if(digitalRead(5) == 1)
      {
        Serial.println("4");
        Serial.write("4");
        while(digitalRead(5) == 1)
        {
           delay(10);
        }
      }
      else if(digitalRead(6) == 1)
      {
        Serial.println("5");
        Serial.write("5");
        while(digitalRead(6) == 1)
        {
           delay(10);
        }
      }
      delay(100);
}
