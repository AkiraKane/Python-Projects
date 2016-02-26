import re
import urlparse
import csv

#Read data in
#Call is_valid & extract_ip functions
def read_input():
    input_file = open('access_log.txt', 'rU')
    valid = open('valid_access_log_czarnika.txt', 'w')
    invalid = open('invalid_access_log_czarnika.txt', 'w')
    invalid_ip = []
    ip_attempt_count = []
    for row in input_file:
        result = is_valid(row)
        if result:
            valid.write(row)
        else:
            invalid.write(row)
            i = extract_ip(row)
            if i not in invalid_ip:
                invalid_ip.append(i)
                ip_attempt_count.append({'IP Address': i, 'Attempts' :1})
            else:
                for y in ip_attempt_count:
                    if i == y['IP Address']:
                        y['Attempts'] += 1


    result = sorted(ip_attempt_count, key=mykey, reverse=True)
    return result

#Sorting Helper
def mykey(x):
    return x['Attempts'],[-ord(c) for c in x['IP Address']]

#Determine if line is valid or invalid
def is_valid(line):
    result = False

    #Verb POST|GET|HEAD|CONNECT
    verb = re.search(r'(POST|GET|HEAD)',line)
    connect = re.search(r'CONNECT', line)
    if verb:
        #Status Code 2xx,3xx,5xx
        status_code = re.search(r'(http://|https://).*HTTP/1.\d"\s(2\d.|3\d.|5\d.)', line, re.IGNORECASE)
        if status_code:
            #Verify URL http|https
            url = re.search(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}[\./][a-z]{2,6}'
                            r'\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)', line)
            #Verfiy URL with no .domain
            url2 = re.search(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}[\./:]', line)
            if url:
                o = urlparse.urlparse(url.group())
                queries = o.query
                q = urlparse.parse_qsl(queries)
                temp = True
                for x in q:
                    #Verify Query Results > 80
                    if len(x[1]) > 80:
                        temp = False
                if temp:
                    result = True
            elif url2:
                o = urlparse.urlparse(url2.group())
                queries = o.query
                q = urlparse.parse_qsl(queries)
                temp = True
                for x in q:
                    #Verify Query Results > 80
                    if len(x[1]) > 80:
                        temp = False
                if temp:
                    result = True
    if connect:
        #Status Code 2xx,3xx,5xx
        status_code = re.search(r'HTTP/1.\d"\s(2\d.|3\d.|5\d.)', line)
        if status_code:
            result = True
    return result

#Extract IP
def extract_ip(line):
    return re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line).group()

#Write Results
def write_ip(result):
    with open('suspicious_ip_summary_czarnika.csv', 'wb') as output_file:
            keys = ['IP Address', 'Attempts']
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(result)

#Czarnika Main
def main():
    result = read_input()
    write_ip(result)


# Standard boilerplate to call the main() function.
if __name__ == '__main__':
    main()