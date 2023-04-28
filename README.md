# command-processor
Run your commands and do math on remote server.

## Installation
```git clone <url> && cd command-processor && pip install -r requirements.txt```<br>
Make a <b>.env</b> file and add the following variable:
```SERVER_ENDPOINT=<your server endpoint>```<br>
Server endpoint format should be like this: ```tcp://host:port```<br>

## Usage
Run ```python server.py``` to establish the connection.<br>
Run ```python client.py <file>``` to send commands to the server.<br>
The file should contain the commands to be executed on the server (in json format according to command.json).<br>
