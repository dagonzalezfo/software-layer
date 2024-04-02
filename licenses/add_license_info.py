# this will ingest GitHub REST API output to a list
# recovering the information

# command that do the magic:
#curl -L  -H "Accept: application/vnd.github+json"   -H "Authorization: Bearer TOKEN"   -H "X-GitHub-Api-Version: 2022-11-28"   https://api.github.com/repos/SINGROUP/SOAPLite/license | jq  '.license|{spdx_id}'

# python traduction:
import requests
import argparse
import json

parser=argparse.ArgumentParser(description='Script to ingest licences')

parser.add_argument('--source', help='Project available in GitHub,pypi,cran or user that push the license')
parser.add_argument('project', help='Project')
parser.add_argument('--manual',required=False)
args=parser.parse_args()

def github(source):
    """
    Function that gets spdx_id from github using his API
    """
    repo=source.removeprefix('github:')
    url="https://api.github.com/repos/"+repo+"/license"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization" : "Bearer TOKEN",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    
    r=requests.get(url, headers=headers)
    if r.status_code != 200:
        return "not found"
    else:
        return(r.json()['license']['spdx_id'])

def pypi(project):
    """
    Function that retrives licence from PiPy
    """
    url = "https://pypi.org/pypi/"
    r = requests.get(url + project  + "/json")
    if r.status_code != 200:
        return "not found"
    else:
        return(r.json()['info']['license'])

def cran(project):
    """
    Function that retrieves licence from CRAN
    """
    url = "http://crandb.r-pkg.org/"
    r = requests.get(url + project)
    if r.status_code != 200:
        return "not found"
    else:
        return(r.json()['License'])

def repology(project):
    url="https://repology.org//api/v1/"
    r = requests.get(url + project).json()
    if r.status_code != 200:
        return "not found"
    else:
        return(r['License'])

def ecosysteDotms_pypi(project):
    """
    Function that retrieves license info from ecosystem.ms for pipy packages
    """
    url = "https://packages.ecosyste.ms/api/v1/registries/pypi.org/packages/"
    r = requests.get(url + project)
    if r.status_code != 200:
        return "not found"
    else:
        return(r.json()['licenses'])
def ecosysteDotms_github(source):
    """
    Function that retrieves license info from ecosystem.ms for github repos
    """
    repo=source.removeprefix('github:')
    url= "https://repos.ecosyste.ms/api/v1/hosts/GitHub/repositories/"
    r = requests.get(url + repo)
    if r.status_code != 200:
        return "not found"
    else:
        return(r.json()['license'])

def licenseInfo(project):
    """
    Function that create the project info
    """
    if args.source=='pypi': 
        lic=ecosysteDotms_pypi(project)
#        lic=pypi(project)
    elif "github" in args.source:
        lic=ecosysteDotms_github(args.source)
#        lic=github(args.source)
    elif args.manual:
        lic=args.manual
    
    info=[("license",lic), ("source",args.source)]
    return info

def updateJson(project,info):
    """
    Function that updates json file
    """
    with open('licenses.json','r') as licDict:
        licenses=json.loads(licDict.read())
    
    if project in licenses.keys():
        print('project in licenses.json')
    else: 
        print('we do not have the license, adding into licenses.json')
        licenses[project]=dict(info)
        licJson=json.dumps(licenses, indent=4)

        with open('licenses.json','w') as licFile:
            licFile.write(licJson)

def main():
    project=args.project
    info=licenseInfo(project)
    updateJson(project,info)

main()