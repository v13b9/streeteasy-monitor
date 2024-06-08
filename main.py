from src.streeteasymonitor.monitor import Monitor

def main():
    with Monitor() as monitor:
        monitor.run()


if __name__ == '__main__':
    main()