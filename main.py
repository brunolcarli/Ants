from core.engine import run
from core.settings import ANT_COUNT



if __name__ == '__main__':
    print('Initializing simulation')
    print(f'MAX ant count: {ANT_COUNT}')
    run()