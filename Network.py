import math
import numpy as np
import matplotlib.pyplot as plt
from ImageToSpikes import ImageToSpikes
from Layer import Layer
from pyNN.utility import Timer
from pyNN.nest import *
from SpykeTorch import utils as ut

def areal_filtering(x,y,r=0):
    a_2 = math.log(2) / math.pi                            # a^2
    return math.exp(-(math.pi / a_2)*(x * x + y * y - r * r)) / a_2

def gaussian_kernel(kernel_size,angle,circle = False):
    kernel = np.zeros((kernel_size,kernel_size))
    for row in range(kernel_size):
        for column in range(kernel_size):
            if circle == False:
                if angle % 90 == 0:
                    kernel[row][column] = areal_filtering((row - math.floor(kernel_size / 2.0)) * math.cos(math.radians(angle)),(column - math.floor(kernel_size / 2.0)) * math.sin(math.radians(angle)))
                else:
                    kernel[row][column] = areal_filtering((row - math.floor(kernel_size / 2.0)) * math.cos(math.radians(angle)) - (column - math.floor(kernel_size / 2.0)) * math.sin(math.radians(angle)),(column - math.floor(kernel_size / 2.0)) * math.cos(math.radians(angle)) - (row - math.floor(kernel_size / 2.0)) * math.sin(math.radians(angle)))
            else:
                kernel[row][column] = areal_filtering((row - math.floor(kernel_size / 2.0)),(column - math.floor(kernel_size / 2.0)),math.floor(kernel_size / 2.0))
    
    return kernel

class Network:
    def __init__(self,input_neurons,runtime,image_path,kernel_size,gaussian_filters,weights):
        self.neurons = input_neurons
        self.runtime = runtime
        self.img = image_path
        self.kernel_size = kernel_size
        self.gaussian_filters = gaussian_filters #[0,135,90,45,1], [None,135,None,None,1]
        self.weights = weights

    def create_network(self):
        
        #Create the kernels corresponding to the gaussian filter that is selected
        kernels = []
        for i in range(len(self.gaussian_filters)):
            if self.gaussian_filters[i] != None:
                if i != 4:
                    kernels.append(gaussian_kernel(self.kernel_size,self.gaussian_filters[i]))
                else:
                    #######################################Addd circle filters
                    kernels.append(gaussian_kernel(self.kernel_size,self.gaussian_filters[i],True))
                    
        setup(timestep=0.5, min_delay = 0.5, max_delay = 11.0)
        stdp = STDPMechanism(weight=0.5,timing_dependence=SpikePairRule(tau_plus=20.0, tau_minus=20.0,A_plus=0.05, A_minus=0.0675),weight_dependence=AdditiveWeightDependence(w_min=0, w_max=19.7))
        
        retina = ImageToSpikes(self.img)
        retina_spikes = retina.to_spikes(self.neurons,self.runtime)
        v1_neurons = int((1 + self.neurons - self.kernel_size) * (1 + self.neurons - self.kernel_size))
        population_sizes = []
        for i in range(len(kernels)):
            population_sizes.append(v1_neurons)
            
        lip_size = [int(population_sizes[0] / 2)]
        v4_population_sizes = [int(size / 2) for size in population_sizes]
        
        input_layer = Layer('retina')
        self.v1 = Layer('v_1')
        self.v2 = Layer('v_2')
        self.v4_1 = Layer('v_4_1')
        self.v4_2 = Layer('v_4_2')
        self.lip = Layer('lip')
        
        input_layer.add_populations(SpikeSourceArray,[self.neurons*self.neurons],retina_spikes)
        self.v1.add_populations(IF_curr_exp,population_sizes)
        self.v2.add_populations(IF_curr_exp,population_sizes)
        self.v4_1.add_populations(IF_curr_exp,v4_population_sizes)
        self.v4_2.add_populations(IF_curr_exp,v4_population_sizes)
        self.lip.add_populations(IF_curr_exp,lip_size)
        
        input_layer.connect_with_given_kernel_weights(self.v1,kernels)
        self.v1.connect_layers(self.v2,"one",self.weights[0])
        self.v2.connect_with_subsampling(self.v4_1,self.weights[1],stdp)
        self.v4_1.connect_layers(self.v4_2,"one",self.weights[2])
        self.v4_2.connect_layers(self.lip,"choose",self.weights[3])
        self.lip.winner_takes_all(self.weights[4])
        
        for i in range(len(kernels)):
            self.v1.populations[i].record('spikes')
            self.v2.populations[i].record('spikes')
            self.v4_1.populations[i].record('spikes')
            self.v4_2.populations[i].record('spikes')
        self.lip.populations[0].record('spikes')

        run(self.runtime)
        
        self.v1_spikes = []
        self.v2_spikes = []
        self.v4_1_spikes = []
        self.v4_2_spikes = []
        for i in range(len(kernels)):
            self.v1_spikes.append(self.v1.populations[i].get_data())
            self.v2_spikes.append(self.v2.populations[i].get_data())
            self.v4_1_spikes.append(self.v4_1.populations[i].get_data())
            self.v4_2_spikes.append(self.v4_2.populations[i].get_data())
        self.lip_spikes = [self.lip.populations[0].get_data()]
    
    def get_total_spikes_lip(self):
        total_spikes = 0
        for spikes in self.lip_spikes[0].segments[0].spiketrains:
            total_spikes += len(spikes)
        return total_spikes
    
    def get_different_ids_lip(self):
        neurons_used = 0
        for spikes in self.lip_spikes[0].segments[0].spiketrains:
            if len(spikes) > 0:
                neurons_used += 1
        return neurons_used
    
    def display(self, layer, figure):
        orientations = []
        for i in range(len(self.gaussian_filters)):
            if i == 0 and self.gaussian_filters[i] != None:
                orientations.append('Horizontal')
            if i == 1 and self.gaussian_filters[i] != None:
                orientations.append('Anti-diagonal')
            if i == 2 and self.gaussian_filters[i] != None:
                orientations.append('Vertical')
            if i == 3 and self.gaussian_filters[i] != None:
                orientations.append('Diagonal')
            if i == 4 and self.gaussian_filters[i] != None:
                orientations.append('Circular')
        if layer != 'lip':
            ax = []
            for i in range(len(self.v1.populations)):
                ax.append(figure.add_subplot(1,len(self.v1.populations),i+1))
                ax[i].set_title("Spikes for layer " + str(layer) + "; Orientation " + str(orientations[i]))
                ax[i].set_xlabel("Runtime")
                ax[i].set_ylabel("Neuron id")
                if layer == 'v1':
                    for spike in self.v1_spikes[i].segments[0].spiketrains:
                        y = np.ones_like(spike) * spike.annotations['source_id']
                        ax[i].plot(spike, y, '.')
                elif layer == 'v2':
                    for spike in self.v2_spikes[i].segments[0].spiketrains:
                        y = np.ones_like(spike) * spike.annotations['source_id']
                        ax[i].plot(spike, y, '.')
                elif layer == 'v4_1':
                    for spike in self.v4_1_spikes[i].segments[0].spiketrains:
                        y = np.ones_like(spike) * spike.annotations['source_id']
                        ax[i].plot(spike, y, '.')
                elif layer == 'v4_2':
                    for spike in self.v4_2_spikes[i].segments[0].spiketrains:
                        y = np.ones_like(spike) * spike.annotations['source_id']
                        ax[i].plot(spike, y, '.')
        elif layer == 'lip':
            ax = figure.add_subplot(1,1,1)
            ax.set_title("Spikes for layer LIP")
            ax.set_xlabel("Runtime")
            ax.set_ylabel("Neuron id")
            for spike in self.lip_spikes[0].segments[0].spiketrains:
                y = np.ones_like(spike) * spike.annotations['source_id']
                ax.plot(spike, y, '.')
