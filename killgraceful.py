import argparse
import os
import signal
import sys
import time

def kill_gracefully(pid, signals, sleep_time, verbose):
    for sig in signals:
        if verbose > 1:
            print(f"Trying: kill -{sig} {pid}")
        try:
            os.kill(pid, sig)
        except OSError as e:
            if verbose > 1:
                print('Kill error. Job done? Check it out.')
            break
        if verbose > 1:
            print(f"Sleeping for {sleep_time}")
        time.sleep(sleep_time)

def main():
    parser = argparse.ArgumentParser(description='Send signals to kill gracefully a process.')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='Turn verbose mode on (cumulative).')
    parser.add_argument('-t', '--time', type=int, default=5, help='Set the interval between signals in seconds. (default 5s)')
    parser.add_argument('-p', '--pid', type=int, required=True, help='Set the PID of the process to kill gracefully')
    parser.add_argument('-s', '--signals', type=int, choices=range(1, 6), default=4,
                        help='Set the numbers of signals to try. The order is: 1: SIGKILL, 2: SIGTERM SIGKILL, \
                        3: SIGTERM SIGINT SIGKILL, 4: SIGTERM SIGINT SIGQUIT SIGKILL (default), \
                        5: SIGTERM SIGINT SIGQUIT SIGABRT SIGKILL')
    args = parser.parse_args()

    signal_map = {
        1: [signal.SIGKILL],
        2: [signal.SIGTERM, signal.SIGKILL],
        3: [signal.SIGTERM, signal.SIGINT, signal.SIGKILL],
        4: [signal.SIGTERM, signal.SIGINT, signal.SIGQUIT, signal.SIGKILL],
        5: [signal.SIGTERM, signal.SIGINT, signal.SIGQUIT, signal.SIGABRT, signal.SIGKILL],
    }

    if args.verbose > 0:
        print(f"Starting killgracefully.py script")
        print(f"Verbose level: {args.verbose}")
        print(f"PID of the process to kill: {args.pid}")
        print(f"Number of signals to send: {args.signals}")
        if args.verbose > 1:
            sig_names = [signal.Signals(sig).name for sig in signal_map[args.signals]]
            print(f"Signals to send: {', '.join(sig_names)}")
        print(f"Time between signals: {args.time}")

    kill_gracefully(args.pid, signal_map[args.signals], args.time, args.verbose)

if __name__ == "__main__":
    main()
