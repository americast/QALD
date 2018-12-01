# Question Answering over Linked Data

## An attempt to build an automatic system to answer natural language queries

[![Gitter chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/QALD/Lobby#)

The natural language queries are processed and transformed into SPARQL queries, which is used to lookup DBpedia to find a solution.

Install requirements using:  
`pip3 install -r req.txt`

Create a folder `data/` and place datasets there.  
Run the standalone implementation using `python3 Sparql.py "u<query>"`.  
Otherwise, run the flask app using `python3 app.py` and answer interact from the frontend.

Sample dataset used can be found at https://github.com/ag-sc/QALD/blob/master/7/data/qald-7-train-largescale.json.

To open the front end, simply open `index.html` when inside the folder `qald-interface` from a browser.
