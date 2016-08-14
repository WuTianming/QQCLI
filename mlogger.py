import time
from commander import *
from functools import partial
import json

def str_len(str):  
    try:  
        row_l=len(str)  
        utf8_l=len(str.encode('utf-8'))  
        return (utf8_l-row_l)//2+row_l  
    except:  
        return row_l
    return row_l

class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

levels = Enum(('w', 'i', 'e', 'v', 'r', 's'))

_supressed_tags = set()
_supressed_levels = set()
_sav = []

def log(tag, s, pretty, level, save=False, cmdr=None):
    if save:
        _sav.append((time.strftime('%H:%M:%S'), level, tag, s))
    if tag in _supressed_tags or level in _supressed_levels:
        return
    if level == levels.w:
        color = 'yellow'
    elif level == levels.i:
        color = 'magenta'
    elif level == levels.e:
        color = 'error'
    elif level == levels.v:
        color = 'normal'
    elif level == levels.r:
        color = 'green'
    elif level == levels.s:
        color = 'blue'
    if cmdr == None:
        print(pretty.format(time=time.strftime('%H:%M:%S'), tag=tag, msg=s))
    else:
        cmdr.output(pretty.format(time=time.strftime('%H:%M:%S'), tag=tag + (11 - str_len(tag)) * ' ', msg=s), color)

pretty_warning = (
    'WARN {time} {tag} {msg}')
pretty_information = (
    'INFO {time} {tag} {msg}')
pretty_error = (
    'EROR {time} {tag} {msg}')
pretty_verbose = (
    'VERB {time} {tag} {msg}')
pretty_receive = (
    'RECV {time} {tag} {msg}')
pretty_send = (
    'SEND {time} {tag} {msg}')

w = partial(log, pretty=pretty_warning, level=levels.w)
i = partial(log, pretty=pretty_information, level=levels.i)
e = partial(log, pretty=pretty_error, level=levels.e)
v = partial(log, pretty=pretty_verbose, level=levels.v)
r = partial(log, pretty=pretty_receive, level=levels.r)
s = partial(log, pretty=pretty_send, level=levels.s)

def supress_tag(tag):
    _supressed_tags.add(tag)

def supress_level(level):
    _supressed_levels.add(level)

def unsupress_tag(tag):
    _supressed_tags.discard(tag)

def unsupress_level(level):
    _supressed_levels.discard(level)

def unsupress_all_tags():
    _supressed_tags.clear()

def unsupress_all_levels():
    _supressed_levels.clear()

def output(*s, sep=' ', end='\n', file=None, flush=False):
    v('print', sep.join(map(lambda x: str(x), s)))

def save(filename=None, supressed_tags=None,
         supressed_levels=None, prompt=True):
    if filename == None:
        filename = './mlogger_%s.log' % (time.strftime('%Y_%m_%d_%H_%M_%S'))
    if (supressed_tags or supressed_levels) == None:
        with open(filename, 'w') as f:
            json.dump(_sav, f, ensure_ascii=False, indent=4)
    else:
        if supressed_levels == 'default':
            supressed_levels = _supressed_levels
        if supressed_tags == 'default':
            supressed_tags = _supressed_tags
        supressed_levels = supressed_levels or ()
        supressed_tags = supressed_tags or ()

        s = [i for i in _sav
            if not(i[1] in supressed_levels or i[2] in supressed_tags)]
        with open(filename, 'w') as f:
            json.dump(s, f, ensure_ascii=False, indent=4)
    if prompt:
        i('logger', 'Save file created: '+filename, save=False)
