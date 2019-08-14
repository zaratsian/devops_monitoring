import re
import psutil
from flask import Flask, jsonify, Response

app = Flask(__name__)

@app.route('/metrics')
def metrics():
    
    prometheous_metrics = []
    
    # Get total memory per VM/Server
    used_memory_pct = round(psutil.virtual_memory().percent / float(100), 4)
    prometheous_metrics.append('gce_memory_total {}'.format(used_memory_pct))
    
    # Get pid memory for all processes
    for proc in psutil.process_iter():
        try:
            processName = re.sub('[^a-zA-Z0-9_]','_',proc.name())
            processID = proc.pid
            processMemory = round(proc.memory_percent(), 4)
            prometheous_metrics.append('gce_process_{}_memory {}'.format(processName, processMemory))
        except Exception as e:
            print('[ EXCEPTION ] {}'.format(e))
    
    return Response('\n'.join(prometheous_metrics), mimetype="text/plain")


if __name__ == '__main__':
    app.run('0.0.0.0', 9090, threaded=True)

#ZEND
