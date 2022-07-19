from ImageToSpikes import ImageToSpikes
from Network import Network
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import glob

neurons = 16
runtime = 100
kernel_size = 5
weights = [7,4,12,12,-10]
orientations = [0,135,90,45,1]
layers = ['v1','v2','v4_1','v4_2','lip']
fig = []

for i in range(5):
    if i == 4:
        fig.append(plt.figure(figsize=(5,5), dpi=50))
    else:
        fig.append(plt.figure(figsize=(25,5), dpi=50))

        
      
# Vertical fragment/street
snn = Network(neurons,runtime,"vert.jpg",kernel_size,orientations,weights)
snn.create_network()
for i in range(len(layers)):
    snn.display(layers[i],fig[i])

#plt.show()

# Diagonal fragment/street
snn = Network(neurons,runtime,"diag.jpg",kernel_size,orientations,weights)
snn.create_network()
for i in range(len(layers)):
    snn.display(layers[i],fig[i])

# Circular fragment/street
snn = Network(neurons,runtime,"circle.jpg",kernel_size,orientations,weights)
snn.create_network()
for i in range(len(layers)):
    snn.display(layers[i],fig[i])

#plt.show()
snn = Network(10,runtime,"vert.jpg",kernel_size,orientations,weights)
snn.create_network()
for i in range(len(layers)):
    snn.display(layers[i],fig[i])

total_spikes = []
ids = []
for img in glob.glob('images/exp2/*.jpg'):
    snn = Network(neurons,runtime,img,kernel_size,orientations,weights)
    snn.create_network()
    total_spikes.append(snn.get_total_spikes_lip())
    ids.append(snn.get_different_ids_lip())

x = np.arange(1,len(ids) + 1)
plt.bar(x - 0.1,total_spikes, 0.2, label="Total number of spikes")
plt.bar(x + 0.1,ids, 0.2, label="Spikes neurons")
plt.title("Number of different spikes and spiked neurons.")
plt.xlabel("Images")
plt.ylabel("Spikes")
plt.legend(bbox_to_anchor=(1.0, 0.2))
plt.show()


total_spikes = []
ids = []
for img in glob.glob('images/data/*.JPG'):
    snn = Network(neurons,runtime,img,kernel_size,orientations,weights)
    snn.create_network()
    total_spikes.append(snn.get_total_spikes_lip())
    ids.append(snn.get_different_ids_lip())

x = np.arange(1,len(ids) + 1)
plt.bar(x - 0.1,total_spikes, 0.2, label="Total number of spikes")
plt.bar(x + 0.1,ids, 0.2, label="Spikes neurons")
plt.title("Number of different spikes and spiked neurons.")
plt.xlabel("Images")
plt.ylabel("Spikes")
plt.legend(bbox_to_anchor=(1.0, 0.2))
plt.show()