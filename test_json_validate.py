import unittest
from app import json_validate

class TestJsonValidation(unittest.TestCase):

    def test_valid(self):
        # Valid JSON data
        json_data = {
            "PolicyName": "ExamplePolicy",
            "PolicyDocument": {
                "Version": "2024-04-22",
                "Statement": [
                    {
                        "Sid": "1",
                        "Effect": "Allow",
                        "Action": ["s3:GetObject"],
                        "Resource": "arn:aws:s3:::example-bucket/*"
                    }
                ]
            }
        }
        self.assertTrue(json_validate(json_data))

    def test_empty_data(self):
    # Empty JSON data
        json_data = {}
        self.assertFalse(json_validate(json_data))

    def test_invalid_policy_name(self):
    # Invalid PolicyName
        json_data = {
            "PolicyName": "Invalid Policy Name 123!@#",
            "PolicyDocument": {
                "Version": "2024-04-22",
                "Statement": [
                    {
                        "Sid": "1",
                        "Effect": "Allow",
                        "Action": ["s3:GetObject"],
                        "Resource": "arn:aws:s3:::example-bucket/*"
                    }
                ]
            }
        }
        self.assertFalse(json_validate(json_data))

    def test_missing_key(self):
        json_data = {
            # Missing 'PolicyName'
            "PolicyDocument": {
                "Version": "2024-04-22",
                "Statement": [
                    {
                        "Sid": "1",
                        "Effect": "Allow",
                        "Action": ["s3:GetObject"],
                        "Resource": "arn:aws:s3:::example-bucket/*"
                    }
                ]
            }
        }
        self.assertFalse(json_validate(json_data))
    
    def test_misspeled_key(self):
        # Misspeled 'Version' key
        json_data = {
            "PolicyName": "root",
            "PolicyDocument": {
                "Verion": "2024-04-22",
                "Statement": [
                    {
                        "Sid": "1",
                        "Effect": "Allow",
                        "Action": ["s3:GetObject"],
                        "Resource": "arn:aws:s3:::example-bucket/*"
                    }
                ]
            }
        }
        self.assertFalse(json_validate(json_data))

    def test_keys_different_order(self):
        # Keys in different order
        json_data = {
            "PolicyName": "ExamplePolicy",
            "PolicyDocument": {
                "Statement": [
                    {
                        "Action": ["s3:GetObject"],
                        "Effect": "Allow",
                        "Sid": "1",
                        "Resource": "arn:aws:s3:::example-bucket/*"
                    }],
                    "Version": "2024-04-22"
            }
        }
        self.assertTrue(json_validate(json_data))

    def test_invalid_version_format(self):
        # Invalid version format
        json_data = {
            "PolicyName": "ExamplePolicy",
            "PolicyDocument": {
                "Version": "22-04-2024",
                "Statement": [
                    {
                        "Sid": "1",
                        "Effect": "Allow",
                        "Action": ["s3:GetObject"],
                        "Resource": "arn:aws:s3:::example-bucket/*"
                    }
                ]
            }
        }
        self.assertFalse(json_validate(json_data))

    def test_invalid_version(self):
        # Invalid version 
        json_data = {
            "PolicyName": "ExamplePolicy",
            "PolicyDocument": {
                "Version": "2025-04-11",
                "Statement": [
                    {
                        "Sid": "1",
                        "Effect": "Allow",
                        "Action": ["s3:GetObject"],
                        "Resource": "arn:aws:s3:::example-bucket/*"
                    }
                ]
            }
        }
        self.assertFalse(json_validate(json_data))

    def test_empty_statement(self):
        # Empty statement
        json_data = {
            "PolicyName": "ExamplePolicy",
            "PolicyDocument": {
                "Version": "2024-04-22",
                "Statement": [
                ]
            }
        }
        self.assertFalse(json_validate(json_data))

    def test_asterisk_resource(self):
        # Resource is single asterisk
        json_data = {
            "PolicyName": "ExamplePolicy",
            "PolicyDocument": {
                "Version": "2024-04-22",
                "Statement": [
                    {
                        "Sid": "1",
                        "Effect": "Allow",
                        "Action": ["s3:GetObject"],
                        "Resource": "*"
                    }
                ]
            }
        }
        self.assertFalse(json_validate(json_data))

    def test_invalid_effect(self):
        # Effect not in Allow or Deny
        json_data = {
            "PolicyName": "ExamplePolicy",
            "PolicyDocument": {
                "Version": "2024-04-22",
                "Statement": [
                    {
                        "Sid": "1",
                        "Effect": "-",
                        "Action": ["s3:GetObject"],
                        "Resource": "arn:aws:s3:::example-bucket/*"
                    }
                ]
            }
        }
        self.assertFalse(json_validate(json_data))
    
    def test_missing_value(self):
        # Missing Sid value
        json_data = {
            "PolicyName": "ExamplePolicy",
            "PolicyDocument": {
                "Version": "2024-04-22",
                "Statement": [
                    {
                        "Sid": "",
                        "Effect": "Allow",
                        "Action": ["s3:GetObject"],
                        "Resource": "arn:aws:s3:::example-bucket/*"
                    }
                ]
            }
        }
        self.assertFalse(json_validate(json_data))

    def test_invalid_statemnt(self):
        # Statements are not in JSON format
        json_data = {
            "PolicyName": "ExamplePolicy",
            "PolicyDocument": {
                "Version": "2024-04-22",
                "Statement": [
                    {
                        "Sid: 1, Effect: Allow, Action: [s3:GetObject], Resource: arn:aws:s3:::example-bucket/*"
                    }
                ]
            }
        }
        self.assertFalse(json_validate(json_data))

    def test_missing_statement_key(self):
        # Missing 'Action' key
        json_data = {
            "PolicyName": "ExamplePolicy",
            "PolicyDocument": {
                "Version": "2024-04-22",
                "Statement": [
                    {
                        "Sid": "1",
                        "Effect": "Allow",
                        "Resource": "arn:aws:s3:::example-bucket/*"
                    }
                ]
            }
        }
        self.assertFalse(json_validate(json_data))

if __name__ == '__main__':
    unittest.main()
