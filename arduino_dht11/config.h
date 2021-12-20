/* General settings */
unsigned long currentMillis;

/* DHT SETTINGS */
#define INTERVAL 5000
#define DHT_PIN 5
#define DHT_TYPE DHT11
unsigned long PREV_DHT_MILLIS = 0;
static DHT dht(DHT_PIN, DHT_TYPE);
float humidity = 0;
float current_temperature = 0;
