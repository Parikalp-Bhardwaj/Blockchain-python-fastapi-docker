import datetime
import hashlib
import json
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Blockchian:
    def __init__(self):
        self.chain = []
        self.create_block(proof=1,previous_hash = 1)
        
    def create_block(self,proof,previous_hash):
        block = {"index":len(self.chain)+1,
                 "timestamp":str(datetime.datetime.now()),
                 "proof":proof,
                 "previous_hash":previous_hash}
        
        self.chain.append(block)
        return block
    
    def previous_hash(self):
        return self.chain[-1]
    
    def proof_of_work(self,previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hashVal = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hashVal[:4] == "0000":
                check_proof = True
            else:
                new_proof +=1
        
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def chain_valid(self,chain):
        previous_block = chain[0] 
        block_index = 1
        
        while block_index < len(chain):
            block = chain[block_index]
            if block["previous_hash"] != self.hash(previous_block):
                return False
            
            previous_proof = previous_block['proof']
            proof = block["proof"]
            hashVal = hashlib.sha256(
                str(proof**2 - previous_proof**2).encode()).hexdigest()
             
            if hashVal[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
         
        return True
            

blockchain = Blockchian()


class List(BaseModel):
    msg : str
    

@app.post("/mine_block")
def mine_block(items:List):
    previous_block = blockchain.previous_hash()
    previous_proof = previous_block["proof"]
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof,previous_hash)
    
    response = {"message":items.msg,"index":block["index"],"timestamp":block["timestamp"],
                "proof":block["proof"],"previous_hash":block["previous_hash"]}
    
    
    return response

@app.get("/get_block")
def get_block():
    return {"chain":blockchain.chain,"length":len(blockchain.chain)}


@app.get("/valid")
def isValid():
    valid = blockchain.chain_valid(blockchain.chain)
     
    if valid:
        response = {'message': 'The Blockchain is valid.'}
    else:
        response = {'message': 'The Blockchain is not valid.'}
        
    return response


if __name__=="__main__":
    uvicorn.run(app,port=8000,host="0.0.0.0")
	
	