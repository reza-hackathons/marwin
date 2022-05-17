import os
import sys
import json
import argparse
import urllib
import subprocess
import shlex
import shutil

def persist(recipe: dict, token: str) -> None:
  '''
  makes a copy of the compute pod on IPFS
  '''
  if not recipe: 
    return
  print('Persisting the compute pod to ipfs...')  
  # zip and upload 
  shutil.make_archive(f'pod', 'zip', f'./{recipe["name"]}')
  print('Persisting pod to IPFS...')
  command = shlex.split(f'node ./web3-helper/put-files.js --token={token} ./pod.zip')
  proc = subprocess.Popen(command)  
  proc.wait()
  if proc.returncode == 0:
    print(f'Pod persisted successfully, please note the ^ CID down as it will be required when forking this pod.\nYou can also view your pod online at YOUR_CID.ipfs.dweb.link')
    print('Done.')
  else:
    print(f'Pod not persisted, it is either a network problem or a bug with our tools.')

def run_pod(recipe: dict) -> None:
  '''
  Runs a compute pod on Golem
  '''
  if not recipe: 
    return
  golem = recipe['golem']
  command = f'{golem["exec"]}'.split(' ')
  command[-1] = f'{recipe["name"]}/{command[-1]}'
  print(f'Running pod {command}...')
  proc = subprocess.Popen(command)  
  proc.wait()
  print(f'Exit code: {proc.returncode}')
  print('Pod execution finished.')

def fork(cid: str, token: str) -> None:
  '''
  Fork a (public) pod
  '''
  print(f'Forking pod "{cid}"...')  
  command = shlex.split(f'curl https://{cid}.ipfs.dweb.link/pod.zip -o pod.zip')
  proc = subprocess.Popen(command)  
  proc.wait()
  # unpck and bingo!
  shutil.unpack_archive(f'pod.zip', './pod', 'zip')
  print(f'Pod is ready at "pod" directory!, ' \
        f'now it can be run with\n' \
        f'`python cli.py --recipe pod/pod_name.recipe --run`')

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Marvin command line interface')
  parser.add_argument('--recipe', help = 'specify a recipe file')
  parser.add_argument('--persist', action = 'store_true', help = 'Persist pod to ipfs')
  parser.add_argument('--fork', help = 'Fork a public pod, reference is expected')  
  parser.add_argument('--run', action='store_true', help = 'Run the pod')
  args = vars(parser.parse_args())
  
  creds = None
  with open('./creds.json', 'r') as f:
    creds = json.loads(f.read())
    
  # import recipe, if any
  '''
  A typical recipe:
  {
    "name": "blender",
    "description": "Blender requestor pod that renders a .blend file.",
    "version": "1.0",
    "author": "greenpepe",
    "public": true,
    "golem": {
      "exec": "python3 script/blender.py",
      "script": "script",
      "payload": "payload",
      "output": "output",
      "log": "logs"
    }
  }
  '''  
  recipe = {}
  if args['recipe']:
    with open(args['recipe'], 'r') as f:
      recipe = json.loads(f.read())  
  if not recipe:
    print('Warning: invalid recipe.')
  # persist  
  if args['persist']:
    persist(recipe, creds['token'])  
  # fork the pod
  if args['fork']:
    fork(args['fork'], creds['token'])
  # run the pod    
  if args['run']:
    run_pod(recipe)
  
