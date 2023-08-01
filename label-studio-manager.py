import os
import requests
import argparse
import json


base_url = "http://192.168.2.193:1879/"
api_key = "02e02bdf304115753da546aeb885ed47728a1e21"


def text_to_json(text):
    json_data = json.loads(text)
    return json_data


def list_projects():

    url = base_url+"api/projects/"

    payload = {}
    headers = {
        'Authorization': f'Token {api_key}',
        'Cookie': 'sessionid=eyJ1aWQiOiJkNWQxYWUzMy00OTdhLTRhOGItODA1Mi0xNmUxZDhkYTM5YjkiLCJvcmdhbml6YXRpb25fcGsiOjF9:1qQlB3:ZslyD1wIH9sCkCqP-VVAgGTL1fM0aP9_kNzL6Sy_hjs'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    json_ = text_to_json(response.text)

    results = json_["results"]
    ids = []
    for result in results:
        proj_id = result["id"]
        proj_title = result["title"]
        ids.append(proj_id)
        print(proj_title, proj_id)

    return ids


def delete_projects(ids):

    payload = {}
    headers = {
        'Authorization': f'Token {api_key}',
        'Cookie': 'sessionid=eyJ1aWQiOiJkNWQxYWUzMy00OTdhLTRhOGItODA1Mi0xNmUxZDhkYTM5YjkiLCJvcmdhbml6YXRpb25fcGsiOjF9:1qQlLG:sDu81ABRpsBPUv2UAQTW30tAyMti3QQuxVExh63fZCA'
    }

    for id in ids:
        url = f"{base_url}api/projects/{id}/"
        response = requests.request("DELETE", url, headers=headers, data=payload)
    print("delete completed")


parser = argparse.ArgumentParser(description='list all projects')
# Add the arguments
parser.add_argument('--delete', action='store_true', required=False, help='list of all projects')
parser.add_argument('--list', action='store_true', required=False, help='list of all projects')
# Execute the parse_args() method
args = parser.parse_args()

if __name__ == "__main__":
    if args.list:
        list_projects()
    if args.delete:
        ids = list_projects()
        delete_projects(ids)

