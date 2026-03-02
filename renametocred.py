db_host = 'yourMariaDBHostname'
db_port = 3306
db_name = 'dbname'
db_user = 'yourDBuser'
db_pass = 'yourdbpass'
SHELLY_API_KEY = 'yourshellyAPIKEY'
SHELLY_WEB_USER = 'your_local_shelly_username'
SHELLY_WEB_PASS = 'whatever_you_typed_in'
TIBBER_API_KEY = 'yourTibberKEy'

# You can get the shelly device IDs from their cloud service
# under device information.
# Each device has its own ID.
# control.shelly.cloud

ROOMS = {"room1":
             {"dbtable": "room1_db",
              "ipaddress": "IPoftheshellydevice"},
         "room2": {
             "dbtable": "room2_db",
             "ipaddress": "IPoftheshellydevice"},
             "room3": {
                 "dbtable": "room3_db",
                 "ipaddress": "IPoftheshellydevice"
             }}
