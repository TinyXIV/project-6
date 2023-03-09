"""
Nose tests for test_mymongo.py

Write your tests HERE.
"""

from mymongo import brevets_insert, brevets_fetch, collection
import arrow
import nose    # Testing framework
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)

def test_insert():
    start_time = arrow.get("2021-01-20T05:00:00")
    checkpoints = [
        {'km': "0", 'open_time': "2021-01-20T05:00", 'close_time': "2021-01-20T06:00"},
        {'km': "50", 'open_time': "2021-01-20T06:28", 'close_time': "2021-01-20T08:30"},
        {'km': "150", 'open_time': "2021-01-20T09:25", 'close_time': "2021-01-20T15:00"},
        {'km': "200", 'open_time': "2021-01-20T10:53", 'close_time': "2021-01-20T18:30"}
    ]
    start_time_str = start_time.format("YYYY-MM-DDTHH:mm")
    brevets_insert("200", start_time_str, checkpoints)

    brevet = brevets_fetch()
    start_time_str = start_time.format("YYYY-MM-DDTHH:mm")
    brevets_insert("200", start_time_str, checkpoints)
    
    brevet = brevets_fetch()
    assert brevet is not None
    assert brevet[1] == "2021-01-20T05:00"

    checkpoint_1 = brevet[2][0]
    assert checkpoint_1['km'] == "0"
    assert checkpoint_1['open_time'] == "2021-01-20T05:00"
    assert checkpoint_1['close_time'] == "2021-01-20T06:00"

    checkpoint_2 = brevet[2][1]
    assert checkpoint_2['km'] == "50"
    assert checkpoint_2['open_time'] == "2021-01-20T06:28"
    assert checkpoint_2['close_time'] == "2021-01-20T08:30"

    checkpoint_3 = brevet[2][2]
    assert checkpoint_3['km'] == "150"
    assert checkpoint_3['open_time'] == "2021-01-20T09:25"
    assert checkpoint_3['close_time'] == "2021-01-20T15:00"

    checkpoint_4 = brevet[2][3]
    assert checkpoint_4['km'] == "200"
    assert checkpoint_4['open_time'] == "2021-01-20T10:53"
    assert checkpoint_4['close_time'] == "2021-01-20T18:30"


def test_fetch():
    start_time = arrow.get("2021-06-15T04:00:00")
    checkpoints = [
        {'km': "0", 'open_time': "2021-06-15T04:00", 'close_time': "2021-06-15T05:00"},
        {'km': "100", 'open_time': "2021-06-15T06:56", 'close_time': "2021-06-15T10:40"},
        {'km': "200", 'open_time': "2021-06-15T09:53", 'close_time': "2021-06-15T17:20"},
        {'km': "300", 'open_time': "2021-06-15T13:00", 'close_time': "2021-06-16T00:00"},
        {'km': "400", 'open_time': "2021-06-15T16:08", 'close_time': "2021-06-16T06:40"}
    ]
    start_time_str = start_time.format("YYYY-MM-DDTHH:mm")
    brevets_insert("400", start_time_str, checkpoints)

    brevet = brevets_fetch()
    assert brevet is not None
    assert brevet[1] == "2021-06-15T04:00"

    checkpoint_1 = brevet[2][0]
    assert checkpoint_1['km'] == "0"
    assert checkpoint_1['open_time'] == "2021-06-15T04:00"
    assert checkpoint_1['close_time'] == "2021-06-15T05:00"

    checkpoint_2 = brevet[2][1]
    assert checkpoint_2['km'] == "100"
    assert checkpoint_2['open_time'] == "2021-06-15T06:56"
    assert checkpoint_2['close_time'] == "2021-06-15T10:40"

    checkpoint_3 = brevet[2][2]
    assert checkpoint_3['km'] == "200"
    assert checkpoint_3['open_time'] == "2021-06-15T09:53"
    assert checkpoint_3['close_time'] == "2021-06-15T17:20"

    checkpoint_4 = brevet[2][3]
    assert checkpoint_4['km'] == "300"
    assert checkpoint_4['open_time'] == "2021-06-15T13:00"
    assert checkpoint_4['close_time'] == "2021-06-16T00:00"
    
    checkpoint_5 = brevet[2][4]
    assert checkpoint_5['km'] == "400"
    assert checkpoint_5['open_time'] == "2021-06-15T16:08"
    assert checkpoint_5['close_time'] == "2021-06-16T06:40"
