#!/usr/bin/python2.7

from bs4 import BeautifulSoup
import os.path
import sys

def print_help():
    print " Usage: python nmap_parse.py [nmap_file.xml] [output_file.csv]"
    print ""
    print " Examples:"
    print "",
    print "="*78
    print "  python nmap_parse.py 192_168_1_0#24.xml out.csv"
    print ""

def main():
    # handle bad run
    num_args = len(sys.argv)
    if num_args < 2 or num_args > 3:
        print_help()
        exit(0)
    
    # handle filename arguments
    nmap_file = sys.argv[1]
    if num_args == 3:
        out_filename = sys.argv[2]
    else:
        out_filename = "out.csv"
    
    # read and parse file data
    try:
        if not (os.path.exists(out_filename)):
            o = open(out_filename, 'w')
            o.write("ip,proto,port,service\n")
        else:
            o = open(out_filename, 'a')

    
        # get data
        nmap_file_data = open(nmap_file,'r').read()
        xml_data = BeautifulSoup(nmap_file_data, 'lxml')
    
        # parse data
        for host in xml_data.find_all('host'):
            ip = host.address['addr']
            print ip
            for port in host.find_all('port'):
                if port.state['state'] == "open":
                    for service in port.find_all('service'):
                        out_data = "%s,%s,%s,%s\n" % (\
                                ip, port['protocol'], \
                                port['portid'], \
                                service['name'])
                        o.write(out_data)
        # cleanup
        o.close()
    except Exception as e:
        print "An error has occurred"
        print "msg: %s" % (e)

if __name__ == '__main__':
    main()
