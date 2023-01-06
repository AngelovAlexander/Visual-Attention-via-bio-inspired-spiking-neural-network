A visual attention algorithm (and a GUI application) for detecting streets.

Program classes and files:
- Layer.py -> Creating layers that are part of the spiking neural network. If offers methods for creating connections and for plotting data.
- ImageToSpikes.py -> Class for creating input spikes from a given picture. It provides functions for visualization and comparison.
- Network.py -> The main program of the project. It creates the entire network from an image and specified parameters.
- gui.py -> A user interface of ImageToSpike.py and Network.py
- spike_statistics.py and network_experiments.py -> Show several experimentations performed on the ImageToSpikes and Network classes.
- images -> Stores data sets used for experimentations
- statistics -> Stores results of the experiment.

More information can be found in the Dissertation pdf.
