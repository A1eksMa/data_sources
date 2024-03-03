class UpdateSource():
    '''
    This class contains methods of updating sources
    '''
    def __init__(self):
        logger.info('Init UpdateSource() object')
        self.src_arc_dir = ''
        self.src_cur_dir = ''
        self.src_upd_dir = ['/home/sky/test/', '/home/sky/','/home/sky/fall']

    def check_paths(self, paths_list):
        '''
        Check, that folders exist
        '''
        logger.info('Start "check_paths" function')

        valid_paths_list = []

        for i in paths_list:

            logger.info(f'Start validation {i} path...')

            if os.path.exists():
                logger.info(f'Validation success. Path {i} exist')
                valid_paths_list.append(i)

            else:
                logger.info(f'Validation failed. Path {i} not exist')

        return valid_paths_list
