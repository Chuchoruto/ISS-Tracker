from flask import Flask, request
import xmltodict
import requests
import math

app = Flask(__name__)

data = {}


def get_data() -> list:
    """
    This function returns all of the data in the set

    Args:
        NA
        
    Returns:
        A list of dictionaries that represent the data in the set of ISS Locations
    """

    url = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml'
    response = requests.get(url)
    data = xmltodict.parse(response.text)
    return data['ndm']['oem']['body']['segment']['data']['stateVector']

data = get_data()

# This method is called in the default curl command w/o more arguments
@app.route('/', methods = ['GET'])
def location() -> list:
    """
    This function returns all of the data in the set

    Args:
        NA
        
    Returns:
        A list of dictionaries that represent the data in the set of ISS Locations
    """
    try:
        global data
        return data
    except NameError:
        return "Data has been deleted and must be reposted first using /post-data\n"
    return data

@app.route('/epochs', methods = ['GET'])
# Returns the list of all EPOCH names when called
def allEpochs() -> list:
    """
    This function returns all of the EPOCHs in the set

    Args:
        NA
        
    Returns:
        A list of Strings representing the EPOCHs in the set
    """
    global data
    
    try:
        limit = int(request.args.get('limit', len(data)))
    except ValueError:
        return "Bad input. Please enter an int\n",400
    except NameError:
        return "Data has been deleted and must be reposted first using /post-data\n"

    try:
        offset = int(request.args.get('offset', 0))
    except ValueError:
        return "Bad input. Please enter an int\n",400

    
    epochs = []
    totalResults = 0
    index = 0
    for e in data:
        if(limit == totalResults):
            break
        if(index >= offset):
            epochs.append(e["EPOCH"])
            totalResults+= 1
            
        index += 1
    return epochs


# Returns the state vector for a sepcific EPOCH when called
@app.route('/epochs/<epoch>', methods = ['GET'])
def specEpoch(epoch: str) -> dict:
    """
    This takes a specific EPOCH string value and returns its state vector below

    Args:
        (String) sepoch: EPOCH string value for a specific time recorded for the ISS
        
    Returns:
        A dictionary of relevant data for the given epoch
    """
    global data

    try:
        for e in data:
            if (e["EPOCH"] == epoch):
                return e
    except NameError:
        return "Data has been deleted and must be reposted first using /post-data\n"
    
    return "Error: Epoch not found\n"



@app.route('/epochs/<epoch>/speed', methods = ['GET'])
def epochSpeed(epoch: str) -> dict:
    """
    This takes a specific EPOCH string value and returns the speed of the ISS at the given epoch

    Args:
        (String) epoch: EPOCH string value for a specific time recorded for the ISS
        
    Returns:
        The speed of the ISS at the given EPOCH
    """
    
    global data
    try:
        for e in data:
            if (e["EPOCH"] == epoch):
                xV = float(e["X_DOT"]["#text"])
                yV = float(e["Y_DOT"]["#text"])
                zV = float(e["Z_DOT"]["#text"])
                speed = math.sqrt(xV*xV + yV*yV + zV*zV)
                return {"Speed (km/s)": speed}
    except NameError:
        return "Data has been deleted and must be reposted first using /post-data\n"
    
    return "Error: Epoch not found\n"


@app.route('/delete-data', methods = ['DELETE'])
def deleteData() -> str:
    """
    This Deletes the global data dictionary object

    Args:
        NA
        
    Returns:
        Data Deleted Successfully or Data Already Deleted if calling the data variable causes a NameError
    """
    global data
    try:
        del data
    except NameError:
        return "Data has already been deleted. Repost first using /post-data\n"
    return "Data deleted successfully\n"



@app.route('/post-data', methods = ['POST'])
def postData() -> str:
    """
    This Posts data to the global data dictionary object

    Args:
        NA
        
    Returns:
        Data Posted Successfully after setting the global data variable to the dataset requested
    """
    global data
    data = get_data()
    
    return "Data Posted Successfully\n"

@app.route('/help', methods=['GET'])
def help() -> str:
    """
    This function returns a brief description of all available routes (plus their methods) for this API.

    Args:
        NA
        
    Returns:
        A string of human readable text that lists all available routes and their methods.
    """
    return '''
    Available routes:
    
    GET /
    Returns all data in the set.
    
    GET /epochs
    Returns a list of all EPOCHs in the set.

    GET /epochs?limit=int&offset=int
    Returns a list of EPOCHs in the set starting at the offset index and printing a total of limit results.
    
    GET /epochs/<epoch>
    Returns the state vector for a specific EPOCH.
    
    GET /epochs/<epoch>/speed
    Returns the speed of the ISS at a specific EPOCH.
    
    POST /post-data
    Posts data to the global data dictionary object.
    
    DELETE /delete-data
    Deletes the global data dictionary object.
    '''


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
