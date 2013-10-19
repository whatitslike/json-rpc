import json
import unittest

from ..jsonrpc1 import (
    JSONRPC10Request,
    JSONRPC10Response,
)


class TestJSONRPC10Request(unittest.TestCase):

    """ Test JSONRPC10Request functionality."""

    def setUp(self):
        self.request_params = {
            "method": "add",
            "params": [1, 2],
            "_id": 1,
        }

    def test_correct_init(self):
        """ Test object is created."""
        JSONRPC10Request(**self.request_params)

    def test_validation_incorrect_no_parameters(self):
        with self.assertRaises(ValueError):
            JSONRPC10Request()

    def test_method_validation_str(self):
        self.request_params.update({"method": "add"})
        JSONRPC10Request(**self.request_params)

    def test_method_validation_not_str(self):
        self.request_params.update({"method": []})
        with self.assertRaises(ValueError):
            JSONRPC10Request(**self.request_params)

        self.request_params.update({"method": {}})
        with self.assertRaises(ValueError):
            JSONRPC10Request(**self.request_params)

        self.request_params.update({"method": None})
        with self.assertRaises(ValueError):
            JSONRPC10Request(**self.request_params)

    def test_params_validation_list(self):
        self.request_params.update({"params": []})
        JSONRPC10Request(**self.request_params)

        self.request_params.update({"params": [0]})
        JSONRPC10Request(**self.request_params)

    def test_params_validation_tuple(self):
        self.request_params.update({"params": ()})
        JSONRPC10Request(**self.request_params)

        self.request_params.update({"params": tuple([0])})
        JSONRPC10Request(**self.request_params)

    def test_params_validation_dict(self):
        self.request_params.update({"params": {}})
        with self.assertRaises(ValueError):
            JSONRPC10Request(**self.request_params)

        self.request_params.update({"params": {"a": 0}})
        with self.assertRaises(ValueError):
            JSONRPC10Request(**self.request_params)

    def test_params_validation_none(self):
        self.request_params.update({"params": None})
        with self.assertRaises(ValueError):
            JSONRPC10Request(**self.request_params)

    def test_params_validation_incorrect(self):
        self.request_params.update({"params": "str"})
        with self.assertRaises(ValueError):
            JSONRPC10Request(**self.request_params)

    def test_request_args(self):
        self.assertEqual(JSONRPC10Request("add", []).args, ())
        self.assertEqual(JSONRPC10Request("add", [1, 2]).args, (1, 2))

    def test_id_validation_string(self):
        self.request_params.update({"_id": "id"})
        JSONRPC10Request(**self.request_params)

    def test_id_validation_int(self):
        self.request_params.update({"_id": 0})
        JSONRPC10Request(**self.request_params)

    def test_id_validation_null(self):
        self.request_params.update({"_id": "null"})
        JSONRPC10Request(**self.request_params)

    def test_id_validation_none(self):
        self.request_params.update({"_id": None})
        JSONRPC10Request(**self.request_params)

    def test_id_validation_float(self):
        self.request_params.update({"_id": 0.1})
        JSONRPC10Request(**self.request_params)

    def test_id_validation_list_tuple(self):
        self.request_params.update({"_id": []})
        JSONRPC10Request(**self.request_params)

        self.request_params.update({"_id": ()})
        JSONRPC10Request(**self.request_params)

    def test_id_validation_default_id_none(self):
        del self.request_params["_id"]
        JSONRPC10Request(**self.request_params)

    def test_data_method_1(self):
        r = JSONRPC10Request("add", [])
        self.assertEqual(json.loads(r.json), r.data)
        self.assertEqual(r.data, {
            "method": "add",
            "params": [],
            "id": None,
        })

    def test_data_method_2(self):
        r = JSONRPC10Request(method="add", params=[])
        self.assertEqual(json.loads(r.json), r.data)
        self.assertEqual(r.data, {
            "method": "add",
            "params": [],
            "id": None,
        })

    def test_data_params_1(self):
        r = JSONRPC10Request("add", params=[], _id=None)
        self.assertEqual(json.loads(r.json), r.data)
        self.assertEqual(r.data, {
            "method": "add",
            "params": [],
            "id": None,
        })

    def test_data_params_2(self):
        r = JSONRPC10Request("add", ())
        self.assertEqual(json.loads(r.json), r.data)
        self.assertEqual(r.data, {
            "method": "add",
            "params": [],
            "id": None,
        })

    def test_data_params_3(self):
        r = JSONRPC10Request("add", (1, 2))
        self.assertEqual(json.loads(r.json), r.data)
        self.assertEqual(r.data, {
            "method": "add",
            "params": [1, 2],
            "id": None,
        })

    def test_data_id_1(self):
        r = JSONRPC10Request("add", [], _id="null")
        self.assertEqual(json.loads(r.json), r.data)
        self.assertEqual(r.data, {
            "method": "add",
            "params": [],
            "id": "null",
        })

    def test_data_id_1_notification(self):
        r = JSONRPC10Request("add", [], _id="null", is_notification=True)
        self.assertEqual(json.loads(r.json), r.data)
        self.assertEqual(r.data, {
            "method": "add",
            "params": [],
            "id": None,
        })

    def test_data_id_2(self):
        r = JSONRPC10Request("add", [], _id=None)
        self.assertEqual(json.loads(r.json), r.data)
        self.assertEqual(r.data, {
            "method": "add",
            "params": [],
            "id": None,
        })

    def test_data_id_2_notification(self):
        r = JSONRPC10Request("add", [], _id=None, is_notification=True)
        self.assertEqual(json.loads(r.json), r.data)
        self.assertEqual(r.data, {
            "method": "add",
            "params": [],
            "id": None,
        })

    def test_data_id_3(self):
        r = JSONRPC10Request("add", [], _id="id")
        self.assertEqual(json.loads(r.json), r.data)
        self.assertEqual(r.data, {
            "method": "add",
            "params": [],
            "id": "id",
        })

    def test_data_id_3_notification(self):
        r = JSONRPC10Request("add", [], _id="id", is_notification=True)
        self.assertEqual(json.loads(r.json), r.data)
        self.assertEqual(r.data, {
            "method": "add",
            "params": [],
            "id": None,
        })

    def test_data_id_4(self):
        r = JSONRPC10Request("add", [], _id=0)
        self.assertEqual(json.loads(r.json), r.data)
        self.assertEqual(r.data, {
            "method": "add",
            "params": [],
            "id": 0,
        })

    def test_data_id_4_notification(self):
        r = JSONRPC10Request("add", [], _id=0, is_notification=True)
        self.assertEqual(json.loads(r.json), r.data)
        self.assertEqual(r.data, {
            "method": "add",
            "params": [],
            "id": None,
        })

    def test_is_notification(self):
        r = JSONRPC10Request("add", [])
        self.assertTrue(r.is_notification)

        r = JSONRPC10Request("add", [], _id=None)
        self.assertTrue(r.is_notification)

        r = JSONRPC10Request("add", [], _id="null")
        self.assertFalse(r.is_notification)

        r = JSONRPC10Request("add", [], _id=0)
        self.assertFalse(r.is_notification)

        r = JSONRPC10Request("add", [], is_notification=True)
        self.assertTrue(r.is_notification)

        r = JSONRPC10Request("add", [], is_notification=True, _id=None)
        self.assertTrue(r.is_notification)

        r = JSONRPC10Request("add", [], is_notification=True, _id=0)
        self.assertTrue(r.is_notification)

    def test_set_unset_notification_keep_id(self):
        r = JSONRPC10Request("add", [], is_notification=True, _id=0)
        self.assertTrue(r.is_notification)
        self.assertEqual(r.data["id"], None)

        r.is_notification = False
        self.assertFalse(r.is_notification)
        self.assertEqual(r.data["id"], 0)

    def test_error_if_notification_true_but_id_none(self):
        r = JSONRPC10Request("add", [], is_notification=True, _id=None)
        with self.assertRaises(ValueError):
            r.is_notification = False


    # TODO: test from_json


class TestJSONRPC10Response(unittest.TestCase):

    """ Test JSONRPC10Response functionality."""
