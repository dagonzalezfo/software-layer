# this will ingest GitHub REST API output to a list
# recovering the information

# command that do the magic:
#curl -L  -H "Accept: application/vnd.github+json"   -H "Authorization: Bearer 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"   -H "X-GitHub-Api-Version: 2022-11-28"   https://api.github.com/repos/SINGROUP/SOAPLite/license | jq  '.license|{spdx_id}'

# python traduction:
import requests
import argparse
import json

parser=argparse.ArgumentParser(description='Script to ingest licences')

parser.add_argument('--source', help='Project available in GitHub,pypi,cran')
parser.add_argument('project', help='Project. For GitHub you should specify owner/repo')
parser.add_argument('--manual',required=False)
args=parser.parse_args()
print (args)

def github(repo):
	"""
	Function that gets spdx_id from github using his API
	"""
	
	url="https://api.github.com/repos/"+repo+"/license"
	headers = {
		"Accept": "application/vnd.github+json",
		"Authorization" : "Bearer TOKEN",
		"X-GitHub-Api-Version": "2022-11-28",
	}
	
	test=requests.get(url, headers=headers)
	if test==200:
		return(test.json()['license']['spdx_id'])
	else:
		return('no available')

def pypi(project):
	"""
	Function that retrives licence from PiPy
	"""
	url = "https://pypi.org/pypi/"
	r = requests.get(url + project  + "/json").json()
	return(r['info']['license'])

def cran(project):
    """
	Function that retrieves licence from CRAN
	"""
    url = "http://crandb.r-pkg.org/"
    r = requests.get(url + project).json()
    return(r['License'])

#    if r.status_code != 200:
#        return "not found"
#    else:
#        return r.json()['Licence']    

def repology(project):
    url="https://repology.org//api/v1/"
    r = requests.get(url + project).json()
    return(r['License'])

def licenseInfo(project):
	"""
	Function that create the project dict
	"""
	if args.source=='pypi': 
		lic=pypi(project)
		info=[("license",lic), ("source",args.source)]
	print(project,info)
	return info

def updateJson(project,info):
	"""
	Function that updates json file
	"""
	with open('licenses.json','r') as licDict:
		licenses=json.loads(licDict.read())
	
	if project not in licenses.keys():
		print('we do not have the license')
		licenses[project]=dict(info)
	licJson=json.dumps(licenses, indent=4)

	with open('licenses.json','w') as licFile:
		licFile.write(licJson)

def main():
	project=args.project
	info=licenseInfo(project)
	updateJson(project,info)
#	repo="SINGROUP/SOAPLite"
#	print(gitHUBLicenses("SINGROUP/SOAPLite"))
#	pypiLicenses("easybuild")
#	CRANLicenses('mirai')


main()

