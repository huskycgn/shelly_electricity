db_host = 'yourMariaDBHostname'
db_port = 3306
db_name = 'dbname'
db_user = 'yourDBuser'
db_pass = 'yourdbpass'
SHELLY_API_KEY = 'yourshellyAPIKEY'

# You can get the shelly device IDs from their cloud service
# under device information.
# Each device has its own ID.
# control.shelly.cloud

ROOMS = {"room1":
             {"dbtable": "room1_db",
              "shellydeviceid": "IDoftheshellydevice"},
         "room2": {
             "dbtable": "room2_db",
             "shellydeviceid": "IDoftheshellydevice"},
             "kuehlschrank": {
                 "dbtable": "kuehlschrank",
                 "shellydeviceid": "IDoftheshellydevice"
             }}
