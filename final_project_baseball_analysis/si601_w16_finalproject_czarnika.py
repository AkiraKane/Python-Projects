import csv
import re

def read_baseball_reference():
    names = []
    data = []
    keys = []
    first_line = True
    with open('leagues_MLB_2014-standard-batting_players_standard_batting.csv', 'rU') as csvfile:
        input_file = csv.reader(csvfile, delimiter=',')
        input_file.next()
        for row in input_file:
            player = {}
            if first_line:
                for x in range(0, len(row)-1):
                    row[x] = "".join(c for c in row[x] if c not in ('"'))
                    keys.append(str(row[x]))
                first_line = False
            else:
                row[1] = "".join(c for c in row[1] if c not in ('#','*'))
                name = row[1]
                if name not in names and name != 'Name' and name != 'LgAvg per 600 PA':
                    if int(row[6]) > 100:
                        names.append(name)
                        for key in range(0,len(keys)):
                            if decimal(row[key]):
                                player[keys[key]] = float(row[key])
                            elif numeric(row[key]):
                                player[keys[key]] = int(row[key])
                            else:
                                player[keys[key]] = row[key]
                        player.pop('Rk')
                        data.append(player)
    keys.remove('Rk')
    return keys, names, data

def decimal(inputString):
    return bool(re.search(r'[\d{1,4}]?\.\d{1,4}', inputString))
def numeric(inputString):
    return bool(re.search(r'\d', inputString))

def read_fangraphs(baseball_reference):
    keys = baseball_reference[0]
    names = baseball_reference[1]
    data = baseball_reference[2]
    first_line = True

    with open('FanGraphs Leaderboard.csv', 'rU') as csvfile:
        input_file = csv.reader(csvfile, delimiter=',')
        for row in input_file:
            if first_line:
                for x in range(0, len(row)-1):
                    row[x] = "".join(c for c in row[x] if c not in ('"'))
                    if row[x] == 'Team':
                        row[x] = 'Tm'
                    if row[x] == 'AVG':
                        row[x] = 'BA'
                    if row[x].decode('utf-8-sig') not in keys:
                        keys.append(str(row[x].decode('utf-8-sig')))
                first_line = False
            else:
                name = row[0]
                if name in names:
                    if int(row[3]) > 100:
                        for x in range(0,len(data)):
                            player = data[x]
                            if name == data[x]['Name']:
                                for key in range(28,len(keys)):
                                    if key-20 < 12:
                                        if '%' in row[key-20]:
                                            temp = "".join(c for c in row[key-20] if c not in ('%'))
                                            player[keys[key]] = round(float(temp) / 100,3)
                                        else:
                                            player[keys[key]] = float(row[key-20])
                                    else:
                                        player[keys[key]] = float(row[key-17])
                                data[x] = player
    return keys, data


def filter_data(data):
    result = []
    keys = data[0]
    rows = data[1]
    for row in rows:
        if row.get('WAR'):
            result.append(row)
    data = sorted(result, key=lambda x: float(x['WAR']), reverse=True)
    return keys,data

def write_data(result):
    with open('merged_data.csv', 'wb') as output_file:
            keys = result[0]
            data = result[1]
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)


def main():
    baseball_reference = read_baseball_reference()
    fangraphs_data = read_fangraphs(baseball_reference)
    filtered_data = filter_data(fangraphs_data)
    write_data(filtered_data)

'#Standard boilerplate to call the main() function.'
if __name__ == '__main__':
    main()
