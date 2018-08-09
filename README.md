# massive-intr-test

Customizer & Visualizer of massive_intr.c by SUNGJAE ;)
* Customize affinity & priority on fork() with ini file.
* Plot the loop count with matplotlib.

### Python requirements:
~~~
# if you didn't install python
sudo apt-get install python3 python3-pip

# need tinker while using matplotlib
sudo apt-get install python3-tk

# virtualenv (optional)
sudo apt-get install virtualenv
virtualenv venv -p python3
source venv/bin/activate

# if you activated virtualenv,
pip install -r requirements.txt
# if not,
pip3 install -r requirements.txt
~~~

### C requirements:
~~~
# do make on ./application
make
~~~

### Simple Run
~~~
# run massive_intr on ./application
sudo ./massive_intr {configfile}
~~~

### Run (with graph)
~~~
# if you activated virtualenv
python run.py {configfile}
# if not,
python3 run.py {configfile}
~~~
