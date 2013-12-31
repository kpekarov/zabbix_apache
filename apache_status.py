#!/usr/bin/env python

import re
import sys
import urllib
import socket
from optparse import OptionParser

def getURL(WebServer,Port,URL):
    try:
        # Setup connection string
        ConnectionString = ("http://%s:%s%s") % (WebServer, Port, URL)

        conn = urllib.urlopen(ConnectionString)
        URLresponse = conn.read()

        # Clean up the connection
        conn.close()

        # The response to the function is the output of the URL called
        return URLresponse

    # Catch all exceptions
    except:
        print "Error getting URL"
#flags=(re.IGNORECASE|re.DOTALL)
def get_metric(status_page, reg_base, flags=(re.IGNORECASE)):
  reg_comile = re.compile(reg_base, flags)
  match = reg_comile.search(status_page)
  if match:
    return match.group("metric")
  else:
    return False

if __name__ == "__main__":

  parser = OptionParser()

  parser.add_option("-u", "--url",     action='store', type='string',  dest='url',     default="127.0.0.1", help="url")
  parser.add_option("-s", "--stat",    action='store', type='string',  dest='stat',    default="/server-status?auto", help="status page url")
  parser.add_option("-p", "--port",    action='store', type='int',     dest='port',    default=80, help="port")
  parser.add_option("-t", "--timeout", action='store', type='int',     dest='timeout', default=5, help="timeout")
  parser.add_option("-m", "--metric",  action='store', type='string',  dest='metric',  default="", help="metrics name")
  parser.add_option("-o", "--out",     action='store', type='string',  dest='out',     default="stdout", help="stdout, file")
  parser.add_option("-r", "--print",   action='store', type='string',  dest='pr_val',  default="value", help="value, all")
  parser.add_option("-i", "--inp",     action='store', type='string',  dest='inp',     default="web", help="file, web")
  parser.add_option("-f", "--file",    action='store', type='string',  dest='fl_name', default="/tmp/apache_stat", help="file name")

  (options, args) = parser.parse_args()
  url = options.url
  port = options.port
  timeout = options.timeout
  metric = options.metric
  out = options.out
  stat = options.stat
  inp = options.inp
  fl_name = options.fl_name
  pr_val = options.pr_val
  output = False

  socket.setdefaulttimeout(timeout)

  if inp=="web":
    status_page = getURL(url,port,stat)
  if inp=="file":
    fd = open(fl_name, "r")
    status_page = fd.read()

  if out=="file":
    status_page = getURL(url,port,stat)
    fd = open(fl_name, "w")
    fd.write(status_page)

  sc_board_regexp = "Scoreboard: (?P<metric>(.*))"

  REQ_MATRIX = {
    "TotalAccesses":                {"reg_exp":"Total accesses: (?P<metric>\d+)"},
    "TotalTraffic":                 {"reg_exp":"Total kBytes: (?P<metric>\d+.\d+)"},
    "ReqPerSec":                    {"reg_exp":"ReqPerSec: (?P<metric>(\d+.\d+|.\d+))"},
    "BytesPerSec":                  {"reg_exp":"BytesPerSec: (?P<metric>\d+.\d+|\d+)"},
    "BytesPerReq":                  {"reg_exp":"BytesPerReq: (?P<metric>\d+.\d+|\d+)"},
    "BusyWorkers":                  {"reg_exp":"BusyWorkers: (?P<metric>\d+)"},
    "IdleWorkers":                  {"reg_exp":"IdleWorkers: (?P<metric>\d+)"},
    "WaitingForConnection":         {"reg_exp":sc_board_regexp, "key":"_"},
    "StartingUp":                   {"reg_exp":sc_board_regexp, "key":"S"},
    "ReadingRequest":               {"reg_exp":sc_board_regexp, "key":"R"},
    "SendingReply":                 {"reg_exp":sc_board_regexp, "key":"W"},
    "KeepAlive":                    {"reg_exp":sc_board_regexp, "key":"K"},
    "DNSLookup":                    {"reg_exp":sc_board_regexp, "key":"D"},
    "ClosingConnection":            {"reg_exp":sc_board_regexp, "key":"C"},
    "Logging":                      {"reg_exp":sc_board_regexp, "key":"L"},
    "GracefullyFinishing":          {"reg_exp":sc_board_regexp, "key":"G"},
    "IdleCleanupOfWorker":          {"reg_exp":sc_board_regexp, "key":"I"},
    "OpenSlotWithNoCurrentProcess": {"reg_exp":sc_board_regexp, "key":"."},
  }

  if metric in REQ_MATRIX:

    reg_base = REQ_MATRIX[metric]["reg_exp"]

    output = get_metric(status_page, reg_base)

    if "key" in REQ_MATRIX[metric] and output:
      output = len(re.findall(REQ_MATRIX[metric]["key"], output))

  if pr_val=="all":
    output = status_page

  print output

