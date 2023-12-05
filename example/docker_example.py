
def main():
    import logging
    import time
    for i in range(1, 101):
        logger = logging.getLogger("easier-docker")
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s ==> %(message)s')
        logger.info(f'sleep 30s, times:{i}')
        time.sleep(30)


if __name__ == '__main__':
    main()
