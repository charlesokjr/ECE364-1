#######################################################
#   Author:     <Kaiwen Yu>
#   email:      <yu872@purdue.edu>
#   ID:         <ee364e08>
#   Date:       <9/24/2019>
#######################################################

from pprint import pprint

def getDriversFor(carID):
    '''TAke in a car ID and return the set of all drivers who can drive that car'''
    driver_records = []
    name_list = set()
    with open("drivers.dat","r") as nFile:
        contents = nFile.readlines()
    car_list = contents[1].split()
    if carID not in car_list:
        raise ValueError("Oops! No such carID. Please check and try again...")
    else:
        index = 0
        for index in range(len(car_list)):
            if car_list[index] == carID:
                break
        for content in contents[3:]:
            record = content.split("|")
            driver_records.append(record)
        for rec in driver_records:
            if 'X' in rec[index+1]:
                f_name, l_name = rec[0].split()
                #print(rec[0].split())
                name_list.add(f_name + " " + l_name)
    return name_list


def getCommonDriversFor(*args):
    with open("cars.dat","r") as nFile:
        contents = nFile.readlines()
    car_map = {}
    id_list = []
    driver_set = set()
    for content in contents[2:]:
        record = content.split()
        car_ID = record[0]
        car_name = record[2] + " " +record[3]
        car_map[car_name] = car_ID
    for name in args:
        id_list.append(car_map[name])
    with open("drivers.dat","r") as nFile:
        contents1 = nFile.readlines()
    car_list = contents1[1].split()
    index = 0
    index_map = {}
    index_list = []
    driver_records = []
    for index in range(len(car_list)):
        index_map[car_list[index]] = index+1
    for id in id_list:
        index_list.append(index_map[id])
    for content in contents1[3:]:
        record = content.split("|")
        driver_records.append(record)
    for rec in driver_records:
        flag = 1
        for index in index_list:
            if 'X' not in rec[index]:
                flag = 0
                break
        if flag == 1:
            f_name, l_name = rec[0].split()
            #print(rec[0].split())
            driver_set.add(f_name+" "+l_name)
    return driver_set


def getCarsFor(names):
    fianl_map = {}
    driver_records = []
    driver_map = {}
    with open("cars.dat","r") as nFile:
        contents = nFile.readlines()
    car_map = {}
    for content in contents[2:]:
        record = content.split()
        car_ID = record[0]
        car_name = record[2] + " " +record[3]
        car_map[car_ID] = car_name
    with open("drivers.dat","r") as nFile:
        contents = nFile.readlines()
    car_list = contents[1].split()
    for content in contents[3:]:
        record = content.split("|")
        driver_records.append(record)
        d_name = record[0].split()[0] + " "+ record[0].split()[1]
        index_list = []
        for index in range(1,len(record)):
            if 'X' in record[index]:
                index_list.append(index)
            driver_map[d_name] = index_list
    for name in names:
        name_set = set()
        for index in driver_map[name]:
            id = car_list[index - 1]
            carname = car_map[id]
            name_set.add(carname)
        fianl_map[name] = name_set
    return fianl_map


def getBounds():
    with open("signals.dat","r") as nFile:
        contents = nFile.readlines()
    signal_list = contents[0].split()
    signal_map = {}
    final_map = {}
    for content in contents[2:]:
        temp = content.split()
        for index in range(len(temp)):
            data = temp[index]
            key = signal_list[index]
            signal_map.setdefault(key, []).append(float(data))
    for signal in signal_list[1:]:
        all_data = signal_map[signal]
        vmin = round(min(all_data), 3)
        vmax = round(max(all_data), 3)
        mean = round(sum(all_data)/len(all_data), 3)
        final_map[signal] = (vmin, mean, vmax)
    return final_map


def getSampled(name):
    with open("signals.dat", "r") as nFile:
        contents = nFile.readlines()
    signal_list = contents[0].split()
    signal_map = {}
    final_map = {}
    if name not in signal_list:
        raise ValueError("Oops! No such signal name. Please check and try again...")
    for content in contents[2:]:
        temp = content.split()
        for index in range(len(temp)):
            data = temp[index]
            key = signal_list[index]
            signal_map.setdefault(key, []).append(float(data))
    time_list = signal_map['Time']
    data_list = signal_map[name]
    final_list = []
    for index in range(len(time_list)):
        if time_list[index] % 1 == 0:
            final_list.append(data_list[index])
    return final_list


def getDuration(start, end):
    with open("signals.dat", "r") as nFile:
        contents = nFile.readlines()
    signal_list = contents[0].split()
    signal_map = {}
    for content in contents[2:]:
        temp = content.split()
        for index in range(1,len(temp)):
            data = temp[index]
            key = signal_list[index]
            time = temp[0]
            if start <= float(time) <= end:
                signal_map.setdefault(key, []).append(float(data))
    return signal_map


def getValueAt(name, timestamp):
    with open("signals.dat", "r") as nFile:
        contents = nFile.readlines()
    signal_list = contents[0].split()
    signal_map = {}
    for content in contents[2:]:
        temp = content.split()
        for index in range(len(temp)):
            data = temp[index]
            key = signal_list[index]
            signal_map.setdefault(key, []).append(float(data))
    record = signal_map[name]
    time = signal_map['Time']
    flag = 0
    index = 0
    for index in range(len(time)):
        if time[index]== timestamp:
            flag = 2
            break
        if time[index]> timestamp:
            flag = 1
            break
    if flag == 2:
        final_value = record[index]
    else:
        if abs(time[index]-timestamp) < abs(time[index-1]-timestamp):
            final_value = record[index]
        else:
            final_value = record[index-1]
    return final_value


if __name__ == "__main__":
    # pprint(getDriversFor('C-260'))
    pprint(getCommonDriversFor('Chevrolet 1500','Pontiac Montana','Isuzu Rodeo','Geo Tracker'))
    # pprint(getCarsFor({'Sang, Chanell','Chock, Velvet'}))
    # pprint(getBounds())
    # pprint(getSampled('ISO610'))
    # pprint(getDuration(1.0,2.0))
    # pprint(getValueAt('TNP064',1.1))