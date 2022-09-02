import json
from pprint import pprint
from subprocess import check_output


def get_pods_output(kubectl=False):
    if kubectl:
        cmd = "kubectl get pods -n microservices-nonprod -o json".split()
        output = check_output(cmd)
    else:
        with open('pods.json', 'rb') as doc:
            output = doc.read()
    return json.loads(output.decode('utf-8'))


def get_secrets_by_service(kubectl=False):
    output = get_pods_output(kubectl)
    items = output['items']
    result = []
    for item in items:
        name = item['metadata']['labels'].get('app', None)
        if not name:
            continue
        secrets = {}
        for values in item['spec']['containers'][0].get('env', []):
            if 'valueFrom' not in values:
                continue
            secret = values['valueFrom']['secretKeyRef']['name']
            key = values['valueFrom']['secretKeyRef']['key']
            if secret in secrets:
                secrets[secret].append(key)
            else:
                secrets[secret] = []

        if not secrets:
            continue

        result.append({'name': name, 'secrets': secrets})

    return result


if __name__ == '__main__':
    pprint(get_secrets_by_service(kubectl=True), indent=2)
