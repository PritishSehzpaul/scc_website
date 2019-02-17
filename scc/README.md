### SCC(Student Counselling Cell) website to gauge the student's stress level and taking appropriate measures.

#### Dependencies
- Flask - `pip install flask=1.0.2`
- HTML5
- Bootstrap
- FontAwesome

#### Build version
- Python - 3.7.2
- Flask - 1.0.2

#### Steps to start development
1. Clone the repo - `git clone https://github.com/PritishSehzpaul/scc_website.git`
2. Move to the cloned repository's directory
3. Move to `scc_website/scc` directory - 
```sh
cd scc_website\scc
```
4. To run the application you can either use the flask command or python’s `-m` switch with Flask. Before you can do that you need to tell your terminal the application to work with by exporting the `FLASK_APP` environment variable:
```sh
$ export FLASK_APP=views.py
$ flask run
 * Running on http://127.0.0.1:5000/
```
If you are on Windows, the environment variable syntax depends on command line interpreter. On Command Prompt:
```cmd
set FLASK_APP=views.py
```
And on PowerShell:
```powershell
PS $env:FLASK_APP = "views.py"
```
Alternatively you can use `python -m flask`:
```sh
$ export FLASK_APP=views.py
$ python -m flask run
 * Running on http://127.0.0.1:5000/
```
5. To run the server in a debug mode for development set `FLASK_DEBUG` environment variable in the terminal:
```sh
export FLASK_DEBUG=development
```
And on Windows command prompt use:
```cmd
set FLASK_DEBUG=development
```
6. To set the host server URL and port use:
```sh
$ python -m flask run --host=0.0.0.0 --port=8000
 * Running on http://0.0.0.0:8000/
```
Or
```sh
$ flask run --host=0.0.0.0 --port=8000
 * Running on http://0.0.0.0:8000/
```

### References:
1. Refer to [Flask's quickstart guide](http://flask.pocoo.org/docs/1.0/quickstart/) for more info regarding flask 
