# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import tests.fixtures

from beautiful_traceback import parsing


def _validate_traceback(tb_result, tb_expect):
    assert tb_result.exc_name == tb_expect.exc_name
    assert tb_result.exc_msg == tb_expect.exc_msg
    assert tb_result.is_caused == tb_expect.is_caused
    assert tb_result.is_context == tb_expect.is_context

    assert len(tb_result.stack_frames) == len(tb_expect.stack_frames)

    for result_entry, expect_entry in zip(
        tb_result.stack_frames, tb_expect.stack_frames
    ):
        assert result_entry.module == expect_entry.module
        assert result_entry.call == expect_entry.call
        assert result_entry.lineno == expect_entry.lineno
        assert result_entry.src_ctx == expect_entry.src_ctx

    # same as above (except if the Traceback class changes)
    assert tb_result == tb_expect


def test_parse_basic_trace():
    traceback_results = parsing.parse_tracebacks(tests.fixtures.BASIC_TRACEBACK_STR)

    assert len(traceback_results) == 1
    tb_result = traceback_results[0]
    tb_expect = tests.fixtures.BASIC_TRACEBACK
    _validate_traceback(tb_result, tb_expect)


def test_parse_nested_trace():
    traceback_results = parsing.parse_tracebacks(tests.fixtures.CHAINED_TRACEBACK_STR)
    for tb_result, tb_expect in zip(
        traceback_results, tests.fixtures.CHAINED_TRACEBACK
    ):
        _validate_traceback(tb_result, tb_expect)
