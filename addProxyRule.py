import yaml
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyEventHandler(FileSystemEventHandler):

    def on_modified(self, event):
        path = os.path.abspath(event.src_path)

        # your config file path example：
        # proxyFile = (r'/Users/woodii/.config/clash/hrProxy.yaml')
        proxyFile = (r'your config file path')
        # Rules to be added
        newRules = [
            # example
            # 'DOMAIN-SUFFIX,gs-robot.com,DIRECT'
        ]
        if path == proxyFile:
            fileHasBeenChang = False

            with open(proxyFile) as readFile:
                fruits_list = yaml.load(readFile, Loader=yaml.FullLoader)

                for rule in newRules:
                    if rule not in fruits_list['rules']:
                        fruits_list['rules'].append(rule)
                        fileHasBeenChang = True
                if fileHasBeenChang:
                    with open(proxyFile, 'w') as writeFile:
                        yaml.dump(fruits_list, writeFile)


if __name__ == "__main__":
    # clash Directory
    # example
    # proxyFile = (r'/Users/woodii/.config/clash')
    proxyFile = (r'your clash directory')
    event_handler = MyEventHandler()
    observer = Observer()
    observer.schedule(event_handler, proxyFile, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
