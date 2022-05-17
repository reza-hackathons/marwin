import { Web3Storage } from 'web3.storage'
import minimist from 'minimist'
import fs from 'fs'
import AdmZip from 'adm-zip'
import path from 'path'
import FileReader from 'filereader'

async function main () {
  const args = minimist(process.argv.slice(2))
  const token = args.token

  if (!token) {
    return console.error('A token is needed. You can create one on https://web3.storage')
  }
  if (args._.length < 1) {
    return console.error('Please supply the CID')
  }

  const cid = args._

  const client = new Web3Storage({ token })
  const res = await client.get(cid)
  if (!res.ok) {
    throw new Error(`failed to get ${cid} - [${res.status}] ${res.statusText}`)
  }

  // unpack File objects from the response
  const files = await res.files()
  for (const file of files) {
    console.log(`${file.cid} -- ${file.name} -- ${file.size}`)
    console.log(file)
    const data = await fs.readFile(file);
    fs.writeFile(`${path.resolve()}/${file.name}`, data, (err) => {
      if (err)
        console.log(err);
      else {
        console.log("File written successfully\n");
    }})
    // try {
    //   const zip = new AdmZip(file)
    //   zip.extractAllTo(path.resolve())
    // }
    // catch(e) {
    //   console.log(e)
    // }
    // var reader = new FileReader();
    // reader.onload = function(ev) {      
    //   console.log(ev)
    //   try {
    //     const zip = new AdmZip(ev)
    //     zip.extractAllTo(path.resolve())
    //   }
    //   catch(e) {
    //     console.log(e)
    //   }
    // }
    // reader.onerror = function(err) {
    //   console.error("Failed to read file", err);
    // }
    // reader.readAsArrayBuffer(file);
  }
}

main()