
bool top = false;
bool bottom = false;
int prox;
char lift_var;
void setup() {
 pinMode(A0, OUTPUT); //RELAY 0: EMERGENCY STOP
 pinMode(A1, OUTPUT); //RELAY 1: COMMAND ON/OFF
 pinMode(A2, OUTPUT); //RELAY 2: LINEAR ACTUATOR
 pinMode(A3, OUTPUT); //RELAY 3: LEFT DOOR
 pinMode(A4, OUTPUT); //RELAY 4: RIGHT DOOR
 pinMode(A5, OUTPUT); //RELAY 5: LIFT ACTUATORS
 //pinMode(A6, OUTPUT); //AUXILLERY RELAY
 //pinMode(A7, OUTPUT); //AUXILLERY RELAY
 pinMode(13, OUTPUT); // TOP RAISE
 pinMode(12, OUTPUT); // TOP LOWER
 pinMode(11, OUTPUT); // BOTTOM RAISE
 pinMode(10, OUTPUT); // BOTTOM LOWER
 pinMode(9, INPUT_PULLUP);   // PROXIMITY SWITCH
 
 Serial.begin(9600);
 
 //Serial.print("Motor Control Interface\n#######################\n\n");
 //Serial.print("Commands are listed below:\n\n");
 //Serial.print("0:\tEmergency Stop\n1:\tAllow Commands\n");
 //Serial.print("2:\tPad Actuator\n3:\tLeft Door\n4:\tRight Door\n5:\tLift Actuators\n");
 
}

void lift_control() {
  while(!Serial.available()){
  }
  lift_var = Serial.read();
  prox = digitalRead(9);
  switch(lift_var){
    case 'T':
    top = !top;
    if((top == true)){                //Need to set a flag for the prox swtich -- can simulate with normal switch
      digitalWrite(13, HIGH);
      while(prox == HIGH){
        prox = digitalRead(9);
        //Serial.print("Waiting for proxy switch...\n");
        //delay(500);
        }
      digitalWrite(13, LOW);
      //Serial.print("The top lift has been raised\n");
      Serial.write('>');
      }
    
    
    if((top == false)){
      digitalWrite(12, HIGH);
      delay(20000);
      digitalWrite(12, LOW);
      //Serial.print("The top lift has been lowed\n");
      Serial.write('<');
    }
    break;

    case 'B':
    bottom = !bottom;
    if(bottom == true){
      digitalWrite(11, HIGH);
      delay(20000);
      digitalWrite(11, LOW);
      //Serial.print("The bottom lifts have been raised\n");
      Serial.write('>');
    }
    
    else{
      digitalWrite(10, HIGH);
      delay(20000);
      digitalWrite(10, LOW);
      //Serial.print("The bottom lifts have been lowered\n");
      Serial.write('<');
    }
    break;

    default:
    break;
  }
}

void switchControl()  {
  
   //controls which motor will be used
   char control_var = Serial.read();
    
   //Is this mechanism on or off?
   static bool emergency_stop = false;
   static bool on = false;
   static bool linear_extended = false;
   static bool left_open = false;
   static bool right_open = false;
   static bool lift_extended = false;

  switch(control_var)
  {
    case '0':
    emergency_stop = !emergency_stop;
    if(emergency_stop == true){
      digitalWrite(A0, HIGH);
      //returns that the command is high
      Serial.write('1');
    }
    else{
      digitalWrite(A0, LOW);
      //returns that the command is low
      Serial.write('0');
    }
    break;

    case '1':
    on = !on;
    if(on == true){
      digitalWrite(A1, HIGH);
       //returns that the command is high
      Serial.write('1');
    }
    else{
      digitalWrite(A1, LOW);
      //returns that the command is low
      Serial.write('0');
    }
    break;

    case '2':
    linear_extended = !linear_extended;
    if(linear_extended == true){
      digitalWrite(A2, HIGH);
       //returns that the command is high
      Serial.write('1');
    }
    else{
      digitalWrite(A2, LOW);
      //returns that the command is low
      Serial.write('0');
    }
    break;

    case '3':
    left_open = !left_open;
    if(left_open == true){
      digitalWrite(A3, HIGH);
       //returns that the command is high
      Serial.write('1');
    }
    else{
      digitalWrite(A3, LOW);
      //returns that the command is low
      Serial.write('0');
    }
    break;

    case '4':
    right_open = !right_open;
    if(right_open == true){
      digitalWrite(A4, HIGH);
      Serial.write('1');
    }
    else{
      digitalWrite(A4, LOW);
      //returns that the command is low
      Serial.write('0');
    }
    break;

    case '5':
    //Serial.print("Press T to change top platform position.\nPress B to change bottom platform position\n"); 
    lift_control();
    break;

    case '6':
    if(left_open != right_open){
      Serial.write('!');
      break;
    }
    left_open = !left_open;
    if(left_open == true){
      digitalWrite(A3, HIGH);
       //returns that the command is high
    }
    else{
      digitalWrite(A3, LOW);
      //returns that the command is low
    }
 
    right_open = !right_open;
    if(right_open == true){
      digitalWrite(A4, HIGH);
      Serial.write('1');
    }
    else{
      digitalWrite(A4, LOW);
      //returns that the command is low
      Serial.write('0');
    }
    break;

    default:
    //sends back '!' to denote an invalid command
    Serial.write('!');
    break;
  }
}

void loop() {
  if(Serial.available() > 0){
    switchControl();
  }

}
