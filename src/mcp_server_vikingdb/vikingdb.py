from typing import Optional,List,Dict
from dotenv import load_dotenv
import os
import random
from volcengine.viking_db import *



class VikingDBConnector:
    """
    Encapsulates the connection to a VikingDB server and some  methods to interact with it.
    :param vikingdb_host: The host to use for the VikingDB server.
    :param vikingdb_region: The region to use for the VikingDB server.
    :param vikingdb_ak: The Access Key to use for the VikingDB server.
    :param vikingdb_sk: The Secret Key to use for the VikingDB server.
    :param collection_name: The name of the collection to use.
    :param index_name: The name of the index to use.
    """
    
    def __init__(
            self, 
            vikingdb_host: str, 
            vikingdb_region: str, 
            vikingdb_ak: str, 
            vikingdb_sk: str,
            collection_name: str,
            index_name: str
    ):
        self._vikingdb_host = vikingdb_host
        self._vikingdb_region = vikingdb_region
        self._vikingdb_ak = vikingdb_ak
        self._vikingdb_sk = vikingdb_sk
        self._collection_name = collection_name
        self._index_name = index_name
        
        self._client = VikingDBService(
            host=self._vikingdb_host,
            region=self._vikingdb_region,
            ak=self._vikingdb_ak,
            sk=self._vikingdb_sk,
            connection_timeout=100)
        
        self._collection = self._client.async_get_collection(self._collection_name)
        self._index = self._client.get_index(self._collection_name, self._index_name)
    
    async def collection_intro(self):
            self._collection = await self._client.async_get_collection(self._collection_name)
            intro_dict = {"collection_name":self._collection.collection_name,
                          "primary_key":self._collection.primary_key,
                          "description":self._collection.description,
                          "store_status":self._collection.stat,
                          "create_time":self._collection.create_time,
                          "update_time":self._collection.update_time,
                          "update_person":self._index.update_person,}
            return intro_dict
        
    async def index_intro(self):
            self._index = await self._client.async_get_index(self._collection_name, self._index_name)
            intro_dict = {"index_name":self._index.index_name,
                          "primary_key":self._index.primary_key,
                          "description":self._index.description,
                          "index_vector":self._index.vector_index,
                          "index_scalar":self._index.scalar_index,
                          "create_time":self._index.create_time,
                          "update_time":self._index.update_time,
                          "update_person":self._index.update_person,}
            return intro_dict
        
    async def upsert_information(self, information:str):
        self._collection = await self._client.async_get_collection(self._collection_name)
        vector = await  self._client.async_embedding_v2(EmbModel("bge-m3", params={"return_token_usage": True}), [RawData("text", information)])
        vector = vector["sentence_dense_embedding"][0]
        field1 = {"text_id": random.randint(10,100000),"text_content": information,"text_vector":vector}
        data1 = Data(field1)
        datas = []
        datas.append(data1)
        await self._collection.async_upsert_data(datas)  
        
        
    async def search_information(self, query:str):
        self._collection = await self._client.async_get_collection(self._collection_name)
        self._index = await self._client.async_get_index(self._collection_name, self._index_name)
        search_vector = await self._client.async_embedding_v2(EmbModel("bge-m3", params={"return_token_usage": True}), [RawData("text", query)])
        search_vector = search_vector["sentence_dense_embedding"][0]
        search_res = await self._index.async_search_by_vector(search_vector,limit=1) #纯稠密检索
        
        return search_res[0].fields
