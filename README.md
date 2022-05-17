# Marwin
## Intro
Marwin is an attempt to integrate the Golem network's compute prowess into the IPFS network. The whole idea revolves around the concept of compute pods.  With the help of IPFS the user is in charge of all the stuff required to run a DApp.   
A compute pod is a directory structure containing a `recipe` file, `script`, `payload`, `ouput`, and `log` folders. Here's a sample recipe file:  
<pre>
{
  "name": "blender",
  "description": "Blender requestor pod that renders a .blend file.",
  "version": "1.0",
  "author": "reza",
  "public": true,
  "golem": {
    "exec": "python3 script/blender.py",
    "script": "script",
    "payload": "payload",
    "output": "output",
    "log": "logs"
  }
}  
</pre>
The `public` property is used to share the pod with others, the `golem` property directs how the inputs and outputs of a typical golem session are going to be interacted with. The `exec` property is used to invoke the golem tooling which will use the stuff from the `script` and `payload` properties. The `output` and the `log` properties contain the outputs of a compute session.  
## How to run?
You would need we3.storage and the Golem toolsets.  
- Get familiar with IPFS and web3.storage stuff here https://web3.storage, then head into `web-helper` folder and run `npm install`
- Get Golem tools up and running from here https://handbook.golem.network/requestor-tutorials/flash-tutorial-of-requestor-development
- Get a virtual environment and install necessary libraries. You'd need typical ones like `yapapi`, `requests`, ...
- Make sure the `foo/logs` folder exists and then invoke `python3 cli.py --recipe foo/recipe.json --run`
- Once Golem is done, observe the contents of the `foo/log` and `foo/output`. Now you can save your compute pod on the IPFS with `python3 cli.py --recipe foo/recipe.json --persist`  

When you persist a pod to the IPFS, a CID is generated for you. You need to take a note of that CID for further usages.  
To start, there is a standard Blender task already persisted by us for you:  
Just run `python3 cli.py --fork bafybeib36wmi4vooocsqq6kmjkels5bbnjp37z4sxrfttc7qeorvrljszi` and bingo!


## Demo
https://youtu.be/Qtvce7-fM0w
