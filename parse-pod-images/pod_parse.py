#! /opt/homebrew/bin/python3

# Get pods with kubectl get po --all-namespaces -o json and pass to stdin
import sys
import json

data = json.load(sys.stdin)
res = []
for item in data["items"]:
    if item["kind"] == "Pod":
        for c in item["spec"]["containers"]:
            if "harbor" not in c["image"] and "service" in c["image"]:
                owner = item["metadata"].get("ownerReferences", [None])[0]
                if owner:
                    if owner["kind"] == "ReplicaSet":
                        for i in data["items"]:
                            if i["kind"] == "ReplicaSet" and i["metadata"]["uid"] == owner["uid"]:
                                owner = i["metadata"].get("ownerReferences", [None])[0]
                res.append({
                    "name": item["metadata"]["name"],
                    "ns": item["metadata"]["namespace"],
                    "images": [c["image"] for c in item["spec"]["containers"]],
                    "owner": {
                        "kind": owner["kind"],
                        "name": owner["name"],
                    } if owner else {}
                    # "owner": {
                    #     "kind": item["metadata"].get("ownerReferences", [{"kind": "none", "name": "none"}])[0]["kind"],
                    #     "name": item["metadata"].get("ownerReferences", [{"kind": "none", "name": "none"}])[0]["name"],
                    # }
                    # "owner": [{
                    #     "kind": owner["kind"],
                    #     "name": owner["name"],
                    # } for owner in pod["metadata"].get("ownerReferences", [{"kind": "none", "name": "none"}])]
                })
                break


# sys.stdout.write(json.dumps(res, indent=4,))
sys.stdout.write("ns;owner_name;owner_kind;pod_name;image;\n")
for item in res:
    for image in item["images"]:
        if "harbor" not in image:
            # autopep8: off
            sys.stdout.write(f"{item["ns"]};{item["owner"].get("name", "")};{item["owner"].get("kind", "")};{item["name"]};{image};\n")
            # autopep8: on

# print(res)
