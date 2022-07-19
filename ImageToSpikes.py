import numpy as np
from PIL import Image
from SpykeTorch import utils as ut
import torchvision.transforms as tr
from SpykeTorch import functional as f
import matplotlib.pyplot as plt

class ImageToSpikes:
    def __init__(self,image):
        self.img = Image.open(image).convert('L')
        self.spikes = None
        
    def to_spikes(self,number_of_neurons,runtime=50):    
        self.img = self.img.resize((number_of_neurons,number_of_neurons),Image.ANTIALIAS)
        self.spikes = tr.ToTensor()(self.img) * 255
        self.spikes.unsqueeze_(0)
        self.spikes = f.local_normalization(self.spikes,1)
        self.spikes = ut.Intensity2Latency(runtime,to_spike=False)(self.spikes) #Add runtime
        self.spikes = self.spikes.numpy().reshape(-1)
        reshaped_spikes = []
        
        for i in range(number_of_neurons * number_of_neurons):
            all_spikes_per_neuron = self.spikes[i:len(self.spikes):number_of_neurons * number_of_neurons].copy()
            neuron_spikes = []
            for j in range(len(all_spikes_per_neuron)):
                if all_spikes_per_neuron[j] > 0:
                    neuron_spikes.append(j)
            reshaped_spikes.append(neuron_spikes)
        self.spikes = reshaped_spikes
        return self.spikes
    
    def plot_spikes(self,ax):
        if self.spikes == None:
            return None
        neuron_id = 0
        for neuron_spikes in self.spikes:
            ax.plot(neuron_spikes,np.ones_like(neuron_spikes) * neuron_id,'.')
            neuron_id += 1
        ax.set_xlabel("Runtime")
        ax.set_ylabel("Neuron id")
        
    def get_total_number_of_spikes(self):
        total_number = 0
        for i in range(len(self.spikes)):
            total_number += len(self.spikes[i])
        return total_number
    
    def get_number_of_common_spikes(self,other):
        number_of_common_spikes = 0
        for i in range(min(len(self.spikes),len(other.spikes))):
            for spike in self.spikes[i]:
                if spike in other.spikes[i]:
                    number_of_common_spikes += 1
        return number_of_common_spikes
        
    def display_difference(self,other,ax):
        if self.spikes == None or other.spikes == None:
            return None
        diff_spikes = []
        for i in range(min(len(self.spikes),len(other.spikes))):
            neuron_spikes = []
            for spike in self.spikes[i]:
                if spike not in other.spikes[i]:
                    neuron_spikes.append(spike)
            for spike in other.spikes[i]:
                if spike not in self.spikes[i]:
                    neuron_spikes.append(spike)
            diff_spikes.append(neuron_spikes)
        
        neuron_id = 0
        for neuron_spikes in diff_spikes:
            ax.plot(neuron_spikes,np.ones_like(neuron_spikes) * neuron_id,'.')
            neuron_id += 1
        ax.set_xlabel("Runtime")
        ax.set_ylabel("Neuron id")
        
    def display_common(self,other,ax):
        if self.spikes == None or other.spikes == None:
            return None
        common_spikes = []
        for i in range(min(len(self.spikes),len(other.spikes))):
            neuron_spikes = []
            for spike in self.spikes[i]:
                if spike in other.spikes[i]:
                    neuron_spikes.append(spike)
            common_spikes.append(neuron_spikes)
        
        neuron_id = 0
        for neuron_spikes in common_spikes:
            ax.plot(neuron_spikes,np.ones_like(neuron_spikes) * neuron_id,'.')
            neuron_id += 1
        ax.set_xlabel("Runtime")
        ax.set_ylabel("Neuron id")