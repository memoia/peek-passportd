import re
import calendar


def prepare_record(dct):
    """Remove ruby-style prefixes/brackets from field names"""
    def get_field_name(key):
        match = re.match(r'\S+\[(\S+)\]$', key)
        return match.group(1) if match else key
    return {get_field_name(k): v for (k, v) in dct.iteritems()}


def date_bounds(dt):
    """Given a datetime instance, return unix timestamp boundaries"""
    start = calendar.timegm(dt.date().timetuple())
    return (start, start + 86400)
