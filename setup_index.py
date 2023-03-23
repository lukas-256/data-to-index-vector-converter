import sys, getopt, os
import itertools, threading, time
from llama_index import SimpleDirectoryReader, GPTSimpleVectorIndex

# store your api key as 'OPENAI_API_KEY' or
# os.environ['OPENAI_API_KEY'] = 'api key'

# global variable to track loading state
done = False

# function which will initialize the vector index file
# if the file already exists or there is no 'Data' directory in the current path the program will exit
def initialize_index(index_file_name):

    if os.path.exists(index_file_name):
        sys.exit('File already exists ...')
    else:
        if os.path.exists('./Data'):
            documents = SimpleDirectoryReader('./Data').load_data()
            print('Loaded ' + str(len(documents)) + ' file(s) ...')

            # start a background thread which will emulate a loading circle
            t = threading.Thread(target=animate)
            t.daemon = True
            t.start()
            
            # create the index vector file with the help of openai's text-ada
            index = GPTSimpleVectorIndex(documents)
            index.save_to_disk(index_file_name)

            global done
            done = True
        else:
            sys.exit('No \'Data\' directory found ... maybe create one?' )

# function used for emulating a loading circle
def animate():
    global done
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)

# the main program
if __name__ == '__main__':

    index_file_name = 'index.json'

    opts, args = getopt.getopt(sys.argv[1:],'ui:',['file='])
    
    # parse command line arguments. if no input file specified then use default name index.json
    for opt, arg in opts:
        if opt in ('-i', '--file'):
            index_file_name = arg
        elif opt == '-u':
            sys.exit(sys.argv[0] + ' [-i <index_file_name> | --file <index_file_name>]')
            
    initialize_index(index_file_name)
    print('\rSuccessfully created index with name: ' + index_file_name)
