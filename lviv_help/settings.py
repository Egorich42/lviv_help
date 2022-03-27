
def create_logger(name):
    import logging

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    return logging.getLogger(name)
