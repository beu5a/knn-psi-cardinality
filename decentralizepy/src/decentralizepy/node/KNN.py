import logging
import math
import os
import queue
import time
import json
import sys

from random import Random
from threading import Lock, Thread, Event


import csv
from collections import defaultdict

import torch
import numpy as np
import heapq
import hashlib

from decentralizepy import utils
from decentralizepy.graphs.Graph import Graph
from decentralizepy.mappings.Mapping import Mapping
from decentralizepy.node.OverlayNode import OverlayNode


class KNN_2(OverlayNode):



    def local_data_to_profile(self):
        d , e = self.get_local_data()

        d = list(zip(d,e))
        
        arr = np.array(d, dtype=[('movie_id', int), ('rating', float)])
        #filter the array based on criteria
        filtered_arr = arr[arr['rating'] > 3.5]

        profile = np.unique(filtered_arr['movie_id'])

        return profile , np.unique(filtered_arr)
   
    def get_local_data(self):
        user_id = self.rank + 1
        dataloader = self.dataset.get_trainset()

        final_inputs = []
        final_ratings = [] 
        for batch in dataloader:
            # Get the input features from the batch
            inputs,ratings = batch
            # Use boolean masking to filter the rows with the specified user ID
            mask = inputs[:, 0] == user_id
            filtered_inputs = inputs[mask]
            filtered_ratings = ratings[mask]
            if filtered_inputs.size(0) > 0:
                #filtered_data.append((filtered_inputs.numpy(), filtered_ratings.numpy()))
                final_inputs.append(int(filtered_inputs[0][1]))
                final_ratings.append(float(filtered_ratings))

        return final_inputs , final_ratings
    
    def dummy_create_user_profiles(self):
        csv_file = './ml-latest-small/ratings.csv'
        user_profiles = defaultdict(set)

        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                user_id, movie_id, rating, timestamp = row
                rating = float(rating)
                if rating > 3.5:
                    user_profiles[user_id].add(movie_id)

        return user_profiles
    
    def create_hashed_profile(self,movie_ids):
        hashed_profile = list()

        movie_ids_str = [str(id) for id in movie_ids]
        for movie_id in movie_ids_str:
            hashed_movie_id = hashlib.sha256(movie_id.encode()).digest()
            hashed_profile.append(hashed_movie_id)

        return hashed_profile
    
    def jaccard_similarity(self,other_profile):
        set1 = set(self.str_profile)
        set2 = set(other_profile)
        return len(set1.intersection(set2)) / len(set1.union(set2))
      


    def create_request_to_send(
        self,
        channel="KNNConstr",
    ):     
        message = {"CHANNEL": channel, "KNNRound": self.knn_round, "REQUEST": self.str_profile}
        return message
    

    
    def create_result_to_send(
        self,
        request,
        channel="KNNConstr"
    ):
        jaccard = self.jaccard_similarity(request) 
        message = {"CHANNEL": channel, "KNNRound": self.knn_round, "JACCARD": jaccard}
        return message , jaccard
    
    
    def create_random_discovery_message_to_send(self,channel="KNNConstr"):
        ##Select one neighbor randomly and send a request to it, add some random nodes to avoid local minima then keep the best.
        top_k = self.top_k_neighbors()
        top_k_ids = [x[0] for x in top_k]
        top_k_ids.append(self.uid)
        message = {"CHANNEL": channel, "KNNRound": self.knn_round , "RANDOM_DISCOVERY": top_k_ids}
        return message 
    
    def create_random_discovery_response_to_send(self,channel="KNNConstr"):
        top_k = self.top_k_neighbors()
        top_k_ids = [x[0] for x in top_k]
        top_k_ids.append(self.uid)
        message = {"CHANNEL": channel, "KNNRound": self.knn_round , "RANDOM_DISCOVERY_RESPONSE": set(top_k_ids)}
        return message
    
    
    def create_knn_bye_message_to_send(self,channel="KNNConstr"):
        message = {"CHANNEL": channel, "KNNRound": self.knn_round, "KNNBYE": True}
        return message


    def receive_KNN_message(self):
        return self.receive_channel("KNNConstr", block=False)
    
    def top_k_neighbors(self, k_ = 4):
        k = self.initial_neighbors
        self.mutex.acquire()
        top_k = heapq.nlargest(k, self.similarities.items(), key=lambda x: x[1])
        self.mutex.release()
        return top_k
    
    def top_k_neighbors_without_mutex(self, k_ = 4):
        k = self.initial_neighbors
        top_k = heapq.nlargest(k, self.similarities.items(), key=lambda x: x[1])
        return top_k


    def receiver_thread(self):
        knnBYEs = set()
        self.num_initializations = 0

        while True:

            if len(knnBYEs) == self.mapping.get_n_procs() - 1:
                if self.exit_receiver.is_set():
                    self.exit_sender.set()
                    logging.debug("Exiting Receiver thread")
                    return


            logging.debug("Waiting for messages")
            x = self.receive_KNN_message()
            if x == None:
                continue
           

            if "REQUEST" in x[1]:
                logging.debug(
                    "A REQUEST message received from {} from KNNRound {}".format(
                        x[0], x[1]["KNNRound"]
                    )
                )
                #if a request is received and the request is not sent yet, remove the peer from the list of active candidates
                self.mutex.acquire()
                if x[0] in self.current_candidates:
                    self.current_candidates.remove(x[0])
                self.mutex.release()

                to_send , jaccard = self.create_result_to_send(x[1]["REQUEST"])
                message  =(x[0],to_send)
                self.sending_queue.put(message)
                self.mutex.acquire()
                self.similarities[x[0]] = jaccard
                self.mutex.release()


            elif "JACCARD" in x[1]:
                logging.debug(
                    "A JACCARD message received from {} from KNNRound {}".format(
                        x[0], x[1]["KNNRound"]
                    )
                )

                self.mutex.acquire()
                self.similarities[x[0]] = x[1]["JACCARD"]
                self.mutex.release()

            elif "RANDOM_DISCOVERY" in x[1]:
                logging.debug(
                    "A RANDOM_DISCOVERY message received from {} from KNNRound {}".format(
                        x[0], x[1]["KNNRound"]
                    )
                )
                message = (x[0],self.create_random_discovery_response_to_send())
                self.sending_queue.put(message)
                self.mutex.acquire()
                self.next_candidates.union(x[1]["RANDOM_DISCOVERY"])
                self.mutex.release()

            elif "RANDOM_DISCOVERY_RESPONSE" in x[1]:
                logging.debug(
                    "A RANDOM_DISCOVERY_RESPONSE message received from {} from KNNRound {}".format(
                        x[0], x[1]["KNNRound"]
                    )
                )
                self.mutex.acquire()
                self.next_candidates.union(x[1]["RANDOM_DISCOVERY_RESPONSE"])
                self.mutex.release()
           
            elif "KNNBYE" in x[1]:
                logging.debug("{} KNN Byes received".format(knnBYEs))

                self.mutex.acquire()
                knnBYEs.add(x[0])
                self.mutex.release()

            else:
                logging.debug(
                    "Unsupported message received from {}".format(
                        x[0]
                    )
                )
              
    def sender_thread(self):
        knnBYEs = set()

        while True:
            try:
                message = self.sending_queue.get(timeout=5) #timeout is 5 seconds
                if message[0] != self.uid:
                    self.communication.send(message[0], message[1])
                    if "KNNBYE" in message[1]:
                        knnBYEs.add(message[0])
                    logging.debug("Message sent to {} : {}".format(message[0],message[1].keys()))
                else:
                    logging.debug("Message {} not sent to self".format(message[1].keys()))
            
            except queue.Empty:
                if len(knnBYEs) == self.mapping.get_n_procs() - 1:
                    if self.exit_sender.is_set():
                        logging.debug("Exiting Sender thread")
                        return
     


    def knn_round_end(self):
        self.mutex.acquire()
        cond = all([x in self.similarities for x in self.current_candidates])
        self.mutex.release()
        return cond


    def build_topology(self, knn_rounds=4, random_nodes=4):
        self.knn_round = 0
        self.exit_receiver = Event()
        self.exit_sender = Event()
        self.current_candidates = set(self.out_edges)
        self.next_candidates = set()
        self.similarities = {}

        t = Thread(target=self.receiver_thread)
        u = Thread(target=self.sender_thread)
        t.start()
        u.start()

        for round in range(knn_rounds):
            self.knn_round = round
            logging.info("Starting KNN Round {}".format(round))

            start_time = time.perf_counter()

            self.mutex.acquire()
            for receiver in self.current_candidates:
                to_send = self.create_request_to_send()
                self.sending_queue.put((receiver,to_send))
            self.mutex.release()

            ##select a random node and send random discovery messages to them

            send = False
            random_neighbor = None

            self.mutex.acquire()
            if len(self.similarities):
                random_neighbor = self.rng.sample(self.top_k_neighbors_without_mutex(), 1)[0]
                random_neighbor = random_neighbor[0]
                send = True
            self.mutex.release()

            if send and random_neighbor != self.uid:
                to_send = self.create_random_discovery_message_to_send()
                self.sending_queue.put((random_neighbor,to_send))





            while not self.knn_round_end():
                time.sleep(0.001) #POLL FREQ 
                logging.debug("Waiting for KNN Round {} to end".format(round))

            
            end_time = time.perf_counter()
            self.times.append(end_time-start_time)
            
            random_candidates = set(
                self.rng.sample(list(range(self.mapping.get_n_procs())), random_nodes)
            )

            self.mutex.acquire()
            self.next_candidates = self.next_candidates.union(random_candidates)
            self.mutex.release()

            logging.info("Completed KNN Round {}".format(round))
            logging.debug("OutNodes: {}".format(self.out_edges))


            self.mutex.acquire()
            aux = {'top_k' : self.top_k_neighbors_without_mutex(),'coverage' : len(self.similarities)}
            self.convergence.append(aux)
            #cleanse the next candidates from the already selected nodes
            self.next_candidates = self.next_candidates.difference(self.similarities.keys())
            if self.uid in self.next_candidates:
                self.next_candidates.remove(self.uid)
            self.current_candidates = self.next_candidates
            self.next_candidates = set()
            self.mutex.release()



        ##add knn bye to message
        to_send = self.create_knn_bye_message_to_send()
        logging.info("Sending KNNByes")
        self.exit_receiver.set()
        
        for receiver in range(self.mapping.get_n_procs()):
            if receiver != self.uid:
                self.sending_queue.put((receiver,to_send))

        
        logging.info("KNNByes Sent")
        t.join()
        logging.info("Receiver Thread Returned")
        u.join()
        logging.info("Sender Thread Returned")



    def run(self):
        """
        Start the decentralized learning

        """

        self.profile = self.dummy_create_user_profiles()[str(self.rank + 1)]
        self.othersInfo[self.uid] = len(self.profile)
        self.str_profile = self.create_hashed_profile(self.profile)
        self.connect_neighbors()
        logging.info("Connected to all neighbors")
        self.build_topology(knn_rounds=self.knn_rounds)
        self.my_neighbors = self.top_k_neighbors_without_mutex()
        logging.info("Total number of neighbor: {}".format(len(self.my_neighbors)))
        logging.info("Neighbors: {}".format(self.my_neighbors))
        bytes = self.communication.total_bytes
        self.disconnect_neighbors()
        logging.info("All neighbors disconnected. Process complete!")
        logging.info("Final Distributions: {}".format(self.similarities))
        logging.info("Neighbors Reached: {}".format(len(self.similarities)))
        logging.info("Total Communication Costs:{}".format(bytes))

        results_dict = { "neighbors": self.similarities, "communication": bytes}
        with open(
                os.path.join(self.log_dir, "{}_results.json".format(self.rank)), "w") as of:
                    json.dump(results_dict, of)
                    of.write('\n')  # Add a line break
                    json.dump(self.convergence, of)
                    of.write('\n')
                    json.dump(self.times, of)




    def __init__(
        self,
        rank: int,
        machine_id: int,
        mapping: Mapping,
        graph: Graph,
        config,
        iterations=1,
        knn_rounds=4,
        log_dir=".",
        weights_store_dir=".",
        log_level=logging.INFO,
        test_after=5,
        train_evaluate_after=1,
        reset_optimizer=1,
        initial_neighbors=2,
        *args
    ):
        """
        Constructor

        Parameters
        ----------
        rank : int
            Rank of process local to the machine
        machine_id : int
            Machine ID on which the process in running
        mapping : decentralizepy.mappings
            The object containing the mapping rank <--> uid
        graph : decentralizepy.graphs
            The object containing the global graph
        config : dict
            A dictionary of configurations. Must contain the following:
            [DATASET]            make default for this
                dataset_package
                dataset_class
                model_class
            [OPTIMIZER_PARAMS]    make default for this
                optimizer_package
                optimizer_class
            [TRAIN_PARAMS]        make default for this
                training_package = decentralizepy.training.Training
                training_class = Training
                epochs_per_round = 25
                batch_size = 64
        iterations : int    make def for this 0
            Number of iterations (communication steps) for which the model should be trained
        log_dir : str
            Logging directory
        weights_store_dir : str  make def for this 0
            Directory in which to store model weights
        log_level : logging.Level
            One of DEBUG, INFO, WARNING, ERROR, CRITICAL
        test_after : int
            Number of iterations after which the test loss and accuracy arecalculated
        train_evaluate_after : int
            Number of iterations after which the train loss is calculated
        reset_optimizer : int
            1 if optimizer should be reset every communication round, else 0
        args : optional
            Other arguments

        """

        total_threads = os.cpu_count()
        self.threads_per_proc = max(
            math.floor(total_threads / mapping.procs_per_machine), 1
        )
        torch.set_num_threads(self.threads_per_proc)
        torch.set_num_interop_threads(1)
        self.instantiate(
            rank,
            machine_id,
            mapping,
            graph,
            config,
            iterations,
            log_dir,
            weights_store_dir,
            log_level,
            test_after,
            train_evaluate_after,
            reset_optimizer,
            *args
        )

        self.rng = Random()
        self.rng.seed(self.uid + 100)

        self.initial_neighbors = initial_neighbors
        self.in_edges = set()
        self.out_edges = set(
            self.rng.sample(
                list(self.graph.neighbors(self.uid)), self.initial_neighbors
            )
        )
        self.knn_rounds = knn_rounds
        self.responseQueue = queue.Queue()
        self.mutex = Lock()
        self.communication_lock = Lock()
        self.othersInfo = {}
        self.sending_queue = queue.Queue()
        self.similarities = {}
        self.convergence = []
        self.times = []


        logging.info(
            "Each proc uses %d threads out of %d.", self.threads_per_proc, total_threads
        )
        self.run()   #changing the run method will be required 



