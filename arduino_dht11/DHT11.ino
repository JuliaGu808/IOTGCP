void initDHT() {
  pinMode(DHT_PIN, INPUT);
  dht.begin();
  Serial.println("DHT sensor init ....");
}

/*
 * read DHT and change data to json file
 * then use transmitter method to send out
 */
void sendDhtMessage() {
  current_temperature = dht.readTemperature();
  humidity = dht.readHumidity();
  
//  current_temperature = random(1500,3500)/100.0;
//  humidity = random(30,70);
  
  if((currentMillis - PREV_DHT_MILLIS) >= INTERVAL 
        && !isnan(current_temperature) 
        && !isnan(humidity)){
    PREV_DHT_MILLIS = currentMillis;
    Serial.print(current_temperature);
    Serial.print("::");
    Serial.println(humidity);
  }
}
