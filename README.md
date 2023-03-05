
# ISS TRACKER

This project provides relevant data to the user about the ISS. It helps determine the speed and location of the ISS at given times

### Data Used

The data used is accessed from the link https://spotthestation.nasa.gov/trajectory_data.cfm
It is loaded into the script via API request from the Python requests library as follows

All positional data is on kilometers and all velocities and speeds are in km/s.
There is more information about the state vector information on the website linked aboce.

```
import requests
import json

url = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml'
response = requests.get(url)
data = xmltodict.parse(response.text)
```


### Script/Flask App
`iss_tracker.py`
The Flask App I have created runs the app on a local port and actively queries data from the dataset linked above based on the user's curl input.

| Curl Route  | Method   | Output      |
| ----------- | -------- | ----------- |
| `/`      | GET |Entire Dataset       |
| `/epochs`   | GET | All Epochs in the Dataset        |
| `/epochs/<epoch>`| GET | State Vector of the specific Epoch |
| `/epochs/<epoch>/speed` | GET | Speed of the specific Epoch |
| `/help` | GET | Returns help text (as a string) that briefly describes each route |
| `/delete-data` | DELETE | Deletes all data from the dictionary object |
| `/post-data` | POST | Reloads the dictionary object with data from the web |

### INSTRUCTIONS TO RUN


#### Method 1 - Installing Dpendencies Manually

Installations Necessary

In order to start the flask app, the following lines must be executed in the terminal to install dependencies

```
pip3 install flask
```
```
pip3 install requests
```
```
pip3 install xmltodict
```

Run the following code in the terminal to begin the flask app
```
flask --app iss_tracker --debug run
```

Then in a separate terminal run curl commands such as
```
curl 'localhost:5000/help'
```

#### Method 2 - Pulling prebuilt Docker image from Dockerhub and running Flask app

Run the following commands in terminal:

Pull docker image from docker hub
```
docker pull lucalabardini/iss_tracker:hw05
```

Run the Flask app using the prebuilt image
```
docker run -it --rm -p 5000:5000 lucalabardini/iss_tracker:hw05
```

Then in a separate terminal run curl commands such as
```
curl 'localhost:5000/help'
```

#### Method 3 - Building image from dockerfile

Make sure you are in the directory with the dockerfile and iss_tracker.py script

Run ls and make sure output looks like this
```
ls
```
```
Dockerfile README.md iss_tracker.py
```

Build your image using the dockerfile
```
docker build -t <username>/iss_tracker:<tag> .
```

Run the Flask app using the newly built image
```
docker run -it --rm -p 5000:5000 <username>/iss_tracker:<tag>
```

Then in a separate terminal run curl commands such as
```
curl 'localhost:5000/help'
```


### Example Input/Output and Usage

#### Important Note
Data is loaded into the flask app from the web upon running the app. All curl commands will work when the flask app starts.



Below are examples of certain inputs that the user can put into the separate terminal

Running the command:
```
curl 'localhost:5000/'
```
Should return the whole dataset which looks something like
```
[
  {
    "EPOCH": "2023-063T11:59:00.000Z",
    "X": {
      "#text": "2511.5681106492402",
      "@units": "km"
    },
    "X_DOT": {
      "#text": "5.2410359153923798",
      "@units": "km/s"
    },
    "Y": {
      "#text": "-5991.3267501460596",
      "@units": "km"
    },
    "Y_DOT": {
      "#text": "0.32894397165270001",
      "@units": "km/s"
    },
    "Z": {
      "#text": "1991.1683453687999",
      "@units": "km"
    },
    "Z_DOT": {
      "#text": "-5.57976406061041",
      "@units": "km/s"
    }
  },
  {
    "EPOCH": "2023-063T12:00:00.000Z",
    "X": {
      "#text": "2820.04422055639",
      "@units": "km"
    },
    "X_DOT": {
      "#text": "5.0375825820999403",
      "@units": "km/s"
    },
    "Y": {
      "#text": "-5957.89709645725",
      "@units": "km"
    },
    "Y_DOT": {
      "#text": "0.78494316057540003",
      "@units": "km/s"
    },
    "Z": {
      "#text": "1652.0698653803699",
      "@units": "km"
    },
    "Z_DOT": {
      "#text": "-5.7191913150960803",
      "@units": "km/s"
    }
  }
]
```

Running the command:
```
curl 'localhost:5000/epochs'
```
Should return a list of all the epoch values in the dataset which looks something like this but much longer
```
[
  "2023-063T11:31:00.000Z",
  "2023-063T11:35:00.000Z",
  "2023-063T11:39:00.000Z",
  "2023-063T11:43:00.000Z",
  "2023-063T11:47:00.000Z",
  "2023-063T11:51:00.000Z",
  "2023-063T11:55:00.000Z",
  "2023-063T11:59:00.000Z",
  "2023-063T12:00:00.000Z"
]
```
Query parameters for list of epoch values in the set
```
curl 'localhost:5000/epochs?limit=int&offset=int'
```
limit sets the number of results returned by the app. offset sets the starting index of the epochs to be printed. The query will only accept ints. Any other type will cause an error.
For example
```
curl 'localhost:5000/epochs?limit=5&offset=2'
```
Will return
```
[
  "2023-055T12:08:00.000Z",
  "2023-055T12:12:00.000Z",
  "2023-055T12:16:00.000Z",
  "2023-055T12:20:00.000Z",
  "2023-055T12:24:00.000Z"
]
```


Running the command:
```
curl 'localhost:5000/epochs/<epoch>'
```
Should return the state vector of the specific epoch specified in the angled brackets which will look like this
```
{
  "EPOCH": "2023-063T12:00:00.000Z",
  "X": {
    "#text": "2820.04422055639",
    "@units": "km"
  },
  "X_DOT": {
    "#text": "5.0375825820999403",
    "@units": "km/s"
  },
  "Y": {
    "#text": "-5957.89709645725",
    "@units": "km"
  },
  "Y_DOT": {
    "#text": "0.78494316057540003",
    "@units": "km/s"
  },
  "Z": {
    "#text": "1652.0698653803699",
    "@units": "km"
  },
  "Z_DOT": {
    "#text": "-5.7191913150960803",
    "@units": "km/s"
  }
}
```
Running the following command:
```
curl 'localhost:5000/epochs/<epoch>/speed'
```
Should return the speed of the epoch specified in the angled brackets which will look like this
```
{
  "Speed (km/s)": 7.661757196327827
}
```

Running the following command:
```
curl -X DELETE 'localhost:5000/delete-data'
```
Should return one of
```
Data deleted successfully
```
Or
```
Data has already been deleted. Repost first using /post-data
```
This means that the data has been deleted from the App and must be reloaded using the /post-data route


Running the following command:
```
curl -X POST 'localhost:5000/post-data'
```
Should return
```
Data Posted Successfully
```
This means that the data was reloaded into the flask app and all of the other routes will now work properly again
