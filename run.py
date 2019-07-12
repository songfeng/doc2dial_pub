#!/usr/bin/env python3
# import cf_deployment_tracker
import os
from pathlib import Path
import sys
import argparse


if __name__ == '__main__':
    if sys.version_info < (3, 0):
        raise RuntimeError('It requires Python 3.')
    parser = argparse.ArgumentParser()
    parser.add_argument('--domain', default='demo', type=str)
    parser.add_argument('--port', default=8081, type=int)
    parser.add_argument('--dburi', default='mongodb://localhost', type=str)
    args = parser.parse_args()
    os.environ['domain'] = args.domain
    os.environ['dburi'] = args.dburi
    from webapp import create_app, socketio
    app = create_app(debug=True)
    socketio.run(app, host='0.0.0.0', port=args.port)
