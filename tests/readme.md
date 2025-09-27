# free_port_checking.ipynb 

Jupyter notebook to identify available network ports on your machine, typically within a user-defined range (e.g., 80009000). Useful for developers deploying services locally or in Docker, ensuring that a port is free before binding a server or launching a new container.

# test_embedding_endpoint.ipynb

Interactive notebook to test and verify the API endpoint of your deployed embedding model service.

* Sends sample requests (text or batch) to the model endpoint (e.g., via REST API or FastAPI).

* Checks for correct embedding responses, response time, and error handling.

* Useful for confirming the model is running as expected and reachable from your environment.

# test_embedding_client.ipynb 

Jupyter notebook to validate your embedding client code, which acts as the Python interface for communicating with the embedding model service.

* Tests client initialization, connectivity, and typical function calls (e.g., get_embedding("Cancer")).

* Checks response correctness and error handling from a user/application perspective.

* Useful for integration testing before plugging into larger pipelines.

