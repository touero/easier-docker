
def main():
    import logging
    import time
    for i in range(1, 101):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info(f'sleep 30s, times:{i}')
        time.sleep(30)


if __name__ == '__main__':
    main()
