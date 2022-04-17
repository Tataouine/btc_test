#!/usr/bin/python

import time
import datetime as dt
import smtplib
import os
import multiprocessing
from multiprocessing import Pool
from multiprocessing import cpu_count
import pandas as pd
from bit import Key
import random
import bit


class go():
    def __init__(self):
        self.num_cpu = os.cpu_count()
        self.cores = 4

    def num_of_cores(self):
        self.cores = input(
            f"\nNumber of available cores: {self.num_cpu}\n \n How many cores to be used? \n \n Type something>")


# valeur maximum possible
max_value = 115792089237316195423570985008687907852837564279074904382605163141518161494336
max_value_by_core = max_value // 12

startvalue = int('8000000000000000', 16)
endvalue =   int('ffffffffffffffff', 16)

diff = endvalue - startvalue



def run(cores, numero_core, file_value):
    value_by_core = diff // cores
    LOG_EVERY_N = 100000
    start_time = dt.datetime.today().timestamp()
    start_value_actual_core = (value_by_core * numero_core) + startvalue
    end_value_actual_core = (
        value_by_core * numero_core) + value_by_core

    i = 0
    print("Core " + str(numero_core) + ":  Generating Private Key..")
    while True:
        i = i+1
        pvk = random.randrange(startvalue, endvalue)
        key = Key().from_int(pvk)

        

        if key.address.startswith('16jY7qLJ'):
            print("& private : "+key.to_wif()+" public = " +
                  key.address + " segwit_address = " + key.segwit_address)
            f = open("address.txt", "a")
            f.write("private : "+key.to_wif()+" public = " + key.address)
            f.close()
            print("\n continue...\n")
            if str(key.address) == '16jY7qLJnxb7CHZyqBP8qca9d51gAjyXQN':
                print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&& private : "+key.to_wif() +
                      " public = " + key.address + " segwit_address = " + key.segwit_address)
                f = open("address.txt", "a")
                f.write("private : "+key.to_wif()+" public = " + key.address)
                f.close()
                break

        if (i % LOG_EVERY_N) == 0:
            time_diff = dt.datetime.today().timestamp() - start_time
            print('Core :'+str(numero_core)+" K/s = " + str(i / time_diff))


        # print ('private : '+key.to_wif()+" public = " + key.address + " segwit_address = " + key.segwit_address +"/n")


if __name__ == "__main__":
    jobs = []
    obj = go()
    #obj.num_of_cores()
    try:
        for numero_core in range(obj.cores):
            file_value = pd.read_csv(open('bit.txt', 'r'))
            p = multiprocessing.Process(
                target=run, args=(obj.cores, numero_core, file_value))
            jobs.append(p)
            p.start()
    except KeyboardInterrupt:
        print("\n\nCtrl+C pressed. \nexitting...")
        exit()
    else:
        exit()
